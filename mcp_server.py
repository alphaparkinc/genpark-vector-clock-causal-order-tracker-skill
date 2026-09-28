import sys
import json
from client import VectorClock

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "compare_vector_clocks",
                        "description": "Compare two vector clock states and deduce causality (BEFORE, AFTER, CONCURRENT, EQUAL)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "clock_1": {"type": "object"},
                                "clock_2": {"type": "object"}
                            },
                            "required": ["clock_1", "clock_2"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "compare_vector_clocks":
            vc1 = VectorClock("temp", args["clock_1"])
            vc2 = VectorClock("temp", args["clock_2"])
            rel = vc1.compare(vc2)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"relationship": rel})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
