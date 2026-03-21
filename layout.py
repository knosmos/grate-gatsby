import phidl
from phidl import Device
import phidl.geometry as pg
from phidl import quickplot as qp

import devices as dev
import util


def chip(flexure_width: float, flexure_length: float, name: str = "1"):
    """ """
    width = 8000
    height = 18000

    D = Device("chip")
    D << util.box(width, height)

    ### DUAL DEVICES ###
    f = dev.flexible_grating(
        N=50, bar_w=6, bar_l=300, pitch=10, spring_l=100, spring_w=2
    )
    a = dev.anchor(anchor_w=100, anchor_h=100, L1=1300, L2=500, w=5, space=94)
    c = dev.comb(N=200, w=3, L=100, pitch=12, inset=20, w_fixed=300, w_float=100)
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
        comb=c, anchor=a, vcc_pad_size=(1000,1000),gnd_pad_size=(1000,1000),
    ).rotate(-90)
    D.add_ref(comb).move((width / 4 - 1500, height * 1 / 8 + 1000))
    D.add_ref(comb).move((width / 4 - 1500, -height * 1 / 8 - 1000))

    ### GRATINGS
    g = dev.grating(N=100, bar_w=6, bar_l=1000, pitch=10)
    undriven_grate = dev.just_grate_gatsby(
        grating=g
    )
    D.add_ref(undriven_grate)

    qp(D)
    return D


if __name__ == "__main__":
    phidl.set_quickplot_options(blocking=True)
    chip(10, 10)
