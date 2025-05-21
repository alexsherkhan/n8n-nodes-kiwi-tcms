import sys
import json
from tcms_api import TCMS

def process_text(text):
    """Process text with newline preservation"""
    if not isinstance(text, str):
        return text
        
    # Unescape JSON-encoded newlines
    return text.replace('\\n', '\n')

def process_params(params):
    """Deep process parameters structure"""
    if isinstance(params, dict):
        return {k: process_text(v) if isinstance(v, str) else process_params(v) 
                for k, v in params.items()}
    elif isinstance(params, list):
        return [process_text(item) if isinstance(item, str) else process_params(item) 
                for item in params]
    return params

def main():
    try:
        # Read and parse input
        args = json.loads(sys.stdin.read())
        client = TCMS(
            url=args["url"],
            username=args["username"],
            password=args["password"]
        )
        
        # Process parameters with newline restoration
        processed = process_params(args.get("params", {}))
        
        # Execute API method
        obj, method = args["action"].split('.', 1)
        rpc_method = getattr(getattr(client.exec, obj), method)
        
        if isinstance(processed, list):
            result = rpc_method(*processed)
        elif isinstance(processed, dict):
            result = rpc_method(processed)
        else:
            result = rpc_method(processed)
        
        # Return result
        print(json.dumps(result, default=str))
        sys.exit(0)

    except Exception as e:
        error_info = {
            "error": str(e),
            "input_sample": {
                "action": args.get("action"),
                "text_preview": str(args.get("params", {}).get("text", ""))[:100],
                "has_newlines": '\\n' in json.dumps(args.get("params", {}).get("text", ""))
            }
        }
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()