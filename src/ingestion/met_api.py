import requests

url = 'https://collectionapi.metmuseum.org/public/collection/v1/search'

print("Please enter a search term for the MET collection:")
keyword = input()

search = f'https://collectionapi.metmuseum.org/public/collection/v1/search?q={keyword}'
#Using the MET API keyword search to look for objects that are tagged with a specific keyword

response = requests.get(search)

print(response.json())
#This response will print all object IDs that are tagged with the keyword, these must be decoded to get the object information

object_ID = response.json()['objectIDs'][0]
#requests.get(search) returns an array of object IDs, this variable contains the value of the position 0 of the array
#which is the first element of the array or the first object returned
print(object_ID)


object_decode = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_ID}'
#fetches information from the first object using the object ID from the search results

object_response = requests.get(object_decode)

#Selected the most relevant attributes of the object to make a neat summary of the object information
print("Title:", object_response.json()['title'])
##this causes an error when the title field is empty, need to add a try/except block to handle nulls
print("Object Name:", object_response.json()['objectName'])
print("Department:", object_response.json()['department'])
print("Culture:", object_response.json()['culture'])
print("Period:", object_response.json()['period'])
print("Primary Image:", object_response.json()['primaryImage'])

#Next steps: Decide if it makes sense to iterate through the array to fetch all object information for all object IDs returned from the search
#It would be ideal to be able to display the images in the Primary Image field and have the wiki links readily available for the user after search
#Identify which object attributes are most relevant to the model in progress to make the most meaningful connections between objects
