import random
from itertools import combinations, product

keyboard = [ #### QWERTY ####
    "1234567890-",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm"
]

def build_adjacency(layout):
    adjacency = {}
    # loop over rows
    for row_idx in range(len(layout)):
        row = layout[row_idx]
        # loop over columns
        for col_idx in range(len(row)):
            char = row[col_idx]
            neighbors = []
            # check nearby keys (up, down, left, right, diagonals)
            for i in [-1, 0, 1]:     
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue  
                    r = row_idx + i
                    c = col_idx + j
                    # make sure we're inside keyboard bounds
                    if 0 <= r < len(layout) and 0 <= c < len(layout[r]):
                        neighbors.append(layout[r][c])
            adjacency[char] = neighbors
    return adjacency

def swap(placeholder,swappedval, i):
    placeholder[i] = swappedval
    return placeholder


def remove_typesquatting(website):
    return [website[:i] + website[i+1:] for i in range(len(website))]

def duplicate_typesquatting(website):
    a =  []
    for i in range(len(website)):
        placeholder = list(website)
        duplicatedchar = placeholder[i]
        placeholder.insert(i+1, duplicatedchar)
        a.append("".join(placeholder))
    return a

keyboard_adj = build_adjacency(keyboard)
## UNCOMMENT TO CHECK FOR A SPECIFIC KEY
# keyboard_adj_list = keyboard_adj['i']
# print(f"Neighbors of 'i':", keyboard_adj["i"])

def swap_typosquatting(website):
    placeholder = list(website)
    ret_obj = {
        "1swap": [],
        "2swap": []
    }
    #print("----- 1 character swapped -----")
    for i in range(len(website)):
        if website[i] not in keyboard_adj:  # skip if not in keyboard
            continue

        keyboard_adj_list = keyboard_adj[website[i]]
        new_char = random.choice(keyboard_adj_list)

        # Ensure first char never becomes "-"
        if i == 0:
            while new_char == "-":
                new_char = random.choice(keyboard_adj_list)

        ret_obj["1swap"].append("".join(swap(placeholder, new_char, i)))
        placeholder = list(website)

    #print("----- 2 characters swapped -----")
    for i in range(len(website)):
        for j in range(i + 1, len(website)):
            new_placeholder = list(website)

            if website[i] in keyboard_adj:
                neigh_i = random.choice(keyboard_adj[website[i]])
                if i == 0:  # same rule for first char in 2-swap
                    while neigh_i == "-":
                        neigh_i = random.choice(keyboard_adj[website[i]])
                new_placeholder[i] = neigh_i

            if website[j] in keyboard_adj:
                neigh_j = random.choice(keyboard_adj[website[j]])
                new_placeholder[j] = neigh_j
            ret_obj["2swap"].append("".join(new_placeholder))

    return ret_obj
def leetTranslate(website) :
    print("--- Leet ---")
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
    
    letters = list(website.upper())
    
    indices_leetable = [i for i, l in enumerate(letters) if l in leet_dict]

    results = set()  # avoid duplicates

    # For i = 1 up to len(indices_leetable)
    for i in range(1, len(indices_leetable) + 1):
        for combo in combinations(indices_leetable, i):
            # For each index in combo, try all possible substitutions
            options = [leet_dict[letters[idx]] for idx in combo]
            for repl in product(*options):
                new_website = letters[:]  # copy original letters
                for idx, sub in zip(combo, repl):
                    new_website[idx] = sub
                results.add("".join(new_website))

    return sorted(results)


def edits1(website):
    "All edits that are one edit away from `website`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(website[:i], website[i:])    for i in range(len(website) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return deletes + transposes + replaces + inserts

def edits2(website): 
    "All edits that are two edits away from `website`."
    results = []
    
    for edit in edits1(website) :
        results += edits1(edit)
        
    return results

if __name__ == "__main__":
    website = input("Enter a website: ")

    print(swap_typosquatting(website))
    print(remove_typesquatting(website))
    print(duplicate_typesquatting(website))
    print("\n".join(leetTranslate(website)))
    print("\n".join(edits1(website)))
    print("\n".join(edits2(website)))