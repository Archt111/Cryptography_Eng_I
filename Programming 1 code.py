import string

PERSONAL_CODE = "925ec0e6647de953b8f6d43a"
ROUNDS=16

def upper_check(a_string):
    # Turn only characters to numbers without using upper
    # prep_str = ""
    if len(a_string) != 16:
        return False
    for c in a_string:
        if c not in string.punctuation and not c.isdigit() and c != ' ' and not c.isupper():
                return False
                # c = chr(ord(c) - 32)
            # prep_str += c
    return True

def text_2_no(text):
    c_as_num =[ord(c1)-65 for c1 in text]
    return c_as_num

def no_2_text(num_list):
    text = "".join([chr(n1+65) for n1 in num_list])
    return text

def hex_2_bin(hex_str):
    pcode = []
    for hc in hex_str:
        hex_as_bin_str = bin(int(hc, 16))[2:].zfill(4)
        bin_list = [int(bit) for bit in hex_as_bin_str]
        pcode.append(bin_list)
    return pcode
    
def padding_16(num_list):
    multiplier = 16 - len(num_list)%16
    num_list.extend([0]*multiplier)

def matrix_multiplication(pcode,key):
    # 8x4 * 4x4 = 8x4
    if len(pcode[0]) != len(key):
        print("Incompatible matrix sizes")

    res=[]
    for row1 in range(len(pcode)):
        res.append([]) 
        for col2 in range(len(key[0])):
            res[row1].append(0)
            for col1 in range(len(pcode[0])):
                res[row1][col2] += (pcode[row1][col1] * key[col1][col2])%26
            res[row1][col2] %= 26

    return res            

def get_Mult():
    return [int(PERSONAL_CODE[hc], 16)+1 for hc in range(16)]

def key_schedule(key_str):
    """
    if not (len(hexa_str)==8 and all(h in "0123456789abcdef" for h in hexa_str) and upper_check(cap_str)):
        print("Input is not valid")
        return False
    """     
    mat = hex_2_bin(PERSONAL_CODE[16:])
    key_array = [ord(x) - 65 for x in key_str]
    key  = [key_array[i:i+4] for i in range(0, 16, 4)]

    return matrix_multiplication(mat,key)


def encryption(num_list, key_sched, Mult):
    num_list2 =[]
    i = 0
    while i+16 <= len(num_list):
        block_16 = num_list[i:(i+16)]
        left_half = block_16[:8]
        right_half = block_16[8:]
        
        for round in range(ROUNDS):
            print(f"index: {str(round)}\nleft:{str(no_2_text(left_half))}\nright:{str(no_2_text(right_half))}")
            column = round%4
            round_key = [row[column] for row in key_sched]
            medium =[]
            medium = [(left_half[i]+(Mult[round]*right_half[i] + round_key[i]))%26 for i in range(len(left_half))]

            # medium = [(x+round*y)%26 for x,y in zip(left_half,right_half)]
            left_half = right_half
            right_half = medium

        num_list2.extend(right_half + left_half)
        i += 16
    return num_list2

def feistel_network(plain,key):
    if not (upper_check(plain) and upper_check(key)):
        print("Invalid input, please only type 16 captial characters for each text")
        return
    
    num_list = text_2_no(plain)
    if len(num_list)%16!=0:
        padding_16(num_list)
    
    key_sched = key_schedule(key)
    Mult = get_Mult()
    num_list2 = encryption(num_list,key_sched, Mult)

    return no_2_text(num_list2)

if __name__=="__main__":
    
    plain = input("Enter plaintext: ")
    key = input("Enter keytext: ")
    print(feistel_network(plain,key))



    