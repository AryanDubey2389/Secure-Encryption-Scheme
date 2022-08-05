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
    # print("key generated = ",key_temp)
    return key_temp

class CPA:
    def __init__(self,message,length):
        self.length = length
        self.func_key = ""
        self.message  = message
        self.generate_key()

    def generate_key(self):
        for i in range(self.length):
            self.func_key+=str(random.randint(0,1))

    # def change_key(self):
    #     self.func_key = ""
    #     for i in range(self.length):
    #         self.func_key+=str(random.randint(0,1))

    def generate_r(self):
        r = ""
        for i in range(self.length):
            r+=str(random.randint(0,1))
        return r

    def encrypt(self):
        r = self.generate_r()
        # print("generated r = ",r)
        prf = PRF(int(self.func_key,2),self.length,r)
        prf.find_function()
        # print("output encrypt = ",prf.output)
        cipher = prf.output^self.message
        encrypted_output = (cipher,r)
        return encrypted_output

    def decrypt(self,encrypted):
        r = encrypted[1]
        cipher_value = encrypted[0]
        prf = PRF(int(self.func_key,2),self.length,r)
        prf.find_function()
        decrypted_message = cipher_value^prf.output
        return decrypted_message

if __name__=="__main__":
    message = int(generate_key(17),2)
    print("message = ",message)
    cpa = CPA(message,17)
    cipher_value = cpa.encrypt() #Encrypting the message
    # cipher_value = (47227, '11110100000011101')
    print(cipher_value)    
    decrypt_value = cpa.decrypt(cipher_value) #Decrypting the message
    print("decrypt_valye = ",decrypt_value)
    