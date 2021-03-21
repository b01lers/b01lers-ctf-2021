a = [0x4d4a5258,
        0x495a5433,
        0x47525657,
        0x51595255,
        0x47525a44,
        0x434e4a55,
        0x4e555948,
        0x454d444f,
        0x50554641,
        0x3d3d3d3d,
        ]

for ent in a:
    for i in range(1, 5):
        index = 4 - i
        char = (ent>>8*index) & 0xff
        print(chr(char), end='')
