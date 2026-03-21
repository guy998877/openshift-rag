import argparse
from pathlib import Path

from core.config import DEFAULT_DOCS_ROOT, DEFAULT_PROCESSED_DIR
from api.routes import create_app


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m api")
    parser.add_argument("--docs-root", type=Path, default=DEFAULT_DOCS_ROOT)
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    app = create_app(args.docs_root, args.processed_dir)
    print(f"Viewer running at http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=False)


main()
