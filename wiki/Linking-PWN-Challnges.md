Some challenges need a specific libc or linker or some such. In *all* cases, we want to distribute any libraries with the binary unless there's a very good reason not to. To link to a particular library:

## Dynamically With Provided ld.so (note: UNCOMMON):

`$(CC) -o chal chal.c -L$(shell pwd) -Xlinker -rpath=$(shell pwd) -Xlinker -I$(shell pwd)/ld.so`

The libraries you'll need in the local directory for this to take are:
```
.rwxr-xr-x  165k novafacing 19 Dec 15:32  ld.so
.rwxr-xr-x   12M novafacing 19 Dec 16:27  libc.so.6
.rwxr-xr-x   14k novafacing 19 Dec 15:34  libdl.so.2
.rwxr-xr-x  132k novafacing 19 Dec 15:33  libgcc_s.so.1
```

You can find them with `find / -type f | grep <libname>`

## Statically with Provided ld.so (note: UNCOMMON):

`$(CC) -o chal chal.c -L$(shell pwd) -Xlinker -rpath=$(shell pwd) -Xlinker -I$(shell pwd) -l:libc.a -static`

The libraries you'll need in the local directory for this to take are:
```
.rwxr-xr-x  165k novafacing 19 Dec 15:32  ld.so
.rw-r--r--   21M novafacing 19 Dec 16:39  libc.a
.rwxr-xr-x   14k novafacing 19 Dec 15:34  libdl.so.2
.rwxr-xr-x  132k novafacing 19 Dec 15:33  libgcc_s.so.1
```