"""
Optically tunable diffraction grating with comb drive actuation
6.2600 / 3.155, Spring 2026
Wafer layout code
Jieruei Chang
"""

from itertools import product

from phidl import Device
import phidl.geometry as pg
from phidl import quickplot as qp

import devices as dev
import util


def chip(
    finger_length: float,
    spring_length: float,
    flexure_width: float,
    flexure_length: float,
    grating_width: float,
    name: str = "1",
):
    """
    Delicious.
    """
    width = 8000
    height = 18000
    margin = 100
    print(
        "finger_length:",
        finger_length,
        "spring_length:",
        spring_length,
        "flexure_width:",
        flexure_width,
        "flexure_length:",
        flexure_length,
        "grating_width:",
        grating_width,
    )

    D = Device("chip")
    box = util.box(width, height, margin)

    f = dev.flexible_grating(
        N=50, bar_w=grating_width, bar_l=500, pitch=grating_width*2, spring_l=spring_length, spring_w=2
    )
    a = dev.anchor_single(
        anchor_w=50,
        anchor_h=100,
        L=flexure_length,
        w=flexure_width,
        space=94,
    )
    a_extra = dev.anchor_extraduty(
        anchor_w=50,
        anchor_h=100,
        L1=flexure_length,
        L2=flexure_length,
        w=flexure_width,
        space=94,
    )
    c = dev.comb(
        N=100, w=3, L=finger_length, pitch=12, inset=20, w_fixed=100, w_float=50
    )
    c_small = dev.comb(
        N=100, w=2, L=finger_length, pitch=8, inset=20, w_fixed=50, w_float=50
    )
    g = dev.grating(N=100, bar_w=grating_width, bar_l=1000, pitch=10)

    ### DUAL DEVICES ###
    grate = dev.grate_gatsby(
        flexible_grating=f,
        anchor=a,
        comb=c,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
        gnd_trace_length=0,
    )
    D.add_ref(grate).move((-width / 4 - 600, height / 4 + 1000))
    grate_small_comb = dev.grate_gatsby(
        flexible_grating=f,
        anchor=a,
        comb=c_small,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
        gnd_trace_length=0,
    )
    D.add_ref(grate_small_comb).move((-width / 4 - 600, 0))
    grate_extraduty = dev.grate_gatsby(
        flexible_grating=f,
        anchor=a_extra,
        comb=c,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
    )
    D.add_ref(grate_extraduty).move((-width / 4 - 600, -height / 4 - 1000))

    ### SINGLE DEVICES
    half_grate = dev.less_grate_gatsby(
        flexible_grating=f,
        anchor=a,
        comb=c,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
    ).rotate(180)
    D.add_ref(half_grate).move((width / 4, height * 4 / 8 - 1000))
    half_grate_small_comb = dev.less_grate_gatsby(
        flexible_grating=f,
        anchor=a,
        comb=c_small,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
    ).rotate(180)
    D.add_ref(half_grate_small_comb).move((width / 4, height * 3 / 8 - 1000))
    half_grate_extraduty = dev.less_grate_gatsby(
        flexible_grating=f,
        anchor=a_extra,
        comb=c,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
    ).rotate(180)
    D.add_ref(half_grate_extraduty).move((width / 4, -height * 3 / 8 + 1500))
    half_grate_extraduty_comb_small = dev.less_grate_gatsby(
        flexible_grating=f,
        anchor=a_extra,
        comb=c_small,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
    ).rotate(180)
    D.add_ref(half_grate_extraduty_comb_small).move((width / 4, -height * 4 / 8 + 1500))

    ### COMBS
    comb = dev.combed_gatsby(
        comb=c,
        anchor=a,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
    ).rotate(-90)
    D.add_ref(comb).move((width / 4 - 300, height * 1 / 8 + 700))
    comb_small = dev.combed_gatsby(
        comb=c_small,
        anchor=a,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
    ).rotate(-90)
    D.add_ref(comb_small).move((width / 4 - 2500, height * 1 / 8 + 700))
    comb_extraduty = dev.combed_gatsby(
        comb=c,
        anchor=a_extra,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
    ).rotate(-90)
    D.add_ref(comb_extraduty).move((width / 4 - 300, -height * 1 / 8 - 500))
    comb_extraduty_small = dev.combed_gatsby(
        comb=c_small,
        anchor=a_extra,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
    ).rotate(-90)
    D.add_ref(comb_extraduty_small).move((width / 4 - 2500, -height * 1 / 8 - 500))

    ### GRATINGS
    undriven_grate = dev.just_grate_gatsby(grating=g)
    D.add_ref(undriven_grate).move((200, 0))

    # ID
    id_text = util.knockout(name, 50).move(
        (-width / 2 + margin, height / 2 - margin - 400)
    )
    text_dev = Device("id_text")
    text_dev.add_ref(id_text)
    D << text_dev

    ### KNOCKOUT
    # due to computational cost, we'll first generate
    # a simplified model of the device. We'll filter for
    # gratings/combs and use the bounding boxes of those
    # components. For other components, we'll just use the original geometry.

    D_simplified = Device("simplified")
    for device in D.references:
        for ref in device.parent.references:
            # print(ref.parent.name)
            if "grating" in ref.parent.name or "comb" in ref.parent.name or "anchor" in ref.parent.name:
                simplified_ref = pg.rectangle(size=ref.bbox[1] - ref.bbox[0])
                simplified_ref.move(ref.bbox[0]).move(device.origin)
                D_simplified << simplified_ref
            else:
                D_simplified.add_ref(ref.parent).rotate(ref.rotation).move(ref.origin).move(device.origin)
    outline = pg.kl_outline(D_simplified, distance=90, tile_size=(20000,20000))
    # D << outline
    # D_simplified
    # D_simplified.remap_layers({0: 1})
    # D << D_simplified

    pour = pg.rectangle(size=(width, height)).move((-width / 2, -height / 2))
    pour = pg.boolean(pour, box, "A-B")
    pour = pg.boolean(pour, outline, "A-B")
    pour = pg.boolean(pour, D_simplified, "A-B")

    # substrate pads
    pour = pg.boolean(pour, pg.rectangle((2000, 2000)).move((width / 4, -1000)), "A-B")
    pour = pg.boolean(pour, pg.rectangle((1000, 3000)).move((-width / 4 + 900, height/4 - 1000 + 1600)), "A-B")
    pour = pg.boolean(pour, pg.rectangle((1000, 3000)).move((-width / 4 + 900, -height/4 - 1000 - 2600)), "A-B")

    D << pour
    # D_simplified.remap_layers({0: 1})
    # D << D_simplified
    # outline.remap_layers({0: 2})
    # D << outline

    # qp(D)
    return D


def wafer():
    flexure_lengths = [100, 150, 200, 250, 300, 350]
    flexure_widths = [3, 5, 7]
    grating_widths = [6]
    finger_lengths = [100, 50]
    spring_lengths = [100, 150]
    devices = []
    f = open("output/device_params.csv", "w")
    f.write(
        "num, finger_length, spring_length, flexure_width, flexure_length, grating_width\n"
    )
    for num, paramset in enumerate(
        product(
            finger_lengths,
            spring_lengths,
            flexure_widths,
            flexure_lengths,
            grating_widths,
        )
    ):
        print(f"Generating device {num} with parameters {paramset}...")
        device = chip(*paramset, name=str(num))
        devices.append(device)
        f.write(f"{num}, {", ".join(map(str, paramset))}\n")
    f.close()
    D = Device("wafer")
    G = pg.grid(devices, spacing=(200, 200), separation=True, shape=(12, 6))
    circ_outer = pg.circle(3 * 25400)
    circ_inner = pg.circle(3 * 25400 - 100)
    D << pg.boolean(circ_outer, circ_inner, "A-B", layer=2)
    w = G.bbox[1][0] - G.bbox[0][0]
    h = G.bbox[1][1] - G.bbox[0][1]
    G.move((-G.bbox[0][0] - w / 2, -G.bbox[0][1] - h / 2))
    D << G
    D.write_gds("output/wafer.gds")

if __name__ == "__main__":
    # phidl.set_quickplot_options(blocking=True)
    # D = chip(100, 150, 3, 7, 6)
    # D.write_gds("output/test_chip.gds")
    wafer()