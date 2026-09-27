"""Shape payloads for history open views (lining / blackout layer)."""

from __future__ import annotations

from copy import deepcopy


def lining_enabled(result: dict) -> bool:
    lining = result.get("lining")
    return isinstance(lining, dict) and bool(lining.get("enabled"))


def open_drop_lining(result: dict) -> dict:
    """Keep lining.enabled / hem, but drop lining meters or merge into main."""
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if not lining_enabled(out):
        return out
    lining = dict(out.get("lining") or {})
    lining_m = float(lining.get("meters") or 0)
    main_m = float(out.get("meters") or 0)
    out["list_lining_meters"] = lining_m
    # Merge lining meters into the main line and zero the nested meters.
    out["meters"] = round(main_m + lining_m, 2)
    lining["meters"] = 0.0
    lining["panels"] = lining.get("panels") if lining.get("panels") == 0 else 0
    lining["cut_height"] = lining.get("cut_height") if lining.get("cut_height") == 0 else 0.0
    out["lining"] = lining
    out["open_lining_dropped"] = True
    return out


def summarize_lining(result: dict) -> dict:
    """Flat view of lining switch / side meters for open consumers."""
    if not isinstance(result, dict):
        return {}
    lining = result.get("lining") or {}
    return {
        "enabled": bool(lining.get("enabled")),
        "hem": lining.get("hem"),
        "lining_meters": lining.get("meters"),
        "list_lining_meters": result.get("list_lining_meters"),
        "meters": result.get("meters"),
        "open_lining_dropped": bool(result.get("open_lining_dropped")),
    }
