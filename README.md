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

## Version Informaiton

**V1**
- Simple one file with all the class, all the methods and the support functions.

**V2**
- Separated the main function from the Polyverse Class

**V3**
- Added Flask to be able to serve the requests

**V4**
- Dockerize the solution to be able to use it from anywhere.

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
  - Writes an element into the API map
- __clean_element_poliverse
- __verify_position

**Public Methods**
- get_polyverse_map
- show_local_polyverse
- clean_polyverse
- write_local_map
- delete_local_map
- merge_map
- local_map_payload
- duplicate_polyverse