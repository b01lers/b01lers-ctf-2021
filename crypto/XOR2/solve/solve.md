For cross-check, here are the keys:

key1= b'\x94\x9a\\\xf2B\xf1\xe1\xa6i\xe9\x18\x96k\x17\x97\xf5WDbw-\x03\\\r&\x8f+:\xa1-B\xd1\xbf-\xb98\xf5N\xc7>\xa4\x8a\xe8C\xd4E.2; \xc8\xf5\x9b'
key2= b'\xd5\xb6,EQI=\xee](\x86Q\xbb\x00\xce\xc3\x1a\xb2\x96]s\x9c\xdb\xec\x98\xd5\xba\x05W\xdb\x8b\x92;\xfa\x8a\xcb\x81\x1fy[\x0e\xe9\xab\xa3\xad~3\xff\xf0\x18\xaf?\xb7\xd6v\xf24\xff4?\x8c\x8b\xf75\xb9\x9bP\xd6%\x81\xcc'

The key lengths are Nkey1=53, Nkey2=71.

---

I will give details later (so this section will be replaced). But in a nutshell:

   1) find key lengths via trial and error, taking all integer pairs up to length n, iterating
      n, n+1, n+2... One can construct a XOR distinguisher that yields for the correct key lengths
      0 or 1 with high probability. This takes less than 5 mins to find Nkey1 and Nkey2. 
      Let Nkey1 < Nkey2. The general strat from here is to find candidates for key1, xor the cipher
      text with those, then use the single XOR solver to find key2, score the resulting plaintext
      based on how 'good' it is, and then find the key1 value that results in the best score.

   2) Key1 bytes can be first found via a correlation method at a given bit position (0-7), which
      exploits a natural imbalance between 0 and 1 for English text at that position. Unfortunately,
      the correlation involves xorring bytes, and that reduces the imbalance a lot. Still, bits
      4-7 of key1 can be found with practical certainty given the about 3000 chars of ciphertext given.

   3) Most of bits 1 and 3 of key 1 are also correct, but bits 0 and 2 are largely a tossup. Bits 0-3 can
      be fixed, however, by scoring the resulting reconstructed plaintexts using a more sophisticated
      natural language function, specifically, the n-gram likelihoods used in the automated 2TP solver
      in b01lerCTF 2020. The search space is large, so you need some quick heuristics first and then
      refine the key1 candidate via a slower, more thorough search. In the end the result is almost perfect,
      except for a few bits that you can fix by hand.



