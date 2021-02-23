-- This is the non-pico8 code I used to figure out how LZW compression works
-- Also partly doubles as a solution

function spairs(t, order)
	-- collect the keys
	local keys = {}
	for k in pairs(t) do keys[#keys+1] = k end

	-- if order function given, sort by it by passing the table and keys a, b,
	-- otherwise just sort the keys
	table.sort(keys, function(a,b) return t[a] < t[b] end)

	-- return the iterator function
	local i = 0
	return function()
		i = i + 1
		if keys[i] then
			return keys[i], t[keys[i]]
		end
	end
end

function compress(uncompressed)
	local dictionary = {}

	w = ""
	compressed = {}
	comp_i = 1
	code = 1
	local wc = ""
	for i = 1, #uncompressed do
		local c = string.sub(uncompressed, i, i)

		-- while c is in the function compress
		wc = w .. c
		if dictionary[wc] == nil then
			if dictionary[w] ~= nil then
				-- compressed = compressed .. " " .. dictionary[w] .. c
				compressed[comp_i] = dictionary[w]
				compressed[comp_i + 1] = string.byte(c)
				comp_i = comp_i + 2
			else
				-- compressed = compressed .. " " .. 0 .. wc
				compressed[comp_i] = 0
				compressed[comp_i + 1] = string.byte(wc)
				comp_i = comp_i + 2
			end
			dictionary[wc] = code
			code = code + 1
			w = ""
		else
			w = wc
		end
	end
	if wc then
		compressed[comp_i] = dictionary[wc]
	end
	return compressed, dictionary
end

function uncompress(compressed)
	dictionary = {}
	uncompressed = ""
	i = 1
	code = 1

	while i < #compressed+1 do
		input_code = compressed[i]
		print(input_code)
		ichar = compressed[i + 1]
		print(ichar)
		if ichar == nil then
			uncompressed = uncompressed .. dictionary[input_code]
			break
		end
		char = string.char(ichar)
		if input_code == 0 then
			uncompressed = uncompressed .. char
			dictionary[code] = char
			code = code + 1
		else
			uncompressed = uncompressed .. dictionary[input_code] .. char
			dictionary[code] = dictionary[input_code] .. char
			code = code + 1
		end
		i = i + 2
	end

	return uncompressed, dictionary
end

-- compressed, dict = compress('TOBEORNOTTOBEORTOBEORNOT')
compressed, dict = compress('bctf{wordonswordsononwordswordswords}')
-- compressed, dict = compress('picturethispicture')
for i=1,#compressed do
	io.write(string.format('%02X ', compressed[i]))
end
print("")

for k, v in spairs(dict) do
	print(k, v)
end

uncompressed, dict = uncompress(compressed)
-- uncompressed, dict = uncompress({0, 112, 0, 105, 0, 99, 0, 116, 0, 117, 0, 114, 0, 101, 4, 104, 2, 115, 1, 105, 3, 116, 5, 114})
print(uncompressed)

for k, v in spairs(dict) do
	print(k, v)
end

