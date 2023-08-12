# GEOSPATIAL ANALYSIS USING PYTHON.
## INTRODUCTION
This project is my way of perfoming the various aspects of geospatial analysis with python3 involving using python to acquire and work with geographic data and deriving data from spatial information, perform other spatial operations, and also explore real-world operations such as enviromental monitoring, urban planning and disaster management.

**Contributions from the community are welcome and encouraged** 

The first part of this application is data acquisition and the script for that is data_download.py

## HOW TO INSTALL AND RUN THE PROJECT.

Follow these steps to run this project on your local machine.

### Prerequisites.
- Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/)


### Installation.
1. Clone the repository by using the terminal and navigating to the directory on local machine you wish to install the project and running the following command.
```bash
git clone https://github.com/danielsampah99/geospatial-analysis-using-python.git
```

2. Install dependencies in the virtual environment after creation and activation.
That can be done using the following:

- Navigate to the just cloned repository directory.
```bash
cd geospatial-analysis-using-python
```

- Create a virtual environment using venv called **sentinelvenv**
```bash
python -m venv sentinelenv
```

- Activate the virtual environment by running the below command.
```bash
# On windows.
venv\Scripts\activate

# On Linux/MacOS
source venv/bin/activate
```

- Install the required python packages using pip.
```bash
pip install -r requirements.txt
```

## RUN THE PROJECT.
### Sentinel Data Acquisition - download_data.py

Run the script. Enter requested information such as start date, end date, cloud cover percentage when prompted.
```bash
# On windows
python download_data.py

# On Linux/MacOS 
python3 download_data.py
```


> **.geojson file.**
    Create a geojson file or search area by heading to [geojson.io](https://www.geojson.io) and digitizing/ selecting a search area and replacing the coodrinates with what is in this repository.
