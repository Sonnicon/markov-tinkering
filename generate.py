import json
import random
from pathlib import Path


def get_data_from_path(input_file_path=Path("data.json")):
    if not input_file_path.is_file():
        print("Data file not found")
        return
    f = input_file_path.open("r")
    result = json.load(f)
    f.close()
    return result


def map_weighted_random(input_map, total=-1):
    if total == -1:
        total = sum(input_map.values())

    index = random.randint(1, total)
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
            start_total = sum(contexed.values())

            context_factor = start_total / len(contextual) / max(contextual.values())
            for key in contexed.keys():
                if not key == "@end":
                    contexed[key] += int((contextual[key]) * context_factor)

            total = sum(contexed.values())

            # Size multiplier
            if "@end" in contexed:
                contexed["@end"] *= int(total / start_total)

            word = map_weighted_random(contexed)
        else:
            word = map_weighted_random(current)
        if word == "@end":
            return output
        output += word + " "
        current = word_map.get(word)


if __name__ == '__main__':
    m = get_data_from_path()
    if m:
        print(generate(m["word_map"], m["context_map"]))
