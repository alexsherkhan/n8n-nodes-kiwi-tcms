import sys
import json
import re
from tcms_api import TCMS

def fix_json_newlines(text):
    """Convert escaped \\n back to real newlines"""
    if not isinstance(text, str):
        return text
    return text.replace('\\n', '\n')

def deep_restore_newlines(data):
    """Recursively restore newlines in the entire JSON structure"""
    if isinstance(data, dict):
        return {k: fix_json_newlines(v) if isinstance(v, str) else deep_restore_newlines(v) 
                for k, v in data.items()}
    elif isinstance(data, list):
        return [fix_json_newlines(item) if isinstance(item, str) else deep_restore_newlines(item) 
                for item in data]
    return data

def main():
    try:
        # 1. Read JSON input (with escaped \n)
        raw_input = sys.stdin.read()
        args = json.loads(raw_input)
        
        # 2. Restore newlines in all parameters
        processed_params = deep_restore_newlines(args.get("params", {}))
        
        # 3. Initialize TCMS client
        client = TCMS(
            url=args["url"],
            username=args["username"],
            password=args["password"]
        )
        
        # 4. Execute the API method
        obj, method = args["action"].split('.', 1)
        rpc_method = getattr(getattr(client.exec, obj), method)
        
        if isinstance(processed_params, list):
            result = rpc_method(*processed_params)
        else:
            result = rpc_method(processed_params)
        
        # 5. Return the result
        print(json.dumps(result, default=str))
        sys.exit(0)

    except Exception as e:
        error_info = {
            "error": str(e),
            "input_sample": {
                "text": str(args.get("params", {}).get("text", ""))[:200],
                "has_escaped_newlines": '\\n' in raw_input
            }
        }
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()