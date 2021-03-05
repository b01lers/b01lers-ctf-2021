This challenge is mostly about figuring out how the flag is encoded in the given
audio file.  In the description the author says that it was recorded off of an old
cassette tape.  Through a little searching on old cassette tape encodings, I
found that KCS was a common standard for storing data on cassette tapes.

There exist many programs already for encoding and decoding KCS, the one I found
that worked can be found here: http://www.dabeaz.com/py-kcs/index.html

If we run a decoder on the given audio file you will get the flag as a result.

