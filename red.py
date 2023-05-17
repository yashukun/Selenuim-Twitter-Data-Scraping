from elasticsearch import Elasticsearch
es = Elasticsearch(['http://172.17.4.15:9200/'])
response = es.indices.delete(index='social_posts')
print(response)
print(es.ping())
