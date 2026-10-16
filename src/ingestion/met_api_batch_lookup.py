import requests
import pandas as pd

url = 'https://collectionapi.metmuseum.org/public/collection/v1.1/search'
#Changed 10/2/2026 to v1.1/search because Solr backed search was retired, v 1.1 replaces this with an Elastic-backed search, paginated via offset and limit

print("Please enter a search term for the MET collection:")
keyword = input()

search = f'https://collectionapi.metmuseum.org/public/collection/v1.1/search?q={keyword}'
#Using the MET API keyword search to look for objects that are tagged with a specific keyword


#The search endpoint can also serve the API's HTML 403 bot-protection page when
#requests come too fast, so check the status and back off and retry before decoding
returned_object = None
for attempt in range(3):
    response = requests.get(search, timeout=20)
    if response.status_code == 200 and 'json' in response.headers.get('Content-Type', ''):
        returned_object = response.json()
        break
    print(f"Search failed with status {response.status_code}; backing off {60 * (attempt + 1)}s.")
    time.sleep(60 * (attempt + 1))

if returned_object is None:
    raise SystemExit("The MET API is currently blocking requests from this IP; wait a few minutes and rerun.")

print(returned_object)
#This response will print all object IDs that are tagged with the keyword, these must be decoded to get the object information

##for returned_object in response.json():
##df.select(explode(response.json).alias("objectIDs"))
##Abandoned attempt ^^
##df = pd.DataFrame
##df = pd.read_json(response)
##print(df)
##ingest data by exploding each element of the nested json and loading them into a dataframe
##https://learn.microsoft.com/en-us/azure/databricks/semi-structured/complex-types


#################################################################
##objectIDs = returned_object['objectIDs']
#requests.get(search) returns an array of all object IDs tagged with the keyword,
#each ID must be decoded against the objects endpoint to get that object's full record

##object_records = []
##for object_ID in objectIDs:
##    object_decode = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_ID}'
##    #fetches the full JSON record for each object using the object ID from the search results
##    object_response = requests.get(object_decode)
##    record = object_response.json()
##    if object_response.status_code == 200 and 'objectID' in record:
##        object_records.append(record)
##    else:
##        print(f'object {object_ID} not found, skipping')

##full_df = pd.DataFrame(object_records)
#one row per object with every field from the API, nested arrays (constituents, measurements, tags, additionalImages) are preserved as lists of dicts
##print(full_df)
#################################################################

objectIDs = returned_object['objectIDs']

object_records = []

for object_ID in objectIDs:
    object_decode = (
        f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_ID}'
    )

    object_response = requests.get(object_decode, timeout=20)

    # Check whether the API returned a successful response.
    if object_response.status_code != 200:
        print(
            f"Object {object_ID} failed with status "
            f"{object_response.status_code}; skipping."
        )
        continue

    # Only attempt JSON decoding after the HTTP status check.
    try:
        record = object_response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Object {object_ID} returned invalid JSON; skipping.")
        continue

    # Check that the response contains an actual object record.
    if 'objectID' in record:
        object_records.append(record)
    else:
        print(f"Object {object_ID} did not contain an object record; skipping.")

print(f"Successfully retrieved {len(object_records)} objects.")

print(object_records)

full_df = pd.DataFrame(object_records)
display(full_df)