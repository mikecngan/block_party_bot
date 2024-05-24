import pandas as pd
from SchoolBoardPolygons import get_district_2, get_district_4

district = 2
send = False

if district == 2:
    District2 = get_district_2()
elif district == 4:
    District2 = get_district_4()

# URL of the JSON data
url = "https://data.cityofchicago.org/resource/9zhy-9n5f.json"

# Read the JSON data into a DataFrame
block_parties = pd.read_json(url)

import geopandas as gpd
from shapely.geometry import Point

# Convert 'location' column to Point objects
block_parties['geometry'] = block_parties['location'].apply(lambda loc: Point(float(loc['longitude']), float(loc['latitude'])) if pd.notnull(loc) else None)
# Convert DataFrame to GeoDataFrame
block_parties_geo = gpd.GeoDataFrame(block_parties, geometry='geometry')

# Set the CRS of block_parties_geo to match District2
block_parties_geo.crs = District2.crs

# Filter out rows with None in 'geometry' column
block_parties_geo = block_parties_geo[block_parties_geo['geometry'].notnull()]

# Check if each point is within any polygon in District2
block_parties_geo['in_district'] = block_parties_geo.apply(lambda row: District2.contains(row['geometry']).any(), axis=1)

# Print every column in the GeoDataFrame of the block parties in district sorted by applicationstartdate from the earliest
print(block_parties_geo[block_parties_geo['in_district']].sort_values('applicationstartdate'))

district2_block_parties = block_parties_geo[block_parties_geo['in_district']].sort_values('applicationstartdate')

# export it to csv
district2_block_parties.to_csv('block_parties_in_district.csv', index=False)

import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token="")
logger = logging.getLogger(__name__)

# The name of the file you're going to upload
file_name = "./block_parties_in_district.csv"
# ID of channel that you want to upload file to
channel_id = "C06SR2UK7HT"

if send:
    try:
        # Call the files.upload method using the WebClient
        # Uploading files requires the `files:write` scope
        result = client.files_upload_v2(
            channels=channel_id,
            initial_comment="Upcoming block parties in District " + str(district),
            file=file_name,
        )
        # Log the result
        logger.info(result)

    except SlackApiError as e:
        logger.error("Error uploading file: {}".format(e))