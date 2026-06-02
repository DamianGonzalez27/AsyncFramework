from logger_tracker import logg_info

class ElasticsearchRepository:

    def __init__(self, es_client):
        self.es_client = es_client

    def create_index(self, index_name, mappings):
        logg_info(f"start: create_index ElasticsearchRepository")
        self.es_client.indices.create(
            index=index_name,
            body={
                "mappings": mappings
            }
        )
        logg_info(f"success: create_index ElasticsearchRepository")
        return True

    def update_index(self, index_name, mappings):
        logg_info(f"start: update_index ElasticsearchRepository")
        self.es_client.indices.put_mapping(
            index=index_name,
            body={
                "mappings": mappings
            }
        )
        logg_info(f"success: update_index ElasticsearchRepository")
        return True

    def describe_index(self, index_name):
        logg_info(f"start: describe_index ElasticsearchRepository")
        return self.es_client.indices.get(index=index_name)

    def delete_index(self, index_name):
        logg_info(f"start: delete_index ElasticsearchRepository")
        self.es_client.indices.delete(index=index_name)
        logg_info(f"success: delete_index ElasticsearchRepository")
        return True