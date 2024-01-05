# Modified AES-Keccak cipher by Ha My Nguyen
# SNUM = '---'

import sys
L = 5
################# File reading #################
i=1                         # argv[1] is the file name, used later.
for arg in sys.argv[1:] :   
    if i==2:                #  length of a block in byte
        quant = int(sys.argv[2])
    i += 1


def AES_Keccak(file_name, quant, outQ, S, Sbox, SNUM):
    start = 0 # This is where we start the block each iteration
    counter = 1 # We know which block we currently get
    full = True
    with open(file_name, 'rb') as file:   # r=read b=binary
        while True:

            file.seek(start)
            block = file.read(quant)  # read 'quant' bytes from the current position

            # If the block is empty, we've reached the end of the file
            if not block:
                break

            # turn bytes of each block into integers
            dec_block = [int(byte)%256 for byte in block] 


            if counter == 1:
                for i in range(len(dec_block)):
                    S[i//5][i%5] = (S[i//5][i%5] + dec_block[i%len(dec_block)]) % 256

            else:
                # Pad the last block with zeros if it's less than 10 bytes
                dec_block += [0] * (quant - len(dec_block))
                
                # Insert each input block as 10 (or fewer) integers to the first two rows of S
                for i in range(quant):
                    S[i//5][i%5] = (S[i//5][i%5] + dec_block[i]) % 256

        
            modified_AES(S, Sbox, SNUM)

            # Update the numbers to continue go thru all the blocks of the file
            start += quant
            counter += 1

    output = []
    if full:
        # Iteratively take the first 2 rows of S into output
        while len(output) < outQ:
            output.extend([S[i][j] for i in range(2) for j in range(L)])
            modified_AES(S, Sbox, SNUM)

    return bytearray(output[:outQ]).hex()

############## AES operations ####################

# SubBytes
def SubBytes(S,Sbox):
    # Substitute bytes in S with corresponding values in Sbox.
    for i in range(L):
        for j in range(L):
            S[i][j] = Sbox[S[i][j]]

# ShiftRows
def ShiftRows(S, SNUM):
    # Take 4 last chars and index backwards
    steps = [int(c) for c in SNUM[-4:][::-1]]

    # From row 1 to 4, we rotate left with steps(row) (1):
    for row in range(1,L):
        # If shift = 0, shift = 1, else do as (1)
        shift = 1 if steps[row-1]%5==0 else steps[row-1]%5 
        S[row] = S[row][shift:] + S[row][:shift]

# Matrix multiplication, taken from assignment 1 with State and Transformation matrix
def matrix_multiplication(S,T):
    # 5x5 * 5x5 
    res=[]
    for row1 in range(len(S)):
        res.append([]) 
        for col2 in range(len(T[0])):
            res[row1].append(0)
            for col1 in range(len(S[0])):
                res[row1][col2] += (S[row1][col1] * T[col1][col2])%256
            res[row1][col2] %= 256

    return res

# MixColumns
def MixColumns(S, SNUM):
    # Create transformation matrix from SNUM
    T=[[0]*5 for _ in range(L)]
    for i in range(L*L):
        T[i//5][i%5] += int(SNUM[i%9])

    S = matrix_multiplication(T, S)

def modified_AES(S, Sbox, SNUM):
    for _ in range(6):
        SubBytes(S, Sbox)
        ShiftRows(S, SNUM)
        MixColumns(S, SNUM)
    
if __name__== "__main__": 
    # From exercise 5, C = Sbox
    Sbox=[243, 228, 213, 180, 165, 136, 103, 88, 55, 40, 25, 234, 219, 204, 171, 
        156, 141, 94, 79, 46, 31, 16, 239, 210, 195, 162, 147, 132, 85, 70, 37, 
        22, 7, 230, 201, 186, 153, 138, 123, 90, 61, 28, 13, 254, 221, 192, 
        177, 144, 129, 114, 81, 52, 19, 4, 245, 212, 197, 168, 135, 120, 
        105, 72, 43, 10, 251, 236, 203, 188, 159, 126, 111, 96, 63, 48, 1, 
        242, 227, 194, 179, 150, 117, 102, 87, 54, 39, 248, 233, 218, 185, 170, 
        155, 108, 93, 78, 45, 30, 127, 224, 209, 176, 161, 146, 99, 84, 69, 36, 
        21, 6, 215, 200, 167, 152, 137, 104, 75, 60, 27, 12, 253, 206, 191, 158, 
        143, 128, 95, 66, 51, 18, 3, 244, 211, 182, 149, 134, 119, 86, 57, 42, 9, 
        250, 235, 202, 173, 140, 125, 110, 77, 62, 33, 0, 241, 226, 193, 164, 131, 
        116, 101, 68, 53, 24, 247, 232, 217, 184, 169, 122, 107, 92, 59, 44, 15, 238, 
        223, 208, 175, 160, 113, 98, 83, 50, 35, 20, 229, 214, 199, 166, 151, 118, 
        89, 74, 41, 26, 11, 220, 205, 190, 157, 142, 109, 80, 65, 32, 17, 2, 225, 
        196, 181, 148, 133, 100, 71, 56, 23, 8, 249, 216, 187, 172, 139, 124, 91, 
        76, 47, 14, 255, 240, 207, 178, 163, 130, 115, 82, 67, 38, 5, 246, 231, 198, 
        183, 154, 121, 106, 73, 58, 29, 252, 237, 222, 189, 174, 145, 112, 97, 64, 49, 34]


    # Initiate State and other constants
    S = [ [0]*5 for _ in range(5)]
    L = len(S)
    SNUM = '150545512'

    plaintext = input('what to be hashed: ')
    #plaintext = plaintext.replace(' ','')
    with open('binall', 'wb') as file:
        for i in plaintext:
            file.write(bytes(i,'utf-8'))

    quant = 10
    outQ = 25
    print(AES_Keccak('binall',quant, outQ, S, Sbox, SNUM))
