import re

DATA_DIR_NAME = "data/"
DATA_FILE_NAME = "smaller_data.txt"
NEEDED_ATRIBUTES = "(type\.object\.name|\.display_name|type\.object\.type)" #\#label|\#type
OUTPUT_FILE_NAME = "parsed_objects.json"

json_file = open("{}{}".format(DATA_DIR_NAME, OUTPUT_FILE_NAME),"w")
json_file.write("{\n")

def print_object_to_file(object, title):
    print("\"{}\": {},".format(title,object[title]).replace('\'','\"'),file=json_file)

with open("{}{}".format(DATA_DIR_NAME,DATA_FILE_NAME),"r") as file:
    parsed_object = {}
    parsed_title=""
    for line in file:
        if(re.search(NEEDED_ATRIBUTES, line)):
            triplet = line.split("\t")
            temp = triplet[0].split('.')
            line_title = temp[len(temp)-1].replace('>','')

            if parsed_title == "":
                parsed_title = line_title
                parsed_object[line_title]={}
            elif line_title != parsed_title:
                print(parsed_object)
                print_object_to_file(parsed_object, parsed_title)
                parsed_object={}
                parsed_title = line_title
                parsed_object[line_title]={}
                #also index objects
            attribute=""
#            if("#" in triplet[1]):
#                attribute = triplet[1].split('#')[1].replace('>','')
#            else:
            temp = triplet[1].split('.')
            attribute = temp[len(temp)-1].replace('>','')
            object=""
#            if('#' in triplet[2]):
#                object=triplet[2].split('#')[1].replace('>','')
            if('"' in triplet[2]):
                object = triplet[2].split('"')[1]
            else:
                temp = triplet[2].split('.')
                object = temp[len(temp)-1].replace('>','')
            parsed_object[parsed_title][attribute] = object
    print(parsed_object)
    parsed_object={}

json_file.write("\"end\":{ }\n}")
json_file.close()
#Need to refine the parsing of attributes - if name/label/we, put it into alt_title arr probably