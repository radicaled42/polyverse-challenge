# Megaverse Challenge

## Create your own megaverse*

*Megaverse is like Metaverse but cooler because you create it!

Welcome to our Crossmint coding challenge, in which you will help us mint a new megaverse into existence!

Megaverses are 2D spaces comprised of combinations of different astral objects: 🪐POLYanets with 🌙SOLoons around them and ☄comETHs floating around.

Your job as the master of the megaverse will be to create one with some given parameters and shapes. You will use a megaverse creator API to help you with such legendary quest.

The challenge is composed of 2 phases. In the first one you will learn how to interact with the API and create some 🪐POLYanets and validate them. In the second one you will create a bigger megaverse with some peculiar shape.

### Important things to know

By the end of the challenge, you will be asked to submit the code you used to solve it. This code will be manually reviewed and evaluated by our engineers, so here are the criteria we will be mainly using for:
- The code is clean and easy to understand
- You model the problem properly, including classes / interfaces, extension when applies, etc.
- Errors should be considered, the program should be resilient
- You avoid duplication and encourage extension for similar use cases
- Your logic is properly abstracted in classes (or equivalent), functions, variables, etc.
- Your solution is automated (i.e. you don't manually call the API to create the 100+ entities required for Phase 2)
- We expect the problem to be a little over-engineered, take a little time to show off what you know. But this should be done to a reasonable amount, don't go overboard.


## Phase 2: Crossmint logo. With 🌙SOLoons and ☄comETHs!

In this second phase, you will have to build another megaverse… including the shape of our logo!

This new map has some other entities as well: 🌙SOLoons and ☄comETHs.
🌙SOLoons can only be adjacent to a 🪐POLYanet, and they can have a variety of colors.
☄comETHs can go alone in the universe, but they have a direction they’re facing.

You can see their specifications and APIs on the same Docs.

**IMPORTANT: Building the map manually is NOT a solution we are looking for here. There are multiple ways to solve this problem, but maybe the /api/map/[candidateId]/goal endpoint might help.**

The final result will look like this:

```bash
------------------------------
-------C----------------------
--PP---------C---------PP-----
--P-PP--------------SPP-P--C--
---P-SPPS-------C--PP--P-----C
---P--S-PP--C----PPS---P------
----P-----P-----P-----P-------
----P-----P----SP-----PS------
----SP----SP---P-----P--------
-----PS----PS--P-----P-----C--
--C---PP----P-P---SPP---------
-------SPP--P-P--PP-----------
----------PP-P-PP--------C--C-
----C-------PPP---------------
---------SPP-P-PPS------------
-C------PP--P-P--PPS------C---
---C--PPS---P-P----PPS--------
-----P-----P--SP-----P--C-----
-----PS----P---P-----PS-------
----P-----PS----P-----P-------
C---P-----P-----P-----P-------
---P----PPS-----SPPS---P------
---P-SPPS-----C----PP--PS--C--
--P-PP---------------PP-P-----
--PP--------C----------PP-----
------------------------------
---C-----------C----------C---
-----C------------------------
----------C---------C---------
------------------------------
```

## Version Information

**V1**
- Simple one file with all the class methods and support functions.

**V2**
- Separated the main function from the Polyverse class.

**V3**
- Added Flask to handle API requests.

**V4**
- Dockerized the solution for use in any environment.
- 
## Methods

**Private Methods**
- __reset_map: 
  - reset the local map in **self.map**, doesn't need any input
- __api_call
  - Generates the api call to the server. Needs **method**, **url**, **headers**, **payload**
    - method: GET/POST/DELETE
    - url: API url
    - headers: this is a dictionary and can be empty
    - payload: this is a dictionary and can be empty
- __write_element_polyverse
  - Writes an element into the API map, it requires **element_data**, **binary_api**
    - element_data: All the arguments to create an element (row, column, candidateID, direction/color)
    - binary_api: the number of the element to create
- __clean_element_poliverse
  - Deletes an element into the API map, it requires **element_data**, **binary_api**
    - element_data: All the arguments to create an element (row, column, candidateID)
    - binary_api: the number of the element to create
- __verify_position
  - Check if its possible to write an element on the designated position. It requires **element_data**
  - element_data: All the arguments to create an element (row, column, candidateID, direction/color)

**Public Methods**
- get_polyverse_map
  - It makes an API call to retrieve the map of the candidate.
- show_local_polyverse
  - It makes a representation of the map in 2D with single characters
- clean_polyverse
  - Remove all the elements from the API map
- write_local_map
  - Writes the element_data information in the local map. It requires **element_data**
    - element_data: All the arguments to create an element (row, column, candidateID, type, direction/color)
- delete_local_map
  - Deletes the element_data information in the local map. It requires **element_data**
  - element_data: All the arguments to delete an element (row, column, candidateID, type)
- merge_map
  - Merges local map into external map (Local --> External)
- local_map_payload
  - Given the row, column and element_data, this method will create the payload to write on the local map.
  - payload: {row, column, payload: {type, direction/color}}
- duplicate_polyverse
  - It duplicates a map. It can take an external url or by default it will use the candidate goal map. The url is not a require argument

## Flask Routes

**/show**
- Returns the actual candidate map
  - method: GET

**/clean**
- Remove all the elements from the API map
  - method: POST

**/write**
- Writes an element into the API map.
  - method: POST
  - arguments: start, end (optional), type, color/destination.
    - start: the position to delete or the point to start a line.
    - end: (optional) it the position where the lines end.
    - type: its the type of element to create
    - color/destination (optional) 

Write single element
```json
{
    "start": "(1,1)",
    "payload": {
        "type": 2,
        "direction": "up"
    }
}
```

Write multiple elements
```json
{
    "start": "(1,1)",
    "end": "(5,1)",
    "payload": {
        "type": 2,
        "direction": "up"
    }
}
```

**/delete**
- Deletes an element into the API map.
  - method: DELETE
  - arguments: start, end (optional), type.
    - start: the position to delete or the point to start a line.
    - end: (optional) it the position where the lines end.
    - type: its the type of element to delete

Delete single element
```json
{
    "start": "(1,1)",
    "payload": {
        "type": 2
    }
}
```

Delete multiple elements
```json
{
    "start": "(1,1)",
    "end": "(1, 3)",
    "payload": {
        "type": 2
    }
}
```

**/duplicate**
- It duplicates a map
  - method: POST
  - arguments: url (optional)

Duplicate URL Payload
```json
{
    "url": "https://something.something.com"
}
