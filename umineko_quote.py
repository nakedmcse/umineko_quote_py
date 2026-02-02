# Partial Umineko Quote Finder Implementation
import time
from parser import parse_all_quotes
from indexer import build_index, search
from characters import get_character_name
from utils import get_size,sizeWords

start = time.time()
parsed = parse_all_quotes('umineko.txt')
end = time.time()
print(f"Parsed {len(parsed)} quotes ({sizeWords(get_size(parsed))}) in {(end-start)*1000:.4f} ms")

start = time.time()
index = build_index(parsed)
end = time.time()
print(f"Indexed quotes ({sizeWords(get_size(index))}) in {(end-start)*1000:.4f} ms")
print()

start = time.time()
search_one = search('Dont be absurd', parsed, index)
end = time.time()
print(f'Search one: "Dont be absurd" - {len(search_one)} results in {(end-start)*1000:.4f} ms')
for r in search_one:
    print(f'{get_character_name(r.character_id)} - Ep. {r.episode}: {r.text}')
print()

start = time.time()
search_two = search('it seems that no one', parsed, index)
end = time.time()
print(f'Search two: "it seems that no one" - {len(search_two)} results in {(end-start)*1000:.4f} ms')
for r in search_two:
    print(f'{get_character_name(r.character_id)} - Ep. {r.episode}: {r.text}')
print()

start = time.time()
search_three = search('with your fellow monsters', parsed, index)
end = time.time()
print(f'Search three: "with your fellow monsters" - {len(search_three)} results in {(end-start)*1000:.4f} ms')
for r in search_three:
    print(f'{get_character_name(r.character_id)} - Ep. {r.episode}: {r.text}')
print()