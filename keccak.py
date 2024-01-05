from bitarray import bitarray
import numpy as np

# Chi constant table 
CHI_TABLE = np.array([[1, 0, 0, 1, 1], 
                      [1, 1, 0, 0, 1],  
                      [1, 1, 1, 0, 0],
                      [0, 1, 1, 1, 0], 
                      [0, 0, 1, 1, 1]])

def chi(x):
  """Implement chi nonlinear step"""

  binx = bin(x)[2:].zfill(64) # to binary string

  result = 0
  for i in range(5):
    parity = binx[i*16:i*16+16].count('1') % 2 
    result ^= CHI_TABLE[i, parity] << (64*i)

  return result

# Keccak parameters
WIDTH = 1600
LANE_SIZE = 25 
LANES = 64


RC = [0x0000000000000001, 0x0000000000008082, 0x800000000000808a, 0x8000000080008000,
          0x000000000000808b, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
          0x000000000000008a, 0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
          0x000000008000808b, 0x800000000000008b, 0x8000000000008089, 0x8000000000008003,
          0x8000000000008002, 0x8000000000000080, 0x000000000000800a, 0x800000008000000a,
          0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008]


def keccak_theta(state_ba):

  # Get length of input bitarray
  state_length = len(state_ba)

  # Calculate rows and cols 
  rows = 5
  cols = state_length // rows  

  # Reshape to rows x cols
  state_matrix = np.array(list(state_ba)).reshape((rows,cols))

  # Rest of theta function

  C = bitarray(5)
  D = bitarray(5)

  for x in range(5):
    # Calculate C values 
    C[x] = state_matrix[x,0] ^ state_matrix[x,1] ^ state_matrix[x,2] ^ state_matrix[x,3] ^ state_matrix[x,4]

  for x in range(5):   
    # Calculate D values
    D[x] = C[(x - 1) % 5] ^ np.roll(C[(x + 1) % 5], 1) 

  for x in range(5):
    for y in range(5):  
      # Perform theta step  
      state_matrix[x,y] ^= D[x]
  
    # Reshape output 
  new_state_ba = bitarray()
  state_matrix.tofile(new_state_ba)

  return new_state_ba
    

def keccak_rho_pi(state_ba):

  state_matrix = np.array(list(state_ba)).reshape((5,5))

  for x in range(5):
    # Rotation step
    col = state_matrix[:,x]
    state_matrix[:,x] = np.roll(col, -x)

  # Permutation step  
  state_matrix = state_matrix[[0,1,3,2,4],:]

  new_state_ba = bitarray()
  new_state_ba.fromlist(state_matrix.ravel())

  return new_state_ba

def keccak_chi(state_ba):

  state_matrix = np.array(list(state_ba)).reshape((5,5))

  for x in range(5):
    for y in range(5): 
      # Non-linear chi step  
      state_matrix[x,y] = chi(state_matrix[x,y])

  new_state_ba = bitarray()
  new_state_ba.fromlist(state_matrix.ravel())

  return new_state_ba

def keccak_iota(state_ba, rc):

  state_matrix = np.array(list(state_ba)).reshape((5,5))

  # XOR RC value  
  state_matrix[0,0] ^= rc

  new_state_ba = bitarray()
  new_state_ba.fromlist(state_matrix.ravel())

  return new_state_ba

def keccak_round(state_ba):

  state_ba = keccak_theta(state_ba)
  state_ba = keccak_rho_pi(state_ba)
  state_ba = keccak_chi(state_ba)
  state_ba = keccak_iota(state_ba, RC[0])

  return state_ba

# Pad input state to full lane size
FULL_SIZE = LANES * LANE_SIZE
padding = FULL_SIZE - WIDTH
initial_state = bitarray(WIDTH) + bitarray(padding)  

# Get padded state as bitarray 
state_ba = keccak_round(initial_state)

# Get length after padding
state_length = len(state_ba) 

# Calculate number of lanes
lanes = state_length // LANE_SIZE 

# Reshape to 2D array 
state_matrix = np.array(list(state_ba)).reshape((-1, lanes))

# Extract A[0,0]
A_00 = state_matrix[0,0]

print(f"A[0,0]: {hex(A_00)}")
