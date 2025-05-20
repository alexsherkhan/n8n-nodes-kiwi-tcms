import sys
import json
from tcms_api import TCMS

def preserve_formatting(text):
    """
    Preserves Markdown formatting and newlines in text
    - Maintains **bold** markers
    - Keeps original line breaks
    - Safely handles None/empty values
    """
    if not isinstance(text, str):
        return text
        
    # Protect Markdown formatting during processing
    protected = text.replace('**', '[[BOLD]]')
    
    # Normalize line endings (Windows/Mac/Unix)
    protected = protected.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove only harmful control characters (ASCII 0-31 except \t, \n)
    cleaned = ''.join(
        c for c in protected 
        if ord(c) >= 32 or c in ['\t', '\n']
    )
    
    # Restore original formatting
    return cleaned.replace('[[BOLD]]', '**')

def process_params(params):
    """
    Recursively processes parameters while preserving:
    - Nested structures (dicts/lists)
    - Text formatting
    - Data types
    """
    if isinstance(params, dict):
        return {k: preserve_formatting(v) if isinstance(v, str) else process_params(v) 
                for k, v in params.items()}
    elif isinstance(params, list):
        return [preserve_formatting(item) if isinstance(item, str) else process_params(item) 
                for item in params]
    return params

def main():
    try:
        # Parse and validate input
        args = json.loads(sys.stdin.read())
        client = TCMS(
            url=args["url"],
            username=args["username"],
            password=args["password"]
        )

        # Extract method details
        object_name, method_name = args["action"].split('.', 1)
        rpc_method = getattr(getattr(client.exec, object_name), method_name)
        
        # Process parameters with formatting preservation
        params = process_params(args.get("params", {}))

        # Special method handling
        if args["action"] == "TestPlan.add_case":
            # Convert parameter formats to [plan_id, case_id]
            if isinstance(params, dict):
                params = [params.get("plan_id"), params.get("case_id")]
            elif not isinstance(params, list):
                params = [params]
            
            if len(params) != 2:
                raise ValueError("TestPlan.add_case requires exactly 2 parameters: plan_id and case_id")
            
            result = rpc_method(int(params[0]), int(params[1]))
        else:
            # Standard execution
            if isinstance(params, list):
                result = rpc_method(*params)
            elif isinstance(params, dict):
                result = rpc_method(params)
            else:
                result = rpc_method(params)

        # Return successful result
        print(json.dumps(result, default=str))
        sys.exit(0)

    except Exception as e:
        # Enhanced error reporting
        error_info = {
            "error": str(e),
            "action": args.get("action"),
            "input_params": {
                "url": args.get("url"),
                "username": args.get("username"),
                "params_received": params if 'params' in locals() else None
            },
            "python_version": sys.version,
            "platform": sys.platform
        }
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()