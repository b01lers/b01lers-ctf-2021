flag_clean = "bctf{@_l3ast_u_didn7_g3t_tet4nu5}"
open('src/flag.enc', 'wb').write(b''.join([bytes([ord(c)^(i*i % 256)]) for (i,c) in enumerate(flag_clean)]))
