# preprocessing.py
# Import necessary packages.
import glob
import os
import shutil
import xml.etree.ElementTree as ET
from zipfile import ZipFile, is_zipfile
import numpy as np

import rasterio

# Set the path to the 6S executable
os.environ['SIXS_PATH'] = '/path/to/6s/executable'

# Module level variables.
zipped_file = r"C:\Users\danny\Downloads\sentinel data\S2B_MSIL1C_20230922T081639_N0509_R121_T38VMN_20230922T090935.zip"
extract_to = r"C:\Users\danny\Downloads\sentinel data"


def unzipping_data(zipped_file_arg=zipped_file, extracted_file_arg=extract_to):
    """Unzipping the zipped the Sentinel-2 data."""
    # Extract the zipped file.
    if is_zipfile(zipped_file_arg):
        print(f"{zipped_file_arg} is a zip file.")
        with ZipFile(file=zipped_file_arg, mode="r") as zipped:
            # Check if file is a valid zipfile or has a zip extension.

            zipped.extractall(path=extracted_file_arg)
            print(
                f"{len(zipped.filelist)} files have been extracted FROM {zipped.filename} TO {extracted_file_arg}")
    else:
        print(f"{zipped_file_arg} is not a zip file.")


jp2_band_files = glob.glob(pathname=os.path.join(extract_to, "**/IMG_DATA/*.jp2"), recursive=True)
tiff_output_directory = fr"{os.path.dirname(jp2_band_files[1])}\TIFF IMAGE DATA"


def band_conversion(jp2_bands_directory=None, tif_bands_directory=tiff_output_directory):
    """converting bands from jpeg2000 (.jp2) file format to geotiff files."""
    # Create the output directory.
    if tif_bands_directory is None:
        tif_bands_directory = tiff_output_directory
    if jp2_bands_directory is None:
        jp2_bands_directory = jp2_band_files

    jp2_bands_directory = glob.glob(pathname=os.path.join(extract_to, "**/IMG_DATA/*.jp2"), recursive=True)
    tif_bands_directory = fr"{os.path.dirname(jp2_bands_directory[1])}\TIFF IMAGE DATA"
    os.makedirs(name=tif_bands_directory, exist_ok=True)

    print(f"The output directory has a path: {tif_bands_directory}")
    print(f"The are {len(jp2_bands_directory)} files and folders in the {jp2_bands_directory} directories.")

    # Loop through each band files and convert it.
    for jp2_band_file in jp2_bands_directory:
        # Create the output file.
        tif_band_file = os.path.join(tif_bands_directory,
                                     os.path.relpath(jp2_band_file, tif_bands_directory).replace(".jp2", ".tif"))
        print(f"{tif_band_file}")

        # Open the input band using rasterio.
        with rasterio.open(jp2_band_file) as source:
            print(f"coordinate reference system: {source.crs}")
            profile = source.profile
            profile['driver'] = 'GTiff'
            profile['crs'] = source.crs
            with rasterio.open(tif_band_file, 'w', **profile) as dst:
                dst.write(source.read())

        # Move the .tif files to the new TIF IMAGE DATA directory.
        shutil.move(src=tif_band_file, dst=tif_bands_directory)


# TODO: Uninstall the py6s module.


def atmospheric_correction():
    """make corrections for aerosol and visibility of the tif bands."""

    # Converting the digital numbers of the bands to radiance values.
    input_bands = glob.glob(os.path.join(tiff_output_directory, "*.tif"))
    input_band = input_bands[0]
    # print(input_bands)

    # Find a list of files that have .xml extension.
    all_xml_files = glob.glob(os.path.join(extract_to, "**", "*.xml"), recursive=False)

    # Path to the main metadata file.
    meta_file = all_xml_files[-1]

    # Parsing the xml file.
    tree = ET.parse(meta_file)
    root = tree.getroot()

    # Find the physical gain and offset elements.
    physical_gains = root.findall(".//PHYSICAL_GAINS")
    offset_list = root.findall(".//RADIO_ADD_OFFSET")

    # Dictionaries to store band gains and offset values and their respective values.
    band_gains = {}
    band_offsets = {}

    # Iterate the physical gains list and assign each to respective bands.
    for physical_gain in physical_gains:
        band_id = physical_gain.get("bandId")
        gain_value = float(physical_gain.text)
        band_gains[band_id] = gain_value

    # Iterate the band offset list and assign each to respective bands.
    for offset_element in offset_list:
        band_id = offset_element.get("band_id")
        offset_value = int(offset_element.text)
        band_offsets[band_id] = offset_value

    # Convert each pixel value to radiance.
    channel_gain = band_gains["1"]
    channel_offset = band_offsets["1"]
    print(channel_offset+channel_gain)

    # Open file input band file with rasterio.
    with rasterio.open(input_band, "r") as src:
        input_band = src.read()

        # Create a temporary array for radiance values.
        temp_data_array = np.empty_like(input_band)

        # Looping through the image.
        for i, row in enumerate(input_band):
            for j, col in enumerate(row):

                # Check if pixel is not nan to avoid pixel correction.
                if input_band.any() != np.nan:
                    temp_data_array[i][j] = input_band[i][j] * channel_gain + channel_offset
                    print(f"Radiance Calculated for band: {input_band}")
                    return temp_data_array


atmospheric_correction()
