class PRG:  # Blum Micali pseudo random generator
    def __init__(self,prime_no,generator,bit_length,seed):
        self.prime_no = prime_no
        self.generator = generator
        self.bit_length = bit_length
        self.seed = seed
        self.generated_random_string = ""

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

if __name__=="__main__":
    prg = PRG(36389,4,100,123123)
    prg.generate_random_bit()
    print(prg.generated_random_string)
    print(prg.generated_random_string.count('0')/len(prg.generated_random_string))


    