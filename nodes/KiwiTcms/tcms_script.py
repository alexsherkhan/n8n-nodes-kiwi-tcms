import sys
import json
import re
from tcms_api import TCMS

def protect_text(text):
    """Protect special characters before JSON serialization"""
    if not isinstance(text, str):
        return text
        
    # Step 1: Replace newlines with Unicode placeholder
    protected = text.replace('\n', '↲')
    
    # Step 2: Protect Markdown formatting
    protected = protected.replace('**', '〚bold〛').replace('*', '〚italic〛')
    
    return protected

def restore_text(text):
    """Restore original formatting after JSON processing"""
    if not isinstance(text, str):
        return text
        
    # Step 1: Restore Markdown
    restored = text.replace('〚bold〛', '**').replace('〚italic〛', '*')
    
    # Step 2: Restore newlines
    restored = restored.replace('↲', '\n')
    
    # Step 3: Clean remaining control chars
    return ''.join(c for c in restored if ord(c) >= 32 or c in ['\n', '\t'])

def deep_process(data):
    """Recursively process all strings in the data structure"""
    if isinstance(data, dict):
        return {k: restore_text(v) if isinstance(v, str) else deep_process(v) 
                for k, v in data.items()}
    elif isinstance(data, list):
        return [restore_text(item) if isinstance(item, str) else deep_process(item) 
                for item in data]
    return data

def main():
    try:
        # Read and protect input
        raw_input = sys.stdin.read()
        protected_input = protect_text(raw_input)
        args = json.loads(protected_input)
        
        # Initialize client
        client = TCMS(
            url=args["url"],
            username=args["username"],
            password=args["password"]
        )
        
        # Process parameters
        processed_params = deep_process(args.get("params", {}))
        
        # Execute method
        obj, method = args["action"].split('.', 1)
        rpc_method = getattr(getattr(client.exec, obj), method)
        
        if isinstance(processed_params, list):
            result = rpc_method(*processed_params)
        else:
            result = rpc_method(processed_params)
        
        # Return result with protected newlines
        print(json.dumps(result, default=str))
        sys.exit(0)

    except Exception as e:
        error_info = {
            "error": str(e),
            "input_sample": {
                "action": args.get("action", ""),
                "text_preview": str(args.get("params", {}).get("text", ""))[:100] + "...",
                "newlines_preserved": '↲' in raw_input if 'raw_input' in locals() else False
            }
        }
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()