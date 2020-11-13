from pathlib import Path
import json


def get_input_file(input_file_path):
    if not input_file_path.is_file():
        input_file_path.touch()
        print("Please input datas into inputs.txt")
        return
    return open(input_file_path, "r")


def write_output(output_file_path, content):
    f = output_file_path.open("w")
    json.dump(content, f)
    f.close()


def add_to_map(current_map, word):
    if word in current_map:
        current_map[word] += 1
    else:
        current_map[word] = 1


def read_file(f):
    word_map = {"@start": {}}
    context_map = {}

    sentence = []
    current_map = word_map.get("@start")
    while True:
        word = ""
        end_of_sentence, end_of_file = False, False

        while True:
            letter = f.read(1)
            # EOF
            if not letter:
                end_of_file = True
                break
            # End of word
            if letter == " ":
                break
            # End of sentence
            if letter in ".;!?":
                end_of_sentence = True
                break
            # Ignored characters
            if letter in ",:;\"'-()\r\n":
                continue
            word += letter

        # Consecutive end of word characters
        if len(word) == 0 and not end_of_file:
            continue

        word = word.lower()

        add_to_map(current_map, word)
        sentence.append(word)
        if word not in word_map:
            word_map[word] = {}
        current_map = word_map[word]

        if end_of_sentence or end_of_file:
            add_to_map(current_map, "@end")

            # Context
            for i1 in range(0, len(sentence)):
                w = sentence[i1]
                if w not in context_map:
                    context_map[w] = {}
                for i2 in range(0, len(sentence)):
                    if not i1 == i2:
                        add_to_map(context_map[w], sentence[i2])
            sentence = []
            if end_of_file:
                break
            current_map = word_map.get("@start")

    return {"word_map": word_map, "context_map": context_map}


if __name__ == '__main__':
    file = get_input_file(Path("input.txt"))
    if file:
        write_output(Path("data.json"), read_file(file))
