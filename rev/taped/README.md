This is a simple challenge where the flag was encoded on a cassette tape using
the KCS encoding standard.  All that is given is an audio file containing what
was recorded from the cassette and the challenge simply is to decode it.  Challenge
information is contained in `dist/description.md` and the only file that needs
to be distributed is `dist/tape.wav`.

Since there exist decoding programs already that can solve this out of the box
I might consider turning this into a REV challenge where the program that encoded
the data is given (and it uses a slightly different format such that you can't
easily use other programs to decode it).
