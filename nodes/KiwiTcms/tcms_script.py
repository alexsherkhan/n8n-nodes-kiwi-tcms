import sys
import json
from tcms_api import TCMS

def preserve_newlines(text):
    """Forcibly saves all line breaks"""
    if not isinstance(text, str):
        return text
    
    return (text.replace(r'\n', '\n')
             .replace(r'\\n', '\n')
             .replace('⏎', '\n'))  

def deep_process(data):
    """Deep processing of all strings in the structure"""
    if isinstance(data, dict):
        return {k: preserve_newlines(v) if isinstance(v, str) else deep_process(v) 
                for k, v in data.items()}
    elif isinstance(data, list):
        return [preserve_newlines(item) if isinstance(item, str) else deep_process(item) 
                for item in data]
    return data

def main():
    try:
        
        raw_data = sys.stdin.read()
        print(f"DEBUG Raw input: {raw_data[:500]}", file=sys.stderr) 
        
        
        args = json.loads(raw_data)
        
        
        processed = deep_process(args.get("params", {}))
        
        
        client = TCMS(args["url"], args["username"], args["password"])
        
        
        obj, method = args["action"].split('.', 1)
        rpc_method = getattr(getattr(client.exec, obj), method)
        
        if isinstance(processed, list):
            result = rpc_method(*processed)
        else:
            result = rpc_method(processed)
        
        
        print(json.dumps(result, default=str))
        
    except Exception as e:
        error_info = {
            "error": str(e),
            "input_sample": raw_data[:500] if 'raw_data' in locals() else None,
            "python_version": sys.version
        }
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()