import sys

"""Read and parse TM definition from CSV"""
def read_tm_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    #parse file
    name_machine = lines[0].strip()
    start_state = lines[4].strip()
    accept_state = lines[5].strip()
    reject_state = lines[6].strip()
    transitions = {}
    
    for line in lines[7:]:
        if line.strip():
            curr, read, next_state, write, direction = line.strip().split(',')
            if (curr, read) not in transitions:
                transitions[(curr, read)] = []
            transitions[(curr, read)].append((next_state, write, direction))
            
    return name_machine, start_state, accept_state, reject_state, transitions

"Breadth first search exploration"
def breadth_first_exp(start_state, accept_state, reject_state, transitions, input, max=1000):
    #configuration tree
    tree = [[("", start_state, input)]]
    parent = {}
    total = 0
    
    #go through each level
    for depth in range(max):
        if not tree[depth]:  #end loop when no more configurations to explore
            return False, depth, total, []
            
        tree.append([]) 
        
        for config in tree[depth]:
            left, right, state = config
            
            #check if accepting
            if state == accept_state:
                path = get_path(config, parent)
                return True, depth, total, path
                
            #skip if rejecting
            if state == reject_state:
                continue
                
            #get current character
            curr_char = right[0] if right else "_"
            
            #get possible transitions
            moves = transitions.get((state, curr_char), [])
            
            #no more possible --> go to reject state
            if not moves:
                next = (left, reject_state, right)
                tree[depth + 1].append(next)
                parent[next] = config
                total += 1
                continue
                
            #apply possible transitions
            for next_state, write_char, direction in moves:
                new_left, new_right = apply_move(left, right, write_char, direction)
                next = (new_left, next_state, new_right)
                tree[depth + 1].append(next)
                parent[next] = config
                total += 1
                
    return False, max, total, []

"""single move on tape"""
def apply_move(left_tape, right, write_char, direction):
    # Write character
    if not right:
        right = write_char
    else:
        right = write_char + right[1:]
        
    # Move head
    if direction == 'R':
        if len(right) > 1:
            left_tape += right[0]
            right = right[1:]
        else:
            left_tape += right
            right = "_"
    else:  # direction == 'L'
        if left_tape:
            right = left_tape[-1] + right
            left_tape = left_tape[:-1]
        else:
            right = "_" + right
            
    return left_tape, right

"""Get path at start to current config"""
def get_path(config, parent):
    path = [config]
    while config in parent:
        config = parent[config]
        path.append(config)
    return list(reversed(path))

def main():
    if len(sys.argv) != 3:
        print("Error")
        sys.exit(1)
        
    file = sys.argv[1]
    input = sys.argv[2]
    
    #read def
    name_machine, start_state, accept_state, reject_state, transitions = read_tm_file(file)
    
    #run breath first search 
    check_accept, steps, total, path = breadth_first_exp(name_machine, start_state, accept_state, reject_state, transitions, input)
    
    #results
    print(f"Machine: {name_machine}")
    print(f"Input: {input}")
    print(f"Depth: {steps}")
    print(f"Total transitions: {total}")
    
    if check_accept:
        print(f"\nString accepted in {steps} steps")
        print("Accepting path:")
        for left, state, right in path:
            print(f"  {left} {state} {right}")
    else:
        print(f"\nString rejected in {steps} steps")

if __name__ == "__main__":
    main()