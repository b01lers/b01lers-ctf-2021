b /glibc-2.32/elf/dl-lookup.c:407 # break here, then continue twice.
c
c # This is where the corruption starts, fix it:

Test libc base: 0x7f172057b000

# Line 407
## Bad
pwndbg> x/xg map->l_gnu_bitmask
0x7fa4bd1ef940: 0x0000000000000000
## Good
pwndbg> x/xg map->l_gnu_bitmask
0x7f172057e940: 0x010220a044103081
## Patch
0x3940 = 0x010220a044103081

# Line 409
## Bad
pwndbg> x/xg &bitmask[(new_hash/ 64) & map->l_gnu_bitmask_idxbits]
0x7f94047a4100: 0x0000000000000000
## Good
pwndbg> x/xg &bitmask[(new_hash/ 64) & map->l_gnu_bitmask_idxbits]
0x7f172057f100: 0xf000028c0200130e
## Patch
0x4100 = 0xf000028c0200130e

# Line 420
## Bad
pwndbg> x/xw &map->l_gnu_buckets[new_hash % map->l_nbuckets]
0x7f94047a4228: 0x00000000
## Good
pwndbg> x/xw &map->l_gnu_buckets[new_hash % map->l_nbuckets]
0x7f172057f228: 0x00000089
## Patch
0x4228 = 0x00000089

# Line 427 Iteration 1
## Bad
pwndbg> x/xg hasharr
0x7f94047a52f8: 0x0000000000000000
## Good
pwndbg> x/xg hasharr
0x7f17205802f8: 0x7c967e3e7c93f2a0
## Patch
0x52f8 = 0x7c967e3e7c93f2a0

# Line 427 Iteration 2
## Bad
pwndbg> x/xg hasharr
0x7f94047a52fc: 0x0000000000000000
## Good
pwndbg> x/xg hasharr
0x7f17205802fc: 0xa36b4f2b7c967e3e
## Patch
0x52fc = 0xa36b4f2b7c967e3e
