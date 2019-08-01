# AHS Heatmap
## About
This program reads from sensors around Andover High School (AHS) and, from any amount of given SVG floor plans, hosts a web site containing interactive versions of these floor plans, in which rooms are colored according to their temperature or carbon dioxide values. These maps provide a simple, quick, and comprehensible method of locating rooms, wings, or floors with ventilation problems. It can work with any amount of floor plans, given that they meet the [required format](#floor-plan-requirements).

## Floor Plan Requirements
This project supports any number of heatmaps, granted they meet the following criteria:
* They are in SVG format
* They are placed inside the `/static/svg_and_conversions` folder ([link](https://github.com/Energize-Andover/AHS-Heatmap/tree/master/static/svg_and_conversions))
* They are named `Andover-HS-level-{level}.svg`, where `{level}` is replaced with a number representing the level of the building mapped, with `1` being the field house and `4` being the floor containing rooms 301 and up
* The room numbers are located fully inside their room
* Rooms do not have holes in their walls

An example of a properly formatted floor plan can be seen here:
<p align="center">
  <img src="https://i.imgur.com/Mt1kolY.png" alt="Sample Floor Plan">
</p>

## Features
* Quickly fetches data from all sensors 
* Usable on any map provided in SVG format
* Easy-to-use, understandable, and interactive maps
* Automatically regenerates and updates maps
* Map updating process ensures no downtime for viewers
* Error catching in the case of server failure
* Easy configuration of the definition of pure red, blue, and green values
  * Colors corresponding to sensor readings belong to a generated *even* gradient
  
## Installation
1) Clone this repository
2) [Optional]: Create a [python virtual enviornment](https://docs.python-guide.org/dev/virtualenvs/) for this project
3) Install the project's dependencies (see [Dependencies](#dependencies))
4) Install [Inkscape](https://inkscape.org/) and add it to your system's PATH (you should be able to open Inkscape by opening a terminal and running `inkscape` from any directory)
5) Ensure you have an internet connection and run `main.py`

See [Security Notice](#security-notice) to learn more

## Dependencies
To run this project on a machine, you must first install its many required packages. See [requirements.txt](https://github.com/Energize-Andover/AHS-Heatmap/blob/master/requirements.txt) for a list of required packages and their versions.

To quickly install all requirements, use the command `pip install -r requirements.txt` while in the `AHS-Heatmap` directory, or simply run [install_packages.sh](https://github.com/Energize-Andover/AHS-Heatmap/blob/master/install_packages.sh) to have the installation process done automatically.

## Security Notice
If you seek to run this project on a machine in a secure manner, do not simply run `wsgi.py` or `app.py` (both start the app using [Flask](https://palletsprojects.com/p/flask/)). The app should instead be run by using [gunicorn](https://gunicorn.org/) to run `wsgi.py`, a more secure and reliable long-term method of hosting a web server.

## Credits
This project was made by [Daniel Ivanovich](https://ivanovich.us) for the [Energize Andover Program](https://www.energizeandover.com/) between the falls of 2018 and 2019. The [buildingEnergyApi](https://github.com/navkal/buildingEnergyApi) was used to request data from the sensors. [jQuery](https://jquery.com/) and [Bulma](https://bulma.io/) were used to create the website component of this project. 

This project is licensed under the [MIT License](https://github.com/Energize-Andover/AHS-Heatmap/blob/master/LICENSE).
