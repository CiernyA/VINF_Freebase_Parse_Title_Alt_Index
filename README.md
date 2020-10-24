# VINF_Freebase_Parse_Title_Alt_Index

### Dependencies: 
* Elasticsearch (installed by "pip install elasticsearch")

The code was tested on a file with 1M lines from freebase (the file can't be uploaded to github). It parses name, display name and object.type. For name and display name the values are parsed and compared, if they are different both are added into the "name" array in the JSON object. If the are the same, only one value is kept.


### Output from script
This is just a sample, the whole output is in data/parsed_objects.json
```
{
  "footballdb_id": {"name": ["footballdb ID"], "type": "property"},
  "discoveries": {"name": ["Discoveries"], "type": "property"},
  "fuel_tank_capacity": {"name": ["Fuel Tank Capacity"], "type": "property"},
  "engine_type": {"name": ["Engine Type"], "type": "property"},
  "max_passengers": {"name": ["Maximum Number of Passengers"], "type": "property"},
  "first_flight": {"name": ["First flight"], "type": "property"},
  "11b60thzvr": {"name": ["Musical Track", "Musical Recording"], "type": "notable_for"},
}
```