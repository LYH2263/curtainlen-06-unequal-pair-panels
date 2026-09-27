import math
from app.engines.helpers import ceil_units


def split_panels(total_panels: int, left_ratio: float) -> tuple[int, int]:
    """按左侧占比向下取整分幅，右侧为余数。占比须在 [0,1]，总幅数须大于 0。"""
    ratio = float(left_ratio)
    if not math.isfinite(ratio) or ratio < 0.0 or ratio > 1.0:
        raise ValueError("left_ratio must be within [0,1]")
    total = int(total_panels)
    if total <= 0:
        raise ValueError("total panels must be greater than 0")
    left = int(math.floor(total * ratio))
    return left, total - left


def fabric_meters(
    window_w: float,
    window_h: float,
    fullness: float,
    hem_top: float,
    hem_bottom: float,
    fabric_width: float,
    left_ratio: float = 0.5,
) -> dict:
    if fabric_width <= 0:
        raise ValueError("fabric width required")
    finished_w = float(window_w) * float(fullness)
    panels = max(1, ceil_units(finished_w / float(fabric_width)))
    cut_h = float(window_h) + float(hem_top) + float(hem_bottom)
    meters = panels * cut_h
    left_panels, right_panels = split_panels(panels, left_ratio)
    return {
        "finished_width": round(finished_w, 3),
        "panels": panels,
        "cut_height": round(cut_h, 3),
        "meters": round(meters, 2),
        "fabric_width": float(fabric_width),
        "left_ratio": float(left_ratio),
        "left_panels": left_panels,
        "right_panels": right_panels,
    }
