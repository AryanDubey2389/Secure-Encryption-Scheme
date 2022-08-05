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

class MAC:
    def __init__(self,message,length,key):
        self.length = length
        self.func_key = key
        self.message  = message
        # if length%4 or len(message) >= 2**(length/4):
        #     raise Exception("Please Check value of N or message length")
        # self.generate_key()


    def generate_key(self):
        for i in range(self.length):
            self.func_key+=str(random.randint(0,1))
    
    def generate_message_identifier(self,length):
        message_identifier = ""
        for i in range(length):
            message_identifier+=str(random.randint(0,1))
        return message_identifier

    def pad_sequence(self):
        append_val = 0
        message_length = bin(len(self.message))[2:].zfill(int(self.length/4))
        print(message_length)
        print(len(self.message))
        if (len(self.message))%(int(self.length/4)):
            append_val = int(self.length/4)-(len(self.message)%int(self.length/4))
        for i in range(append_val):
            self.message+='0'
        message_identifier = self.generate_message_identifier(int(self.length/4))
        slice_message = []
        start = 0
        # print("append_val = ",append_val)
        while start<len(self.message):
            # print("Start = ",start)
            slice_message.append(self.message[start:int(start+(self.length/4))])
            start = start + int(self.length/4)
        print(slice_message)
        tag_set = []
        for i in range(len(slice_message)):
            prf = PRF(int(self.func_key,2),len(message_identifier+message_length+bin(i+1)[2:].zfill(int(self.length/4))+slice_message[i]),message_identifier+message_length+bin(i+1)[2:].zfill(int(self.length/4))+slice_message[i])
            prf.find_function()
            tag_set.append(prf.output)
        # print("tag_set = ",tag_set)
        final_output = []
        final_output.append((self.func_key,message_identifier))
        for i in tag_set:
            final_output.append(i)
        # print(final_output)
        return final_output

    def verify_variable_length_message(self,encrypt,message):
        # print("insert")
        key_used = encrypt[0][0]
        message_identifier = encrypt[0][1]
        unpadded_length = bin(len(message))[2:].zfill(int(self.length/4))
        append_val = 0
        if len(message)%int(self.length/4):
            append_val = int(self.length/4)-(len(message)%int(self.length/4))
        for i in range(append_val):
            message+='0'
        # flag = 0
        if (len(message)/int(self.length/4))!=(len(encrypt)-1):
            return 0
        start = 0
        slice_message = []
        while start<len(self.message):
            # print("Start = ",start)
            slice_message.append(self.message[start:start+int(self.length/4)])
            start = start + int(self.length/4)
        print(slice_message)
        # print("Here")
        verify_tags = []
        for i in range(len(slice_message)):
            # prf = PRF(int(key_used,2),len(i),i)
            prf = PRF(int(key_used,2),len(message_identifier+unpadded_length+bin(i+1)[2:].zfill(int(self.length/4))+slice_message[i]),message_identifier+unpadded_length+bin(i+1)[2:].zfill(int(self.length/4))+slice_message[i])
            prf.find_function()
            verify_tags.append(prf.output)
        # print("verify tags = ",verify_tags)
        for i in range(1,len(encrypt)):
            if (encrypt[i] != verify_tags[i-1]):
                return 0
        return 1

    def encrypt(self):
        prf = PRF(int(self.func_key,2),self.length,self.message)
        prf.find_function()
        tag = prf.output
        encrypted_output = (tag,self.message,self.func_key)
        return encrypted_output

    def verify(self,encrypted):
        given_tag = encrypted[0]
        prf = PRF(int(encrypted[2],2),self.length,encrypted[1])
        prf.find_function()
        generated_tag = prf.output
        if given_tag==generated_tag:
            return 1
        else:
            return 0

class CPA:
    def __init__(self,message,length,key):
        self.length = length
        self.func_key = ""
        self.message  = message
        self.func_key = key
        # self.generate_key()

    def generate_key(self):
        for i in range(self.length):
            self.func_key+=str(random.randint(0,1))

    def change_key(self):
        self.func_key = ""
        for i in range(self.length):
            self.func_key+=str(random.randint(0,1))

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

class CCA:
    def __init__(self,length):
        self.length = length

    def generate_key(self):
        key_gen = ""
        for i in range(self.length):
            key_gen+=str(random.randint(0,1))
        return key_gen
    
    def assign_key(self):
        key_e = self.generate_key()
        key_m = self.generate_key()
        return key_e,key_m

    def encrypt(self,key_e,key_m,message):
        if(self.length!=len(message)):
            raise Exception("Message and key length doesn't match")
        cpa = CPA(int(message,2),len(message),key_e)
        cipher_value = cpa.encrypt()
        mac = MAC(message,len(message),key_m)
        tags = mac.encrypt()
        return (cipher_value,tags)

    def verify(self,tokens,key_e,key_m):
        cipher_input = tokens[0]
        tags = tokens[1]
        cpa = CPA(0,self.length,key_e)
        mac = MAC("",self.length,key_m)
        if mac.verify(tags):
            print("Decrypted Message is",cpa.decrypt(cipher_input))
        else:
            print("message has not been validated!!")

        





if __name__=="__main__":
    # message = int(generate_key(17),2)
    message = generate_key(17)
    print("Message value = ",int(message,2))
    # print("message = ",message)
    # print("converted = ",int(message,2))
    cca = CCA(len(message))
    key_e,key_m = cca.assign_key()
    print("key1 = {} key2 = {}".format(key_e,key_m))
    output = cca.encrypt(key_e,key_m,message)
    cca.verify(output,key_e,key_m)
    print("output = ",output)
