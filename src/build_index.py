from data_preparation import prepare_data
from store import rebuild_vector_store
_,all_chunks = prepare_data()
vector_store = rebuild_vector_store(all_chunks)
print(vector_store._collection.count())
