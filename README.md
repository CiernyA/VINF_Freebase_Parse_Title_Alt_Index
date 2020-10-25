# VINF_Freebase_Parse_Title_Alt_Index

### Dependencies: 
* Elasticsearch

The code was tested on a file with 1M lines from freebase (the file can't be uploaded to github). It parses name, display name and object.type. For name and display name the values are parsed and compared, if they are different both are added into the "name" array in the JSON object. If the are the same, only one value is kept.


### Output from script
This is just a sample, the whole output is in data/parsed_objects.json
```
[
  {"name": ["footballdb ID"], "title": "footballdb_id", "type": "property"},
  {"name": ["Discoveries"], "title": "discoveries", "type": "property"},
  {"name": ["Fuel Tank Capacity"], "title": "fuel_tank_capacity", "type": "property"},
  {"name": ["Engine Type"], "title": "engine_type", "type": "property"},
  {"name": ["Screenwriter", "Scriptwriter"], "title": "11b80bfsmv", "type": "notable_for"},
]
```