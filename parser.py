# Umineko File Parser
import re
from dataclasses import dataclass
from typing import List

# Parsing Regexes
inline_command = re.compile(r'\[([^\]]+)\]')
inline_text = re.compile(r'`([^`]+)`')
inline_voice = re.compile(r'lv 0\*"(\d+)"\*"(.*)"')

# Data Classes
@dataclass
class ParsedQuote:
    text: str
    character_id: int
    episode: int
    audio_ids: List[int]

# Parser
def apply_format(string: str) -> str:
    retval = []
    first_idx = string.find('{')
    if first_idx == -1:
        return string
    if '}' not in string:
        return string
    last_idx = len(string) - string[::-1].find('}') -1
    if first_idx != 0:
        retval.append(string[:first_idx-1]) # before formatting

    extract = string[first_idx+1:last_idx-1]
    if '{' in extract:
        extract = apply_format(extract) # recurse

    # parse formatting
    split = extract.split(':')
    match len(split):
        case 1:
            extract = extract.replace("n"," ").replace("0","").replace("qt","\"").replace("-","")
            extract = extract.replace("ob","(").replace("eb",")")
            extract = extract.replace("os","[").replace("es","]")
        case 2:
            extract = split[1]
        case 3:
            if split[0] != 'y':
                extract = split[2]
            else:
                extract = ""
    retval.append(extract)

    if last_idx < len(string)-1:
        retval.append(string[last_idx+1:]) # after formatting
    return "".join(retval)

def parse_formatting(strings: List[str]) -> str:
    formatted = []
    for s in strings:
        if '{' not in s:
            formatted.append(s)
            continue
        formatted.append(apply_format(s))
    return "".join(formatted)

def parse_dline(line: str) -> ParsedQuote | None:
    quote = ParsedQuote("", 100, -1, [])
    text = inline_text.findall(line)
    if not text:
        return None
    quote.text = parse_formatting(text)

    commands = inline_command.findall(line)
    if not commands:
        return quote
    audio_ids = set()

    for command in commands:
        matches = inline_voice.findall(command)
        if not matches:
            continue
        quote.character_id = int(matches[0][0])
        audio_id = matches[0][1]
        quote.episode = int(audio_id[0]) if audio_id[0].isdigit() else -1
        audio_ids.add(audio_id)

    quote.audio_ids = list(audio_ids)
    return quote

def parse_all_quotes(filename: str) -> List[ParsedQuote]:
    with open(filename, "r") as file:
        quotes = [y for y in (parse_dline(x) for x in file.read().splitlines() if x.startswith(("d ","d2 "))) if y is not None]
    return quotes
