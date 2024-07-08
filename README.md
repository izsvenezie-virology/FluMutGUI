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


>*__Important:__* FluMutGUI has the [`--skip-unmatch-names`](https://izsvenezie-virology.github.io/FluMut/docs/usage/usage-cli#options) and [`--skip-unknown-segments`](https://izsvenezie-virology.github.io/FluMut/docs/usage/usage-cli#options) options flagged by default.
>Read the log for a list of skipped sequences.


## Cite FluMutGUI
We are currently writing the paper. 
Until the publication please cite the FluMut GitHub repository:

[https://github.com/izsvenezie-virology/FluMut](https://github.com/izsvenezie-virology/FluMut)

## License
FluMutGUI is licensed under the GNU Affero v3 license (see [LICENSE](LICENSE)).

# Fundings

This work was supported by FLU-SWITCH Era-Net ICRAD (grant agreement No 862605) and by the NextGeneration EU-MUR PNRR Extended Partnership initiative on Emerging Infectious Diseases (Project no. PE00000007, INF-ACT)

![](https://github.com/izsvenezie-virology/FluMut/blob/main/docs/images/Logo-Flu-Switch.png) ![](https://github.com/izsvenezie-virology/FluMut/blob/main/docs/images/Logo-Inf-act.jpg) ![](https://github.com/izsvenezie-virology/FluMut/blob/main/docs/images/Logo-eu.png)

>Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Health and Digital Executive Agency (HEDEA). 
>Neither the European Union nor the granting authority can be held responsible for them
