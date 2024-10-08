import requests
import json
import pprint
import sys
import os
import pandas as pd
import datetime as dt
from dotenv import load_dotenv
import requests
import os
import tarfile
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import time  

from google.cloud import storage

#import rasterio  
import numpy as np  

# install python packages:
# pip install requests json5 pandas python-dotenv google-cloud-storage rasterio numpy

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
    



def write_pretty_print_to_file(dict, filename,directory):  
    # Ensure the directory exists  
    os.makedirs(directory, exist_ok=True)  
    
    # Create the full file path  
    file_path = os.path.join(directory, filename)  
    with open(file_path, 'w') as file:  
        pp = pprint.PrettyPrinter(indent=4, stream=file)  
        pp.pprint(dict)  
    print(f"Output has been written to {filename}")  
# ===================================
# GET_M2M_API_KEY() EXAMPLE USE
# Source: siderAI  
load_dotenv()
m2m_username = os.getenv("M2M_USERNAME")
m2m_app_token = os.getenv("M2M_APP_TOKEN")
m2m_api_key = get_m2m_api_key(m2m_username, m2m_app_token)  

dataset_name = 'landsat_ot_c2_l2'   # Define the dataset name for Landsat scenes  

# Define the dataset name for Landsat scenes
date_range = {
        "start": (dt.date.today() - dt.timedelta(days=16)).isoformat(), # start = current - 16
        "end": dt.date.today().isoformat() # end = current
    }


# Cooridinates from server.js endpoint (/retrieve-satellite-data)
# Only use if everything else works / delete if not
# def get_satellite_data():
#     url = "http://localhost:3000/retrieve-satellite-data"
#     satelite_data_response = requests.get(url)


#     if satelite_data_response.status_code == 200:
#         data = satelite_data_response.json()
#         lat = data.get('lat')
#         lng = data.get('lng')

#         # Now you can use lat and lng in your Landsat processing logic
#         print(f"Received coordinates: Latitude: {lat}, Longitude: {lng}")

#     else:
#         print(f"Failed to retrieve coordinates. Status code: {satelite_data_response.status_code}")

    
#     edin_location = {
#             "filterType": "mbr",
#             "lowerLeft": {"latitude": float(lat) - 0.05, "longitude": float(lng) - 0.05},
#             "upperRight": {"latitude": float(lat) + 0.05, "longitude": float(lng) + 0.05}
#         }

#backup function in case the above doesn't work
lat = float(input("Enter latitude: "))  # Prompt user for latitude
lng = float(input("Enter longitude: "))  # Prompt user for longitude

# Define the spatial filter for Edinburgh location based on user input
edin_location = {
    "filterType": "mbr",    
    "lowerLeft": {"latitude": lat - 0.05, "longitude": lng - 0.05},
    "upperRight": {"latitude": lat + 0.05, "longitude": lng + 0.05}
}


dataset_dict = search_landsat_scenes(m2m_api_key, dataset_name, date_range,spatial_filter=edin_location)  # Call the function to search for scenes, returns a dictionary  

list_of_dates = []

for x in range(0, len(dataset_dict['results'])):
    list_of_dates.append(dataset_dict['results'][x]['temporalCoverage']['endDate'])

print(list_of_dates[0] + " is the most recent date LandSAT data was captured in Edinburgh.\n")
print(dt.datetime.strptime(list_of_dates[0], '%Y-%m-%d %H:%M:%S') + dt.timedelta(days=16), "is the closest future date that Landsat hovers over a location!\n")

def backup_landsat_function(lat, lng, m2m_api_key, dataset_name, date_range):
    # Define the spatial filter for Edinburgh location based on user input
    edin_location = {
        "filterType": "mbr",    
        "lowerLeft": {"latitude": lat - 0.05, "longitude": lng - 0.05},
        "upperRight": {"latitude": lat + 0.05, "longitude": lng + 0.05}
    }

    # Call the function to search for scenes, returns a dictionary  
    dataset_dict = search_landsat_scenes(m2m_api_key, dataset_name, date_range, spatial_filter=edin_location)

    list_of_dates = []
    
    # Extract dates from the dataset_dict
    for x in range(0, len(dataset_dict['results'])):
        list_of_dates.append(dataset_dict['results'][x]['temporalCoverage']['endDate'])

    # Print the most recent and the closest future date Landsat hovers over the location
    #print(list_of_dates[0] + " is the most recent date LandSAT data was captured in Edinburgh.\n")
    future_date = dt.datetime.strptime(list_of_dates[0], '%Y-%m-%d %H:%M:%S') + dt.timedelta(days=16)
    #print(future_date)
    return future_date

# Example call to the function
lat = float(input("Enter latitude: "))  
lng = float(input("Enter longitude: "))  
future_date = backup_landsat_function(lat, lng, m2m_api_key, dataset_name, date_range)

print(f"DATE FUTURE :{future_date}")


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


# Example usage  
filename = "output.txt"  
directory = "server/"
write_pretty_print_to_file(dataset_dict, filename, directory)  



def get_entity_ids(long, lat, start_date, end_date) -> str:    
    api_key = get_m2m_api_key(m2m_username, m2m_app_token)  
    dataset_name = get_dataset_alias(api_key, long, lat, start_date, end_date)
    # print(f"Dataset Name: {dataset_name}")
    
    date_range= {
        "start": start_date if start_date else "1970-01-01",
        "end": end_date if end_date else "9999-12-31"
    }
    box_location = {
        "filterType": "mbr",
        "lowerLeft": {"latitude": lat - 0.01, "longitude": long - 0.01},
        "upperRight": {"latitude": lat + 0.01, "longitude": long + 0.01}
    }
    
    resp_dict = search_landsat_scenes(api_key, dataset_name, date_range, box_location)
    numOfResp = resp_dict['totalHits']
    entity_id_list = []
    
    for i in range(0,numOfResp):
        entity_id_list.append(resp_dict['results'][i]['entityId'])
    # print(entity_id_list)
    return ','.join(entity_id_list)
    
# ==== GET ENTITY IDS TEST ====
long = -3.20483
lat = 55.93607
start_date = "2024-09-01"  # date format -> "YYYY-MM-DD"
end_date = "2024-09-16"

# calling get_entity_ids() function
# get_entity_ids(long, lat, start_date, end_date)


# DOWNLOADING SCENES 
# endpoint --> download-options
# - Identify product IDs that are "available" for each scene
# - endpoints --> download-request & download-retrieve
# - - Request download URLs for scene ID - product ID pairs
# - - - URLs returned as "available" are available for download
# - - - For URLs returned as "preparing," wait and check download-retrieve to see if they are "available"


# setting up GCS key
# import datetime import timedelta
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gleaming-lead-437206-i7-827426fd2864.json"


# GCS = Google Cloud Storage
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name, retries=3):  
    """Uploads a file to the bucket."""  
    storage_client = storage.Client()  
    bucket = storage_client.bucket(bucket_name)  
    blob = bucket.blob(destination_blob_name)  

    # blob.upload_from_filename(source_file_name)  
    
    for attempt in range(retries):  
        try:  
            blob.upload_from_filename(source_file_name, timeout=60)  # Set timeout to 60 seconds 
            print(f"GCS SUCCESS ==> File {source_file_name} uploaded to {destination_blob_name}.")  
            return  # Exit the function if upload is successful  
        except Exception as e:  
            print(f"Attempt {attempt + 1} failed: {e}")  
            time.sleep(2)  # Wait 2 secsbefore retrying  

    raise Exception("GCS FAILED to upload after multiple attempts.") 


def store_urls_in_gcs(bucket_name, file_name, urls):  
    """Stores the list of URLs in a text file in Google Cloud Storage."""  
    # Initialize a GCS client  
    storage_client = storage.Client()  
    bucket = storage_client.bucket(bucket_name)  

    # Create a new blob (file) in the bucket  
    blob = bucket.blob(file_name)  
    # blob.make_public()

    # Convert the list of URLs to a JSON formatted string  
    json_data = json.dumps(urls)  
    print(f"URL JSON: {json_data}")

    # Write the JSON data to the blob  
    blob.upload_from_string(json_data, content_type='application/json')  
    print(f"Stored {len(urls)} URLs in {file_name} in bucket {bucket_name} as JSON.") 


def generate_signed_url(bucket_name, object_name, expiration= dt.timedelta(hours=1)):  
    """Generates a signed URL for accessing a GCS object."""  
    storage_client = storage.Client()  
    bucket = storage_client.bucket(bucket_name)  
    blob = bucket.blob(object_name)  

    signed_url = blob.generate_signed_url(expiration=expiration)  
    return signed_url  


print("\n========")
print("Testing gpto1's 'download' code:")
print("========\n")


def retrieve_dwn_urls(api_key, entityIds, bucket_name, datasetName="landsat_ot_c2_l2", dwdApp="M2M", filename="download_urls.json"):
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
        
    
    # sotre URLs in Google Cloud Storage
    if download_url_list:  
        store_urls_in_gcs(bucket_name, filename, download_url_list)  

    return download_url_list  
    
    
        
# Setting Bucket to be Public
bucket_name = "my_baldi"
# set_bucket_public_iam(bucket_name)
# https://storage.googleapis.com/my_baldi/download_urls.json

        
# ========== DOWNLOADING LANDSAT EDIN SCENES ============
# input params for downloading
entity_ids = "LC92050212024249LGN00,LC92040212024258LGN00,LC82050212024257LGN00,LC82040212024250LGN00"
dwd_urls_list = retrieve_dwn_urls(m2m_api_key, entity_ids, bucket_name, dataset_name )
print("--> Available download urls: ")
print(dwd_urls_list)

# print(f"SIGNED URL: {generate_signed_url(bucket_name,"download_urls.json")}")
        
# from urllib.parse import urlparse

def download_and_extract_zip(url, download_dir, bucket_name):
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
            # Save the zip file # !!! UNCOMMENT IF YOU WANT TO DOWNLOAD THE FILES | took around 20 mins to download 4 .tar files
            # with open(file_path, 'wb') as file:
                # for chunk in response.iter_content(chunk_size=8192):
                    # file.write(chunk)
            print(f"Downloaded: {filename}")
        
        # Extract the contents of the tar file  
        folder_name = os.path.splitext(filename)[0]
        print(f"****FOLDER NAME: {folder_name}")
        extract_dir = os.path.join(download_dir, folder_name)  
        os.makedirs(extract_dir, exist_ok=True)  

        # Extract the contents of the tar file into the new directory  
        print(f"Extracting: {filename} into {extract_dir}")  
        with tarfile.open(file_path, 'r:*') as tar_ref:  
            tar_ref.extractall(extract_dir)  
        print(f"Extracted: {filename} into {extract_dir}")  
        
        
        
        # Upload extracted files to GCS  
        for root, dirs, files in os.walk(extract_dir):  
            for file in files:  
                local_file_path = os.path.join(root, file)  
                gcs_blob_name = os.path.relpath(local_file_path, extract_dir)  
                upload_to_gcs(bucket_name, local_file_path, gcs_blob_name)  




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
download_directory = "download/path"
bucket_name = "my_baldi"

print("Processing download URLs:")
# for url in dwd_urls_list:
url = dwd_urls_list[0]  # GCS test
print(f"Processing: {url}")
# download_and_extract_zip(url, download_directory, bucket_name)
print("\n*** DONE UNZIPPING LANDSAT FILES ***\n")

# COLOURING THE LANDSAT IMAGE

# File paths for the TIF images  

# print(f"RASTERIO VER: {rasterio.__version__}")

# band_2_path = "path/to/band2.TIF"  # Replace with the actual path to Band 2  
# band_3_path = "path/to/band3.TIF"  # Replace with the actual path to Band 3  
# band_4_path = "path/to/band4.TIF"  # Replace with the actual path to Band 4  

# # Read the TIF files  
# with rasterio.open(band_2_path) as band2:  
#     band2_data = band2.read(1)  # Read the first band (Band 2)  
#     profile = band2.profile

# with rasterio.open(band_3_path) as band3:  
#     band3_data = band3.read(1)  # Read the first band (Band 3)  

# with rasterio.open(band_4_path) as band4:  
#     band4_data = band4.read(1)  # Read the first band (Band 4)  

# # Function to perform contrast stretching  
# def contrast_stretch(band_data):  
#     # Get the minimum and maximum values  
#     min_val = np.min(band_data)  
#     max_val = np.max(band_data)  
    
#     # Perform contrast stretching  
#     stretched = (band_data - min_val) / (max_val - min_val) * 255  
#     return stretched.astype(np.uint8)  

# # Apply contrast stretching to each band  
# band2_stretched = contrast_stretch(band2_data)  
# band3_stretched = contrast_stretch(band3_data)  
# band4_stretched = contrast_stretch(band4_data)  

# # Stack the bands into a 3D array (RGB)  
# rgb_image = np.stack((band4_stretched, band3_stretched, band2_stretched), axis=0)  # Band 4 (Red), Band 3 (Green), Band 2 (Blue)  

# Optionally, save the color image  
output_path = 'server/rgb_stack_L08_20240914_contrast_stretched.tif'  # Replace with desired output path 

# # Update the profile for a 3-band GeoTIFF
# profile.update(
#     dtype=rasterio.uint8,
#     count=3,
#     compress='lzw'
# )

# # Save the color image as a GeoTIFF
# # with rasterio.open(output_path, 'w', **profile) as dst:
#     # dst.write(rgb_image)

# # WRS-2 Path and Row Calculation

# def latlong_to_wrs2(latitude, longitude):
#     EARTH_RADIUS = 6378.137  # km
#     WRS_PATH_WIDTH = 185  # km, approximate width of a WRS-2 path
#     TOTAL_PATHS = 233  # Total number of paths globally
#     TOTAL_ROWS = 248  # Total number of rows globally

#     # Convert latitude and longitude to radians
#     lat_radians = math.radians(latitude)
#     lon_radians = math.radians(longitude)

#     # Calculate WRS-2 Path (simplified estimate, will need fine-tuning)
#     path = int((longitude + 180) / (360 / TOTAL_PATHS)) + 1

#     # Calculate WRS-2 Row (simplified estimate based on latitude)
#     row = int((latitude + 90) / (180 / TOTAL_ROWS)) + 1

#     return path, row

# #Plotting the Pixel on the Map

# def plot_pixel_on_map_with_thumbnail(latitude, longitude, image_url):
#     response = requests.get(image_url)  # Fetch the image from thumbnail URL
#     if response.status_code == 200:
#         img = Image.open(BytesIO(response.content))  # Open the image in PIL

#         # Display the fetched Landsat image as the background
#         plt.imshow(np.asarray(img), extent=[-180, 180, -90, 90])  # World map extent for the image

#         # Plot the pixel (latitude/longitude) on the map
#         plt.scatter(longitude, latitude, c='r', marker='x')  # Drop the red X at the target location
#         plt.title("Target Pixel on Map with Landsat Thumbnail")
#         plt.xlabel("Longitude")
#         plt.ylabel("Latitude")

#         plt.show()
#     else:
#         print(f"Failed to fetch image, status code: {response.status_code}")

# latitude = 55.93607  # Set your latitude
# longitude = -3.20483  # Set your longitude
# thumbnail_url = 'https://landsatlook.usgs.gov/gen-browse?size=thumb&type=refl&product_id=LC08_L1TP_014001_20240903_20240906_02_T1'  # Replace with your own image URL
# plot_pixel_on_map_with_thumbnail(latitude, longitude, thumbnail_url)

