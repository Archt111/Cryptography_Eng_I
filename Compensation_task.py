# Name: My Nguyen
# ID:150545512


# !ChatGPT helps to find out and understands the steps the algorithms, and contributes to the debugging of the code 

# Brute force approach: Multiply each term of the first polynomial by each term of the second polynomial and then sum the results.
def polmul(f,g,p=0): 

    res = [0 for _ in range(len(f)+len(g)-1)]
    # Multiply each term of f with each term of g and add it to the result
    for i in range(len(f)):
        for j in range(len(g)):
            res[i+j] += f[i]*g[j] # As position n is equivalent to x^n

    if p!=0: res = [i%p for i in res]    
    return res

# Auxillary function
# Trim the leading zeros for the next 3 functions
def trim_zero(res):
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res
# Brute force but recursive approach 
# (link to algorithm: https://cse.hkust.edu.hk/mjg_lib/Classes/COMP3711H_Fall14/lectures/DandC_Multiplication_Handout.pdf)
def recursive_polmul(f, g, p):

    # Padding to make 2 functions have equal length
    if len(f) > len(g): g += [0] * (len(f) - len(g))
    else: f += [0] * (len(g) - len(f))

    # Base cases
    N = max(len(f), len(g))
    if N == 1: 
        if p!= 0: return [f[0]*g[0]%p]
        else: return [f[0]*g[0]]
    if not f or not g: return []

    # Split the polynomials into two parts, do multiply recursively for each 2 parts
    mid = N // 2
    f0, f1 = f[:mid], f[mid:]
    g0, g1 = g[:mid], g[mid:]

    U = recursive_polmul(f0, g0, p)
    V = recursive_polmul(f0, g1, p)
    W = recursive_polmul(f1, g0, p)
    Z = recursive_polmul(f1, g1, p)

    # Combine the results to res
    res = [0 for _ in range(2*N-1)]
    for i in range(len(U)):
        res[i] += U[i]
    for i in range(len(V)):
        res[i+mid] += V[i]
    for i in range(len(W)):
        res[i+mid] += W[i]
    for i in range(len(Z)):
        res[i+2*mid] += Z[i]

    if p!=0: res = [i%p for i in res]
    return trim_zero(res)

# Cyclic convolution approach: Slide/shift the coefficients of one fucntion and multiply them pair-wise with the other function
# then add the result together. Lastly, depending on n, the function wrap the result into1 max degree of n
def convol(f, g, n, p=0):

    res = [0 for _ in range(n)]
    # Cyclic convolution requires the polynomials f and g have length = n before wrapping
    f =  f + [0 for _ in range(n-len(f))]
    g = g + [0 for _ in range(n-len(g))]

    for i in range(0, n):
        for j in range(0, n):
            res[i] += f[(i - j) % n] * g[j]

    if p != 0: res = [i % p for i in res]
    return trim_zero(res)  

# Karatsuba approach: Another divide-and-conquer algorithm, very similar to the recursive in principle, but with one multiplication operation less
def karatsuba(f,g,p=0):
    # Padding to make 2 functions have equal length and of power of 2, otherwise algo fails with cases:
    # odd*odd, odd*even(not pow 2), even*even(not pow 2)
    N = max(len(f), len(g))
    deg_pow_2 = 1
    while deg_pow_2 < N: deg_pow_2*=2
    f += [0] * (deg_pow_2 - len(f))
    g += [0] * (deg_pow_2 - len(g))

    # Base cases
    N = len(f)
    if N == 1: 
        if p!= 0: return [f[0]*g[0]%p]
        else: return [f[0]*g[0]]
    if not f or not g: return []

    # Split the polynomials into two parts, do multiplication for 3 parts of the algorithm
    mid = N // 2
    f0, f1 = f[:mid], f[mid:]
    g0, g1 = g[:mid], g[mid:]

    # This is where it starts to differ from the brute-force approach
    low_part = karatsuba(f0,g0,p)
    high_part = karatsuba(f1, g1, p)
    # Padding is not required here since Python automatically handles it.
    # This input results of f0+f1 and g0+g1
    mid_part = karatsuba([sum(x) for x in zip(f0, f1)], [sum(x) for x in zip(g0, g1)], p)

    # Padding so that I can do part 3 - part1 - part2 with zip without using itertools
    max_length = max(len(low_part), len(mid_part), len(high_part))
    for part in [low_part, mid_part, high_part]:
        part += [0]* (max_length-len(part))

    # Combine the results to res
    res = [0 for _ in range(2*N-1)]
    for i in range(len(low_part)):
        res[i] += low_part[i]
    for i in range(len(mid_part)):
        res[i+mid] += (mid_part[i]-low_part[i]-high_part[i])
    for i in range(len(high_part)):
        res[i+2*mid] += high_part[i]

    if p!=0: res = [i%p for i in res]
    return trim_zero(res)

# Test functions
if __name__=="__main__":
    f = [int(item) for item in input("Enter f : ").split()]
    g = [int(item) for item in input("Enter g : ").split()]
    p = int(input("p: "))
    n = int(input("n: "))

    print(polmul(f,g,p))
    print(recursive_polmul(f,g,p))
    print(convol(f,g,n,p))
    print(karatsuba(f,g,p))

