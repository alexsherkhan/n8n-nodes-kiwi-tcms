import sys
import json
from tcms_api import TCMS

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
        params = args.get("params", {})

        if args["action"] == "TestPlan.add_case":
            if isinstance(params, dict):
                params = [params.get("plan_id"), params.get("case_id")]
            elif not isinstance(params, list):
                params = [params]
            
            if len(params) != 2:
                raise ValueError("TestPlan.add_case requires exactly 2 parameters: plan_id and case_id")
            
            result = rpc_method(int(params[0]), int(params[1]))
        else:
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
            "trace": traceback.format_exc(),
            "input_args": args,
            "params_received": params if 'params' in locals() else None
        }
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
