import random
from itertools import combinations, product
from flask import Flask, request, jsonify

app = Flask(__name__)


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
    results = []
    
    print("----- 1 character removed -----")    
    for i in range(len(website)):
        placeholder = list(website)
        del placeholder[i-1]
        results.append("".join(placeholder))
    
    return results

def duplicate_typesquatting(website):
    results = []
    
    for i in range(len(website)):
        placeholder = list(website)
        duplicatedchar = placeholder[i]
        placeholder.insert(i+1, duplicatedchar)
        results.append("".join(placeholder))
        
    return results

def swap_typosquatting(website):
    results = []

    for i, char in enumerate(website):
        if char not in keyboard_adj:  # skip chars not on keyboard
            continue

        new_char = random.choice(keyboard_adj[char])

        # Ensure first char never becomes "-"
        if i == 0:
            while new_char == "-":
                new_char = random.choice(keyboard_adj[char])

        placeholder = list(website)
        placeholder[i] = new_char
        results.append("".join(placeholder))

    return results

def swap2_typosquatting(website):
    results = []

    for i in range(len(website)):
        for j in range(i + 1, len(website)):
            new_placeholder = list(website)

            if website[i] in keyboard_adj:
                neigh_i = random.choice(keyboard_adj[website[i]])
                if i == 0:  # first char should not become "-"
                    while neigh_i == "-":
                        neigh_i = random.choice(keyboard_adj[website[i]])
                new_placeholder[i] = neigh_i

            if website[j] in keyboard_adj:
                neigh_j = random.choice(keyboard_adj[website[j]])
                if j == 0:  # same safety check for j if it’s the first char
                    while neigh_j == "-":
                        neigh_j = random.choice(keyboard_adj[website[j]])
                new_placeholder[j] = neigh_j

            results.append("".join(new_placeholder))

    return results

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

keyboard = [ #### QWERTY ####
    "1234567890-",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm"
]

keyboard_adj = build_adjacency(keyboard)

def find_squats(website):
    squats_list = remove_typesquatting(website) + duplicate_typesquatting(website) + swap_typosquatting(website) + swap2_typosquatting(website) + leetTranslate(website) + edits1(website) + edits2(website)
    return squats_list

@app.route('/squats', methods=["POST"])
def squats():
    # Get JSON data
    data = request.get_json()  # Parse JSON body

    # If there's no body or no website param, error
    if not data or "website" not in data:
        return jsonify({"error": "Missing 'website' attribute"}), 400

    # Store website value in variable
    website = data["website"] 
    
    # Check website for TLD, strip and save
    
    # This should return a list of possible domains.
    # do each one and then return the final concatenated result
    # Add back the TLD
    
    domains = find_squats(website)
    
    response = {"domains": domains}
    return jsonify(response), 200
    

if __name__ == '__main__':
    app.run(debug=True)