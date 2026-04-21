"""
Optically tunable diffraction grating with comb drive actuation
6.2600 / 3.155, Spring 2026
Device generation code v0.3
Jieruei Chang
"""

import phidl
from phidl import Device
from phidl import quickplot as qp
import phidl.geometry as pg
import phidl.routing as pr
import numpy as np


def grate_gatsby(
    flexible_grating: Device,
    anchor: Device,
    comb: Device,
    vcc_pad_size: tuple[float, float],
    gnd_pad_size: tuple[float, float],
    gnd_trace_length: float = 500,
) -> Device:
    """
    Optically tunable diffraction grating with comb drive actuation and flexure support.
    flexible_grating: the diffraction grating to be actuated
    anchor: the anchor and flexure support structure
    comb: the comb drive structure
    """
    D = Device("grate_gatsby")

    grating_ref = D.add_ref(flexible_grating)
    comb_left_ref = D.add_ref(comb)
    comb_left_ref.connect("grating_conn", grating_ref.ports["left"])
    a_tl = (
        D.add_ref(anchor)
        .mirror((1, 0))
        .connect("floating", comb_left_ref.ports["anchor_top"])
    )
    a_bl = D.add_ref(anchor).connect("floating", comb_left_ref.ports["anchor_bottom"])

    comb_right_ref = D.add_ref(comb)
    comb_right_ref.mirror((1, 0))
    comb_right_ref.connect("grating_conn", grating_ref.ports["right"])
    a_tr = D.add_ref(anchor).connect("floating", comb_right_ref.ports["anchor_top"])
    a_br = (
        D.add_ref(anchor)
        .mirror((0, 1))
        .connect("floating", comb_right_ref.ports["anchor_bottom"])
    )

    # pads. we'll need two gnd pads (top and bottom) and a vcc trace that routes around the device.
    D << pr.route_sharp(
        a_tl.ports["fixed_l"],
        a_tr.ports["fixed_l"],
        width=a_tl.ports["fixed_l"].width,
        path_type="manhattan",
    )
    D << pr.route_sharp(
        a_br.ports["fixed_l"],
        a_bl.ports["fixed_l"],
        width=a_bl.ports["fixed_l"].width,
        path_type="manhattan",
    )
    D.add_port(
        name="gnd_port_top",
        midpoint=(
            (a_tl.ports["fixed_l"].midpoint[0] + a_tr.ports["fixed_l"].midpoint[0]) / 2,
            a_tl.ports["fixed_l"].midpoint[1] + gnd_trace_length,
        ),
        orientation=90,
    )
    D.add_port(
        name="gnd_port_bottom",
        midpoint=(
            (a_bl.ports["fixed_l"].midpoint[0] + a_br.ports["fixed_l"].midpoint[0]) / 2,
            a_bl.ports["fixed_l"].midpoint[1] - gnd_trace_length,
        ),
        orientation=270,
    )
    gnd_pad_top = D.add_ref(pg.compass(size=gnd_pad_size)).connect(
        "S", D.ports["gnd_port_top"]
    )
    gnd_pad_bot = D.add_ref(pg.compass(size=gnd_pad_size)).connect(
        "N", D.ports["gnd_port_bottom"]
    )
    D << pr.route_sharp(
        a_tl.ports["fixed_l"],
        gnd_pad_top.ports["S"],
        width=a_tl.ports["fixed_l"].width,
        path_type="L",
    )
    D << pr.route_sharp(
        a_bl.ports["fixed_l"],
        gnd_pad_bot.ports["N"],
        width=a_bl.ports["fixed_l"].width,
        path_type="L",
    )
    D.add_port(
        name="vcc_port",
        midpoint=(
            (
                comb_left_ref.ports["fixed_conn"].midpoint[0]
                + comb_right_ref.ports["fixed_conn"].midpoint[0]
            )
            / 2,
            comb_left_ref.ports["fixed_conn"].midpoint[1]
            - 2100
            - comb_left_ref.ports["fixed_conn"].width / 2,
        ),
        orientation=-90,
    )
    vcc_pad = D.add_ref(pg.compass(size=vcc_pad_size)).connect("N", D.ports["vcc_port"])
    D << pr.route_sharp(
        comb_left_ref.ports["fixed_conn"],
        vcc_pad.ports["W"],
        width=comb_left_ref.ports["fixed_conn"].width,
        path_type="U",
    )
    D << pr.route_sharp(
        comb_right_ref.ports["fixed_conn"],
        vcc_pad.ports["E"],
        width=comb_right_ref.ports["fixed_conn"].width,
        path_type="U",
    )
    # dev_text = pg.text(f"D U A L", size=200, justify="center")
    # D.add_ref(dev_text).move((gnd_pad_bot.ports["S"].midpoint[0], -4500))
    # qp(D)
    return D


def less_grate_gatsby(
    flexible_grating: Device,
    anchor: Device,
    comb: Device,
    vcc_pad_size: tuple[float, float],
    gnd_pad_size: tuple[float, float],
) -> Device:
    """
    Single sided optically tunable diffraction grating (only one comb drive).
    """
    D = Device("less_grate_gatsby")

    grating_ref = D.add_ref(flexible_grating)
    comb_left_ref = D.add_ref(comb)
    comb_left_ref.connect("grating_conn", grating_ref.ports["left"])
    a_top = (
        D.add_ref(anchor)
        .mirror((1, 0))
        .connect("floating", comb_left_ref.ports["anchor_top"])
    )
    a_bot = D.add_ref(anchor).connect("floating", comb_left_ref.ports["anchor_bottom"])

    # calculate distance we need to route from anchor to grating
    grating_right_point = grating_ref.ports["right"].midpoint
    anchor_top_point = a_top.ports["fixed_l"].midpoint
    anchor_bot_point = a_bot.ports["fixed_l"].midpoint
    dist = (
        grating_right_point[0] - anchor_top_point[0] + a_top.ports["fixed_l"].width / 2
    )
    D.add_ref(
        pr.route_sharp(
            a_top.ports["fixed_l"],
            a_bot.ports["fixed_l"],
            width=a_top.ports["fixed_l"].width,
            path_type="U",
            length1=dist,
        )
    )
    D.add_port(
        name="gnd_port",
        midpoint=(
            anchor_top_point[0] + dist + a_top.ports["fixed_l"].width / 2,
            (anchor_top_point[1] + anchor_bot_point[1]) / 2,
        ),
        orientation=0,
    )

    # pads
    vcc_pad = D.add_ref(pg.compass(size=vcc_pad_size)).connect(
        "E", comb_left_ref.ports["fixed_conn"]
    )
    gnd_pad = D.add_ref(pg.compass(size=gnd_pad_size)).connect("W", D.ports["gnd_port"])

    # text
    # vcc_text = pg.text("V C C", size=200, justify="center").rotate(180)
    # gnd_text = pg.text("G N D", size=200, justify="center").rotate(180)
    # dev_text = pg.text(f"S I N G L E", size=200, justify="center").rotate(180)

    # D.add_ref(vcc_text).move(
    #     (vcc_pad.ports["N"].midpoint[0], vcc_pad.ports["N"].midpoint[1] + 300)
    # )
    # D.add_ref(gnd_text).move(
    #     (gnd_pad.ports["N"].midpoint[0], gnd_pad.ports["N"].midpoint[1] + 300)
    # )
    # D.add_ref(dev_text).move((-1200, -1500))
    # qp(D)
    return D


def just_grate_gatsby(grating: Device) -> Device:
    """
    Just the diffraction grating, without any actuation or support structures.
    """
    D = Device("just_grate_gatsby")
    w = 1000
    rect = pg.rectangle(size=(w, w), layer=0).move((-w / 2, -w / 2))
    bbox = pg.bbox(bbox=grating.bbox)
    grating_w, grating_h = (
        grating.bbox[1][0] - grating.bbox[0][0],
        grating.bbox[1][1] - grating.bbox[0][1],
    )
    grating_ref = D.add_ref(grating)
    grating_ref.move((-grating_w / 2, -grating_h / 2))
    bbox.move((-grating_w / 2, -grating_h / 2))
    rect = pg.boolean(rect, bbox, operation="A-B", layer=0)
    D << rect

    # text
    # dev_text = pg.text(f"G R A T E", size=200, justify="center")
    # D.add_ref(dev_text).move((0, -1300))
    # qp(D)
    return D


def combed_gatsby(
    comb: Device,
    anchor: Device,
    vcc_pad_size: tuple[float, float],
    gnd_pad_size: tuple[float, float],
) -> Device:
    D = Device("combed_gatsby")
    comb_ref = D.add_ref(comb)

    a_top = (
        D.add_ref(anchor)
        .mirror((0, 1))
        .connect("floating", comb_ref.ports["anchor_top"])
    )
    a_bot = D.add_ref(anchor).connect("floating", comb_ref.ports["anchor_bottom"])
    D << pr.route_sharp(
        a_top.ports["fixed_l"],
        a_bot.ports["fixed_l"],
        width=a_top.ports["fixed_l"].width,
    )
    D.add_port(
        name="gnd_port",
        midpoint=(
            a_top.ports["fixed_l"].midpoint[0] + a_top.ports["fixed_l"].width / 2,
            (a_top.ports["fixed_l"].midpoint[1] + a_bot.ports["fixed_l"].midpoint[1])
            / 2,
        ),
        orientation=0,
    )

    # pads
    vcc_pad = D.add_ref(pg.compass(size=vcc_pad_size)).connect(
        "E", comb_ref.ports["fixed_conn"]
    )
    gnd_pad = D.add_ref(pg.compass(size=gnd_pad_size)).connect("W", D.ports["gnd_port"])

    # text
    # vcc_text = pg.text("V C C", size=200, justify="center")
    # gnd_text = pg.text("G N D", size=200, justify="center")
    # dev_text = pg.text(f"C O M B", size=200, justify="center")
    # D.add_ref(vcc_text).move(
    #     (vcc_pad.ports["N"].midpoint[0], vcc_pad.ports["N"].midpoint[1] + 200)
    # )
    # D.add_ref(gnd_text).move(
    #     (gnd_pad.ports["N"].midpoint[0], gnd_pad.ports["N"].midpoint[1] + 200)
    # )
    # D.add_ref(dev_text).move((0, -1200))
    # qp(D)
    return D


def rigor_mortis_gatsby(
    comb: Device,
    anchor: Device,
    grating: Device,
    vcc_pad_size: tuple[float, float],
    gnd_pad_size: tuple[float, float],
) -> Device:
    """
    Single sided optically tunable diffraction grating with no springs. The entire device
    will just shift side to side; in theory we should be able to measure a phase shift.
    """
    D = Device("rigor_mortis_gatsby")
    grating_ref = D.add_ref(grating)
    comb_ref = D.add_ref(comb)
    comb_ref.connect("grating_conn", grating_ref.ports["right"])

    grating_width = grating.bbox[1][0] - grating.bbox[0][0]
    grating_top = grating.bbox[1][1]
    grating_bottom = grating.bbox[0][1]

    support_truss = truss(w=grating_width + 6, h=22, margin=2, dist=2.5)
    if "spring_conn" not in support_truss.ports:
        support_truss.add_port(
            "spring_conn", midpoint=(25, 22), width=50, orientation=90
        )
    support_truss_top = D.add_ref(support_truss).move((grating.bbox[0][0], grating_top))
    support_truss_bot = (
        D.add_ref(support_truss)
        .mirror((1, 0))
        .move((grating.bbox[0][0], grating_bottom))
    )

    a_top = (
        D.add_ref(anchor)
        .mirror((0, 1))
        .connect("floating", comb_ref.ports["anchor_top"])
    )
    a_bot = D.add_ref(anchor).connect("floating", comb_ref.ports["anchor_bottom"])
    a_top2 = D.add_ref(anchor).connect(
        "floating", support_truss_top.ports["spring_conn"]
    )
    a_bot2 = (
        D.add_ref(anchor)
        .mirror((0, 1))
        .connect("floating", support_truss_bot.ports["spring_conn"])
    )
    D << pr.route_sharp(
        a_top.ports["fixed_l"],
        a_bot.ports["fixed_l"],
        width=a_top.ports["fixed_l"].width,
        path_type="U",
        length1=grating_width + 100,
    )
    D << pr.route_sharp(
        a_top2.ports["fixed_l"],
        a_bot2.ports["fixed_l"],
        width=a_top2.ports["fixed_l"].width,
        path_type="U",
        length1=100 - 6,
    )

    # pads
    vcc_pad = D.add_ref(pg.compass(size=vcc_pad_size)).connect(
        "E", comb_ref.ports["fixed_conn"]
    )
    gnd_port = D.add_port(
        name="gnd_port",
        midpoint=(
            a_top.ports["fixed_l"].midpoint[0]
            + a_top.ports["fixed_l"].width / 2
            - 100
            - grating_width,
            (a_top.ports["fixed_l"].midpoint[1] + a_bot.ports["fixed_l"].midpoint[1])
            / 2,
        ),
        orientation=180,
    )
    gnd_pad = (
        D.add_ref(pg.compass(size=gnd_pad_size))
        .move((-gnd_pad_size[0], 0))
        .connect("E", gnd_port)
    )

    # qp(D)
    return D


def flexible_grating(
    N: int, bar_w: float, bar_l: float, pitch: float, spring_l: float, spring_w: float
) -> Device:
    """
    Flexible diffraction grating.

    N: number of grating bars
    bar_w: width of bars
    bar_l: length of bars
    pitch: distance between start of one bar to the start of the next
    spring_l: length of the springs
    spring_w: width of spring bar
    """
    D = Device("grating")
    # assert spring_w * 2 < bar_w, "spring thickness must be less than half the bar width"
    offset = bar_w / 3 - spring_w

    # Grating bars
    grating_model = grating(N, bar_w, bar_l, pitch)
    D.add_ref(grating_model)

    # Springs
    spring_model = spring(L=spring_l, w=spring_w, space=pitch - bar_w + 2 * offset)
    fillet = fillet_shape(radius=1)
    for i in range(N - 1):
        spring_ref = D.add_ref(spring_model)
        spring_ref.move((i * pitch + bar_w - offset, bar_l))
        spring_ref_bottom = D.add_ref(spring_model)
        spring_ref_bottom.mirror((1, 0))
        spring_ref_bottom.move((i * pitch + bar_w - offset, 0))
        if offset != 0:
            D.add_ref(fillet).rotate(-90).move((i * pitch + bar_w - offset - 1, bar_l))
            D.add_ref(fillet).rotate(0).move((i * pitch + bar_w - offset - 1, 0))
            D.add_ref(fillet).rotate(90).move(
                (i * pitch + bar_w + spring_w + 1 - offset * 2, 0)
            )
            D.add_ref(fillet).rotate(180).move(
                (i * pitch + bar_w + spring_w + 1 - offset * 2, bar_l)
            )

    # Hack in a bunch of truss holes
    HOLE_DIAM = 4
    OFFSET_Y = 1.5
    SPACE_Y = 6
    hole_template = Device()
    hole_circle = pg.circle(radius=HOLE_DIAM / 2)
    for y in np.arange(OFFSET_Y + HOLE_DIAM / 2, bar_l, SPACE_Y + HOLE_DIAM):
        hole_template.add_ref(hole_circle).move((HOLE_DIAM / 2, y))
    # Left side
    D = pg.boolean(D, hole_template, operation="A-B", layer=0)
    # Right side
    hole_template.move(((N - 1) * pitch + bar_w - HOLE_DIAM, 0))
    D = pg.boolean(D, hole_template, operation="A-B", layer=0)

    # Ports
    D.add_port(name="left", midpoint=(0, bar_l / 2), width=bar_w, orientation=180)
    D.add_port(
        name="right",
        midpoint=((N - 1) * pitch + bar_w, bar_l / 2),
        width=bar_w,
        orientation=0,
    )
    D.name = "grating"
    # qp(D)
    return D


def grating(N: int, bar_w: float, bar_l: float, pitch: float) -> Device:
    """
    Rigid diffraction grating.

    N: number of grating bars
    bar_w: width of bars
    bar_l: length of bars
    pitch: distance between start of one bar to the start of the next
    """
    D = Device("grating")
    assert bar_w < pitch, "bar width must be less than the pitch"
    ref_bar = pg.rectangle(size=(bar_w, bar_l))
    for i in range(N):
        bar_ref = D.add_ref(ref_bar)
        bar_ref.move((i * pitch, 0))
    D.add_port(name="left", midpoint=(-bar_w, bar_l / 2), width=bar_w, orientation=180)
    D.add_port(
        name="right", midpoint=(N * pitch, bar_l / 2), width=bar_w, orientation=0
    )
    # qp(D)
    return D


def spring(
    L: float,
    w: float,
    space: float,
    fillet: float = 5,
    L_right: float = None,
    top_extra=4,
) -> Device:
    """
    Spring for diffraction grating.

    L: length of the spring
    w: width of the spring bar
    space: distance between the two spring bars
    fillet: interior fillet radius
    L_right: length of the rightmost vertical segment. If None, it will be the same as L.
    """
    if L_right is None:
        L_right = L
    D = Device("spring")
    D.add_polygon(
        [
            (-w, 0),
            (-w, L + top_extra),
            (space + w, L + top_extra),
            (space + w, L - L_right),
            (space, L - L_right),
            (space, L - w),
            (0, L - w),
            (0, 0),
        ],
        layer=0,
    )
    D.polygons[0].fillet([0, 0, 0, 0, 0, fillet, fillet, 0])
    D << fillet_shape(radius=1).rotate(90).move((-w, 0))
    D << fillet_shape(radius=1).rotate(0).move((space + w, 0))
    # qp(D)
    return D


def anchor(
    anchor_w: float,
    anchor_h: float,
    L1: float,
    L2: float,
    w: float,
    space: float,
    fillet: float = 3,
    fixed_anchor_w: float = 100,
) -> Device:
    """
    Anchor and flexure support.

    anchor_size: size of the square anchor
    L1: length of left flexure
    L2: length of right flexure
    w: width of flexure bars
    space: distance between the two flexure bars
    fillet: interior fillet radius
    """
    D = Device("anchor")
    # flexures
    if w >= 8:
        flexure_l = truss(w=w, h=L1, margin=(w - 4) / 2)
        flexure_l2 = truss(w=w, h=L1, margin=(w - 4) / 2)
        flexure_r = truss(w=w, h=L2, margin=(w - 4) / 2)
    else:
        flexure_l = pg.rectangle(size=(w, L1))
        flexure_l2 = pg.rectangle(size=(w, L1))
        flexure_r = pg.rectangle(size=(w, L2))
    D.add_ref(flexure_l).move((-w, 0))
    D.add_ref(flexure_l2).move((-4 * w, 0))
    D.add_ref(flexure_r).move((space, L1 - L2))
    # top fillets
    D.add_ref(fillet_shape(radius=fillet).rotate(-90).move((0, L1)))
    D.add_ref(fillet_shape(radius=fillet).rotate(180).move((-w, L1)))
    D.add_ref(fillet_shape(radius=fillet).rotate(-90).move((-3 * w, L1)))
    D.add_ref(fillet_shape(radius=fillet).rotate(180).move((space, L1)))
    # bottom fillets
    D.add_ref(fillet_shape(radius=fillet).rotate(90).move((-w, 0)))
    D.add_ref(fillet_shape(radius=fillet).rotate(0).move((-3 * w, 0)))
    D.add_ref(fillet_shape(radius=fillet).rotate(90).move((-4 * w, 0)))
    # anchor rect
    r = pg.rectangle(size=(anchor_w, anchor_h))
    r_ref = D.add_ref(r)
    r_ref.move((-anchor_w, -anchor_h))
    # suspended
    t = truss(w=space + w * 5, h=anchor_h)
    D.add_ref(t).move((-4 * w, L1))
    D.add_port(
        name="floating", midpoint=(space + w / 2, L1 - L2), width=w, orientation=270
    )
    D << fillet_shape(radius=fillet).rotate(90).move((space, L1 - L2))
    D << fillet_shape(radius=fillet).rotate(0).move((space + w, L1 - L2))
    D.add_port(
        name="fixed",
        midpoint=(-anchor_w + fixed_anchor_w / 2, 0),
        width=fixed_anchor_w,
        orientation=90,
    )
    D.add_port(
        name="fixed_l",
        midpoint=(-anchor_w, -anchor_h / 2),
        width=fixed_anchor_w,
        orientation=180,
    )
    # qp(D)
    return D


def anchor_extraduty(
    anchor_w: float,
    anchor_h: float,
    L1: float,
    L2: float,
    w: float,
    space: float,
    fillet: float = 3,
    fixed_anchor_w: float = 100,
    suspended_h: float = 30,
) -> Device:
    """
    Anchor and flexure support.

    anchor_size: size of the square anchor
    L1: length of left flexure
    L2: length of right flexure
    w: width of flexure bars
    space: distance between the two flexure bars
    fillet: interior fillet radius
    """
    D = Device("anchor")
    # flexures
    if w >= 8:
        flexure_l = truss(w=w, h=L1, margin=(w - 4) / 2)
        flexure_l2 = truss(w=w, h=L1, margin=(w - 4) / 2)
        flexure_r = truss(w=w, h=L2, margin=(w - 4) / 2)
        flexure_r2 = truss(w=w, h=L2, margin=(w - 4) / 2)
    else:
        flexure_l = pg.rectangle(size=(w, L1))
        flexure_l2 = pg.rectangle(size=(w, L1))
        flexure_r = pg.rectangle(size=(w, L2))
        flexure_r2 = pg.rectangle(size=(w, L2))
    D.add_ref(flexure_l).move((-w, 0))
    D.add_ref(flexure_l2).move((-6 * w, 0))
    D.add_ref(flexure_r).move((space, L1 - L2))
    D.add_ref(flexure_r2).move((space - 5 * w, L1 - L2))
    # top fillets
    D.add_ref(fillet_shape(radius=fillet).rotate(-90).move((0, L1)))
    D.add_ref(fillet_shape(radius=fillet).rotate(180).move((-w, L1)))
    D.add_ref(fillet_shape(radius=fillet).rotate(-90).move((-5 * w, L1)))
    D.add_ref(fillet_shape(radius=fillet).rotate(180).move((space, L1)))
    D.add_ref(fillet_shape(radius=fillet).rotate(-90).move((space - 4 * w, L1)))
    D.add_ref(fillet_shape(radius=fillet).rotate(180).move((space - 5 * w, L1)))
    # bottom fillets
    D.add_ref(fillet_shape(radius=fillet).rotate(90).move((-w, 0)))
    D.add_ref(fillet_shape(radius=fillet).rotate(0).move((-5 * w, 0)))
    D.add_ref(fillet_shape(radius=fillet).rotate(90).move((-6 * w, 0)))
    # anchor rect
    r = pg.rectangle(size=(anchor_w, anchor_h))
    r_ref = D.add_ref(r)
    r_ref.move((-anchor_w, -anchor_h))
    # suspended
    t = truss(w=space + w * 7, h=suspended_h)
    D.add_ref(t).move((-6 * w, L1))
    D.add_port(
        name="floating",
        midpoint=(space + w / 2 - 2.5 * w, L1 - L2),
        width=w,
        orientation=270,
    )
    fillet = fillet_shape(radius=fillet)
    D.add_ref(fillet).rotate(90).move((space, L1 - L2))
    D.add_ref(fillet).rotate(0).move((space + w, L1 - L2))
    D.add_ref(fillet).rotate(90).move((space - 5 * w, L1 - L2))
    D.add_ref(fillet).rotate(0).move((space - 4 * w, L1 - L2))
    D.add_port(
        name="fixed",
        midpoint=(-anchor_w + fixed_anchor_w / 2, 0),
        width=fixed_anchor_w,
        orientation=90,
    )
    D.add_port(
        name="fixed_l",
        midpoint=(-anchor_w, -anchor_h / 2),
        width=fixed_anchor_w,
        orientation=180,
    )
    # qp(D)
    return D


def anchor_single(
    anchor_w: float,
    anchor_h: float,
    L: float,
    w: float,
    space: float,
    fillet: float = 3,
    fixed_anchor_w: float = 100,
) -> Device:
    """ """
    D = Device("anchor_single")
    flexure = pg.rectangle(size=(w, L))
    D.add_ref(flexure).move((-w, 0))
    D.add_ref(flexure).move((-6 * w, 0))
    D << pg.rectangle(size=(anchor_w, anchor_h)).move((-anchor_w, L))

    fillet = fillet_shape(radius=fillet)
    D.add_ref(fillet)
    D.add_ref(fillet).rotate(90).move((-w, 0))
    D.add_ref(fillet).move((-5 * w, 0))
    D.add_ref(fillet).rotate(90).move((-6 * w, 0))
    D.add_ref(fillet).rotate(180).move((-w, L))
    D.add_ref(fillet).rotate(-90).move((-5 * w, L))
    D.add_ref(fillet).rotate(180).move((-6 * w, L))

    D.add_port(name="floating", midpoint=(-3 * w, 0), width=w, orientation=270)
    D.add_port(
        name="fixed",
        midpoint=(-anchor_w + fixed_anchor_w / 2, L + anchor_h),
        width=fixed_anchor_w,
        orientation=90,
    )
    D.add_port(
        name="fixed_l",
        midpoint=(-anchor_w, anchor_h / 2 + L),
        width=fixed_anchor_w,
        orientation=180,
    )
    # qp(D)
    return D


def comb(
    N: int,
    w: float,
    L: float,
    pitch: float,
    inset: float,
    w_fixed: float,
    w_float: float,
    w_conn: float = 100,
) -> Device:
    """
    Comb drive.

    N: number of fingers
    w: width of fingers
    L: length of fingers
    pitch: distance between start of one finger to the start of the next
    inset: overlap between the fixed and moving fingers in initial state
    w_fixed: width of fixed vertical structural element
    w_float: width of floating vertical structural element
    """
    D = Device("comb")
    assert w < pitch, "finger width must be less than the pitch"
    finger_model = pg.rectangle(size=(L, w))
    height = (N - 1) * pitch + w

    # Static side
    for i in range(N):
        finger_ref = D.add_ref(finger_model)
        finger_ref.move((0, i * pitch))
    fixed_bar = pg.rectangle(size=(w_fixed, height))
    fixed_bar_ref = D.add_ref(fixed_bar)
    fixed_bar_ref.move((-w_fixed, 0))

    # Moving side
    offset = pitch / 2
    for i in range(N - 1):
        finger_ref = D.add_ref(finger_model)
        finger_ref.move((L - inset, i * pitch + offset))
    float_bar = truss(w=w_float, h=height)
    float_bar_ref = D.add_ref(float_bar)
    float_bar_ref.move((L * 2 - inset, 0))

    # Ports
    D.add_port(
        name="anchor_top",
        midpoint=(L * 2 - inset + w_float / 2, height),
        width=w_float,
        orientation=90,
    )
    D.add_port(
        name="anchor_bottom",
        midpoint=(L * 2 - inset + w_float / 2, 0),
        width=w_float,
        orientation=270,
    )
    D.add_port(
        name="grating_conn",
        midpoint=(L * 2 - inset + w_float, height / 2),
        width=w,
        orientation=0,
    )
    D.add_port(
        name="fixed_conn",
        midpoint=(-w_fixed, height / 2),
        width=w_conn,
        orientation=180,
    )

    # qp(D)
    return D


def fillet_shape(radius: float) -> Device:
    """
    Fillet shape for strengthening corners.

    radius: fillet radius
    """
    c = pg.circle(radius=radius).move((radius, radius))
    r = pg.rectangle(size=(radius, radius))
    fillet_shape = pg.boolean(r, c, operation="A-B", layer=0)
    return fillet_shape


truss_mem = {}  # memoization since truss generation takes a long time


def truss(
    w: float, h: float, diam: float = 4, dist: float = 3, margin: float = 2
) -> Device:
    """
    Truss structure for rigidity. Dimensions should be equiv dist mod (diam+dist) for prettiest results.

    w: width of the truss
    h: height of the truss
    diam: diameter of the circular holes in the truss
    dist: distance between the holes
    margin: distance between hole and truss edge
    """
    global truss_mem
    if (w, h, diam, dist, margin) in truss_mem:
        return truss_mem[(w, h, diam, dist, margin)]
    D = Device("truss")
    r = pg.rectangle(size=(w, h))
    hole = pg.circle(radius=diam / 2)
    H = Device("holes")

    slots_x = np.arange(margin + diam / 2, w - diam / 2 + 1, dist + diam)
    slots_y = np.arange(margin + diam / 2, h - diam / 2 + 1, dist + diam)
    locations = [(x, y) for x in slots_x for y in slots_y]
    for loc in locations:
        H.add_ref(hole).move(loc)
    r = pg.boolean(r, H, operation="A-B", layer=0)
    D.add_ref(r)
    # qp(D)
    truss_mem[(w, h, diam, dist, margin)] = D
    return D


if __name__ == "__main__":
    phidl.set_quickplot_options(blocking=True)
    g = grating(N=50, bar_w=6, bar_l=500, pitch=12)
    c = comb(N=100, w=2, L=50, pitch=8, inset=10, w_fixed=200, w_float=50)
    a = anchor_single(anchor_w=50, anchor_h=100, L=300, w=3, space=94)
    rigor_mortis_gatsby(
        comb=c,
        anchor=a,
        grating=g,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
    )
    # f = flexible_grating(N=50, bar_w=6, bar_l=300, pitch=10, spring_l=100, spring_w=2)
    # a = anchor_extraduty(anchor_w=580, anchor_h=100, L1=1300, L2=500, w=3, space=94)
    # a = anchor_single(anchor_w=580, anchor_h=100, L=1300, w=3, space=94)
    # a = anchor(anchor_w=100, anchor_h=100, L1=1300, L2=500, w=5, space=94)
    # # a = anchor(anchor_w=100, anchor_h=100, L1=1300, L2=1500, w=3, space=94)
    # c = comb(N=200, w=3, L=100, pitch=12, inset=20, w_fixed=500, w_float=100)
    # # c = comb(N=200, w=3, L=100, pitch=12, inset=20, w_fixed=100, w_float=100)
    # grate = grate_gatsby(
    #     flexible_grating=f,
    #     anchor=a,
    #     comb=c,
    #     vcc_pad_size=(1000, 1000),
    #     gnd_pad_size=(1000, 1000),
    # )
    # grate.write_gds("output/grate_full.gds")
    # combed = combed_gatsby(
    #     comb=c,
    #     anchor=a,
    #     vcc_pad_size=(1000, 1000),gnd_pad_size=(1000, 1000),
    #     name="1"
    # )
    # combed.write_gds("output/comb_drive.gds")
    # f = grating(N=100, bar_w=6, bar_l=1000, pitch=10)
    # just_g = just_grate_gatsby(grating=f, name="1")
    # just_g.write_gds("output/just_grate.gds")
