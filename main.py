import math
import time
import numpy as np

def calcLString(fixed_part, conj, n):
  SQL = fixed_part
  for j in range(n):
    i = j + 1
    SQL = SQL + str(i) + conj
  return len(SQL) - len(conj)

def calcL(f, g, n):
  L = f - g
  for j in range(n):
    i = j + 1
    L = L + g + math.floor(math.log10(i)) + 1
  return L

def calcL1(f, g, n):
  factN = math.factorial(n)
  L1 = f - g + n * (g + 1) + math.log10(factN)
  return math.floor(L1)

def calcL1Sterling(f, g, n):
  # https://en.wikipedia.org/wiki/Stirling%27s_approximation
  
  # math
  #factN = math.sqrt(2 * math.pi * n)  
  #factPow = math.pow(n / math.e, n) # overflow
  #factN = factN * factPow
  #L1 = f - g + n * (g + 1) + math.log10(factN)
  #L1 = math.floor(L1)
  
  # numpy
  #factN = np.longdouble(math.sqrt(2 * math.pi * n)) * np.power(np.longdouble(n / math.e), np.longdouble(n))
  #L1 = f - g + n * (g + 1) + np.log10(factN)
  #L1 = np.round(L1)
  
  logSterling = n * math.log10(n) - n + 1/2 * math.log10(2 * math.pi * n) + 1 / (12 * n) - 1 / (360 * n**3)
  L1 = f - g + n * (g + 1) + logSterling
  return math.floor(L1)

def calcL1Ramanujan(f, g, n):
  # https://en.wikipedia.org/wiki/Stirling%27s_approximation#Versions_suitable_for_calculators
  logRamanujan = n * math.log10(n) - n + 1/6 * (math.log10(8 * n**3 + 4 * n**2 + n + 1/30)) + 1/2 * math.log10(math.pi)
  L1 = f - g + n * (g + 1) + logRamanujan
  return math.floor(L1)

#
# Main
#

n_col = 100
conj = ','
fixed_part = 'SELECT NAME, DESCRIPTION, '
for col in range(n_col):
  fixed_part = fixed_part + 'V_' + str(col) + conj
fixed_part = fixed_part[:-len(conj)] + ' FROM TABLE WHERE ID IN ()'

f = len(fixed_part)
g = len(conj)
n = 100000

LString = -1
if True:
  start = time.time()
  LString = calcLString(fixed_part, conj, n)
  end = time.time()
  print("Time LString: ", (end-start) * 10**3, "ms")

L = -1  
if True:
  start = time.time()
  L = calcL(f, g, n)
  end = time.time()
  print("Time L: ", (end-start) * 10**3, "ms")

L1 = -1  
if True:
  start = time.time()
  L1 = calcL1(f, g, n)
  end = time.time()
  print("Time L1: ", (end-start) * 10**3, "ms")

L1Sterling = -1  
if True:
  start = time.time()
  L1Sterling = calcL1Sterling(f, g, n)
  end = time.time()
  print("Time L1Sterling: ", (end-start) * 10**3, "ms")

L1Ramanujan = -1  
if True:
  start = time.time()
  L1Ramanujan = calcL1Ramanujan(f, g, n)
  end = time.time()
  print("Time L1Ramanujan: ", (end-start) * 10**3, "ms")

print(' ')
print('n          : ' + f"{n:,}")
print('LString    : ' + f"{LString:,}")
print('L          : ' + f"{L:,}")
print('L1         : ' + f"{L1:,}")
print('L1Sterling : ' + f"{L1Sterling:,}")
print('L1Ramanujan: ' + f"{L1Ramanujan:,}")

