# Data Model

## Purpose

Using the JSON returned by the Metropolitan Museum of Art dataset API, determine the structure and relationships between entities in the data to create a working model which can be used for the ultimate goal of this project.

## Project Purpose

To produce cultural artifacts all related to an anthropological/cultural concept input by the user. For example, "child rearing", "eyeliner", "democracy", "femininity" - should produce an array of cultural artifacts exploring these concepts across history in different countries and contexts, through art and archeology.

The API returns records with nested columns/attributes, for example, artist includes: artistGender, artistWikidata_URL, artistRole, etc.

## Key Point to Eliminate Redundancy

Repeated entities will be sorted into **relational tables**, to avoid duplication of information

ex: if multiple pieces are painted by Monet, we don't need to duplicate Monet's artist fields for each piece, when instead we can create a relational model where artist to artwork can have a one-to-many or many-to-many relationship, as one artist can make many pieces, and it's possible for more than one artist to collaborate on one or more pieces

## Step 1: **Analyze Relationships & Entities**

(I used an LLM to neatly format the output from the JSON response when fetching a single object from the API, then checked that against the JSON output and expected output from the Met's documentation to ensure accuracy)

### Artwork

- **Identification**
  - objectID
  - accessionNumber
  - accessionYear
  - title
  - objectName
  - department

- **Artist**
  - **constituents[]**
    - constituentID
    - role
    - name
    - gender
    - constituentULAN_URL
    - constituentWikidata_URL
  - artistRole
  - artistPrefix
  - artistDisplayName
  - artistDisplayBio
  - artistSuffix
  - artistAlphaSort
  - artistNationality
  - artistBeginDate
  - artistEndDate
  - artistGender
  - artistWikidata_URL
  - artistULAN_URL

- **Artwork Details**
  - culture
  - period
  - dynasty
  - reign
  - portfolio
  - objectDate
  - objectBeginDate
  - objectEndDate
  - medium
  - classification
  - dimensions
  - **measurements[]**
    - elementName
    - elementDescription
    - **elementMeasurements**
      - Height
      - Width
      - Depth

- **Geographic / Cultural Context**
  - geographyType
  - city
  - state
  - county
  - country
  - region
  - subregion
  - locale
  - locus
  - excavation
  - river

- **Classification & Metadata**
  - **tags[]**
    - term
    - AAT_URL
    - Wikidata_URL
  - isHighlight
  - isPublicDomain
  - isTimelineWork
  - metadataDate
  - GalleryNumber
  - repository

- **Images**
  - primaryImage
  - primaryImageSmall
  - additionalImages[]

- **External References**
  - objectURL
  - objectWikidata_URL
  - linkResource
  - rightsAndReproduction

## Step 2: What fields are most relevant to what we are trying to accomplish with the data?

### *name*

- Name of the "constituent" involved in the piece, usually the artist but the field is generalized to allow flexibility

### *constituentWikidata_URL*

- Provides detailed information from wikidata about the artist
- Will be useful in establishing who created the artwork, where and when they lived, what themes they explored in their artwork, and what influences in their life may change the context of their artwork

### *title*

- Title of the piece

### *primaryImage*

- Displays the image of the artwork

### *objectURL*

- Provides a more detailed page from the Metropolitan Museum of Art about the artwork

### *tags*

- Object that contains all tag information, including links about the tag subjects, can contain multiple terms

### *term*

- String associated with the tag (whatever word/s was/were used as the tag, human-readable)
- **Potentially the most important field**, works for keyword searches by users in the eventual finished product

### *AAT_URL*

- Provides more detailed information about a tag

### *culture*

- Tags which culture the artwork/artist belonged to, if any specific cultural tag is available

## Step 3:  What tables need to be created for this data model?

## Artwork Table

________________________

- objectID **Perhaps obscure from the user but keep this ID as a primary key if useful**
- objectName
- title
- primaryImage
- primaryImageSmall
- additionalImages
- constituents **may join onto Artists table**
- constituentID **may join onto Artists table**
- culture
- period
- dynasty
- reign
- objectDate
- objectBeginDate
- objectEndDate
- medium

## Geographic Information Table

_______________

- geographyType
- city
- state
- county
- country
- region
- subregion
- locale
- locus
- excavation
- river

## Artist Table

________________________

- constituents
- constituentID **Perhaps obscure from the user but keep this ID as a primary key if useful**
- name
- constituentULAN_URL **Could help make the finished product more accessible to a wider range of users**
- artistDisplayName
- artistDisplayBio **Provides essential context about the artist's/constituent's life**
- artistWikidata_URL
- artistNationality
- artistBeginDate
- artistEndDate
- artistGender

## Given how important tags are to the goal of this project, and the nested nature of how they're represented, could it make sense to make tags into their own table?

## Keyword Table
**Making keyword into its own table may allow us to link other datasets to this same tag "bank" and relate datasets more easily**
________________________

- tags[] **turn into tag_ID, assign a primary key to each keyword that appears as a tag**
- term >> **Maybe rename as "keyword" or display to user as "Tag", because this is the string that humans will interpret as the tag on the piece, even though tag_ID will be the machine's primary key that it can associate with each concept**
- AAT_URL
- Wikidata_URL


## Artwork to Tag Bridge Table
**One artwork can contain many tags, so we cannot make tag_ID its own column in the artwork Table, it requires a bridge table to give that flexibility in cardinality**
________________________
- object_ID
- tag_ID

## Step 4: Explore Cardinality and Define Relationships 

I will continue this in an ERD (Entity Relationship Diagram) so I can see visually what I'm working with more easily. I need to figure out which application I want to use to build the diagram. It will be added here later, as either an addition to this document or a standalone document. 


Addendum:

## Step 0: Where I began inspecting the data 

Using the python script in met_api.py, I modified the url to query a specific object ID (436524). I checked out the output in VS Code, input it into an LLM to organize it nicely (carefully checking outputs and only using it for formatting), and compared it against the information on the Met's API user guide to make sure all columns were present. Below is the output which I produced or sifted through in this process, before starting to map out my thinking for the data model. 


src/ingestion/met_api.py
{'objectID': 436524, 'isHighlight': False, 'accessionNumber': '49.41', 'accessionYear': '1949', 'isPublicDomain': True, 'primaryImage': 'https://images.metmuseum.org/CRDImages/ep/original/DP-41223-001.jpg', 'primaryImageSmall': 'https://images.metmuseum.org/CRDImages/ep/web-large/DP-41223-001.jpg', 'additionalImages': [], 'constituents': [{'constituentID': 161947, 'role': 'Artist', 'name': 'Vincent van Gogh', 'constituentULAN_URL': 'http://vocab.getty.edu/page/ulan/500115588', 'constituentWikidata_URL': 'https://www.wikidata.org/wiki/Q5582', 'gender': ''}], 'department': 'European Paintings', 'objectName': 'Painting', 'title': 'Sunflowers', 'culture': '', 'period': '', 'dynasty': '', 'reign': '', 'portfolio': '', 'artistRole': 'Artist', 'artistPrefix': '', 'artistDisplayName': 'Vincent van Gogh', 'artistDisplayBio': 'Dutch, Zundert 1853–1890 Auvers-sur-Oise', 'artistSuffix': '', 'artistAlphaSort': 'Gogh, Vincent van', 'artistNationality': 'Dutch', 'artistBeginDate': '1853', 'artistEndDate': '1890', 'artistGender': '', 'artistWikidata_URL': 'https://www.wikidata.org/wiki/Q5582', 'artistULAN_URL': 'http://vocab.getty.edu/page/ulan/500115588', 'objectDate': '1887', 'objectBeginDate': 1887, 'objectEndDate': 1887, 'medium': 'Oil on canvas', 'dimensions': '17 x 24 in. (43.2 x 61 cm)', 'measurements': [{'elementName': 'Overall', 'elementDescription': None, 'elementMeasurements': {'Height': 43.2, 'Width': 61}}, {'elementName': 'Framed', 'elementDescription': None, 'elementMeasurements': {'Depth': 6.35, 'Height': 66.6751, 'Width': 85.0902}}], 'creditLine': 'Rogers Fund, 1949', 'geographyType': '', 'city': '', 'state': '', 'county': '', 'country': '', 'region': '', 'subregion': '', 'locale': '', 'locus': '', 'excavation': '', 'river': '', 'classification': 'Paintings', 'rightsAndReproduction': '', 'linkResource': '', 'metadataDate': '2026-02-04T04:58:06.107Z', 'repository': 'Metropolitan Museum of Art, New York, NY', 'objectURL': 'https://www.metmuseum.org/art/collection/search/436524', 'tags': [{'term': 'Sunflowers', 'AAT_URL': 'http://vocab.getty.edu/page/aat/300404749', 'Wikidata_URL': 'https://www.wikidata.org/wiki/Q171497'}, {'term': 'Still Life', 'AAT_URL': 'http://vocab.getty.edu/page/aat/300015638', 'Wikidata_URL': 'https://www.wikidata.org/wiki/Q170571'}], 'objectWikidata_URL': 'https://www.wikidata.org/wiki/Q9213165', 'isTimelineWork': False, 'GalleryNumber': '825'}

re-ran the script with only one object ID to inspect what columns the JSON delivers, object ID: 436524

Artwork
│
├── Identification
│   ├── objectID
│   ├── accessionNumber
│   ├── accessionYear
│   ├── title
│   ├── objectName
│   └── department
│
├── Artist
│   ├── constituents[]
│   │   ├── constituentID
│   │   ├── role
│   │   ├── name
│   │   ├── gender
│   │   ├── constituentULAN_URL
│   │   └── constituentWikidata_URL
│   ├── artistRole
│   ├── artistPrefix
│   ├── artistDisplayName
│   ├── artistDisplayBio
│   ├── artistSuffix
│   ├── artistAlphaSort
│   ├── artistNationality
│   ├── artistBeginDate
│   ├── artistEndDate
│   ├── artistGender
│   ├── artistWikidata_URL
│   └── artistULAN_URL
│
├── Artwork Details
│   ├── culture
│   ├── period
│   ├── dynasty
│   ├── reign
│   ├── portfolio
│   ├── objectDate
│   ├── objectBeginDate
│   ├── objectEndDate
│   ├── medium
│   ├── classification
│   ├── dimensions
│   └── measurements[]
│       ├── elementName
│       ├── elementDescription
│       └── elementMeasurements
│           ├── Height
│           ├── Width
│           └── Depth
│
├── Geographic / Cultural Context
│   ├── geographyType
│   ├── city
│   ├── state
│   ├── county
│   ├── country
│   ├── region
│   ├── subregion
│   ├── locale
│   ├── locus
│   ├── excavation
│   └── river
│
├── Classification & Metadata
│   ├── tags[]
│   │   ├── term
│   │   ├── AAT_URL
│   │   └── Wikidata_URL
│   ├── isHighlight
│   ├── isPublicDomain
│   ├── isTimelineWork
│   ├── metadataDate
│   ├── GalleryNumber
│   └── repository
│
├── Images
│   ├── primaryImage
│   ├── primaryImageSmall
│   └── additionalImages[]
│
└── External References
    ├── objectURL
    ├── objectWikidata_URL
    ├── linkResource
    └── rightsAndReproduction

    
Example from Met API website for comparison:
{
    "objectID": 45734,
    "isHighlight": false,
    "accessionNumber": "36.100.45",
    "accessionYear": "1936",
    "isPublicDomain": true,
    "primaryImage": "https://images.metmuseum.org/CRDImages/as/original/DP251139.jpg",
    "primaryImageSmall": "https://images.metmuseum.org/CRDImages/as/web-large/DP251139.jpg",
    "additionalImages": [
        "https://images.metmuseum.org/CRDImages/as/original/DP251138.jpg",
        "https://images.metmuseum.org/CRDImages/as/original/DP251120.jpg"
    ],
    "constituents": [
        {
            "constituentID": 11986,
            "role": "Artist",
            "name": "Kiyohara Yukinobu",
            "constituentULAN_URL": "http://vocab.getty.edu/page/ulan/500034433",
            "constituentWikidata_URL": "https://www.wikidata.org/wiki/Q11560527",
            "gender": "Female"
        }
    ],
    "department": "Asian Art",
    "objectName": "Hanging scroll",
    "title": "Quail and Millet",
    "culture": "Japan",
    "period": "Edo period (1615–1868)",
    "dynasty": "",
    "reign": "",
    "portfolio": "",
    "artistRole": "Artist",
    "artistPrefix": "",
    "artistDisplayName": "Kiyohara Yukinobu",
    "artistDisplayBio": "Japanese, 1643–1682",
    "artistSuffix": "",
    "artistAlphaSort": "Kiyohara Yukinobu",
    "artistNationality": "Japanese",
    "artistBeginDate": "1643",
    "artistEndDate": "1682",
    "artistGender": "Female",
    "artistWikidata_URL": "https://www.wikidata.org/wiki/Q11560527",
    "artistULAN_URL": "http://vocab.getty.edu/page/ulan/500034433",
    "objectDate": "late 17th century",
    "objectBeginDate": 1667,
    "objectEndDate": 1682,
    "medium": "Hanging scroll; ink and color on silk",
    "dimensions": "46 5/8 x 18 3/4 in. (118.4 x 47.6 cm)",
    "measurements": [
        {
            "elementName": "Overall",
            "elementDescription": null,
            "elementMeasurements": {
                "Height": 118.4,
                "Width": 47.6
            }
        }
    ],
    "creditLine": "The Howard Mansfield Collection, Purchase, Rogers Fund, 1936",
    "geographyType": "",
    "city": "",
    "state": "",
    "county": "",
    "country": "",
    "region": "",
    "subregion": "",
    "locale": "",
    "locus": "",
    "excavation": "",
    "river": "",
    "classification": "Paintings",
    "rightsAndReproduction": "",
    "linkResource": "",
    "metadataDate": "2020-09-14T12:26:37.48Z",
    "repository": "Metropolitan Museum of Art, New York, NY",
    "objectURL": "https://www.metmuseum.org/art/collection/search/45734",
    "tags": [
        {
            "term": "Birds",
            "AAT_URL": "http://vocab.getty.edu/page/aat/300266506",
            "Wikidata_URL": "https://www.wikidata.org/wiki/Q5113"
        }
    ],
    "objectWikidata_URL": "https://www.wikidata.org/wiki/Q29910832",
    "isTimelineWork": false,
    "GalleryNumber": ""
}

