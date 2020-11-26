# Solution

### Background
This challenge is using a specific exploit on AES using the CBC block mode. 
Specifically it is taking advantage of the fact that you can alter the previous block of ciphertext to modify the next one in a predictable way.
Namely that if you know what the plaintext was previously you can xor that message by your target message like:

`target_xor = plaintext ^ target_plaintext`

Then you can xor the previous block by this target_xor value to get the plaintext of the target block to change to the target_plaintext instead.
Note that this will not work if the target_plaintext is split across multiple consecutive blocks.


### Problem
For this challenge you are given a python source file of a running service and a ciphertext in hex format. 
From reading the description and looking at the source file you should have the following goal:

Connect to the program over socket to change the coordinates in the given ciphertext from Purdue University to Indiana University.

### First Step
The first step is to find the latitude and longitude of both locations given. When looking at the regex in the source file given you should
notice that coordinates only matter to the first decimal place. After some quick googles like `gps coordinates for <iu/purdue> university`
you should get their coordinates to be the following:

`IU-> lat: 39.1 long: -86.5  |  PURDUE -> lat: 40.4 long: -86.9`


### Putting It All Together
So given this information we know that somewhere in the ciphertext is the string `40.4,-86.9`.
We can use the background information to then make a target_xor value that will alter the plaintext to the wanted coordinates given we know 
which block and where in it that the coordinates are at. With the way the challenge is presented both of those are unknowns.
This means that we must do the following:

For each sequential pair of blocks we must go through all possible positions of the coordinates in the text. 
(a block is of length 16 and the coordinates must be within a single block to make the challenge solvable).
With each position we must prepend 0 bytes to the target_plaintext so that we get the intended position.

**Example:**

starting text position of coordinates -> 3 \
Note "39.1,-86.5" is equivalent to the hex: 33 39 2e 31 2c 2d 38 36 2e 35 \
Note "40.4,-86.9" is equivalent to the hex: 34 30 2e 34 2c 2d 38 36 2e 39 \
So our target_xor = 07 09 00 05 00 00 00 00 00 12 \
new_ciphertext_block = first_ciphertext_block ^ 00 00 00 07 09 00 05 00 00 00 00 00 12 00 00 00 \
send new_ciphertext_block + second_ciphertext_block

We then send this pair of blocks to the running program and see if we get the flag. If not then rinse and repeat through all block pairs and text positions till success.
