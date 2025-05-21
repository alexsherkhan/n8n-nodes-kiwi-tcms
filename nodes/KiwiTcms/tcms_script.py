import sys
import json
from tcms_api import TCMS

def process_text(text):
    """
    Ultimate text processor that preserves:
    - Newlines (\n)
    - Markdown formatting (**bold**, *italic*)
    - Special characters
    """
    if not isinstance(text, str):
        return text

    # Protection phase (before JSON serialization)
    protected = text
    # 1. Protect Markdown
    protected = protected.replace('**', '\uE000').replace('*', '\uE001')
    # 2. Protect newlines
    protected = protected.replace('\n', '\uE002')
    
    # Restoration phase (after JSON serialization)
    restored = protected
    # 1. Restore Markdown
    restored = restored.replace('\uE000', '**').replace('\uE001', '*')
    # 2. Restore newlines
    restored = restored.replace('\uE002', '\n')
    
    # Final cleanup (preserve only safe chars)
    return ''.join(
        c for c in restored 
        if ord(c) >= 32 or c in ['\n', '\t']
    )

def deep_process(data):
    """Recursively process all strings in data structure"""
    if isinstance(data, dict):
        return {k: process_text(v) if isinstance(v, str) else deep_process(v) 
                for k, v in data.items()}
    elif isinstance(data, list):
        return [process_text(item) if isinstance(item, str) else deep_process(item) 
                for item in data]
    return data

def execute_kiwi_action(client, action, params):
    """Execute Kiwi TCMS action with proper parameter handling"""
    if action == "TestPlan.add_case":
        params = [params.get("plan_id"), params.get("case_id")]
        return client.exec.TestPlan.add_case(*map(int, params))
    
    obj, method = action.split('.', 1)
    return getattr(getattr(client.exec, obj), method)(params)

def main():
    try:
        # 1. Read and parse input with custom decoder
        args = json.loads(sys.stdin.read())
        
        # 2. Initialize client
        client = TCMS(
            url=args["url"],
            username=args["username"],
            password=args["password"]
        )
        
        # 3. Deep process all parameters
        processed = deep_process(args.get("params", {}))
        
        # 4. Execute API call
        result = execute_kiwi_action(client, args["action"], processed)
        
        # 5. Output result
        print(json.dumps(result, default=str))
        sys.exit(0)

    except Exception as e:
        error_info = {
            "error": str(e),
            "action": args.get("action"),
            "input_sample": {
                "text_length": len(args.get("params", {}).get("text", "")),
                "has_newlines": '\n' in args.get("params", {}).get("text", "")
            }
        }
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()