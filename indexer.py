# Umineko indexer and search
import string
from parser import ParsedQuote
from typing import List, Dict
from collections import Counter

# Indexer
def index_words(position:int, quote:ParsedQuote, index:Dict[str, List[int]]):
    translator = str.maketrans('', '', string.punctuation)
    clean_text = quote.text.translate(translator)
    for word in clean_text.lower().split():
        if word not in index:
            index[word] = []
        if position not in index[word]:
            index[word].append(position)

def build_index(quotes: List[ParsedQuote]) -> Dict[str, List[int]]:
    index = {}
    for i in range(len(quotes)):
        index_words(i, quotes[i], index)
    return index

# Search
def search(query: str, quotes: List[ParsedQuote], index: Dict[str, List[int]]) -> List[ParsedQuote]:
    translator = str.maketrans('', '', string.punctuation)
    query = query.lower().translate(translator)
    query_hits = []
    for word in query.split():
        if word in index:
            query_hits.extend(index[word])
    counted_hits = Counter(query_hits)
    results_found = [quotes[i[0]] for i in counted_hits.most_common() if i[1] == len(query.split()) ]
    return results_found
