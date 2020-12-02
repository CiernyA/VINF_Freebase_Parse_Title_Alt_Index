#Search system for my indexed data
INDEX_NAME = "vinf_cierny_freebase_2020"
import Elasticsearch
indexer = Elasticsearch()


print("This tool is used to query data indexed in ElasticSearch - 'vinf_index'.")
print("Please specify what to search by: 'type', 'name' or 'id'. To exit type 'exit'")
user_input = input("> ")
while user_input != "exit":
    print("Tralala")
    field = user_input
    query = input("Write a keyword to match:\n> ")
    res = indexer.search(index=INDEX_NAME, body={"query": {"must": { "match": {field: {"query": query}  }}}})
    print("response:\n" + res)
    
    user_input = input("> ")