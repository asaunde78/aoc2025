class Dial():
    def __init__(self, start):
        self.value = start 
        self.count = 0
        self.landed_on_zero = 0
    
    def set_zero(self):
        self.value = 0
        self.count += 1
        print("passing zero")
    def inc_landed(self):
        self.landed_on_zero += 1
        print("landed on zero!")
    def set_max(self):
        self.value = 100

        self.count += 1
        print("passing max")
        
    def parse(self, _input):
        op = _input[:1]
        # print(op)
        val = int(_input[1:])
        if(op == "L"):
            return -val
        if(op == "R"):
            return val
    def handle_turn(self, amount):
        
        if(amount == 0):
            return
        # print("running amount:", amount)
        if(amount > 0):
            top_diff = 100 - self.value
            if (amount < top_diff):
                self.value += amount 
                if(self.value == 0):
                    self.inc_landed()
            else:
                self.set_zero()
                self.handle_turn( amount - (top_diff))
            return
        if(amount < 0):
            bot_diff = self.value
            if( abs(amount) <= bot_diff):
                self.value += amount
                if(self.value == 0):
                    self.inc_landed()
            else:
                self.set_max()
                self.handle_turn(amount + bot_diff)
            return
class NewDial():
    def __init__(self, start):
        self.value = start 
        self.count = 0
        self.landed_on_zero = 0
    
    def parse(self, _input):
        op = _input[:1]
        # print(op)
        val = int(_input[1:])
        if(op == "L"):
            return -val
        if(op == "R"):
            return val
    def get_val(self):
        return self.quick(self.value)
    def quick(self, val):
        return val % 100
    def handle_turn(self, amount):
        begin = self.value 
        self.value += amount
        

        start = begin 
        end = self.value


        if(begin > self.value):
            start = self.value
            end = begin
        
            
        count = 0
        # print("se", start,end)
        for i in range(start, end):
            # print(i)
            if((i % 100 ) == 0 and i!= start and i!=end):
                print("val: ", i)
                count += 1
        self.count += count
        # print("count for range:", count)
        if(self.value % 100 == 0):
            self.count += 1
        # print((self.value % 100))