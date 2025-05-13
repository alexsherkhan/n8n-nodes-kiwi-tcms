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
        method = getattr(getattr(client.exec, object_name), method_name)
        params = args.get("params", {})

        if isinstance(params, list):
            result = method(*params)
        elif isinstance(params, dict):
            result = method(params)
        else:
            result = method(params)

        print(json.dumps(result, default=str))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == '__main__':
    main()