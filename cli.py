import argparse
import uvicorn
import json
import logging
from runners.local import LocalRunner
from runners.slurm import SlurmRunner
from api import create_app

def main():
    parser = argparse.ArgumentParser(description="Agent Rollout Service CLI")
    parser.add_argument("--runner", choices=["local", "slurm"], required=True, help="Runner type")
    parser.add_argument("--port", type=int, default=8008, help="Port to run the API on")
    parser.add_argument("--resources", type=str, default='{"instances": 10}', help="JSON string for available resources")
    
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    try:
        resources = json.loads(args.resources)
    except json.JSONDecodeError:
        print("Error: Invalid JSON for --resources")
        return

    if args.runner == "local":
        runner = LocalRunner(resources)
    elif args.runner == "slurm":
        runner = SlurmRunner(resources)
    else:
        # Should be caught by argparse choices
        print("Invalid runner type")
        return

    app = create_app(runner)
    
    # Suppress /stats logging
    from api import EndpointFilter
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

    print(f"Starting {args.runner} runner API on port {args.port}...")
    uvicorn.run(app, host="0.0.0.0", port=args.port)

if __name__ == "__main__":
    main()
