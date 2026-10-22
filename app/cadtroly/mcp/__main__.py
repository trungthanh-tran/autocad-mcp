from .bootstrap import ensure_runtime_dependencies

ensure_runtime_dependencies()

from .server import main  # noqa: E402

main()
