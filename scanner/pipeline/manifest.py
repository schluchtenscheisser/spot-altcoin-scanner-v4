"""Run manifest generation and persistence helpers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List


def _nested_mapping_value(config: Dict[str, Any], path: List[str], default: Any) -> Any:
    cursor: Any = config
    for key in path:
        if not isinstance(cursor, dict) or key not in cursor:
            return default
        cursor = cursor[key]
    return cursor


def _nested_bool(config: Dict[str, Any], path: List[str], default: bool) -> bool:
    return bool(_nested_mapping_value(config, path, default))


def derive_feature_flags(config: Dict[str, Any]) -> Dict[str, bool]:
    """Return a deterministic map of relevant feature flags and their states."""
    return {
        "decision_enabled": _nested_bool(config, ["decision", "enabled"], True),
        "risk_enabled": _nested_bool(config, ["risk", "enabled"], True),
        "tradeability_enabled": _nested_bool(config, ["tradeability", "enabled"], True),
        "btc_regime_enabled": _nested_bool(config, ["btc_regime", "enabled"], False),
        "breakout_scoring_enabled": _nested_bool(config, ["scoring", "breakout", "enabled"], True),
        "pullback_scoring_enabled": _nested_bool(config, ["scoring", "pullback", "enabled"], True),
        "reversal_scoring_enabled": _nested_bool(config, ["scoring", "reversal", "enabled"], True),
        "mexc_enabled": _nested_bool(config, ["data_sources", "mexc", "enabled"], True),
    }


def build_config_hash(config: Dict[str, Any]) -> str:
    """Build a stable SHA-256 hash from the raw runtime config."""
    canonical_json = json.dumps(config, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def read_canonical_schema_version(changelog_path: Path) -> str:
    """Read canonical_schema_version from docs/canonical/CHANGELOG.md."""
    for line in changelog_path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("canonical_schema_version:"):
            _, value = line.split(":", 1)
            version = value.strip()
            if version:
                return version
            raise ValueError("canonical_schema_version is empty")
    raise ValueError("canonical_schema_version not found in canonical changelog")


def write_manifest_atomic(path: Path, payload: Dict[str, Any]) -> None:
    """Atomically write manifest JSON to avoid partial writes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp_path.replace(path)
