import random
class PRG:
    def __init__(self,prime_no,generator,bit_length,seed):
        self.prime_no = prime_no
        self.generator = generator
        self.bit_length = bit_length
        self.seed = seed
        self.generated_random_string = "" #raise exception for length n+1

    def modular_exponentiation(self,a,b,mod):
        result = 1
        while(b):
            if b%2:
                result = (result%mod*a%mod)%mod
            a = ((a%mod)*(a%mod))%mod
            b = b>>1
        return result
    
    def generate_random_bit(self):
        # n = self.bit_length
        val = self.seed
        for i in range(self.bit_length):
            num = self.modular_exponentiation(self.generator,val,self.prime_no)
            if num <= (self.prime_no-1)/2:
                self.generated_random_string+="1"
            else:
                self.generated_random_string+="0"
            val = num
        
        # self.generated_random_string = self.generated_random_string[::-1]

def decimalToBinary(n):
    return bin(n).replace("0b", "")

class PRF:
    def __init__(self,key,length,func_input):
        self.key = key
        self.length = length
        self.func_input = func_input
        # print("input is",self.func_input)
        self.output = ''
    
    def find_function(self):
        curr_val = self.key
        for i in self.func_input:
            prg = PRG(36389,4,2*self.length,curr_val)
            prg.generate_random_bit()
            output = prg.generated_random_string
            if i=='1':
                curr_val = int(output[:self.length],2)
            else:
                curr_val = int(output[self.length:],2)
        self.output = curr_val

def generate_key(n):
    key_temp = ""
    for i in range(n):
        key_temp+=str(random.randint(0,1))
    return key_temp


if __name__=="__main__":
    print(generate_key(17))
    prf = PRF(int(generate_key(17),2),17,generate_key(17))
    # prf = PRF(int("11110100110100100",2),17,"11110000110111100")
    prf.find_function()
    print(prf.output)
    print(type(prf.output))