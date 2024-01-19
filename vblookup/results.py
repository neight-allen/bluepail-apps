from vblookup.model import get_client
from pprint import pprint

def list_of_seq_unique_by_key(seq, key):
    seen = set()
    seen_add = seen.add
    return [x for sublist in seq for x in sublist if x[key] not in seen and not seen_add(x[key])]


def get_videos(query_text, author=None, n_results=5):
  client = get_client()
  green_brothers = client.get_collection(name="green_brothers")

  where = {"source_key": {"$ne": "oJ-T4RAoh-E"}}
  if author is not None:
    where = {
      "$and": [
        where,
        {
          "author": {
            "$ne": "hank" if author == "john" else "john"
          }
        }
      ]
    }
  
  results = green_brothers.query(
      query_texts=query_text,
      where= where,
      include=["metadatas"],
      n_results=n_results
    )["metadatas"]
  
  unique_results = list_of_seq_unique_by_key(results, "source_key")

  return unique_results
