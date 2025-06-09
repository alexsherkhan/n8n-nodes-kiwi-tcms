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
            
        
            status_stats = defaultdict(int)
            for execution in executions:
                status_name = execution.get("status__name", "UNKNOWN")
                status_stats[status_name] += 1
            
       
            stats_string = "\n".join([
                f"PASSED - {status_stats.get('PASSED', 0)}",
                f"WAIVED - {status_stats.get('WAIVED', 0)}",
                f"IDLE - {status_stats.get('IDLE', 0)}",
                f"PAUSED - {status_stats.get('PAUSED', 0)}",
                f"RUNNING - {status_stats.get('RUNNING', 0)}",
                f"BLOCKED - {status_stats.get('BLOCKED', 0)}",
                f"ERROR - {status_stats.get('ERROR', 0)}",
                f"FAILED - {status_stats.get('FAILED', 0)}",
                f"TOTAL - {len(executions)}"
            ])
            

            result = []
            for execution in executions:
                execution_copy = dict(execution)
                execution_copy["status__name"] = stats_string
                result.append(execution_copy)

   
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