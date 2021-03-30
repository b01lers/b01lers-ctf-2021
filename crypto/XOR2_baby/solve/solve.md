Breaking XOR is a standard problem. It can be done, for example, by first computing the 
Hamming-weight autocorrelation function of the ciphertext, which has local minima
at integer multiples of the key length. Then, one can bruteforce each key byte until
the distribution of plaintext characters matches expectation for English text.
E.g., one can score characters by type (letter, number, etc), or match frequency
distributions to the expected one. Even the average fractions for bits 0, 1, 2, ... 7 
to be 1 can be used to get the corresponding key bit at the given position.

As long as one has about 30-40 ciphertext byte per key byte, this works super well. Here 
we have double XOR, but that is equivalent single XOR with a key that has Nkey1 * Nkey2 
length (more precisely, the effective key length is lcm(Nkey1, Nkey2)). So as long as we 
have enough ciphertext, this is a trivial task.

The attached crude solver does just that, using two different scoring methods. The effective 
key has 1363 bytes, and the solver gets the key almost perfectly. The rest you can fix
by hand.






