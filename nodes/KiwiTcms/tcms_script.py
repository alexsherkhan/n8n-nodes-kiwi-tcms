import sys
import json
import re
from tcms_api import TCMS

def restore_newlines(text):
    """Restores line breaks from JSON"""
    if not isinstance(text, str):
        return text
    
    
    text = re.sub(r'\\{1,2}n', '\n', text)  
    return text

def deep_restore(data):
    """Recursively processes the entire data structure"""
    if isinstance(data, dict):
        return {k: restore_newlines(v) if isinstance(v, str) else deep_restore(v) 
                for k, v in data.items()}
    elif isinstance(data, list):
        return [restore_newlines(item) if isinstance(item, str) else deep_restore(item) 
                for item in data]
    return data

def main():
    try:
        
        raw_input = sys.stdin.read()
        print(f"DEBUG RAW INPUT: {raw_input}", file=sys.stderr)  
        
        
        args = json.loads(raw_input)
        
        
        processed_params = deep_restore(args.get("params", {}))
        
        
        client = TCMS(
            url=args["url"],
            username=args["username"],
            password=args["password"]
        )
        
        
        obj, method = args["action"].split('.', 1)
        rpc_method = getattr(getattr(client.exec, obj), method)
        
        if isinstance(processed_params, list):
            result = rpc_method(*processed_params)
        else:
            result = rpc_method(processed_params)
        
        
        print(json.dumps(result, default=str))
        
    except Exception as e:
        error_info = {
            "error": str(e),
            "input_sample": raw_input[:500],
            "has_newlines": '\\n' in raw_input
        }
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()