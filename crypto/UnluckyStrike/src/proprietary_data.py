from Crypto.Random import get_random_bytes as grb
from Crypto.Random.random import randint


FLAG = open("flag.txt").read().strip()

Nballs = 5


# hack the rolls (eliminate too small result)

Ncalls, totalDigits = 0, 0

def get_random_bytes(n):
   global Ncalls, totalDigits
   Ncalls += 1
   # call 1: key
   # calls 2 through Nballs: ticket
   # call (Nballs+1): IV
   if Ncalls <= Nballs + 1: return grb(n)
   # calls (Nballs+2) through (2Nballs+1): jackpot
   # ensure total number digits of with n rolls remaining is at least 36 - 8*n
   else:
      while True:   # n = 2 * Nballs + 1 - Ncalls
         v = grb(3)
         l = len( str(int.from_bytes(v, "big")) )
         if totalDigits + l >= 36 -  8 * (2 * Nballs + 1 - Ncalls): break 
      totalDigits += l
      return v


# hack the JOKER ending to some corner case

class Joker:
   def __init__(self, msg):
      self.msg = msg

   def __radd__(self, s):
      ret = s + self.msg           # max 69 bytes (min 57, theoretically)
      ret += b" "*(66 - len(ret))  # make it 5 blocks
      padlen = 16 - (len(ret) & 0xf)  # this is 11-14
      s = randint(4, padlen - 1)
      sbyte = bytes([s])
      return ret + sbyte * (padlen - 1)



JOKER = Joker(b"-1,SUPER_JACKPOT_LOTTERY_SECRET_SAUCE")




