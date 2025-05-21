import sys
import json
import re
from tcms_api import TCMS

def encode_newlines(text):
    """Replace real newlines with temporary markers before JSON serialization"""
    if not isinstance(text, str):
        return text
    return text.replace('\n', '⏎')  # Using special symbol

def decode_newlines(text):
    """Restore newlines after JSON serialization"""
    if not isinstance(text, str):
        return text
    return text.replace('⏎', '\n')

def process_text_content(text):
    """Main text processing with format preservation"""
    if not isinstance(text, str):
        return text
        
    # 1. Protect Markdown formatting
    protected = text.replace('**', '〚B〛').replace('*', '〚I〛')
    
    # 2. Encode newlines for JSON safety
    encoded = encode_newlines(protected)
    
    # 3. Clean harmful characters (preserve encoded newlines)
    cleaned = ''.join(
        c for c in encoded 
        if ord(c) >= 32 or c == '⏎'
    )
    
    # 4. Restore everything
    restored = decode_newlines(cleaned)
    return restored.replace('〚B〛', '**').replace('〚I〛', '*')

def process_params(params):
    """Deep processing of all parameters"""
    if isinstance(params, dict):
        return {k: process_text_content(v) if isinstance(v, str) else process_params(v) 
                for k, v in params.items()}
    elif isinstance(params, list):
        return [process_text_content(item) if isinstance(item, str) else process_params(item) 
                for item in params]
    return params

def execute_kiwi_method(client, action, params):
    """Execute Kiwi TCMS API method with proper parameter handling"""
    if action == "TestPlan.add_case":
        if isinstance(params, dict):
            params = [params.get("plan_id"), params.get("case_id")]
        return client.exec.TestPlan.add_case(*map(int, params[:2]))
    
    obj, method = action.split('.', 1)
    rpc_method = getattr(getattr(client.exec, obj), method)
    
    if isinstance(params, list):
        return rpc_method(*params)
    return rpc_method(params)

def main():
    try:
        # Read and parse input
        args = json.loads(sys.stdin.read())
        client = TCMS(args["url"], args["username"], args["password"])
        
        # Process parameters with text protection
        processed = process_params(args.get("params", {}))
        
        # Execute API call
        result = execute_kiwi_method(client, args["action"], processed)
        
        # Output result
        print(json.dumps(result, default=str))
        sys.exit(0)

    except Exception as e:
        error_info = {
            "error": str(e),
            "action": args.get("action"),
            "input_sample": {
                "text_preview": str(args.get("params", {}).get("text", ""))[:200] + "...",
                "has_newlines": '\n' in str(args.get("params", {}).get("text", ""))
            }
        }
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()