# FluMutGUI

[![GitHub Release](https://img.shields.io/github/v/release/izsvenezie-virology/FluMutGUI?label=FluMutGUI)](https://github.com/izsvenezie-virology/FluMutGUI/releases/latest/)

[![install with pip](https://img.shields.io/badge/install%20with-pip-brightgreen.svg)](https://pypi.org/project/flumut-gui/)

FluMut is an open-source tool designed to search for molecular markers with potential impact on the biological characteristics of Influenza A viruses of the A(H5N1) subtype, starting from complete or partial nucleotide genome sequences.

FluMutGUI is an intuitive and user-friendly graphical interface for FluMut.

For the complete documentation please visit [FluMut site](https://izsvenezie-virology.github.io/FluMut/).

## Installation

### Installer

This is the easiest way to install FluMutGUI.
This is currently available only for Windows.
Installers for MacOS and Linux are under development.

Dowonload the installer for your Operating System from the links below, double-click the FluMutGUI installer, and follow the onscreen installation instructions.

- [Windows](https://github.com/izsvenezie-virology/FluMutGUI/releases/latest/download/FluMutGUI_Installer.exe)
- MacOS (available soon)
- Linux (available soon)

### Pip

FluMutGUI is available also on [PyPI](https://pypi.org/project/flumut-gui/).
This option is available for Windows, MacOS and Linux.
Before installing FluMut via Pip you need:

- [Python](https://www.python.org/downloads/)
- [Pip](https://pypi.org/project/pip/) (often packed with Python)

Then, you can install FluMutGUI with this command:

```
pip install flumut-gui
```

## Usage

FluMutGUI is very simple to use:

1. Update the database to latest version
1. Select the FASTA file you want to analyze (learn more [here](https://izsvenezie-virology.github.io/FluMut/docs/usage/input-file))
1. Select which [outputs](https://izsvenezie-virology.github.io/FluMut/docs/output) you want
1. Start the analysis

![](https://github.com/izsvenezie-virology/FluMut/blob/main/docs/images/GUI-usage.png)

FluMut will analyze your samples and will create the selected outputs.
When it finishes check the messages and then you can close the program.

![](https://github.com/izsvenezie-virology/FluMut/blob/main/docs/images/GUI-usage-done.png)

# Advanced options

You can use all [advanced options](./usage-cli#options) from FluMut checking the `Advanced options` flag.

![](https://github.com/izsvenezie-virology/FluMut/blob/main/docs/images/GUI-options.png)

## Cite FluMutGUI

If you use FluMutGUI, please cite:

> Giussani, E., Sartori, A. et al. (2025). FluMut: a tool for mutation surveillance in highly pathogenic H5N1 genomes. Virus Evolution, [10.1093/ve/veaf011](https://doi.org/10.1093/ve/veaf011).

## License

FluMutGUI is licensed under the GNU Affero v3 license (see [LICENSE](LICENSE)).

# Fundings

This work was partially supported by the FLU-SWITCH Era-Net ICRAD (grant agreement No. 862605), by EU funding under the NextGeneration EU-MUR PNRR Extended Partnership initiative on Emerging Infectious Diseases (Project No. PE00000007, INF-ACT), and by KAPPA-FLU HORIZON-CL6-2022-FARM2FORK-02-03 (grant agreement No. 101084171).

<p align="center" margin="10px">
    <img style="height:80px;margin:8px" alt="Logo supporter, FLU-SWITCH" src="docs/images/logo-flu-switch.png"/>
    <img style="height:80px;margin:8px" alt="Logo supporter, INF-ACT" src="docs/images/logo-inf-act.jpg"/>
    <img style="height:80px;margin:8px" alt="Logo supporter, European Union" src="docs/images/logo-eu.png"/>
    <img style="height:80px;margin:8px" alt="Logo supporter, KAPPA-FLU" src="docs/images/logo-kappa-flu.jpg"/>
</p>

> Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Health and Digital Executive Agency (HEDEA).
> Neither the European Union nor the granting authority can be held responsible for them
