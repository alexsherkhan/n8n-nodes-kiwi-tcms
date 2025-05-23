import sys
import json
from tcms_api import TCMS

def decode_special_chars(text):
    """Converts escaped \n's to real line breaks"""
    if not isinstance(text, str):
        return text
    return (text
        .replace(r'\\n', '\n')  
        .replace(r'\n', '\n')   
    )

def deep_decode(data):
    """Recursively processes all JSON"""
    if isinstance(data, dict):
        return {k: decode_special_chars(v) if isinstance(v, str) else deep_decode(v) 
                for k, v in data.items()}
    elif isinstance(data, list):
        return [decode_special_chars(item) if isinstance(item, str) else deep_decode(item) 
                for item in data]
    return data

def main():
    try:
       
        raw_input = sys.stdin.read()
        
        
        args = json.loads(raw_input)
        
        
        processed_params = deep_decode(args.get("params", {}))
        
       
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
        sys.exit(0)

    except Exception as e:
        error_info = {
            "error": str(e),
            "debug_info": {
                "raw_input_sample": raw_input[:200],
                "has_newlines": '\\n' in raw_input,
                "params_type": type(args.get("params"))
            }
        }
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()