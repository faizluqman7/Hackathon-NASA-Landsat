import requests
import json
import pprint
import sys
import os
import pandas as pd
import datetime as dt

# SAMPLE SCRIPT TO TEST M2M API 
# source : https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/files/M2M%20Application%20Token%20Documentation_072024.pdf

def get_m2m_api_key(username, token) -> str:  
    serviceUrl = "https://m2m.cr.usgs.gov/api/api/json/stable/"     # Define the base URL for the M2M API  
    endpoint = "login-token"                                        # Define the specific endpoint for logging in to get the API key  
    url = serviceUrl + endpoint                                     # Construct the full URL for the API request  

    payload = {"username": username, "token": token}    # Create dictionary with username and token for the request  
    json_data = json.dumps(payload)                     # Convert `payload` dictionary to a JSON-formatted string  
    response = requests.post(url, json_data)            # Make a POST request to the API with the JSON data  

    try:  
        httpStatusCode = response.status_code   # Get the HTTP status code from the response  
        if response == None:                    # Check if the response is None  
            print("No output from service")     # Print an error message if there is no response  
            sys.exit()  # Exit the program  

        output = json.loads(response.text)  # Parse the response text as JSON  
        
        response.raise_for_status()
        
    except Exception as e:  # Catch any exceptions that occur during the try block  
        response.close()  # Close the response object  
        print(e)  
        
    response.close()  # Close the response object  
    apiKey = output['data']  # Extract the API key from the output data  
    return apiKey  # Return the API key


# "scene" refers to a specific image or data product captured by a Landsat satellite 
# USING THE M2M API KEY TO DO A SCENE_SEARCH  
def search_landsat_scenes(api_key, dataset_name, acquisition_filter,spatial_filter=None):  
    try:  
        service_url = 'https://m2m.cr.usgs.gov/api/api/json/stable/'  # the base URL for the M2M API  
        api_endpoint = "scene-search"               # the specific API endpoint for scene searching  
        url = service_url + api_endpoint            # Construct the full URL for the API request  
        headers = {                                 # Define the headers for the API request  
            'X-Auth-Token': api_key,                # Include the API key for authentication  
            'Content-Type': 'application/json'      # Specify that the request body is in JSON format  
        }  
        data = {                                     # Define the request body data  
            'datasetName': dataset_name,  
            'sceneFilter':{
                'acquisitionFilter': acquisition_filter,  # Include the date range filter for acquisitions  
                'spatialFilter': spatial_filter
                },
            
        }  
        response = requests.post(url, headers=headers, json=data)   # Makes a POST request to the API  
        response.raise_for_status()                                 # Raise an error if the request was unsuccessful  
        return response.json()['data']                              # Return the 'data' field from the JSON response  
    except requests.exceptions.RequestException as e:  # Handle any request exceptions  
        print(f'Error searching Landsat scenes: {e}')  # Print the error message  
        raise e  
    
    
def search_datasets(api_key, temporal_filter, spatial_filter):
    try:  
        service_url = 'https://m2m.cr.usgs.gov/api/api/json/stable/'  # the base URL for the M2M API  
        api_endpoint = "dataset-search"               # the specific API endpoint for scene searching  
        url = service_url + api_endpoint            # Construct the full URL for the API request  
        headers = {                                 # Define the headers for the API request  
            'X-Auth-Token': api_key,                # Include the API key for authentication  
            'Content-Type': 'application/json'      # Specify that the request body is in JSON format  
        }  
        data = {                                     # Define the request body data  
            'datasetName': dataset_name,  
            'temporalFilter': temporal_filter, # Include the date range filter for acquisitions  
            
            'spatialFilter': spatial_filter
        }  
        response = requests.post(url, headers=headers, json=data)   # Makes a POST request to the API  
        
        response.raise_for_status()                                 # Raise an error if the request was unsuccessful  
        return response.json()                             # Return the 'data' field from the JSON response  
    
    except requests.exceptions.RequestException as e:  # Handle any request exceptions  
        print(f'Error searching Landsat scenes: {e}')  # Print the error message  
        raise e  
    

#downloading purposes
def create_scene_list(api_key, payload):  
    try:  
        service_url = 'https://m2m.cr.usgs.gov/api/api/json/stable/'  # the base URL for the M2M API  
        api_endpoint = "scene-list-add"               # the specific API endpoint for scene searching  
        url = service_url + api_endpoint            # Construct the full URL for the API request  
        headers = {                                 # Define the headers for the API request  
            'X-Auth-Token': api_key,                # Include the API key for authentication  
            'Content-Type': 'application/json'      # Specify that the request body is in JSON format  
        }  
        data = payload
        # {                                     # Define the request body data  
        #     'datasetName': dataset_name,  
        #     'sceneFilter':{
        #         'acquisitionFilter': acquisition_filter,  # Include the date range filter for acquisitions  
        #         'spatialFilter': spatial_filter
        #         },
            
        # }  
        response = requests.post(url, headers=headers, json=data)   # Makes a POST request to the API  
        response.raise_for_status()                                 # Raise an error if the request was unsuccessful  
        return response.json()                             # Return the 'data' field from the JSON response  
    except requests.exceptions.RequestException as e:  # Handle any request exceptions  
        print(f'Error searching Landsat scenes: {e}')  # Print the error message  
        raise e 
    
def download_scenes(api_key, payload):  
    try:  
        service_url = 'https://m2m.cr.usgs.gov/api/api/json/stable/'  # the base URL for the M2M API  
        api_endpoint = "download-options"               # the specific API endpoint for scene searching  
        url = service_url + api_endpoint            # Construct the full URL for the API request  
        headers = {                                 # Define the headers for the API request  
            'X-Auth-Token': api_key,                # Include the API key for authentication  
            'Content-Type': 'application/json'      # Specify that the request body is in JSON format  
        }  
        data = payload
        # {                                     # Define the request body data  
        #     'datasetName': dataset_name,  
        #     'sceneFilter':{
        #         'acquisitionFilter': acquisition_filter,  # Include the date range filter for acquisitions  
        #         'spatialFilter': spatial_filter
        #         },
            
        # }  
        response = requests.post(url, headers=headers, json=data)   # Makes a POST request to the API  
        response.raise_for_status()                                 # Raise an error if the request was unsuccessful  
        return response.json()                             # Return the 'data' field from the JSON response  
    except requests.exceptions.RequestException as e:  # Handle any request exceptions  
        print(f'Error searching Landsat scenes: {e}')  # Print the error message  
        raise e 


# ===================================
# GET_M2M_API_KEY() EXAMPLE USE
# Source: siderAI  
username = "tsnm"  
m2m_application_token = "e0FVsbRLSo5!9DsVnVvna27KopGox5GT7GdZ6xLRF9Ok1n1j0ldz2AiK_uKp6NHp"  
m2m_api_key = get_m2m_api_key(username, m2m_application_token)  

print("API Key: " + m2m_api_key)  

# ===================================
# SEARCH_LANDSAT_SCENES() EXAMPLE USE
dataset_name = 'landsat_ot_c2_l2'   # Define the dataset name for Landsat scenes  
date_range = {                      # Define the date range for the acquisition filter  
    'start': '2024-09-01',      # Start date for the search  
    'end': '2024-09-03'         # End date for the search  
}  

scenes = search_landsat_scenes(m2m_api_key, dataset_name, date_range)  # Call the function to search for scenes, returns a dictionary  

print(f"\n========\nDataset : '{dataset_name}'")  
print(f"Scene 1\n=========\n")  

scenes_dict = scenes['results']         # Extract the 'results' field from the scenes dictionary  
pp = pprint.PrettyPrinter(indent=4)     # Create a PrettyPrinter object for formatted output  

print(pp.pprint(scenes_dict[0]))        # Print the first scene's details in a pretty format



# ========================
# SEARCH_LANDSAT_SCENES(edinburgh)

# Define the dataset name for Landsat scenes
date_range = {
        "start": (dt.date.today() - dt.timedelta(days=16)).isoformat(), # start = current - 16
        "end": dt.date.today().isoformat() # end = current
    }


# CURRENT DATE 2024-09-24


edin_location = {
        "filterType": "mbr",
        "lowerLeft": {
            "latitude": 55.93607,
            "longitude": -3.20483
        },
        "upperRight": {
            "latitude": 55.94672,
            "longitude": -3.18626
        }
    }

dataset_dict = search_landsat_scenes(m2m_api_key, dataset_name, date_range,spatial_filter=edin_location)  # Call the function to search for scenes, returns a dictionary  

list_of_dates = []

for x in range(0, len(dataset_dict['results'])):
    list_of_dates.append(dataset_dict['results'][x]['temporalCoverage']['endDate'])

print(list_of_dates[0] + " is the most recent date LandSAT data was captured in Edinburgh.\n")
print(dt.datetime.strptime(list_of_dates[0], '%Y-%m-%d %H:%M:%S') + dt.timedelta(days=16), "is the closest future date that Landsat hovers over a location!\n")



# function that returns the closest future date that Landsat hovers over the given location

print("\n========\n")
print("Testing dataset-search:")


def get_dataset_alias(api_key, longitude, latitude, start_date=None, end_date=None):
    # Spatial and temporal filters
    spatial_filter = {
        "filterType": "mbr",
        "lowerLeft": {"latitude": latitude - 0.01, "longitude": longitude - 0.01},
        "upperRight": {"latitude": latitude + 0.01, "longitude": longitude + 0.01}
    }

    
    temporal_filter = {
        "start": start_date if start_date else "1970-01-01",
        "end": end_date if end_date else "9999-12-31"
    }

    # Use the dataset search function
    datasets = search_datasets(api_key, temporal_filter, spatial_filter)

    # Full response inspection
    #print(json.dumps(datasets, indent=4))  

    
    # Check if 'data' exists and return the datasetAlias
    if 'data' in datasets and datasets['data']:
        return datasets['data'][0]['datasetAlias']
    else:
        print("No datasetAlias found.")
        return None
    
# # Example user inputs for testing
# #longitude = -3.20483
# #latitude = 55.93607

# longitude = 55.93607
# latitude = -3.20483 
# start_date = "2022-09-01"
# end_date = "2024-09-16"

# # Call the function to get the dataset alias
# dataset_alias = get_dataset_alias(m2m_api_key, longitude, latitude, start_date, end_date)

# # Print the dataset alias for confirmation
# print(f"Dataset Alias: {dataset_alias}")


def write_pretty_print_to_file(dict, filename,directory):  
    # Ensure the directory exists  
    os.makedirs(directory, exist_ok=True)  
    
    # Create the full file path  
    file_path = os.path.join(directory, filename)  
    with open(file_path, 'w') as file:  
        pp = pprint.PrettyPrinter(indent=4, stream=file)  
        pp.pprint(dict)  
    print(f"Output has been written to {filename}")  

# Example usage  
filename = "output.txt"  
directory = "server/"
write_pretty_print_to_file(dataset_dict, filename, directory)  
# print(f"Number of matching datasets: {len(dataset_dict)}")


# print("\n========\n")
# print("Testing scene-list-add:")
# scene_list_payload = {
#     "listId": "edin_scenes",
#     "datasetName": "landsat_ot_c2_l2",
#     "entityIds": ['LC92050212024249LGN00', 'LC92040212024258LGN00','LC82050212024257LGN00', 'LC82040212024250LGN00']
# }


# scene_list = create_scene_list(m2m_api_key, scene_list_payload)
# write_pretty_print_to_file(scene_list, "edin_scene_out.txt", directory)

# download_payload = {
    # "listId":"edin_scenes" ,
#     "datasetName":"landsat_ot_c2_l2",
#     "includeSecondaryFileGroups": True   
# }

# print("\n========\n")
# print("Testing download-option:")

# prod = download_scenes(m2m_api_key, download_payload)

# dwd_scenes_dict = pd.json_normalize(prod).to_dict()
# write_pretty_print_to_file(dwd_scenes_dict, "download_edin_scene.txt", directory)


# DOWNLOADING SCENES 
# endpoint --> download-options
# - Identify product IDs that are "available" for each scene
# - endpoints --> download-request & download-retrieve
# - - Request download URLs for scene ID - product ID pairs
# - - - URLs returned as "available" are available for download
# - - - For URLs returned as "preparing," wait and check download-retrieve to see if they are "available"

print("\n========")
print("Testing gpto1's 'download' code:")
print("========\n")
import time  

def retrieve_dwn_urls(api_key, datasetName, entityIds, dwdApp="M2M"):
# Define the API endpoints  
    download_options_url = "https://m2m.cr.usgs.gov/api/api/json/stable/download-options"  # Replace with the actual URL  
    download_request_url = "https://m2m.cr.usgs.gov/api/api/json/stable/download-request"    # Replace with the actual URL  
    download_retrieve_url = "https://m2m.cr.usgs.gov/api/api/json/stable/download-retrieve"  # Replace with the actual URL  

    dataset_name = datasetName  
    entity_ids = entityIds  

    # Step 1: Request download options  
    download_options_payload = {  
        "datasetName": dataset_name,  
        "entityIds": entity_ids,  
        "includeSecondaryFileGroups": True  
    }  
    headers = {                                 # Define the headers for the API request  
            'X-Auth-Token': api_key,                # Include the API key for authentication  
            'Content-Type': 'application/json'      # Specify that the request body is in JSON format  
        } 

    response = requests.post(download_options_url, json=download_options_payload, headers=headers)  
    download_options = response.json()  # dict of download options
    print(f'--> Num of dwdOptions: {len(download_options.get("data"))}')
    print(f'--> Num of secondaryDownloads for each dwdOption: {len(download_options.get("data")[0].get("secondaryDownloads"))}')

    # Step 2: Identify available product IDs  
    available_products = []  
    for product in download_options.get("data", []):  # gets nested dict that has the download options
        if product.get("available"):                  # `available` key holds a boolean value True/False | If it IS available then it gets added to available_products list
            available_products.append({  
                "entityId": product["entityId"],  
                "productId": product["id"]  
            })  
            

    # Step 3: Request download URLs  
    download_requests = []  
    for product in available_products:  
        download_requests.append({  
            # "label": product["entityId"],  
            "entityId": product["entityId"],  
            "productId": product["productId"]  
        })  
    
    download_request_payload = {  
        "downloads": download_requests,  
        "downloadApplication": dwdApp  # Specify the application if needed  
    }  

    response = requests.post(download_request_url, json=download_request_payload, headers=headers)  
    download_request_response = response.json()  
    

    # Step 4: Check for available URLs  
    available_downloads = download_request_response.get("data", {}).get("availableDownloads", [])  
    preparing_downloads = download_request_response.get("data", {}).get("preparingDownloads", []) 

    # Step 5: Wait for preparing downloads to become available  
    while preparing_downloads:  
        print("Waiting for preparing downloads to become available...")                                
        time.sleep(10)  # Wait for 10 seconds before checking again  

        # Check the status of downloads  
        response = requests.post(download_retrieve_url, json={"label": "test", "downloadApplication": dwdApp})  
        download_retrieve_response = response.json()  
        preparing_downloads = download_retrieve_response.get("data", {}).get("requested", [])  

    # Print available download URLs
    download_url_list = []  
    if available_downloads:  
        # print("Available download URLs:")  
        for download in available_downloads:  
            # print(download["url"])
            download_url_list.append(download["url"])  
    else:  
        print("No available downloads.")
    return download_url_list
    
        
        
# ========== DOWNLOADING LANDSAT EDIN SCENES ============
# input params for downloading
entity_ids = "LC92050212024249LGN00,LC92040212024258LGN00,LC82050212024257LGN00,LC82040212024250LGN00"
dwd_urls_list = retrieve_dwn_urls(m2m_api_key, dataset_name, entity_ids)
print("--> Available download urls: ")
print(dwd_urls_list)

        
import requests
import os
import zipfile
import tarfile
from urllib.parse import urlparse

def download_and_extract_zip(url, download_dir):
    # Create the download directory if it doesn't exist
    os.makedirs(download_dir, exist_ok=True)

    filename="generic-filename"
    file_path = os.path.join(download_dir,"")
    
    try:
        # Download the file
        response = requests.get(url, stream=True)
        print(f"--> dwd url response : {response}")
        response.raise_for_status()
        print("=======\n")
        
        # Check for Content-Disposition header to get the filename  
        if 'Content-Disposition' in response.headers:  
            content_disposition = response.headers['Content-Disposition']  
            if 'filename=' in content_disposition:  
                # Extract the filename from the header  
                filename = content_disposition.split('filename=')[1].strip('"')  
                file_path = os.path.join(download_dir, filename)

        # check if file already saved in directory
        if os.path.exists(file_path):  
            print(f"File already exists: {filename}. Skipping download.")  
        else:    
            # # Save the zip file # !!! UNCOMMENT IF YOU WANT TO DOWNLOAD THE FILES | took around 20 mins to download 4 .tar files
            # with open(file_path, 'wb') as file:
                # for chunk in response.iter_content(chunk_size=8192):
                    # file.write(chunk)
            print(f"Downloaded: {filename}")
        
        # Extract the contents of the tar file  
        
        extract_dir = os.path.join(download_dir, os.path.splitext(filename)[0])  
        os.makedirs(extract_dir, exist_ok=True)  

        # Extract the contents of the tar file into the new directory  
        print(f"Extracting: {filename} into {extract_dir}")  
        with tarfile.open(file_path, 'r:*') as tar_ref:  
            tar_ref.extractall(extract_dir)  
        print(f"Extracted: {filename} into {extract_dir}")  
        
        # Optionally, remove the tar file after extraction  
        os.remove(file_path)  
        print(f"Removed tar file: {filename}")  

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
    except tarfile.TarError:  
        print(f"Failed to extract {filename}: Not a valid tar file")  
    except Exception as e:
        print(f"An error occurred while processing {filename}: {e}")


# !!! REPLACE THIS PATH WITH YOUR OWN PATHS ON YOUR RESPECTIVE LAPTOPS vv
download_directory = "C:/Users/User-PC/Documents/Overseas stuff/Edinburgh/Year 3 drive/coding projects/Landsat data/dwd_&_xtract_test"

print("Processing download URLs:")
for url in dwd_urls_list:
    print(f"Processing: {url}")
    download_and_extract_zip(url, download_directory)
print("\n*** DONE UNZIPPING LANDSAT FILES ***\n")


import rasterio  
import numpy as np  
import matplotlib.pyplot as plt  


# File paths for the TIF images  
# "C:/Users/User-PC/Documents/Overseas stuff/Edinburgh/Year 3 drive/coding projects/Landsat data/dwd_&_xtract_test/LC08_L2SP_204021_20240906_20240914_02_T1/LC08_L2SP_204021_20240906_20240914_02_T1_SR_B2"
band_2_path = "C:/Users/User-PC/Documents/Overseas stuff/Edinburgh/Year 3 drive/coding projects/Landsat data/dwd_&_xtract_test/LC08_L2SP_204021_20240906_20240914_02_T1/LC08_L2SP_204021_20240906_20240914_02_T1_SR_B2.tif"  # Replace with the actual path to Band 2  
band_3_path = "C:/Users/User-PC/Documents/Overseas stuff/Edinburgh/Year 3 drive/coding projects/Landsat data/dwd_&_xtract_test/LC08_L2SP_204021_20240906_20240914_02_T1/LC08_L2SP_204021_20240906_20240914_02_T1_SR_B3.tif"  # Replace with the actual path to Band 3  
band_4_path = "C:/Users/User-PC/Documents/Overseas stuff/Edinburgh/Year 3 drive/coding projects/Landsat data/dwd_&_xtract_test/LC08_L2SP_204021_20240906_20240914_02_T1/LC08_L2SP_204021_20240906_20240914_02_T1_SR_B4.tif"  # Replace with the actual path to Band 4  

# Read the TIF files  
with rasterio.open(band_2_path) as band2:  
    band2_data = band2.read(1)  # Read the first band (Band 2)  
    profile = band2.profile

with rasterio.open(band_3_path) as band3:  
    band3_data = band3.read(1)  # Read the first band (Band 3)  

with rasterio.open(band_4_path) as band4:  
    band4_data = band4.read(1)  # Read the first band (Band 4)  

# Function to perform contrast stretching  
def contrast_stretch(band_data):  
    # Get the minimum and maximum values  
    min_val = np.min(band_data)  
    max_val = np.max(band_data)  
    
    # Perform contrast stretching  
    stretched = (band_data - min_val) / (max_val - min_val) * 255  
    return stretched.astype(np.uint8)  

# Apply contrast stretching to each band  
band2_stretched = contrast_stretch(band2_data)  
band3_stretched = contrast_stretch(band3_data)  
band4_stretched = contrast_stretch(band4_data)  

# Stack the bands into a 3D array (RGB)  
rgb_image = np.stack((band4_stretched, band3_stretched, band2_stretched), axis=0)  # Band 4 (Red), Band 3 (Green), Band 2 (Blue)  

# Optionally, save the color image  
output_path = 'server/rgb_stack_L08_20240914_contrast_stretched.tif'  # Replace with desired output path 

# Update the profile for a 3-band GeoTIFF
profile.update(
    dtype=rasterio.uint8,
    count=3,
    compress='lzw'
)

# Save the color image as a GeoTIFF
with rasterio.open(output_path, 'w', **profile) as dst:
    dst.write(rgb_image)

