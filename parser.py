# Umineko File Parser
import re
from dataclasses import dataclass
from typing import List

# Parsing Regexes
voice_meta_regex = re.compile(r'\[lv 0\*"(\d+)"\*"(.*)"\]')
narrator_line_regex = re.compile(r'^d2? `')
bracket_regex = re.compile(r'\[[^\]]*\]')
episode_marker_regex = re.compile(r'^new_(?:tea|ura|episode) (\d+)\r?$')
text_rules = [
    (re.compile(r'\{[cef]:[A-Fa-f0-9]+:([^}]+)\}'), r'\1'),
    (re.compile(r'\{p:\d+:([^}]+)\}'), r'\1'),
    (re.compile(r'\{ruby:([^:]+):([^}]+)\}'), r'\2 (\1)'),
    (re.compile(r'\{i:([^}]+)\}'), r'\1'),
    (re.compile(r'\{[a-z]+:[^}]*\}'), ''),
]

# Data Classes
@dataclass
class ParsedQuote:
    text: str
    character_id: int
    episode: int
    audio_ids: List[int]

# Parser
def extract_text(text: str) -> str:
    text = text.replace('{n}', ' ').replace('`','').replace('"','')
    text = bracket_regex.sub('', text).removeprefix("d2 ").removeprefix("d ").strip()
    for p in text_rules:
        text = p[0].sub(p[1], text)
    return text

def parse_line(line: str) -> ParsedQuote | None:
    all_matches = voice_meta_regex.findall(line)
    if not all_matches or len(all_matches[0]) < 2:
        return None

    character_id = int(all_matches[0][0])
    first_audio_id = all_matches[0][1]
    episode = int(first_audio_id[0]) if first_audio_id[0].isdigit() else -1

    audio_ids = set()
    for match in all_matches:
        audio_ids.add(match[1])

    text = extract_text(line)
    if text == "":
        print(line)
        return None

    return ParsedQuote(text, character_id, episode, list(audio_ids))

def parse_all_quotes(filename: str) -> List[ParsedQuote]:
    with open(filename, "r") as file:
        quotes = [y for y in (parse_line(x) for x in file.read().splitlines() if x.startswith(("d [lv","d2 [lv"))) if y is not None]
    return quotes
