import re


def str111(num):  # -> !1!1!1!1!1
    """generate string like '!1!1!1!1' with length equal 'num'"""
    return "".join(["1" if i % 2 == 1 else "!" for i in range(num)])


replace_map = (
    ("too", "2"),
    ("to",     "2"),
    ("fore",   "4"),
    ("for",    "4"),
    ("oo",     "00"),
    ("be",     "b"),
    ("are",    "r"),
    ("you",    "u"),
    ("please", "plz"),
    ("people", "ppl"),
    ("really", "rly"),
    ("have",   "haz"),
    ("know",   "no"),
    ("s",      "z"),
)
FOR_REMOVE = ",.'"

def n00bify(string):
    for old, new in replace_map:
        string = re.sub(old, new, string, flags=re.IGNORECASE)

    for char in FOR_REMOVE:
        string = string.replace(char, "")

    if string[0].lower() == "w":
        string = "LOL " + string

    if len(string.replace("!", "")) > 31:
        if string.startswith("LOL "):
            string = "LOL " + "OMG " + string[4:]
        else:
            string = "OMG " + string

    splitted = string.split()
    word_count = len(splitted)
    for i, word in enumerate(splitted):
        if i % 2 == 1:
            splitted[i] = word.upper()
    string = " ".join(splitted)

    if string[0].lower() == "h":
        string = string.upper()

    string = string.replace("?", "?" * word_count)

    string = string.replace("!", str111(word_count))

    return string
