# Partial Umineko Quote Finder Implementation
import time
from parser import parse_all_quotes
from indexer import build_index, search
from characters import get_character_name

start = time.time()
parsed = parse_all_quotes('umineko.txt')
end = time.time()
print(f"Parsed quotes in {(end-start)*1000:.4f} ms")

start = time.time()
index = build_index(parsed)
end = time.time()
print(f"Indexed quotes in {(end-start)*1000:.4f} ms")
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