import random
class fixed_len_hash:
    def __init__(self,g,p):
        self.g = g
        self.p = p
        # self.q = q

    def select_key(self):
        x = random.randrange(1,self.p-1)
        self.h = x
    
    def set_key(self,val):
        self.h = val

    def fast_expo(self,a,b):
        res = 1
        while b:
            if b%2 == 1:
                # res = ((res%p)*(a%p))%p
                res = (res%self.p)*(a%self.p)
            b=b>>1
            # print("b = ",b)
            a = ((a%self.p)*(a%self.p))%self.p
            # a = ((a%p)*(a%p))%p
        return res
    
    def find_output(self,inp1,inp2):
        # print("Enter")
        val1 = self.fast_expo(self.h,inp2)
        val2 = self.fast_expo(self.g,inp1)
        return (val1%self.p*val2%self.p)%self.p
    
    def verify_test(self,inp1,inp2,h):
        val1 = self.fast_expo(h,inp2)
        val2 = self.fast_expo(self.g,inp1)
        return (val1%self.p*val2%self.p)%self.p

class merkle_damgard:

    def __init__(self,pad_len):
        self.pad_len = pad_len
        self.iv = generate_key(self.pad_len)


    def fill_value(self,message,pad_len):
        self.message = message
        self.pad_len = pad_len

    def generate_key(self):
        self.hash_func = fixed_len_hash(4,36389)
        self.hash_func.select_key()
        self.key_s = self.hash_func.h
    
    def set_key(self,val):
        self.hash_func.set_key(val)

    def pad_length(self):
        var = 0
        if len(self.message)%(self.pad_len):
            var = self.pad_len - len(self.message)%(self.pad_len)
        for i in range(var):
            self.message+="0"
        start = 0
        string_vec = []
        temp = ""
        for i in self.message:
            temp+=i
            start+=1
            if(start==self.pad_len):
                string_vec.append(temp)
                start = 0
                temp = ""
        # print(string_vec)
        return string_vec
    
    def chain_prop(self,key_val):
        arr = self.pad_length()
        # hash_func = fixed_len_hash(4,36389)
        # hash_func.select_key()
        hash_func = self.hash_func
        iv = self.iv
        for i in range(len(arr)):
            output = bin(hash_func.verify_test(int(iv,2),int(arr[i],2),key_val))[2:].zfill(self.pad_len)
            iv = output
        return output


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

class HMAC:
    def __init__(self,message,length):
        self.length = length
        self.func_key = ""
        self.message  = message
        self.opad = self.generate_message_identifier(24)
        self.ipad = self.generate_message_identifier(24)
        self.generate_key()
        self.hash_func = ""

    def generate_key(self):
        for i in range(24):
            self.func_key+=str(random.randint(0,1))
        merkle_damgard_hash = merkle_damgard(16)
        self.hash_func = merkle_damgard_hash
        self.hash_func.generate_key()
        return (self.func_key,self.hash_func.key_s)
    
    def generate_message_identifier(self,length):
        message_identifier = ""
        for i in range(length):
            message_identifier+=str(random.randint(0,1))
        return message_identifier

    def encrypt(self,key_set,message):
        hash_key = key_set[1]
        mac_k = key_set[0]
        # print("mack = ",mac_k)
        self.hash_func.set_key(hash_key)
        str1 = bin((int(mac_k,2)^int(self.opad,2)))[2:]
        str2 = bin((int(mac_k,2))^int(self.ipad,2))[2:]+message
        self.hash_func.fill_value(str2,16)
        str3 = self.hash_func.chain_prop(hash_key)
        self.hash_func.fill_value(str1+str3,16)
        tag_t = self.hash_func.chain_prop(hash_key)
        # print("str1 = {}. str2 = {} str3 = {}".format(str1,str2,str3))
        return tag_t
        # tag_t = self.hash.fill_value()

      
    def verify(self,key_set,tag,message):
        hash_key = key_set[1]
        mac_k = key_set[0]
        # print("mack = ",mac_k)
        self.hash_func.set_key(hash_key)
        str1 = bin((int(mac_k,2)^int(self.opad,2)))[2:]
        str2 = bin((int(mac_k,2))^int(self.ipad,2))[2:]+message
        self.hash_func.fill_value(str2,16)
        str3 = self.hash_func.chain_prop(hash_key)
        self.hash_func.fill_value(str1+str3,16)
        tag_t = self.hash_func.chain_prop(hash_key)
        # print("tag_t = {}, tag = {}".format(len(tag_t),len(tag)))
        if tag_t==tag:
            return 1
        else:
            return 0

if __name__=="__main__":
    # message = int(generate_key(17),2)
    message = generate_key(55)
    hmac = HMAC("",16)
    key_set = hmac.generate_key()
    tag = hmac.encrypt(key_set,message)
    print("generated key set(k,s) = ",key_set)
    print("generated tag = ",tag)
    # tag2= hmac.encrypt(key_set,message)
    # print("tag1 = {} , tag2 = {}".format(tag,tag2))
    # print("tag = ",tag)
    print("verifying message")
    print(hmac.verify(key_set,tag,message))
    
    # decrypt_value = cpa.decrypt(cipher_value) #Decrypting the message
    # print("decrypt_valye = ",decrypt_value)
    