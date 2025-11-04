import importlib.util
import pathlib
import sys


_PACKAGE_NAME = "datasync"
_MODULES = ("config", "metrics", "sync")


def _load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    loader = spec.loader
    if loader is None:
        raise ImportError(f"Unable to load module spec for {module_name}")
    loader.exec_module(module)


def pytest_sessionstart(session):  # noqa: D401 - PyTest hook
    """Patch sys.modules so datasync package can be imported from the repo root."""
    repo_root = pathlib.Path(__file__).resolve().parents[1]

    package_init = repo_root / "__init__.py"
    _load_module(_PACKAGE_NAME, package_init)

    for module in _MODULES:
        module_path = repo_root / f"{module}.py"
        _load_module(f"{_PACKAGE_NAME}.{module}", module_path)
