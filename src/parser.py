import re
import json
from elasticsearch import Elasticsearch

DATA_DIR_NAME = "data/"
DATA_FILE_NAME = "big_data.txt"
NEEDED_ATRIBUTES = "(type\.object\.name|\.display_name|type\.object\.type)" #\#label|\#type
ENGLISH_NAME = ""
OUTPUT_FILE_NAME = "parsed_objects.json"

json_file = open("{}{}".format(DATA_DIR_NAME, OUTPUT_FILE_NAME),"w", encoding="utf-8", errors="replace")
json_file.write("[\n")

indexer = Elasticsearch()
index_id = 0

indexer.indices.delete(index="_all")

def print_object_to_file(object):
    print("{},".format(json.dumps(object, sort_keys=True)),file=json_file)

def parse_object_triplet(part):
#    if('#' in part):
#        return part.split('#')[1].replace('>','')
    if('"' in part):
        return part.split('"')[1]
    else:
        temp = part.split('.')
        return temp[len(temp)-1].replace('>','')



with open("{}{}".format(DATA_DIR_NAME,DATA_FILE_NAME),encoding="utf-8") as file:
    parsed_object = {}
    parsed_title=""
    for line in file:
        if(re.search(NEEDED_ATRIBUTES, line)):
            triplet = line.split("\t")
            temp = triplet[0].split('.')
            line_title = temp[len(temp)-1].replace('>','')

            if parsed_title == "":
                parsed_title = line_title
                parsed_object={}
                parsed_object["title"] = parsed_title
            elif line_title != parsed_title:
                print_object_to_file(parsed_object)
                indexer.index(index = "vinf_index", id=index_id, body = parsed_object) 
                index_id += 1

                parsed_title = line_title
                parsed_object={}
                parsed_object["title"] = parsed_title
            attribute=""

            temp = triplet[1].split('.')
            attribute = temp[len(temp)-1].replace('>','')
            if("@" in triplet[2]):
                if not re.search("@en",triplet[2]):
                    continue

            object = parse_object_triplet(triplet[2])
            if(re.search("(name|display_name)",attribute)):                
                attribute = "name" if attribute == "display_name" else attribute
                if(attribute not in parsed_object):
                    parsed_object[attribute] = []
                if(object not in parsed_object[attribute]):
                    parsed_object[attribute].append(object)
            else:
                parsed_object[attribute] = object
    parsed_object={}

json_file.write("\n]")
json_file.close()
