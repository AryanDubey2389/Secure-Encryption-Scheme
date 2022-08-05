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

if __name__ =="__main__":
    hash_func = fixed_len_hash(4,36389)
    hash_func.select_key()
    # print("Hey ya")
    print(len(bin(36389)[2:]))
    val1 = random.randrange(0,36387)
    val2 = random.randrange(0,36387)
    print("input1 = {} input2 = {}".format(val1,val2))
    print("Total input bit = {}".format(len(bin(val1)[2:])+len(bin(val2)[2:])))
    # print(len(bin(val1)[2:])+len(bin(val2)[2:]))
    ans = hash_func.find_output(val1,val2)
    print("output = {}".format(ans))
    print("Output bit = {}".format(len(bin(ans)[2:])))
    print(len(bin(ans)[2:]))
    # print(hash_func.find_output(random.randrange(0,36387),random.randrange(0,36387)))
    

