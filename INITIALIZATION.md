#AHS Heatmap Initialization 
Follow this guide to properly install and initialize the heatmap on your machine.

## Cloning
First, clone this repository. Either use [GitHub Desktop](https://desktop.github.com/), [download the repository as a ZIP and extract](https://github.com/Energize-Andover/AHS-Heatmap/archive/master.zip), or run `git clone https://github.com/Energize-Andover/AHS-Heatmap.git` in the command line. Any of these methods will bring a copy of the repository into a local folder, named `AHS-Heatmap`.

##  Inkscape
An external requirement of the Heatmap is [Inkscape](https://inkscape.org/), a free universal SVG editor. It is used by the program to convert SVG files into PDF and PNG format for further map analysis. Thus, the next step is to visit [inkscape.org](https://inkscape.org/), open the `Download` page, and download and install inkscape for your operating system. 

## Python Packages
The next step is to install the required packages. Navigate to the `AHS-Heatmap` directory in your command line. Run `pip install -r requirements.txt` or, if on a UNIX device, run `install_packages.sh` to install all requirements. 

## Configuration + Index Updating
This is the **most important step**. By this point, your local installation of AHS Heatmap is in a runnable state. To ensure proper operation, edit `config.py`'s global configuration variables to your liking. See the comments (text beginning with `#`s) to understand what each variable is and what it does. Do **not** delete any of the variables - doing so will stop the Heatmap from running. 

Finally, please ensure you keep your machine-specific configurations **out of the reposiory** by running `git update-index --skip-worktree config.py` in the `AHS-Heatmap` directory. Doing so will stop local updates of `config.py` from being tracked, committed, or pushed.