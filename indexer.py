# Umineko indexer and search
import string
from parser import ParsedQuote
from typing import List, Dict
from collections import Counter, defaultdict
translator = str.maketrans('', '', string.punctuation)

# Indexer
def index_words(position:int, quote:ParsedQuote, index:Dict[str, List[int]]):
    clean_text = quote.text.translate(translator)
    seen = defaultdict(set)
    for word in clean_text.lower().split():
        if position in seen[word]:
            continue
        seen[word].add(position)
        if word in index:
            index[word].append(position)
            continue
        index[word] = [position]

def build_index(quotes: List[ParsedQuote]) -> Dict[str, List[int]]:
    index = {}
    for i in range(len(quotes)):
        index_words(i, quotes[i], index)
    return index

# Search
def search(query: str, quotes: List[ParsedQuote], index: Dict[str, List[int]]) -> List[ParsedQuote]:
    query = query.lower().translate(translator)
    query_hits = []
    for word in query.split():
        if word in index:
            query_hits.extend(index[word])
    counted_hits = Counter(query_hits)
    results_found = [quotes[i[0]] for i in counted_hits.most_common() if i[1] == len(query.split()) ]
    return results_found
