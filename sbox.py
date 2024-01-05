# Modified AES-Keccak cipher by Ha My Nguyen
# !!! Note: 

import math as m
SNUM = 150545512
#SNUM =  123459678
#SNUM= 158509729
#SNUM=150233312
# Find the prime number by dividing up numbers up till its square root  
def find_next_prime(a_number):
    isPrime = False
    evaluating = a_number+1

    while not isPrime:       
        isPrime = True #Guilty till proven
        d_limit = m.floor(m.sqrt(evaluating)) 

        for divider in range(2,d_limit+1):
            if evaluating%divider==0:
                isPrime =False 
                break 

        # Evaluate in the outer loop after the for loop
        if not isPrime:
            evaluating+=1
    return evaluating

def traverse_int(a_number):
    # Digest the number in reverse as the string and turn it back to integer
    reversed_num = int(str(a_number)[::-1])
    return reversed_num

# Traverse and make a new list of values with opposite order
def traverse_list(a_list):
    traverse_ver = [a_list[i] for i in range(len(a_list) - 1, -1, -1)]
    return traverse_ver

# Partition the list into smaller sublists with size q
def get_sublists(a_list, q):
    # I learned from Chat-GPT that list comprehension magically handles 
    # the remainder number of values in a sublist without
    # going over the range
    sublists = [a_list[i:i + q] for i in range(0, len(a_list), q)]
    # sublists.append(a_list[len(sublists[0]):])
    return sublists

def s_box(SNUM):

    p1 = find_next_prime(SNUM%1000)  
    p2 = find_next_prime(p1)
    p1 = 11 if p1 < 11 else p1

    # The heck / gives me a float??
    q = int((SNUM % 100000) / 1000) %32 +2
    last_4d = SNUM%10000
    r1 = last_4d
    r2 = traverse_int(last_4d)
    print(p1, p2, q, r1, r2)

    A = [(p1*i+r1)%256 for i in range(256)]
    # Take each consecutive sublist of length q in reverse order
    B = [num for sublist in get_sublists(A,q) for num in traverse_list(sublist)]
    '''i= 0
    while i < (len(A)):
        print("A_o: ", A[i: i+15])
        print("A_l: ", traverse_list(A[i: i+15]))
        print("B_o: ", B[i:i+15])
        i += 15
    #print("B: ", B)
'''
    C = [None] * 256  # Initialize C as a list of 256 zeros
    for i in range(256):
        C[(p2 * i + r2) % 256] = B[i]

    return C

def showcycles(C):
    """
        input: a list of 256 distinct numbers permuting the set {0,1,...255}
        output: prints out cycles of that permutation
		
		See the comment in the end for two examples.
    """
    import sys			# used only for error exit
    if len(C) != 256:
        print("Incorrect length ", len(C), " of your list.")
        sys.exit()

    cycles = []     # start a list of cycles

    B = list(range(256)) + [9999]   # Append 9999 to serve as a sentinel in the list B
    i=0								#   which is used to mark (with -1)  those numbers
    while i<255:					#   that have already appeared in a cycle.
        while B[i]<0 : 		# find the next non-marked element in B
            i += 1			# (note: i++ does not work in Python)
        if i>255 : break    # all B has been marked; work done.
        start=C[B[i]]       # record start of a new cycle
        B[i]=-1             # mark the element in B
        next=start
        cycles += [[next]]  # append to cycles a new list consisting of a list of one element
        while C[next] != start :  	# if C does not return to 'start' yet
            B[next]=-1       		# mark the treated element in B
            next = C[next]   		# go forward in the cycle
            cycles[-1] += [next]    # append to the last list in cycles a new element

    cyclens=[]      # start a list of cycles with their lengths prepended
    for L in cycles:
        cyclens += [[len(L), L]]

    print("\nCycles, ordered by their length")
    cyclens.sort()      # sort with respect to cycle lengths
    for L in cyclens:
        print( L)

    print ("\nCycle lengths:")
    print([row[0] for row in cyclens])  # this is a "list comprehension". The 0th column.

if __name__=="__main__":
    C=s_box(SNUM)
    print(C)
    showcycles(C)


     