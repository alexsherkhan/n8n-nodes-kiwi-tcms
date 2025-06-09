import sys
import json
from tcms_api import TCMS
from collections import defaultdict

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

        if args["action"] == "TestExecution.filter":

            if isinstance(args["params"], dict):
                run_id = args["params"].get("run_id") or args["params"].get("id")
            else:
                run_id = args["params"][0] if args["params"] else None
            
            if not run_id:
                raise ValueError("Missing run_id parameter")
            

            executions = client.exec.TestExecution.filter({'run': run_id})
            

            statuses = client.exec.TestExecutionStatus.filter({})
            status_names = {s['id']: s['name'] for s in statuses}
            

            stats = {name: 0 for name in status_names.values()}
            stats["TOTAL"] = len(executions)
            

            for execution in executions:
                status_id = execution.get("status")
                status_name = status_names.get(status_id, "UNKNOWN")
                stats[status_name] += 1
            

            result = {
                "PASSED": stats.get("PASSED", 0),
                "FAILED": stats.get("FAILED", 0),
                "IDLE": stats.get("IDLE", 0),
                "PAUSED": stats.get("PAUSED", 0),
                "RUNNING": stats.get("RUNNING", 0),
                "BLOCKED": stats.get("BLOCKED", 0),
                "ERROR": stats.get("ERROR", 0),
                "WAIVED": stats.get("WAIVED", 0),
                "TOTAL": stats["TOTAL"]
            }


        elif args["action"] in ["TestPlan.add_case", "TestRun.add_case"]:
            if isinstance(args["params"], dict):
                if args["action"] == "TestPlan.add_case":
                    result = rpc_method(args["params"]["plan_id"], args["params"]["case_id"])
                elif args["action"] == "TestRun.add_case":
                    result = rpc_method(args["params"]["run_id"], args["params"]["case_id"])
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