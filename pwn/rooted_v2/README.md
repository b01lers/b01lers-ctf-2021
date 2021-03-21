# chroot jail escape challenge

## Goal:
  - you are put into a chroot jail run under `fakechroot fakeroot chroot [...]`
  - the binary has a little more complicated vuln and requires a specific byte in the shellcode
  - get to the directory outside the jail and cat the flag
