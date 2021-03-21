from pwn import *
import gmpy2
import multiprocessing as mp

#
# PLAY WITH TEST SERVER
#

r = remote("localhost", 25000) # test server

# read past menu (7 items + choice line)
for i in range(8):
   r.recvuntil("\n")

# get test server params
r.send("1\n")

p = int( r.recvuntil("\n")[2:] )
q = int( r.recvuntil("\n")[2:] )
e = int( r.recvuntil("\n")[2:] )
r.recvuntil("\n")
print(f"p={p}")
print(f"q={q}")
print(f"e={e}")


# check RSA encryption of test vector to see how messages
# get converted to integers

msg0 = 'THIS IS A TEST'
r.send("2\n")
r.recvuntil("\n")
ctxt0 = int( r.recvuntil("\n"), 16 )
r.recvuntil("\n")

# try little-endian ascii/utf-8... whatever  -> fails
x0 = int.from_bytes(msg0.encode("ascii"), "little")
print( pow(x0, e, p*q) == ctxt0 )

# try big-endian ascii/utf-8... whatever -> WORKS
x0 = int.from_bytes(msg0.encode("ascii"), "big")
print( pow(x0, e, p*q) == ctxt0 )


# build byte-string -> int converter
def msg2int(msg):
   return int.from_bytes(msg, "big")


#
# now find e & n for real server
#

r  = remote("localhost", 25000)   # test server
r2 = remote("localhost", 25001)   # real server

# read past menus
# save these as ptxt/ctxt pairs for later analysis
ptxts = [ r.recvuntil("\n").strip()   for i in range(8) ]
ptxts.remove(ptxts[6]) # remove item 7)
ctxts = [ int(r2.recvuntil("\n")[2:], 16)  for i in range(7) ]

print(ptxts)
print(ctxts)

#
# determine exponent and n
#

xvals = [ msg2int(ptxts[i]) for i in range(7) ]

def getEN(xvals, ctxts, elo, ehi, edelta):
   p0 = pow(xvals[0], elo)
   p1 = pow(xvals[1], elo)
   mul0 = xvals[0] ** edelta
   mul1 = xvals[1] ** edelta
   for e in range(elo, ehi, edelta):
      y0 = p0 - ctxts[0]
      y1 = p1 - ctxts[1]
      ncand = gmpy2.gcd(y0, y1)
      if ncand >= 1e20: return e, ncand
      p0 *= mul0     # faster this way than doing pow(...) each time
      p1 *= mul1


def getENmp(Ncores):
   pool = mp.Pool(Ncores)
   elo = 2
   ebatch = 100
   while True:
      ehi = elo + ebatch
      args = [(xvals, ctxts, elo + i, ehi, Ncores)  for i in range(Ncores)]
      results = pool.starmap(getEN, args)
      results = [ v  for v in results   if v != None ]
      if results:  break
      elo = ehi
      sys.stdout.write(".")

   return results[0]

# use multiple cores for efficiency

#print(f"Ncpu= {mp.cpu_count()}")
(e, ncand) = getENmp(2)
print(e, ncand)

###test server results  -> ~7 mins on my laptop, single core
###                        ~3.5 with 2,3,4 cores
#e, ncand = 11111, 78125013664826963778429952016827799165349113528330954448484118632956410108997609964501715799619597226425771000426989875042944777485763729777646305292207673469340992969956797651400700571082298892211287080232582887666521130116630103483743066164628473866133363448327043235300117715631866737882186532613991665878295150344808408031268651247968673204835562621065972227405851166988164272208729005679694171921726573473517510930103509347930748118517335672842282970912814597
### real server results -> ~10 min on my laptop, single core
###                     -> ~5 min on 2 cores
#e, ncand = 12397, 22773501054316189978847426447297976555294712196635711619548646535714349108673592536268901773559128452119139837790241960739406771052120064104023220398906880827527087247425436548928353656972875367426973981467016072783510437703982882407156397664868084974299881499614685231414426733661535600931674239270779081052646773860836872606697808969130311968768581786751582363716815545771556893913833591445390392262991895794399880537305863766499747621897617172453506490232685403030443855749834521879936774363977709894706639695250630108541003751274695379056107906602622564780555249131557008571223117101450512292660697307893910788607


# refine n
n = ncand
for i in range(2, 7):
   n = gmpy2.gcd(n, pow(xvals[i], e) - ctxts[i])

print(f"#extracted key:")
print(f"e={e}")
print(f"N={n}")
print(f"ncand/n={ncand/n}")  # could have refined by division of small factors

# get direct encryption of flag
r2.send("4\n")
in1 = r2.recvuntil("\n")
# get encryption of "encryption of " line for flag
r2.send("5\n")
r2.recvuntil("\n")
in2 = r2.recvuntil("\n")

C1 = int(in1[2:], 16)
C2 = int(in2[2:], 16)
print(f"C1: {C1}")
print(f"C2: {C2}")

#
# now use sage to solve this, the two plaintexts are related as x2 = a * x1 + b
# 

print("#scaling params")
pref = b"encryption of '"
post = b"' gives:"
b0 = msg2int(pref)
b1 = msg2int(post)

print(f"b0={b0}")
print(f"b1={b1}")
print(f"len(post)={len(post)}")
