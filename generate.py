import json
import random
from pathlib import Path


def get_data_from_path(input_file_path):
    if not input_file_path.is_file():
        print("Use generate.py to generate a json first")
        return
    f = input_file_path.open("r")
    result = json.load(f)
    f.close()
    return result


def map_weighted_random(input_map):
    # Todo nicen
    total = 0
    for value in input_map.values():
        total += value
    # Reuse of variable, now stores chosen index
    total = random.randint(1, total)

    for key, value in input_map.items():
        total -= value
        if total <= 0:
            return key


def generate(word_map):
    current = word_map.get("@start")
    output = ""
    while True:
        word = map_weighted_random(current)
        if word == "@end":
            return output
        output += word + " "
        current = word_map.get(word)


if __name__ == '__main__':
    m = get_data_from_path(Path("data.json"))
    if m:
        print(generate(m))
