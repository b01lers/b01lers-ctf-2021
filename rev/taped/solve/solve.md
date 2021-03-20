This challenge is mostly about figuring out how the flag is encoded in the given
audio file.  In the description the author says that it was recorded off of an old
cassette tape.  If you search for cassette tape data encodings, you will find
that the older encodings work by making 1s a specific frequency and 0s another
specific frequency (usually half the frequency of the 1s).  If we look at the
audio file in an audio editor of some kind, we can see that it indeed consists of
two alternating frequencies.

There exist many programs already for encoding and decoding these types of
storage formats, the one I used can be found here: [http://www.dabeaz.com/py-kcs/index.html](http://www.dabeaz.com/py-kcs/index.html)

If we run the decoder on the given audio file we get a slightly mangled output,
but one that is recognizable as something resembling the flag.  If we modify
the program to dump the hex values of each byte being read as well as the
printable ascii character associated with it (if there is one), we will
see the flag plus some stray zero bytes at the beginning.  However, something
about the flag is slightly off.  You might be able to figure out just by looking at
the hex dump that the data is split up into chunks of 5 bytes with the last
byte being a checksum of some sort.  If we then remove every 5th byte (starting
at the actual beginning "b", not the stray zeroes at the start) we will get the
flag.

You can also figure all of the above out using the provided encoder binary, but
it's easier to reverse if you already have some idea what it's doing.

