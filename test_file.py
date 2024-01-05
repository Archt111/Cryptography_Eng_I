import sys

plaintext = input('what to be hashed: ')
#plaintext = plaintext.replace(' ','')
with open('binall', 'wb') as file:
    for i in plaintext:
        file.write(bytes(i,'utf-8'))

