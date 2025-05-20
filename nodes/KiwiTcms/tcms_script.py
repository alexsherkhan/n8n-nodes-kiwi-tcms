import sys
import json
from tcms_api import TCMS

def process_text(text):
    """Text Processing with Formatting Preserved"""
    if not isinstance(text, str):
        return text
    return text.replace('\\n', '\n').replace('\\t', '\t')

def process_params(params):
    """Parameter normalization with structure preservation"""
    if isinstance(params, dict):
        return {k: process_text(v) if isinstance(v, str) else v for k, v in params.items()}
    elif isinstance(params, list):
        return [process_text(item) if isinstance(item, str) else item for item in params]
    return params

def main():
    try:
        args = json.loads(sys.stdin.read())
        client = TCMS(
            url=args["url"],
            username=args["username"],
            password=args["password"]
        )

        object_name, method_name = args["action"].split('.', 1)
        rpc_method = getattr(getattr(client.exec, object_name), method_name)
        params = process_params(args.get("params", {}))

        # Special treatment for methods
        if args["action"] == "TestPlan.add_case":
            if isinstance(params, dict):
                params = [params.get("plan_id"), params.get("case_id")]
            elif not isinstance(params, list):
                params = [params]
            
            if len(params) != 2:
                raise ValueError("TestPlan.add_case requires exactly 2 parameters: plan_id and case_id")
            
            result = rpc_method(int(params[0]), int(params[1]))
        
        elif args["action"] in ["TestPlan.create", "TestCase.create"]:
            # We process text separately for the creation methods
            if isinstance(params, dict) and "text" in params:
                params["text"] = process_text(params["text"])
            result = rpc_method(params)
        
        else:
            # Standard processing
            if isinstance(params, list):
                result = rpc_method(*params)
            elif isinstance(params, dict):
                result = rpc_method(params)
            else:
                result = rpc_method(params)

        print(json.dumps(result, default=str))
        sys.exit(0)

    except Exception as e:
        import traceback
        error_info = {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "input_args": args,
            "params_received": params if 'params' in locals() else None
        }
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
