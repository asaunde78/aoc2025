
import re 


main_pattern = r"^\[(.+)\] ((?:(?:\(\d+(?:,\d+)*\)) )+){(\d+(?:,\d+)*)}$"
button_pattern = r"(?:(?:\((\d+(?:,\d+)*)\)))"


def apply_button(start, button_tuple):
    output = list(start).copy()
    for ind in button_tuple:
        output[ind] -= 1
    return tuple(output) 
def all_zeros(li):
    # print("list: ", li)
    for i in li:
        if i != 0:
            return False 
    return True
def any_less(li):
    for i in li:
        if i < 0:
            return True 
    False
class State():
    def __init__(self, text_input):
        self.state = []
        for i, val in enumerate(text_input.split(",")):
            self.state.append( int(val) )
        self.state = tuple(self.state)
    def __repr__(self):
        return str(self)
    def __str__(self):
        return "".join(list(map(lambda x: "." if x else "#", self.state)))
    def apply(self, button_tuple):
        
        return apply_button(self.state, button_tuple)
    def is_corrected(self):
        return all(self.state)
    def get_state(self):
        return self.state
    def __eq__(self, other):
        return self.state == other.state 
    def __hash__(self):
        return self.state.__hash__()
class Machine():
    def __init__(self, line):
        result = re.search(main_pattern, line)
        self.final_indicator = result.group(1)
        buttons = re.findall(button_pattern, result.group(2))
        self.buttons = []
        for button in buttons:
            b = button.split(",")
            b = [int(i) for i in b]
            b = tuple(b)
            self.buttons.append(b)
        self.joltages = result.group(3)
        self.state =  State(self.joltages)
        print(self.state)
    def apply(self, button_index):
        return self.state.apply(self.buttons[button_index])
    def search(self, starting):
        new_state = starting
        path = []
        depth = 0
        states = {starting:[]}
        
        while True:
            cpy = states.copy()
            for state, path_to in cpy.items():
                for button in self.buttons:
                    current_path = path_to + [button]
                    current_state = apply_button(state, button)
                    print(current_state)
                    if current_state in states:
                        continue 
                    if any_less(current_state):
                        continue 
                    if all_zeros(current_state):
                        # print("BUWAIBDAUIW")
                        print("current path", current_path)
                        return current_path
                    if current_state in states:
                        previous_path = states[current_state]
                        if len(previous_path) > len(current_path):
                            states[current_state] = current_path 
                    states[current_state] = current_path 
            
                    
                
                
with open("test.txt", "r") as f:
    lines = f.readlines()
    total = 0
    for line in lines[:]:
        m = Machine(line)
        # print("machine: ", m)
        print(m.state.get_state())
        l = len(m.search(m.state.get_state()))
        total += l 
    print("Total: ", total)
  
  