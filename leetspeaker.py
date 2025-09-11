# Takes a word
# Makes a list of the letters in said word
# Compare it to an existing leetspeak table 
# Dictionary, letter to list of leetspeak chars usable in URLs

from itertools import combinations, product

def leetTranslate(word) :
    # Initialise dictionary of letters --> leet
    leet_dict = {
        "A": ["4"],
        "B": ["8", "13"],
        "C": ["<", "(", "C"],
        "D": ["D"],
        "E": ["3"],
        "F": ["F"],
        "G": ["6", "9"],
        "H": ["H"],
        "I": ["1"],
        "J": ["J"],
        "K": ["K"],
        "L": ["1", "L", "7"],
        "M": ["M"],
        "N": ["N"],
        "O": ["0"],
        "P": ["P"],
        "Q": ["Q"],
        "R": ["R", "12"],
        "S": ["5", "2"],
        "T": ["7"],
        "U": ["U", "V"],
        "V": ["V"],
        "W": ["W", "VV"],
        "X": ["X"],
        "Y": ["Y"],
        "Z": ["2", "Z"]
    }
    
    # Makes a list of the letters in said word
    # Compare it to an existing leetspeak table 
    # Dictionary, letter to list of leetspeak chars usable in URLs
    
    letters = list(word.upper())
    
    indices_leetable = [i for i, l in enumerate(letters) if l in leet_dict]

    results = set()  # avoid duplicates

    # For i = 1 up to len(indices_leetable)
    for i in range(1, len(indices_leetable) + 1):
        for combo in combinations(indices_leetable, i):
            # For each index in combo, try all possible substitutions
            options = [leet_dict[letters[idx]] for idx in combo]
            for repl in product(*options):
                new_word = letters[:]  # copy original letters
                for idx, sub in zip(combo, repl):
                    new_word[idx] = sub
                results.add("".join(new_word))

    return sorted(results)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))