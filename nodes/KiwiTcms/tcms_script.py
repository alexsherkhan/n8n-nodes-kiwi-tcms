import sys
import json
from tcms_api import TCMS

def preserve_formatting(text):
    """
    Preserves Markdown formatting and newlines in text
    - Maintains **bold** and *italic* markers
    - Keeps original line breaks
    - Handles None/empty values safely
    """
    if not isinstance(text, str):
        return text
        
    # Step 1: Protect formatting markers
    protected = text.replace('**', '[[BOLD]]').replace('*', '[[ITALIC]]')
    
    # Step 2: Protect paragraph breaks (double newlines)
    protected = protected.replace('\n\n', '[[PARAGRAPH]]')
    
    # Step 3: Protect single newlines
    protected = protected.replace('\n', '[[NEWLINE]]')
    
    # Step 4: Remove harmful control characters
    cleaned = ''.join(
        c for c in protected 
        if ord(c) >= 32 or c in ['\t', '\r']
    )
    
    # Step 5: Restore all formatting
    restored = cleaned.replace('[[PARAGRAPH]]', '\n\n')
    restored = restored.replace('[[NEWLINE]]', '\n')
    restored = restored.replace('[[BOLD]]', '**')
    restored = restored.replace('[[ITALIC]]', '*')
    
    return restored

def process_params(params):
    """Recursively processes all parameters while preserving structure"""
    if isinstance(params, dict):
        return {k: preserve_formatting(v) if isinstance(v, str) else process_params(v) 
                for k, v in params.items()}
    elif isinstance(params, list):
        return [preserve_formatting(item) if isinstance(item, str) else process_params(item) 
                for item in params]
    return params

def execute_rpc(client, action, params):
    """Handles special RPC method cases"""
    if action == "TestPlan.add_case":
        if isinstance(params, dict):
            params = [params.get("plan_id"), params.get("case_id")]
        return client.exec.TestPlan.add_case(*map(int, params[:2]))
    
    object_name, method_name = action.split('.', 1)
    method = getattr(getattr(client.exec, object_name), method_name)
    
    if isinstance(params, list):
        return method(*params)
    return method(params)

def main():
    try:
        args = json.loads(sys.stdin.read())
        client = TCMS(args["url"], args["username"], args["password"])
        
        processed_params = process_params(args.get("params", {}))
        result = execute_rpc(client, args["action"], processed_params)
        
        print(json.dumps(result, default=str))
        sys.exit(0)

    except Exception as e:
        error_info = {
            "error": str(e),
            "action": args.get("action"),
            "input_params": {
                "url": args.get("url"),
                "username": "*****"  # Masked for security
            },
            "params_sample": {k: str(v)[:50] + "..." if isinstance(v, str) else v 
                           for k, v in args.get("params", {}).items()}
        }
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()