import sys
import json
from tcms_api import TCMS

def main():
    try:
        import sys
        import json
        from tcms_api import TCMS

        raw_input = sys.stdin.read()
        args = json.loads(raw_input)
        
        client = TCMS(
            url=args["url"],
            username=args["username"],
            password=args["password"]
        )
        
        obj, method = args["action"].split('.', 1)
        rpc_method = getattr(getattr(client.exec, obj), method)
        
        
        if args["action"] == "TestPlan.add_case":
            result = rpc_method(args["params"]["plan_id"], args["params"]["case_id"])
        else:
            
            if isinstance(args.get("params"), list):
                result = rpc_method(*args["params"])
            else:
                result = rpc_method(args.get("params", {}))
        
        print(json.dumps(result, default=str))
        
    except Exception as e:
        error_info = {
            "error": str(e),
            "input_sample": raw_input[:500],
            "type": type(e).__name__
        }
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()