from helpers import NewDial as NewDial
class Dial():
    def __init__(self, start):
        self.value = start 
        self.count = 0
        self.landed_on_zero = 0
    def right(self, amount):
        print("moving right:  ", amount)
        self.value += amount 
        self.correct()
    def left(self, amount):
        print("moving left:  ", amount)
        self.value -= amount 
        self.correct()
    def read(self, _input):
        op = _input[:1]
        # print(op)
        val = int(_input[1:])
        return op, val

    def run(self, _input):
        op, val = self.read(_input)
        self.run_op(op, val)
    def run_op(self, op, val):
        # print(op)
        if op == "L":
            self.left(val)
        if op == "R":
            self.right(val)
        if op!="R" and op!="L":
            print("WHAT")
    def correct(self):
        left = 0
        right = 0
        while self.value < 0:
            self.value += 100
            left += 1
        while self.value > 99:
            right += 1
            self.value -= 100
        
        if(self.value == 0):
            self.count += 1
        
        # print("new value: ", self.value)
    


def main():
    # first problem  solution 
    # d = Dial(50)
    # with open("test.txt", "r") as f:
    #     file = f.readlines()
    #     for line in file:
    #         inp = line.strip()
    #         d.run(inp)
    #     print(d.count)

    # d = NewDial(99)
    
    # d.handle_turn(1001)
    # print(d.count, d.value)

    d=NewDial(50)
    with open("input.txt", "r") as f:
        file = f.readlines()
        count = 0
        for line in file:
            inp = line.strip()
            print("--- new input --- ", inp)
            d.handle_turn(d.parse(inp))
            print("\t-->new value: <", d.value, d.get_val(), ">")
            
        print(d.landed_on_zero)
        print(d.count)
            
        


if __name__ == "__main__":
    main()


