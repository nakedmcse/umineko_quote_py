# Umineko indexer and search
import string
from parser import ParsedQuote
from dataclasses import dataclass
from typing import List, Dict, Set
translator = str.maketrans('', '', string.punctuation)

# Dataclasses
@dataclass
class MultiIndex:
    Words: Dict[str, Set[int]]
    Audio: Dict[int, Set[int]]

# Indexer
def index_words(position:int, quote:ParsedQuote, index:Dict[str, Set[int]]):
    clean_text = quote.text.translate(translator)
    for word in clean_text.lower().split():
        if word not in index:
            index[word] = set()
        index[word].add(position)

def index_audio(position:int, quote:ParsedQuote, index:Dict[int, Set[int]]):
    for audio_id in quote.audio_ids:
        if audio_id not in index:
            index[audio_id] = set()
        index[audio_id].add(position)

def build_index(quotes: List[ParsedQuote]) -> MultiIndex:
    index = MultiIndex({},{})
    for i in range(len(quotes)):
        index_words(i, quotes[i], index.Words)
        index_audio(i, quotes[i], index.Audio)
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

def search_audio(query: int, quotes: List[ParsedQuote], index: Dict[int, Set[int]]) -> List[ParsedQuote]:
    if query not in index:
        return []
    return [quotes[i] for i in index[query]]