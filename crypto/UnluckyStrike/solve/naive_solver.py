from pwn import *
from Crypto.Random import get_random_bytes
import base64


# fairly standard padding oracle attack
#
# the goal is to xor the ticket so that, decrypted, it reads   
#
#     ...junk.. "numbers:jackpot1,jackpot2,...jackpot5" "\x01"
#                <--- at least 49 chars ---------------------->
#                     theoretically could be less, but chall has mean rng
#
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


def redeem(msg):
   msg64 = base64.b64encode(msg)
   r.recvuntil("Redeem a ticket:\n")
   r.send(msg64 + b"\n")
   while True:
      in1 = r.recvuntil("\n")
      if b"invalid" in in1:
         return 0
      if b"did not win" in in1:
         return 1
      if b"bctf" in in1:
         print(in1)   # print flag line
         exit(0)


def xor(msg, pos, otp):   # xor a segment in msg at pos
   n = len(otp)
   xorred = bytes( [ msg[pos + i] ^ otp[i]   for i in range(n)]  )
   return msg[:pos] + xorred + msg[(pos + n):]



def getBlock(ticket0, start):  # extract a block of plaintext
   ptxt = b""
   otp = b""
   for pos in range(1, 17):
      # naive solver, assumes first byte found gives 0x01 ending
      for b in range(1, 257):  # try 0 last
         bb = bytes([ b & 0xff ])
         ticket = xor(ticket0, start - pos, bb + otp)[:(start + 16)]
         if redeem(ticket) == 1:
            otp = bb + otp
            ptxt = bytes([ (b ^ pos) & 0xff]) + ptxt
            break
      else:
         print("bad")
         return b"", b""
      otp = bytes( [ v ^ pos ^ (pos + 1)  for v in otp] )
   return ptxt



r, ticket0, lst = connect()
print(f"jackpot nums: {lst} ({len(lst)})")

n0 = len(ticket0)
print(f"len(ticket0): {n0}")

code = redeem(ticket0)
print(f"original ticket check: {code}")



goal = b"numbers:" + lst + b"\x01"
Ngoal = len(goal)
print(Ngoal, goal)

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
