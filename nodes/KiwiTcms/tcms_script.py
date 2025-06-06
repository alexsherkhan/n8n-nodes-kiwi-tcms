import sys
import json
from tcms_api import TCMS

def main():
    try:
        raw_input = sys.stdin.read()
        args = json.loads(raw_input)
        
        client = TCMS(
            url=args["url"],
            username=args["username"],
            password=args["password"]
        )
        
        obj, method = args["action"].split('.', 1)
        rpc_method = getattr(getattr(client.exec, obj), method)
        

        if args["action"] in [
            "TestPlan.add_case",
            "TestRun.add_case",
            "TestRun.get_cases",  
            "TestRun.status_counts"  
        ]:
            if isinstance(args["params"], dict):
                
                if args["action"] == "TestPlan.add_case":
                    result = rpc_method(args["params"]["plan_id"], args["params"]["case_id"])
                elif args["action"] == "TestRun.add_case":
                    result = rpc_method(args["params"]["run_id"], args["params"]["case_id"])
                elif args["action"] == "TestRun.get_cases":
                    
                    run_id = args["params"].get("run_id") or args["params"].get("id")
                    if not run_id:
                        raise ValueError("Missing run_id or id in params")
                    result = rpc_method(run_id)
            else:
                
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