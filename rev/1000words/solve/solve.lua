function uncompress(compressed)
  -- This is the codebook for decompression.  Essentially this consists of
  -- a mapping from codes to strings that is built up as the input is read
  -- character by character.
  dictionary = {}
  uncompressed = ""
  i = 1
  code = 1

  -- # is an operator that gets the length of a variable in lua
  while i < #compressed+1 do
    -- Each character received is preceded by a code.  The code is 0 if the
    -- following character has never been seen before.  Otherwise, the code
    -- represents a string in the codebook.
    input_code = compressed[i]
    ichar = compressed[i + 1]

    -- This is an edge case where the last part of the string in its entirety
    -- exists in the codebook.  In this case only a code is sent with no
    -- corresponding character.  This isn't really necessary to get the flag,
    -- but it is necessary to uncompress any arbitrary input.
    if ichar == nil then
      uncompressed = uncompressed .. dictionary[input_code]
      break
    end

    -- Gets a strin (character) from an ascii value
    char = string.char(ichar)

    if input_code == 0 then
      -- In this case the current sequence has never been seen before.  This
      -- means we should add the character to the uncompressed string and add
      -- it to our codebook.  Code numbers start at 1 and increase for every
      -- new sequence encountered.
      uncompressed = uncompressed .. char
      dictionary[code] = char
      code = code + 1
    else
      -- In this case the code should represent a string in our codebook, along
      -- with an additional character that when combined with the string in
      -- our codebook creates a new string we have not seen before.  Append
      -- that whole string to the uncompressed string and add it to our
      -- codebook.
      uncompressed = uncompressed .. dictionary[input_code] .. char
      dictionary[code] = dictionary[input_code] .. char
      code = code + 1
    end

    i = i + 2
  end

  return uncompressed
end

-- This is the hexadecimal sequence seen in 1000words.png.  Thankfully, if we
-- look back at the result of running exiv2, the challenge author also included it
-- in the Exif comment field so you don't have to type it out by hand.  How
-- nice of them.
print(uncompress({
  0x00, 0x62, 0x00, 0x63, 0x00, 0x74, 0x00, 0x66,
  0x00, 0x7B, 0x00, 0x77, 0x00, 0x6F, 0x00, 0x72,
  0x00, 0x64, 0x07, 0x6E, 0x00, 0x73, 0x06, 0x6F,
  0x08, 0x64, 0x0B, 0x6F, 0x00, 0x6E, 0x0A, 0x77,
  0x07, 0x72, 0x09, 0x73, 0x0C, 0x72, 0x12, 0x77,
  0x11, 0x64, 0x0B, 0x7D
}))
