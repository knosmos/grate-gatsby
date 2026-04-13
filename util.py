"""
Optically tunable diffraction grating with comb drive actuation
6.2600 / 3.155, Spring 2026
Utility drawing functions
Jieruei Chang
"""

from phidl import Device
import phidl.geometry as pg
from phidl import quickplot as qp


def box(w: float, h: float, m: float = 250, layer: int = 1) -> Device:
    """
    Border box.
    w: width (outer)
    h: height
    m: margin
    layer: phidl layer
    """
    bbox_outer = pg.rectangle((w, h), layer=1).move((-w / 2, -h / 2))
    bbox_inner = pg.rectangle((w - m * 2, h - m * 2)).move(
        (-(w - m * 2) / 2, -(h - m * 2) / 2)
    )
    return pg.boolean(bbox_outer, bbox_inner, "A-B")


def knockout(text: str, margin: float) -> Device:
    """
    Knockout text.
    """
    text_obj = pg.text(f"D E V I C E   {" ".join(text)}", size=400)
    bbox = text_obj.bbox
    text_obj.move((margin, margin))
    rect = pg.rectangle((bbox[1][0] + margin * 2, bbox[1][1] + margin * 2))
    rect = pg.boolean(rect, text_obj, "A-B")
    return rect
