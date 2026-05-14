# grate-gatsby
## Tunable Optical Diffraction Grating via Electrostatic MEMS Actuation

![Concept](https://raw.githubusercontent.com/knosmos/grate-gatsby/refs/heads/main/img/concept.png?test=1)

MEMS-actuated optical diffraction gratings are a promising technology for applications in compact spectrometers and beam steering devices. This repository contains parameterized layout code for a single-mask SOI MEMS diffraction grating design, featuring a tunable grating pitch achieved through comb-drive electrostatic actuation. Each chip is designed to fit on a SOIC-28 package, with grating targets of 590 x 500 microns. Twelve devices are included on each chip: three double-sided comb drive diffraction gratings, four single-sided comb drive diffraction gratings, two comb drive testing devices (without gratings), two phase-shifting diffraction gratings (built with rigid gratings), and one fixed grating target.

[Technical Paper](/img/paper.pdf) (This has a lot more of the theory and fabrication details)

[Project Presentation](https://docs.google.com/presentation/d/e/2PACX-1vQXB0M1xmewHRNvFU4T3vgQ8k_zZIwviEbwVnmHmlpDbTlaOk5E5B1BzpE7vICLoAxJymx_KQaP-qTi/pub?start=false&loop=false&delayms=3000) (We won best presentation!)

[Github Repo](https://github.com/knosmos/grate-gatsby)

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

## Optical Testing
The device works surprisingly well! Here's a picture of the optical testing setup and our chip with a HeNe laser focused on one of the devices:
<p align="center">
<img width="70%" alt="image" src="https://github.com/user-attachments/assets/a22e1d20-6b26-4442-8d40-3cb7fee5c1b7" />
</p>

And a phone video of the actuation:
<p align="center">
<img align="center" width="50%" alt="diffraction-actuation" src="https://github.com/user-attachments/assets/f8fe6eca-3c8e-4d03-bda4-fccb9f366921" />
</p>

What you see moving here is the diffraction off the comb drive; the actual diffraction shift is on the order of microradians and is not visible to the naked eye. However, we live in a society that can make better eyes. Here are measurements of the first-order diffraction shift from a very sensitive quadrant cell photoreceiver:
<p align="center">
<img align="center" width="40%" alt="image" src="https://github.com/user-attachments/assets/11fd9c6b-9ff6-423f-bd1d-8c14732b2e74" />
</p>

The observed results match the general theoretical trend, though less actuation is observed than expected. 

## Imaging
We also imaged our devices after fabrication to evaluate their survival, and characterize their failure modes. Here's a beautiful interferogram of a device, showing that the suspended structure is indeed still suspended:
<p align="center">
<img width="50%" alt="image" src="https://github.com/user-attachments/assets/9fe43dc1-d245-40cf-befe-73736b6084e2" />
</p>

And here is an SEM image of a device. We observe DRIE overetch causing charge accumulation on the oxide layer, creating local electric fields that redirect etching ions into the side walls. On the comb drives, this is enough to significantly reduce the interaction area, which likely explains the reduced actuation.
<p align="center">
<img width="50%" src="https://github.com/user-attachments/assets/1974af83-7483-4327-8b47-f6b6520807bf" />
</p>

## Gallery
<p align="center">
<img width="50%" alt="image" src="https://github.com/user-attachments/assets/367dd296-71cd-4cc2-a26a-14a6dc161c82" />
  <br>
  Holding the chip at gunpoint (with an antistatic gun) while wirebonding
  <br><br>
  <img width="50%" alt="image" src="https://github.com/user-attachments/assets/b285e2b2-40c7-45e6-8be3-878178bd78a7" />
  <br>
  Very pretty (and very unsuccessful) first fabrication attempt on a 2.2 micron wafer. The support structures were hilariously undersized (despite handcalcs saying it would be ok).
  <br><br>
  <img width="50%" alt="image" src="https://github.com/user-attachments/assets/16470c2a-1473-4644-9758-b8d998aeba76" />
  <br>
  IMO any optics thing looks much cooler in the dark. You can see so many diffraction orders here
  <br><br>
  <img width="50%" alt="image" src="https://github.com/user-attachments/assets/2e03d07d-fa32-43e3-b16a-59a08bee663d" />
  <br>
  Look at this pretty box (since the headered pcb wouldn't fit in the gel-pak T_T)
</p>

## Contributors
- Jieruei Chang, *MIT EECS* (design and fabrication)
- Keira Boone, *MIT DMSE* (fabrication and packaging)
- Alysha Rawji, *MIT AeroAstro* (SEM imaging)

## Acknowledgments
- Dr. Juan Ferrera (this man spent like 100 hours in the fab to help us finish this thing)
- Ben Newcomb (for tediously fixing the wire bonder after we broke it)
- Prof. Farnaz Niroui (we stole her optics lab for a month to build the testing setup)
