from PIL import Image
from PIL import ImageChops
from pwn import *
import os

checkpath = "elfcraft/data/elfcraft/functions/checks/check{}.mcfunction"

# part 1: generate ELF from checks
elf = open("elf", "wb")
for i in range(228):
	# get the current check file
	f = open(checkpath.format(str(i)))
	checks = f.readlines()
	checks = checks[2:len(checks)-2]
	f.close()

	# generate a png (for example) with the block checks
	byte_img = Image.new("RGB", (16, 5), (255, 255, 255))
	for check in checks:
		x = int(check.split("~")[1].split(" ")[0])
		y = int(check.split("~")[3].split(" ")[0]) % 6
		byte_img.putpixel((x,y), (0, 0, 0))
	
	# the first two characters are always 0x, those can be tossed; we need to find the third and fourth character to know which byte to write to the ELF
	# do this by slicing the generated image and comparing with drawn letters
	char1_img = byte_img.crop((8, 0, 11, 5))
	char2_img = byte_img.crop((12, 0, 15, 5))
	char1 = ""
	char2 = ""
	for j in range(16):
		compare = Image.open("char-bmps/{}.png".format(hex(j)[2:])).convert("RGB")
		if ImageChops.difference(char1_img, compare).getbbox() == None:
			char1 = hex(j)[2:]
		if ImageChops.difference(char2_img, compare).getbbox() == None:
			char2 = hex(j)[2:]
	elf.write(bytes([int(char1 + char2, 16)]))
elf.close()

# part 2: brute force one byte to get the flag
os.system("chmod +x elf")  # lmao
for i in range(0,256):
	p = process("./elf")
	p.sendline(bytes([i]))
	r = p.recvall().decode("utf-8")
	if r[0:4] == "bctf":
		print(r)
		break

# flag: bctf{m1n3cra4ft_ELFcr4ft}
