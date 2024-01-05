import sys
import base64

'''
with open('binall', 'wb') as file:
        for i in range(256):
            byte = bytes([i])
            file.write(byte)


i=1                         # argv[1] is the file name, used later.
for arg in sys.argv[1:] :   # Now see if there are other wishes for 
    if i==2:                #  where to start decoding and how far to go
        start = int(sys.argv[2])
    if i==3:
        quant = int(sys.argv[3])
    i += 1

with open(sys.argv[1], 'rb') as file:   # r=read b=binary
    data = file.read(start+quant)       # argument says how many bytes to read

for byte in data[start:] :              # process only from start onwards
    binbyte = '{:08b}'.format(byte)     # "decoding" is just about formatting
    
    hexbyte = '{:02X}'.format(byte)
    # hexbyte = hex(ord(byte))[2:].upper().zfill(2)  # another way 
    
    decbyte = str(byte)                 # str() is for human readability, not for calculation
    #decbyte = int(str(byte),10)        # these two can be used
    #decbyte = ord(byte)                # as numbers
    
    chrbyte = chr(byte) if byte >= 32 and byte <= 126 else ''
    
    print('binbyte: ', binbyte, 'hexbyte: ', hexbyte, 'decbyte: ', decbyte, 'chrbyte: ', chrbyte)



b64 = base64.b64encode(data[start:start+quant])
print('utf8: ', b64.decode('utf-8'))
'''
i=1                         # argv[1] is the file name, used later.
for arg in sys.argv[1:] :   # Now see if there are other wishes for 
    if i==2:                #  where to start decoding and how far to go
        start = int(sys.argv[2])
    if i==3:
        quant = int(sys.argv[3])
    i += 1

def state_absorb(state,block):
    state = [(int(str(block[i]),10)+state[i])%256 for i in range(block)]


def state_init(state, first_block):
    state = [(int(str(first_block[i%20]),10)+state[i])%256 for i in range(state)]

def sponge():

    start=0
    quant=10
    counter=1 # We know which block we currently get
    state = [0]*20

    with open(sys.argv[1], 'rb') as file:   # r=read b=binary
        while True:
            file.seek(start)
            block = file.read(quant)  

            # If the block is empty, we've reached the end of the file
            if not block:
                break
            if counter == 1:
                state_init(state, block)            
            state_absorb(state, block) # this way first block gets absorbed twice

            # Pad the last block with zeros if it's less than 10 bytes
            block = block.ljust(quant, b'\0')

            start+=quant
            counter+=1

 '''   

    