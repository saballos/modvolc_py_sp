# modvolc_py_sp
This is a python script for thermal anomalies extraction for a single point of interest.
This script is able to download, visualize, compute some basic counting of thermal anomalies and produce CSV format output files for MODIS sensor data processed with the MODVOLC algorithm using the Normalized Thermal Index (NTI) developed by ```Wright et al. (2002). Automated volcanic eruption detection using MODIS. Remote sensing of environment, 82(1), 135-155```. 
See also: ```Wright et al. (2004) "MODVOLC: near-real-time thermal monitoring of global volcanism. Journal of Volcanology and Geothermal Research 135.1-2 : 29-49```, and 
```Wright (2016). MODVOLC: 14 years of autonomous observations of effusive volcanism from space. Geological Society, London, Special Publications, 426(1), 23-53```.
## Requirements
* python (ideally v. 3.11)
* pandas (ideally v. 2.2.2)
* numpy (ideally v. 1.26.4)
* seaborn (ideally v. 0.13.2)
* matplotlib (ideally v. 3.8.4)
* folium (ideally v. 0.16.0)
* requests (ideally v. 2.31)
## Installation
There are different ways to install and run this script.
#### 1. Conda environment creation:
If you have ```conda``` already installed on your OS, follow the steps below. If you do not have ```conda``` installed it in your system (Linux/Unix, macOS, Windows), I recommend to install ```miniconda``` following the instruction on this web page [miniconda page](https://docs.anaconda.com/miniconda/). After the installation of miniconda follow these steps:

* Copy the ```URL``` of this repository to your local computer or codespace by clicking on the ```<> Code``` green button at the top of this tool's GitHub page and copying the ```HTTPS``` address that is shown, i.e. ```https://github.com/saballos/modvolc_py_sp.git```
* Make sure you have the ```Git``` software already installed on your computer. If not, you must downloaded it from the [Git page](https://git-scm.com/downloads) and installed it. There is a version for Linux/Unix, macOS and Windows systems. After the installation of the Git software, open a terminal window in your Linux or macOS system (in Windows OS open a ```git bash``` command line window)
* Locate yourself into the folder this repository will be cloned into, by using the ```cd``` command 
* Type the following command line: ```git clone https://github.com/saballos/modvolc_py_sp.git```, and hit enter. You'll see a new folder named ```modvolc_py_sp```
* If you are using Windows OS, open a ```conda``` terminal window and locate yourself into the ```modvolc_py_sp``` folder that was cloned. But if you are using linux/Unix or macOS move into the ```modvolc_py_sp``` folder with the ```cd``` command (e.g. ```cd modvolc_py_sp```). Then, type the following command line: ```conda env create -f environment.yml``, and hit enter. This process may take a while
* You have now created the ```modvolc_py_sp``` conda environment. Type in your terminal ```conda env list``` and you'll see the ```modvolc_py_sp``` env listed, and now you have to activate it by typing the following command: ```conda modvolc_py_sp```, and hitting enter
* Since your terminal window (or conda command line window) is located inside the ```modvolc_py_sp``` cloned folder and the ```modvolc_py_sp``` conda environment is activated, type now: ```pip .```, and hit enter. Type ```y``` when prompted and hit enter

#### 2. Installation with pip command:
* Linux/Unix users open a terminal window and type: ```pip install modvolc_py_sp```, and hit enter
* For Windows OS users, you need to have installed ```python 3.11``` first, then open a python command line window and type: ```pip install modvolc_py_sp```, and hit enter

#### 3. python environment creation:
For linux/Unix users, create a virtal environment in the following way:
* Clone the ```modvolc_py_sp``` GitHub repository as described above, in section ```1. Conda environment creation```
* Move yourself into the cloned folder with the ```cd``` command
* Type in your terminal: ```python3 -m venv modvolc_py_sp```, and hit enter
* Activate the environment just created by typing: ```source modvolc_py_sp/bin/activate```, and hitting enter
* Type ```pip install -r requirements.txt```, and hit enter

For Windows OS users:
* Clone the ```modvolc_py_sp``` GitHub repository as described above, in section ```1. Conda environment creation```
* Open a python command line window and move yourself into the cloned folder and type in your terminal: ```python.exe -m venv modvolc_py_sp```, and hit enter
* Activate the enviroment just created by typing: ```modvolc_py_sp\Scripts\activate.bat```, and hitting enter
* Type ```pip install -r requirements.txt```, and hit enter
