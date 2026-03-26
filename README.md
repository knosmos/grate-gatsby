# grate-gatsby
## Tunable Optical Diffraction Grating via Electrostatic MEMS Actuation

![Concept](./img/concept.png)

MEMS-actuated optical diffraction gratings are a promising technology for applications in compact spectrometers and beam steering devices. This repository contains parameterized layout code for a single-mask SOI MEMS diffraction grating design, featuring a tunable grating pitch achieved through comb-drive electrostatic actuation. Each chip is designed to fit on a SOIC-28 package, with grating targets of 500 x 500 microns. Seven devices are included on each chip: two double-sided comb drive diffraction gratings, two single-sided comb drive diffraction gratings, two comb drive testing devices (without gratings), and one fixed grating.

## Design Overview
### Chip Layout
![Device Layout](./img/device.png)
The chips are designed to be cut in groups of three to fit in the 25 x 25 mm chamber of the critical point dryer used in the fabrication process. Each device contains 1mm x 1mm pads for wire bonding (and soldering, if necessary) to the SOIC-28 package.

### Grating and Comb Drive Design
![Grating and Comb Drive Design](./img/detail.png)
The minimum feature size is 2 microns. Truss designs are used on large rigid free-moving structures to allow the BOE etch to undercut the structures and release them from the substrate.

### Full Wafer Layout
![Full Wafer Layout](./img/wafer.png)
The full 6-inch wafer layout includes 54 chips generated from a parametric sweep over the flexure and comb drive parameters.

## Contributors
- Keira Boone, *MIT DMSE*
- Jieruei Chang, *MIT EECS*
- Alysha Rawji, *MIT AeroAstro*