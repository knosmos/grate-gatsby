# grate-gatsby
## Tunable Optical Diffraction Grating via Electrostatic MEMS Actuation

![Concept](https://raw.githubusercontent.com/knosmos/grate-gatsby/refs/heads/main/img/concept.png?test=1)

MEMS-actuated optical diffraction gratings are a promising technology for applications in compact spectrometers and beam steering devices. This repository contains parameterized layout code for a single-mask SOI MEMS diffraction grating design, featuring a tunable grating pitch achieved through comb-drive electrostatic actuation. Each chip is designed to fit on a SOIC-28 package, with grating targets of 590 x 500 microns. Twelve devices are included on each chip: three double-sided comb drive diffraction gratings, four single-sided comb drive diffraction gratings, two comb drive testing devices (without gratings), two phase-shifting diffraction gratings (built with rigid gratings), and one fixed grating target.

[Technical paper](/img/paper.pdf)

## Design Overview
### Chip Layout
![Device Layout](https://raw.githubusercontent.com/knosmos/grate-gatsby/refs/heads/main/img/device.png)
The chips are designed to be cut in groups of three to fit in the 25 x 25 mm chamber of the critical point dryer used in the fabrication process. Each device contains 1mm x 1mm pads for wire bonding (and soldering, if necessary) to the SOIC-28 package.

### Grating and Comb Drive Design
![Grating and Comb Drive Design](https://raw.githubusercontent.com/knosmos/grate-gatsby/refs/heads/main/img/detail.png)
The minimum feature size is 2 microns. Truss designs are used on large rigid free-moving structures to allow the BOE etch to undercut the structures and release them from the substrate. A guardrail structure is algorithmically generated around the perimeter of all device to prevent damage during the CPD process.

### Full Wafer Layout
![Full Wafer Layout](https://raw.githubusercontent.com/knosmos/grate-gatsby/refs/heads/main/img/wafer.png)
The full 6-inch wafer layout includes 24 chips generated from a parametric sweep over the flexure and comb drive parameters. The parameters are written to `output/device_params.csv`. The wafer itself is stored at `output/wafer_3993.gds`.

## Results
The device works surprisingly well! Here's a picture of the optical testing setup and our chip with a HeNe laser focused on one of the devices:
<p align="center">
<img width="2531" height="1146" alt="image" src="https://github.com/user-attachments/assets/a22e1d20-6b26-4442-8d40-3cb7fee5c1b7" />
</p>

And a phone video of the actuation:
<p align="center">
<img align="center" width="80%" alt="diffraction-actuation" src="https://github.com/user-attachments/assets/f8fe6eca-3c8e-4d03-bda4-fccb9f366921" />
</p>

What you see moving here is the diffraction off the comb drive; the actual diffraction shift is on the order of microradians and is not visible to the naked eye. However, we live in a society that can make better eyes. Here are measurements of the first-order diffraction shift from a very sensitive quadrant cell photoreceiver:
<p align="center">
<img align="center" width="50%" alt="image" src="https://github.com/user-attachments/assets/57449e0f-ad87-431b-bf16-198db5e904b8" />
</p>

## Contributors
- Jieruei Chang, *MIT EECS*
- Keira Boone, *MIT DMSE*
- Alysha Rawji, *MIT AeroAstro*
