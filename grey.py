from elasticsearch import Elasticsearch
es = Elasticsearch(['http://172.17.4.15:9200/'])
print(es.ping())
es.indices.create(index='social_posts2')
