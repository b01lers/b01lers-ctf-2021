First, let's look at the metadata in the image file.  Pretty much any image
viewer or editor will let you view metadata, but personally I use `exiv2` or
`exiftool`.  If I run `exiv2` on it I get the following (with some lines omitted):

```
File name : 1000words.png
File size : 16228 Bytes
MIME type : image/png
Image size  : 160 x 205
...
Exif comment  : https://drive.google.com/drive/folders/1-vdc2TsLiT3wa8aoB-gY4AOlFW6T5SIV
```

The link leads to a Google drive folder with downloads for a program called
pico8.  Doing a little research leads to the fact that pico8 is a fantasy console
(basically an emulator for a console that never existed) and its programs (carts)
can be distributed as image files.  Now, if we open `1000words.png` in pico8,
it will load it as a program.

I won't explain how to navigate pico8 here, but I found this cheat sheet very
helpful:
![Benjamin Bannekat](https://www.lexaloffle.com/bbs/files/16585/PICO-8_CheatSheet_0111Gm_4k.png)

The first thing you should see is the lua code for the program stored in the image, which
is replicated below (indentation in pico8 is a single character usually):

```lua
music(0)

function _init()

-- utilities
ascii={}
ns='0123456789'
abc='abcdefghijklmnopqrstuvwxyz'
for i=1,#ns do
  ascii[sub(ns,i,i)]=i+47
end
for i=1,#abc do
  ascii[sub(abc,i,i)]=i+96
end
ascii['{']=123
ascii['}']=125
ascii['_']=95

function circsort(a)
  for i=1,#a do
    j=i
    while j>1 and a[j-1].radius<a[j].radius do
      a[j],a[j-1] = a[j-1],a[j]
      j-=1
    end
  end
end

-- end utilities

function lz(d)
  cb={}
  cmp={}
  code=1
  w=''
  wc=''
  cmpi=1
  for i=1,#d do
    c=sub(d,i,i)
    wc=w..c
    if not cb[wc] then
      if cb[w] then
        cmp[cmpi]=cb[w]
        cmp[cmpi+1]=ascii[c]
        cmpi+=2
      else
        cmp[cmpi]=0
        cmp[cmpi+1]=ascii[c]
        cmpi+=2
      end
      cb[wc]=code
      code+=1
      w=''
      wc=''
    else
      w=wc 
    end
  end
  if wc then
    cmp[cmpi]=cb[wc]
  end
  -- array of decimals, 1 per byte
  return cmp
end

msg=lz('picturethispicture')

end -- end _init()

function _draw()
  cls(1)
  cols=4
  circles={}
  for i=0,3 do
    if i % 2 == 0 then clr=1 else clr=7 end
    r=(((t()*1.5+i)*13)%55)+50
    add(circles,{radius=r,clr=clr})
  end
  circsort(circles)
  for circle in all(circles) do
    circfill(64,64,circle.radius,circle.clr)
  end
  circfill(64,64,50,1)

  pal(7,7)
  row=0
  for i=1,#msg do
    col=(i-1)%4
    if col==0 then row+=1 end
    c=msg[i]
    -- convert to hex
    d1=flr(c/16)
    d2=c%16
    t1=t()*30 + i*4 - 14
    x1=40+col*12+cos(t1/90)*2
    y1=20+10*row+cos(t1/50)*2
    x2=x1+5
    y2=y1
    spr(16+d1,x1,y1)
    spr(16+d2,x2,y2)
  end
end
```

A lot of this code is just drawing routines.  However, there is one function
that sticks out called `lz`.  I can see that it takes a string as an input
and outputs an array of integers.  If I look further down in the drawing code
I can see that there is some kind of hex conversion happening on the elements
of the string 'picturethispicture' processed by the `lz` function.

If I press escape to exit the code editor and enter `run` to run the cartridge,
I can see that it indeed is displaying the result of `lz` as hexadecimal.  If
we look back at `1000words.png` in an image viewer, we can see that a very
similar looking hex string.  This likely means that a string (probably the
flag) was run through the `lz` function and the hex string we see in the image
is the output.  So, we need to reverse the algorithm defined in `lz` to get the
flag back.  For the sake of consistency, I wrote the solution code in lua as well

```lua
function uncompress(compressed)
  dictionary = {}
  uncompressed = ""
  i = 1
  code = 1

  while i < #compressed+1 do
    input_code = compressed[i]
    ichar = compressed[i + 1]
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

  return uncompressed
end
print(uncompress({0x00, 0x62, 0x00, 0x63, 0x00, 0x74, 0x00, 0x66, 0x00, 0x7B, 0x00, 0x77, 0x00, 0x6F, 0x00, 0x72, 0x00, 0x64, 0x07, 0x6E, 0x00, 0x73, 0x06, 0x6F, 0x08, 0x64, 0x0B, 0x6F, 0x00, 0x6E, 0x0A, 0x77, 0x07, 0x72, 0x09, 0x73, 0x0C, 0x72, 0x12, 0x77, 0x11, 0x64, 0x0B, 0x7D}))
```

This will print the flag.
**TODO:** write this in python because less people are familiar with lua, also
add more explanation in the code for the solve.  Also maybe consider putting
the hex string in the Exif data somewhere so people can just copy paste instead
of manually entering it.
