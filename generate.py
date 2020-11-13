import json
import random
from pathlib import Path


def get_data_from_path(input_file_path):
    if not input_file_path.is_file():
        print("Use create.py to generate a json first")
        return
    f = input_file_path.open("r")
    result = json.load(f)
    f.close()
    return result


def total_map(input_map):
    total = 0
    for value in input_map.values():
        total += value
    return total


def map_weighted_random(input_map):
    index = random.randint(1, total_map(input_map))
    for key, value in input_map.items():
        index -= value
        if index <= 0:
            return key


def generate(word_map, context_map):
    current = word_map.get("@start")
    word = ""
    output = ""
    while True:
        contextual = {}
        if not len(word) == 0:
            contextual.update(context_map[word])
            contexed = current.copy()
            start_total = total_map(contexed)

            context_factor = start_total / len(contextual) / max(contextual.values())
            for key in contexed.keys():
                if not key == "@end":
                    contexed[key] += int((contextual[key]) * context_factor)

            # Size multiplier
            if "@end" in contexed:
                contexed["@end"] *= int(total_map(contexed) / start_total)
            print(context_factor)
            word = map_weighted_random(contexed)
        else:
            word = map_weighted_random(current)
        if word == "@end":
            return output
        output += word + " "
        current = word_map.get(word)


if __name__ == '__main__':
    m = get_data_from_path(Path("data.json"))
    if m:
        print(generate(m["word_map"], m["context_map"]))
