from pwn import *
from Crypto.Random import get_random_bytes
import base64


# fairly standard padding oracle attack
#
# the goal is to xor the ticket so that, decrypted, it reads   
#
#     ...junk.. "numbers:,jackpot1,jackpot2,...jackpot5" "\x01"
#                <--- at least 49 chars ---------------------->
#                     theoretically could be less, but chall has mean rng
#
# there is a deliberate bug in jackpot verification, so you need that extra comma
# 'n' in 'numbers' falls onto block 2, so 1st and 2nd plaintext blocks get scrambled in last step


def connect():
   while True: # wait for sufficiently short jackpot numbers (otherwise success chance too low)
      r = remote("127.0.0.1", 25002)
      r.recvuntil("raffle ticket:\n")
      ticket64 = r.recvuntil("\n").strip()
      ticket = base64.b64decode(ticket64)

      r.recvuntil("numbers are:\n")
      numbers = r.recvuntil("\n").strip()
      for c in b"[] ":
         numbers = numbers.replace(bytes([c]), b"")
      if len(numbers) <= 40:   return r, ticket, numbers
      r.close()
      #sys.stdout.write(".")


def redeem(msg):
   msg64 = base64.b64encode(msg)
   r.recvuntil("Redeem a ticket:\n")
   r.send(msg64 + b"\n")
   while True:
      in1 = r.recvuntil("\n")
      if b"invalid" in in1:      return 0
      if b"did not win" in in1:  return 1
      if b"bctf" in in1:
         print(in1)   # print flag line
         exit(0)


def xor(msg, pos, otp):   # xor a segment in msg at pos
   n = len(otp)
   xorred = bytes( [ msg[pos + i] ^ otp[i]   for i in range(n)]  )
   return msg[:pos] + xorred + msg[(pos + n):]



# get viable chars prepending a given otp at end of block
def getChars(ticket0, start, otp):
   good = []
   nopts = 2  if  otp == b""  else   1  # for last char: at most 2 options, for rest: 1 option
   for b in range(256):
      bb = bytes([ b ])
      ticket = xor(ticket0, start - len(otp) - 1, bb + otp)[:(start + 16)]
      code = redeem(ticket)
      if code == 1: 
         good.append(b)
         if len(good) == nopts: break
   return good


def getBlock(ticket0, start):  # extract a block of plaintext
   # get options for char at end of block
   good = getChars(ticket0, start, b"")
   if good == []:  # no solution
      print("bad")
      return b""
   # try now each option, assuming it gives 0x01
   print(f"good={good}")
   for g in good:
      ptxt = bytes([g ^ 0x01])
      otp = bytes([g ^ 0x01 ^ 0x02])
      for pos in range(2, 17):
         good = getChars(ticket0, start, otp)
         if len(good) != 1: break
         b = good[0]
         bb = bytes([b])
         otp = bb + otp
         ptxt = bytes([b ^ pos]) + ptxt
         otp = bytes( [ v ^ pos ^ (pos + 1)  for v in otp] )
      if pos == 16: return ptxt
   return ptxt



r, ticket0, lst = connect()
print(f"jackpot nums: {lst}")

n0 = len(ticket0)
print(f"len(ticket0): {n0}")

code = redeem(ticket0)
print(f"redeem(original ticket)= {code}")



goal = b"numbers:" + lst + b"\x01"
Ngoal = len(goal)
print(f"Ngoal={Ngoal}, goal={goal}")

# mutate ticket until we get 3 blocks of goal (last 48 chars)
for i in range(3):
   ptxt0 = getBlock(ticket0, n0 - 16 * (i + 1))
   goal0 = goal[Ngoal - 16*(i+1):Ngoal - 16*i]
   print(i, goal0, ptxt0)
   ticket0 = xor(ticket0, n0 - 16 * (i + 2), xor(ptxt0, 0, goal0))
   print( redeem(ticket0) )


# do that first char by stochastically changing previous block
while True:
   s = get_random_bytes(4)
   ticket = xor(ticket0, n0 - 68, s)
   redeem(ticket)   # terminates if jackpot found
   sys.stdout.write(".")
