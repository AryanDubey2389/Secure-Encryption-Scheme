import random

class fixed_len_hash:
    def __init__(self,g,p):
        self.g = g
        self.p = p
        # self.q = q

    def select_key(self):
        x = random.randrange(1,self.p-1)
        self.h = x

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

class merkle_damgard:
    def __init__(self,message,pad_len):
        self.message = message
        self.pad_len = pad_len
        self.iv = generate_key(self.pad_len)
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
        print(string_vec)
        return string_vec
    
    def chain_prop(self):
        arr = self.pad_length()
        hash_func = fixed_len_hash(4,36389)
        hash_func.select_key()
        iv = self.iv
        for i in range(len(arr)):
            output = bin(hash_func.find_output(int(iv,2),int(arr[i],2)))[2:].zfill(self.pad_len)
            iv = output
        return output



def generate_key(n):
    key_temp = ""
    for i in range(n):
        key_temp+=str(random.randint(0,1))
    # print("key generated = ",key_temp)
    return key_temp


if __name__ =="__main__":
    hash_func = fixed_len_hash(4,36389)
    hash_func.select_key()
    # print("Hey ya")
    message = generate_key(100)
    print("message = ",message)
    print(len(bin(36389)[2:]))
    # val1 = random.randrange(0,36387)
    # val2 = random.randrange(0,36387)
    # print(len(bin(val1)[2:])+len(bin(val2)[2:]))
    # ans = hash_func.find_output(val1,val2)
    # print(len(bin(ans)[2:]))
    # print(hash_func.find_output(random.randrange(0,36387),random.randrange(0,36387)))
    merkle_damgard_hash = merkle_damgard(message,16)
    # merkle_damgard_hash.pad_length()
    print(merkle_damgard_hash.chain_prop())

    

