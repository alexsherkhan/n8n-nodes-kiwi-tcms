import sys
import json
import re
from tcms_api import TCMS

def normalize_newlines(text):
    """Normalize all newline formats to \n"""
    if not isinstance(text, str):
        return text
    return re.sub(r'\r\n|\r|\n', '\n', text)

def protect_formatting(text):
    """Protect Markdown formatting during processing"""
    if not isinstance(text, str):
        return text
    # Protect bold and italic with temporary markers
    return text.replace('**', '〚BOLD〛').replace('*', '〚ITALIC〛')

def restore_formatting(text):
    """Restore original formatting markers"""
    if not isinstance(text, str):
        return text
    return text.replace('〚BOLD〛', '**').replace('〚ITALIC〛', '*')

def clean_text(text):
    """Remove harmful chars while preserving formatting"""
    if not isinstance(text, str):
        return text
    
    # Normalize first
    text = normalize_newlines(text)
    
    # Protect formatting
    text = protect_formatting(text)
    
    # Remove only truly harmful control chars (keep \t \n)
    cleaned = []
    for char in text:
        if ord(char) >= 32 or char in ['\t', '\n']:
            cleaned.append(char)
    
    # Restore formatting
    return restore_formatting(''.join(cleaned))

def process_params(params):
    """Deep process all parameters"""
    if isinstance(params, dict):
        return {k: clean_text(v) if isinstance(v, str) else process_params(v) 
                for k, v in params.items()}
    elif isinstance(params, list):
        return [clean_text(item) if isinstance(item, str) else process_params(item) 
                for item in params]
    return params

def main():
    try:
        args = json.loads(sys.stdin.read())
        client = TCMS(args["url"], args["username"], args["password"])
        
        # Process with formatting preservation
        processed = process_params(args.get("params", {}))
        
        # Execute RPC method
        obj, method = args["action"].split('.', 1)
        rpc_method = getattr(getattr(client.exec, obj), method)
        
        if isinstance(processed, list):
            result = rpc_method(*processed)
        elif isinstance(processed, dict):
            result = rpc_method(processed)
        else:
            result = rpc_method(processed)
        
        print(json.dumps(result, default=str))
        sys.exit(0)

    except Exception as e:
        error_info = {
            "error": str(e),
            "input_sample": {
                "action": args.get("action"),
                "text_preview": str(args.get("params", {}).get("text", ""))[:100]
            }
        }
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()