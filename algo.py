import random

keyboard = [
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

def remove():
    NotImplementedError

def insert():
    NotImplementedError


website = str(input("Enter a website: "))



keyboard_adj = build_adjacency(keyboard)
## UNCOMMENT TO CHECK FOR A SPECIFIC KEY
# keyboard_adj_list = keyboard_adj['i']
# print(f"Neighbors of 'i':", keyboard_adj["i"])

def gen_typosquatting(website):
    placeholder = list(website)

    
    print("----- 1 character swapped -----")
    for i in range(len(website)):
        keyboard_adj_list = keyboard_adj[website[i]]
        randomadjacencydictindex = random.randint(0, len(keyboard_adj_list) - 1)
        
    #    print(f"Neighbors of '{website[i]}':", keyboard_adj_list[randomadjacencydictindex])
        print("".join(swap(placeholder, keyboard_adj_list[randomadjacencydictindex], i)))
        placeholder = list(website)
        
    print("----- 2 characters swapped -----")

    for i in range(len(website)):
        for j in range(i+1, len(website)): # 0, 1 0, 2 | 1, 1 1, 2 these are how the values to be swapped are selected
            # make a copy of the original chars
            new_placeholder = list(website)

            
            if website[i] in keyboard_adj:
                neigh_i = random.choice(keyboard_adj[website[i]])
                new_placeholder[i] = neigh_i

            
            if website[j] in keyboard_adj:
                neigh_j = random.choice(keyboard_adj[website[j]])
                new_placeholder[j] = neigh_j

            print("".join(new_placeholder))


gen_typosquatting(website)