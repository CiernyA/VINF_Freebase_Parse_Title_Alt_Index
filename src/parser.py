import re
import json
from elasticsearch import Elasticsearch, helpers

DATA_DIR_NAME = "data/"
DATA_FILE_NAME = "freebase-rdf-latest"
NEEDED_ATRIBUTES = "(type\.object\.name|\.display_name|type\.object\.type)"
NOT_IMPORTANT_ATTRIBUTES = "(www\.w3\.org|dated_percentage|dated_integer|pronunciation|pagination)"
OUTPUT_FILE_NAME = "vinf_cierny_parsed_objects"
INDEX_NAME = "vinf_cierny_freebase_2020"


json_file = open("{}{}".format(DATA_DIR_NAME, OUTPUT_FILE_NAME),"w", encoding="utf-8")
json_file.write("[\n")

indexer = Elasticsearch()

def print_object_to_file(object):
    print("{},".format(json.dumps(object, sort_keys=True)),file=json_file)

def parse_object_triplet(part):
    if('@' in part):
        return part.split('@')[0].strip('"')
    if('.'):
        temp = part.split('.')
        return temp[len(temp)-1].replace('>','')
    else:
        return part

def handle_data():
    index_id = 0
    parsed_object = {}
    parsed_title=""
    with open("{}{}".format(DATA_DIR_NAME, DATA_FILE_NAME),'r', encoding='UTF-8') as file:
        for line in file:
            if (re.search(NOT_IMPORTANT_ATTRIBUTES, line)):
                continue
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
                    yield {
                        "_index": INDEX_NAME,
                        "_id": index_id,
                        "_source": parsed_object
                    }
                    index_id += 1

                    parsed_title = line_title
                    del parsed_object
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
    del parsed_object

helpers.bulk(indexer, handle_data())
json_file.write("\n]")
json_file.close()
