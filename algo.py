import random

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


website = input("Enter a website: ")

def remove_typesquatting(website):
    print("----- 1 character removed -----")    
    for i in range(len(website)):
        placeholder = list(website)
        del placeholder[i-1]
        print("".join(placeholder))    

def duplicate_typesquatting(website):
    print("----- 1 duplicated character added -----")    
    for i in range(len(website)):
        placeholder = list(website)
        duplicatedchar = placeholder[i]
        placeholder.insert(i+1, duplicatedchar)
        print("".join(placeholder))  


keyboard_adj = build_adjacency(keyboard)
## UNCOMMENT TO CHECK FOR A SPECIFIC KEY
# keyboard_adj_list = keyboard_adj['i']
# print(f"Neighbors of 'i':", keyboard_adj["i"])

def swap_typosquatting(website):
    placeholder = list(website)

    print("----- 1 character swapped -----")
    for i in range(len(website)):
        if website[i] not in keyboard_adj:  # skip if not in keyboard
            continue

        keyboard_adj_list = keyboard_adj[website[i]]
        new_char = random.choice(keyboard_adj_list)

        # Ensure first char never becomes "-"
        if i == 0:
            while new_char == "-":
                new_char = random.choice(keyboard_adj_list)

        print("".join(swap(placeholder, new_char, i)))
        placeholder = list(website)

    print("----- 2 characters swapped -----")
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

            print("".join(new_placeholder))



swap_typosquatting(website)
remove_typesquatting(website)
duplicate_typesquatting(website)