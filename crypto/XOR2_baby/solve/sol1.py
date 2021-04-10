from Crypto.Random import get_random_bytes
import math, os


# xor operation

def xor(msg, key):
   nkey = len(key)
   return bytes( [ msg[i] ^ key[i % nkey]   for i in range(len(msg))] )


# METHOD 1
# character type based scoring

def scoreChar(c):
   if ord('a') <= c <= ord('z') or ord('A') <= c <= ord('Z') or c == 0x20:  return 2.
   if ord('0') <= c <= ord('9') or bytes([c]) in b"\n\t.,?!": return 1.
   if bytes([c]) in b";:'\"-+": return 0.5
   if c < 0x20 or c > 0x7f: return -10.
   return 0

def scoreXOR1(ctxt, gap, k):
   n = len(ctxt)
   tot = 0
   for p in range(0, n, gap):
      tot += scoreChar(ctxt[p] ^ k)
   return tot

def bestXOR1(ctxt, gap):
   scores = [ (k, scoreXOR1(ctxt, gap, k)) for k in range(256) ]
   return sorted(scores, key = lambda v: -v[1])


# METHOD 2
# character distribution based scoring

def buildCharFreqs(fname):
   text = open(fname, "rb").read()
   charFreqTable = [0]*256
   for b in text:
      charFreqTable[b] += 1
   for b in range(256):
      charFreqTable[b] *= 1. / len(text)
   return charFreqTable

# build char freq table from large body of English text
#charFreqTable = buildCharFreqs("ENG.txt")
#
# this is one possible result
charFreqTable = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01953579958439188, 0.0, 0.0, 0.01915375271907812, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16025378649799113, 0.0009440786415383615, 0.0003761389240975697, 1.2956011439017972e-06, 2.228433967511091e-06, 1.4510732811700128e-06, 8.861911824288292e-06, 0.000408010712237554, 0.00028508407570415145, 0.0002865869730310775, 5.944218048221445e-05, 1.0364809151214377e-07, 0.014423461118646903, 0.001367014678953664, 0.008916482544469436, 2.886599348613204e-05, 0.00016428222504674786, 0.00020900637653423792, 0.00010665388616599594, 7.270913619576885e-05, 5.757651483499586e-05, 6.602383429323559e-05, 4.192565301666216e-05, 4.622704881441612e-05, 6.400269650874878e-05, 4.7989066370122564e-05, 0.00046159677554933226, 0.001503726511658182, 1.0364809151214377e-07, 1.0364809151214377e-07, 3.109442745364313e-07, 0.0010545675070903068, 2.7984984708278817e-06, 0.001870796227748439, 0.0010670571021175201, 0.0010472084925929445, 0.0007675659416931807, 0.0008713695053425926, 0.0007078128169364298, 0.0007215980131075449, 0.0013678438636857612, 0.0037327305436725897, 0.0002654427623626002, 0.00024564597688378075, 0.0006925765474841447, 0.0013774831361963906, 0.0008001114424279938, 0.0007202505879178871, 0.0011010018520877473, 4.4413207212953606e-05, 0.0006701367356717656, 0.0013802298106214625, 0.0022418563953619138, 0.00016708072351757575, 0.00028156004059273857, 0.000980459121659124, 6.426181673752914e-05, 0.0004911364816302932, 4.519056789929468e-05, 3.9023506454322127e-05, 7.255366405850064e-07, 3.9645395003394994e-05, 0.0, 0.0005593369258452838, 4.145923660485751e-07, 0.057797492566099756, 0.010211772744096697, 0.017206671495976742, 0.03203290909823984, 0.0914385018041505, 0.015849658857854002, 0.014424964015973828, 0.04641226795394832, 0.047523790087324554, 0.0007459034905671426, 0.005676391379754066, 0.02928908499568461, 0.01792401993733229, 0.05091764319579819, 0.05668700691363865, 0.011790851418284207, 0.00072957891615398, 0.04252701924361561, 0.04557344394934054, 0.06553254233946802, 0.020777192776432828, 0.007196235169642386, 0.015999067581768757, 0.001040212246415875, 0.014799289098469936, 0.0005007239300951666, 1.0364809151214377e-06, 1.0364809151214377e-07, 8.810087778532221e-07, 0.0, 0.0, 0.007863055166385764, 1.6583694641943003e-06, 1.0364809151214377e-07, 5.1824045756071885e-08, 3.3167389283886006e-06, 5.1824045756071885e-08, 6.218885490728626e-07, 5.1824045756071885e-08, 1.0364809151214377e-07, 6.529829765265058e-06, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.877254954922927e-05, 0.0, 1.5547213726821565e-07, 2.332082059023235e-06, 0.0005848343563572712, 1.0364809151214377e-07, 5.1824045756071885e-08, 5.1824045756071885e-08, 0.0002589647566430912, 0.0019666188883514157, 0.0, 0.0, 0.002528080600072699, 0.002444747534496935, 0.0, 0.0, 4.66416411804647e-06, 0.00015878887619660424, 1.461438090321227e-05, 3.7313312944371757e-06, 3.627683202925032e-07, 0.0, 4.975108392582901e-06, 4.042275568973607e-06, 7.022158199947741e-05, 0.0001310630117171058, 2.7984984708278817e-06, 1.264506716448154e-05, 0.0, 0.00010261161059702234, 1.5028973269260847e-06, 7.721782817654711e-06, 3.109442745364313e-07, 6.218885490728626e-07, 2.0729618302428754e-07, 0.00014344895865280697, 2.3839061047793066e-06, 1.5547213726821565e-07, 2.0211377844868037e-06, 1.5547213726821565e-07, 2.0729618302428754e-07, 2.591202287803594e-07, 5.0735740795194374e-05, 8.291847320971502e-07, 7.929079000678998e-06, 2.4875541962914505e-06, 0.0, 1.6583694641943003e-06, 0.0, 0.0, 4.456867935022182e-06, 0.0007283351390558342, 1.0883049608775096e-06, 2.74667442507181e-06, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0364809151214377e-07, 0.0, 1.5028973269260847e-06, 8.810087778532221e-07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0364809151214377e-07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.773606863410782e-07, 0.00786559454462781, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.255366405850064e-07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def charFreq(c):
   return charFreqTable[c]

def scoreXOR2(ctxt, gap, k):
   # create freq table
   n = len(ctxt)
   freqs = [0]*256
   for p in range(0, n, gap):
      freqs[ctxt[p] ^ k] += 1
   # difference from expected frequencies
   norm = 1. / (n // gap)
   diffs = [ (freqs[i] * norm - charFreq(i))**2  for i in range(256) ]
   # penalize for nonprinting chars
   for b in range(256):
      if (b < 0x20 or b > 0x7f) and b != 0xa and b != 0xd and b!= 0x9 :
         if freqs[b] > 0: diffs[b] = 1.
   # normalize and return
   diff = math.sqrt(sum(diffs)) / 256.
   return diff

def bestXOR2(ctxt, gap):
   scores = [ (k, scoreXOR2(ctxt, gap, k)) for k in range(256) ]
   return sorted(scores, key = lambda v: v[1])



#
# find best key, for a given scoring system

def findKey(ctxt, Nkey, bestFn, DBG = False):
   recKey = b""
   for i in range(Nkey):
      cands = bestFn(ctxt[i:], Nkey)
      if DBG: print( cands[:5] )
      recKey += bytes([cands[0][0]])
   return recKey


# hamming weight for keylen determination

hammingWeights = { i: bin(i)[2:].count("1")  for i in range(256) }

def hamming(a):
   return hammingWeights[a]

def corrFnEval(msg, k):
   n = len(msg)
   tot = 0
   for i in range(n - k):
      tot += hamming(msg[i] ^ msg[i + k])
   return tot / (n - k)


#
# read text
ctxt = open("chal1.enc", "rb").read()

#
# find keylen via autocorrelation function (use hamweight(x[i], x[i-n]))

print(f"len(ctxt)= {len(ctxt)}")

corr = [ (k, corrFnEval(ctxt, k))  for k in range(1, 1500) ]
corrSorted = sorted(corr, key = lambda v: v[1])
print( corrSorted[:10] )

#
# find key, try both methods

Nkey = 1363

recKey1 = findKey(ctxt, Nkey, bestXOR1)
print(f"recKEY= {recKey1}")
ptxt1 = xor(ctxt, recKey1)
print(ptxt1)
open("sol1-method1.txt", "wb").write(ptxt1)

recKey2 = findKey(ctxt, Nkey, bestXOR2)
print(f"recKEY2= {recKey2}")
ptxt2 = xor(ctxt, recKey2)
print(ptxt2)
open("sol1-method2.txt", "wb").write(ptxt2)

os.system("grep bctf sol1-method2.txt sol1-method2.txt")

#EOF
