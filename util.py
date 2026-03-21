import phidl
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
