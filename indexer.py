# Umineko indexer and search
import string
from parser import ParsedQuote
from typing import List, Dict, Set
translator = str.maketrans('', '', string.punctuation)

# Indexer
def index_words(position:int, quote:ParsedQuote, index:Dict[str, Set[int]]):
    clean_text = quote.text.translate(translator)
    for word in clean_text.lower().split():
        if word not in index:
            index[word] = set()
        index[word].add(position)

def build_index(quotes: List[ParsedQuote]) -> Dict[str, Set[int]]:
    index = {}
    for i in range(len(quotes)):
        index_words(i, quotes[i], index)
    return index

# Search
def search(query: str, quotes: List[ParsedQuote], index: Dict[str, Set[int]]) -> List[ParsedQuote]:
    query = query.lower().translate(translator)
    query_hits = set()
    for word in query.split():
        if word in index:
            if not query_hits:
                query_hits = query_hits.union(index[word])
            else:
                query_hits = query_hits.intersection(index[word])
    results_found = [quotes[i] for i in query_hits]
    return results_found
