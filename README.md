# VINF_Freebase_Parse_Title_Alt_Index
So far I have tested the script on 10 000 rows from unzipped Freebase database. Right now I am parsing only the type and the name. Later I am planning on adding searching for alternative titles of objects from _display\_name_ and _schema\#label_

The data needs to be indexed. For that I will use elasticsearch.
### Output from script
```
{
  'footballdb_id': {
    'type': 'property',
    'name': 'footballdb ID'
  }
  'discoveries': {
    'name': 'Discoveries',
    'type': 'property'
  }
  'fuel_tank_capacity': {
    'name': 'Fuel Tank Capacity',
    'type': 'property'
  }
  'engine_type': {
  'name': 'Engine Type',
  'type': 'property'
  }
  'max_passengers': {
    'type': 'property',
    'name': 'Maximum Number of Passengers'
  }
  'first_flight': {
    'type': 'property',
    'name': 'First flight'
  }
}
```