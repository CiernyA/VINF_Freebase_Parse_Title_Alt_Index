import re
import json
import zlib
from elasticsearch import Elasticsearch, helpers

DATA_DIR_NAME = "data/"
DATA_FILE_NAME = "freebase-rdf-latest"
#DATA_FILE_NAME = "freebase-rdf-latest.gz"
NEEDED_ATRIBUTES = "(type\.object\.name|\.display_name|type\.object\.type)"
NOT_IMPORTANT_ATTRIBUTES = "(www\.w3\.org|dated_percentage|dated_integer|pronunciation|pagination)"
#Further filter out: 
ENGLISH_NAME = ""
OUTPUT_FILE_NAME = "parsed_objects"

def stream_unzipped_bytes(filename):
    with open(filename, 'rb') as f:
        wbits = zlib.MAX_WBITS | 16
        to_decompress = zlib.decompressobj(wbits)
        fbytes = f.read(16384)
        while fbytes:
            yield to_decompress.decompress(to_decompress.unconsumed_tail + fbytes)
            fbytes = f.read(16384)

def stream_text(gen):
    try:
        buffer = next(gen)
        while buffer:
            lines = buffer.splitlines(keepends=True)
            for line in lines[:-1]:
                yield line.decode() #encoding='UTF-8'
            buffer = lines[-1]
            buffer += next(gen)
            if(len(buffer) < 500):
                print(f"{len(buffer)} - content of buffer: {buffer}")
    except StopIteration:
        print("I got here")
        if buffer:
            yield buffer.decode() #encoding='UTF-8'


json_file = open("{}{}".format(DATA_DIR_NAME, OUTPUT_FILE_NAME),"w", encoding="utf-8") #, errors="replace"
json_file.write("[\n")

indexer = Elasticsearch()

#indexer.indices.delete(index="vinf_index")

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
    #b_generator = (x for x in stream_unzipped_bytes("{}{}".format(DATA_DIR_NAME,DATA_FILE_NAME)))
    parsed_object = {}
    parsed_title=""
    #for line in stream_text(b_generator):
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
                        "_index": "vinf_index",
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
