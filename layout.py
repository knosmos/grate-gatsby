"""
Optically tunable diffraction grating with comb drive actuation
6.2600 / 3.155, Spring 2026
Wafer layout code
Jieruei Chang
"""

from itertools import product

import phidl
from phidl import Device
import phidl.geometry as pg
from phidl import quickplot as qp

import devices as dev
import util


def chip(
    flexure_width: float,
    flexure_length: float,
    finger_length: float,
    grating_width: float,
    spring_length: float,
    name: str = "1",
):
    """
    Delicious.
    """
    width = 8000
    height = 18000
    margin = 100

    D = Device("chip")
    D << util.box(width, height, margin)

    f = dev.flexible_grating(
        N=50, bar_w=6, bar_l=500, pitch=10, spring_l=spring_length, spring_w=2
    )
    a = dev.anchor(
        anchor_w=100,
        anchor_h=100,
        L1=flexure_length,
        L2=flexure_length - 600,
        w=flexure_width,
        space=94,
    )
    c = dev.comb(
        N=200, w=3, L=finger_length, pitch=12, inset=20, w_fixed=300, w_float=100
    )
    g = dev.grating(N=100, bar_w=grating_width, bar_l=1000, pitch=10)

    ### DUAL DEVICES ###
    grate = dev.grate_gatsby(
        flexible_grating=f,
        anchor=a,
        comb=c,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
    )
    D.add_ref(grate).move((-width / 4 - 400, height / 4 + 400))
    D.add_ref(grate).move((-width / 4 - 400, -height / 4 + 800))

    ### SINGLE DEVICES
    half_grate = dev.less_grate_gatsby(
        flexible_grating=f,
        anchor=a,
        comb=c,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
    ).rotate(-90)
    D.add_ref(half_grate).move((width / 4 - 500, height * 3 / 8))
    D.add_ref(half_grate).move((width / 4 - 500, -height * 3 / 8))

    ### COMBS
    comb = dev.combed_gatsby(
        comb=c,
        anchor=a,
        vcc_pad_size=(1000, 1000),
        gnd_pad_size=(1000, 1000),
    ).rotate(-90)
    D.add_ref(comb).move((width / 4 - 1500, height * 1 / 8 + 1000))
    D.add_ref(comb).move((width / 4 - 1500, -height * 1 / 8 - 1000))

    ### GRATINGS
    undriven_grate = dev.just_grate_gatsby(grating=g)
    D.add_ref(undriven_grate)

    # ID
    id_text = util.knockout(name, 100).move(
        (-width / 2 + margin, height / 2 - margin - 400)
    )
    D << id_text

    # qp(D)
    return D


def wafer():
    flexure_widths = [3, 5]
    flexure_lengths = [800, 1000, 1200]
    grating_widths = [6]
    finger_lengths = [50, 80, 100]
    spring_lengths = [50, 100, 200]
    devices = []
    f = open("device_params.txt", "w")
    for num, paramset in enumerate(
        product(
            flexure_widths,
            flexure_lengths,
            finger_lengths,
            grating_widths,
            spring_lengths,
        )
    ):
        device = chip(*paramset, name=str(num))
        devices.append(device)
        f.write(f"{num}: {paramset}\n")
    f.close()
    D = Device("wafer")
    G = pg.grid(devices, spacing=(1, 1), separation=True, shape=(9, 6))
    circ_outer = pg.circle(3 * 25400)
    circ_inner = pg.circle(3 * 25400 - 100)
    D << pg.boolean(circ_outer, circ_inner, "A-B", layer=2)
    w = G.bbox[1][0] - G.bbox[0][0]
    h = G.bbox[1][1] - G.bbox[0][1]
    G.move((-G.bbox[0][0] - w / 2, -G.bbox[0][1] - h / 2))
    D << G
    D.write_gds("wafer.gds")


if __name__ == "__main__":
    # phidl.set_quickplot_options(blocking=True)
    # chip(3, 1300, 100, 5, 200)
    wafer()
