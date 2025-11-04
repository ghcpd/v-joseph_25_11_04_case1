"""Pytest configuration ensuring the repository modules are importable as the
`datasync` package during tests."""

from __future__ import annotations

import importlib
import importlib.util
import pathlib
import sys
import types

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]


def _ensure_module(name: str, module_path: pathlib.Path) -> None:
    """Load a module from `module_path` and register it under `name`"""
    if name in sys.modules:
        return
    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module {name} from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)


def ensure_datasync_package() -> None:
    """Expose local modules under the `datasync` namespace for imports."""
    if "datasync" in sys.modules:
        return

    package = types.ModuleType("datasync")
    package.__path__ = [str(PACKAGE_ROOT)]  # mark as package
    sys.modules["datasync"] = package

    # Load core modules so imports like `from datasync.sync import SyncManager` work
    _ensure_module("datasync.config", PACKAGE_ROOT / "config.py")
    _ensure_module("datasync.metrics", PACKAGE_ROOT / "metrics.py")
    _ensure_module("datasync.sync", PACKAGE_ROOT / "sync.py")


ensure_datasync_package()
