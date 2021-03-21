Below is a quick reference of compiler flags for pwn challenges.

**Important!** on docker, ASLR *cannot* be disabled. Build your challenges around that fact unless it must be disabled for a very very cool challenge.

### Partial RELRO

`-Wl,-z,lazy`

### No NX

`-z execstack`

### No Canary

`-fno-stack-protector`

### No PIE

`-no-pie`

### Full RELRO

`-Wl,-z,now -Wl,-z,relro`

### Stack Canaries in All functions (default is only functions with stack buffers)

`-fPIE -fstack-protector-all -D_FORTIFY_SOURCE=2`

