#!/usr/bin/env python

import struct
import random
import subprocess
import os
import sys

pipe = subprocess.PIPE

#https://github.com/cloudburst/pyptrace/blob/master/defines.py
PTRACE_TRACEME = 0 
#   Return the word in the process's text space at address ADDR.  
PTRACE_PEEKTEXT = 1 
#   Return the word in the process's data space at address ADDR.  
PTRACE_PEEKDATA = 2 
#   Return the word in the process's user area at offset ADDR.  
PTRACE_PEEKUSER = 3 
#   Write the word DATA into the process's text space at address ADDR.  
PTRACE_POKETEXT = 4 
#   Write the word DATA into the process's data space at address ADDR.  
PTRACE_POKEDATA = 5 
#   Write the word DATA into the process's user area at offset ADDR.  
PTRACE_POKEUSER = 6 
#   Continue the process.  
PTRACE_CONT = 7 
#   Kill the process.  
PTRACE_KILL = 8 
#   Single step the process.
#     This is not supported on all machines.  
PTRACE_SINGLESTEP = 9
#  Get all general purpose registers used by a processes.
#     This is not supported on all machines.  
PTRACE_GETREGS = 12
#   Set all general purpose registers used by a processes.
#     This is not supported on all machines.  
PTRACE_SETREGS = 13
#   Get all floating point registers used by a processes.
#     This is not supported on all machines.  
PTRACE_GETFPREGS = 14
#   Set all floating point registers used by a processes.
#     This is not supported on all machines.  
PTRACE_SETFPREGS = 15
#   Attach to a process that is already running. 
PTRACE_ATTACH = 16
#   Detach from a process attached to with PTRACE_ATTACH.  
PTRACE_DETACH = 17
#   Get all extended floating point registers used by a processes.
#     This is not supported on all machines.  
PTRACE_GETFPXREGS = 18
#   Set all extended floating point registers used by a processes.
#     This is not supported on all machines.  
PTRACE_SETFPXREGS = 19
#   Continue and stop at the next (return from) syscall.  
PTRACE_SYSCALL = 24


#   Set ptrace filter options.  
PTRACE_SETOPTIONS  = 0x4200
#   Get last ptrace message.  
PTRACE_GETEVENTMSG = 0x4201
#   Get siginfo for process.  
PTRACE_GETSIGINFO  = 0x4202
#   Set new siginfo for process.  
PTRACE_SETSIGINFO  = 0x4203

PTRACE_LISTEN = 0x4208


#  Options set using PTRACE_SETOPTIONS.
PTRACE_O_TRACESYSGOOD   = 0x00000001
PTRACE_O_TRACEFORK      = 0x00000002
PTRACE_O_TRACEVFORK     = 0x00000004
PTRACE_O_TRACECLONE     = 0x00000008
PTRACE_O_TRACEEXEC      = 0x00000010
PTRACE_O_TRACEVFORKDONE = 0x00000020
PTRACE_O_TRACEEXIT      = 0x00000040
PTRACE_O_MASK           = 0x0000007f
PTRACE_O_TRACESECCOMP   = 0x00000080
PTRACE_O_EXITKILL       = 0x00100000
PTRACE_O_SUSPEND_SECCOMP= 0x00200000


PTRACE_SEIZE       = 0x4206

import ctypes
from ctypes import *
from ctypes import get_errno, cdll 
from ctypes.util import find_library

class user_regs_struct(Structure):
    _fields_ = (
        ("r15", c_ulong),
        ("r14", c_ulong),
        ("r13", c_ulong),
        ("r12", c_ulong),
        ("rbp", c_ulong),
        ("rbx", c_ulong),
        ("r11", c_ulong),
        ("r10", c_ulong),
        ("r9", c_ulong),
        ("r8", c_ulong),
        ("rax", c_ulong),
        ("rcx", c_ulong),
        ("rdx", c_ulong),
        ("rsi", c_ulong),
        ("rdi", c_ulong),
        ("orig_rax", c_ulong),
        ("rip", c_ulong),
        ("cs", c_ulong),
        ("eflags", c_ulong),
        ("rsp", c_ulong),
        ("ss", c_ulong),
        ("fs_base", c_ulong),
        ("gs_base", c_ulong),
        ("ds", c_ulong),
        ("es", c_ulong),
        ("fs", c_ulong),
        ("gs", c_ulong)
    )

libc = CDLL("libc.so.6", use_errno=True)
ptrace = libc.ptrace
ptrace.argtypes = [c_uint, c_uint, c_long, c_long]
ptrace.restype = c_long
ptrace_regs = user_regs_struct()



def pkiller():
    from ctypes import cdll
    import ctypes
    # PR_SET_PDEATHSIG, SIG_KILL --> kill child when parent dies
    cdll['libc.so.6'].prctl(1, 9)
    #ptrace(PTRACE_TRACEME, 0, 0, 0)
    # I cannot do traceme + raise here, because Python subporcess.Popen waits for execv
    # The alternative is to use lower level fork + execv


def parse_status(status):
    def num_to_sig(num):
        sigs = ["SIGHUP", "SIGINT", "SIGQUIT", "SIGILL", "SIGTRAP", "SIGABRT", "SIGBUS", "SIGFPE", "SIGKILL", "SIGUSR1", "SIGSEGV", "SIGUSR2", "SIGPIPE", "SIGALRM", "SIGTERM", "SIGSTKFLT", "SIGCHLD", "SIGCONT", "SIGSTOP", "SIGTSTP", "SIGTTIN", "SIGTTOU", "SIGURG", "SIGXCPU", "SIGXFSZ", "SIGVTALRM", "SIGPROF", "SIGWINCH", "SIGIO", "SIGPWR", "SIGSYS"]
        if num-1 < len(sigs):
            return sigs[num-1]
        else:
            return hex(num)[2:]

    status_list = []
    status_list.append(hex(status))
    ff = [os.WCOREDUMP, os.WIFSTOPPED, os.WIFSIGNALED, os.WIFEXITED, os.WIFCONTINUED]
    for f in ff:
        if f(status):
            status_list.append(f.__name__)
            break
    else:
        status_list.append("")
    status_list.append(num_to_sig((status>>8)&0xff))
    #status_list.append(num_to_sig(os.WEXITSTATUS(status)))
    #status_list.append(num_to_sig(os.WSTOPSIG(status)))
    #status_list.append(num_to_sig(os.WTERMSIG(status)))
    ss = (status & 0xff0000) >> 16
    ptrace_sigs = ["PTRACE_EVENT_FORK", "PTRACE_EVENT_VFORK", "PTRACE_EVENT_CLONE", "PTRACE_EVENT_EXEC", "PTRACE_EVENT_VFORK_DONE", "PTRACE_EVENT_EXIT", "PTRACE_EVENT_SECCOMP"]
    if ss >= 1 and ss-1 <= len(ptrace_sigs):
        status_list.append(ptrace_sigs[ss-1])
    else:
        status_list.append(hex(ss)[2:])
    return status_list


def readmem(pid, pos=-1, tlen=8):
    fd=os.open("/proc/%d/mem" % pid, os.O_RDONLY)
    if pos >= 0:
        os.lseek(fd, pos, 0) #SEEK_SET
    buf = b""
    while True:
        cd = os.read(fd, tlen-len(buf))
        if(cd==b""):
            break
        buf += cd
        if len(buf)==tlen:
            break
    os.close(fd)
    return buf


def parse_inst(inst):
    def convert_v(v, reg):
        tcode = b""
        if v[0] in [x for x in b"0123456789abcdef"]:
            try:
                vv = int(v, 16)
            except ValueError:
                assert False
            assert vv>=0
            assert vv<=0xffffffff
            if reg=="rax": #mov rax, <vv>
                tcode = b"\x48\xc7\xc0"+struct.pack("<I", vv)
            elif reg=="rbx": #mov rbx, <vv>
                tcode = b"\x48\xc7\xc3"+struct.pack("<I", vv)
        elif v[0] == ord(b"r"):
            try:
                rn = int(v[1:], 16)
            except ValueError:
                assert False
            assert rn>=0
            assert rn<0x200
            #lea rcx, qword ptr [rdx+(<8*rn>))]
            tcode += b"\x48\x8D\x8A"+struct.pack("<I", rn*8)
            if reg=="rax": #mov rax, qword ptr[rcx]
                tcode += b"\x48\x8b\x01"
            elif reg=="rbx": #mov rbx, qword ptr[rcx]
                tcode += b"\x48\x8b\x19"
        elif v[0] == ord(b"["):
            try:
                rn = int(v[2:], 16)
            except ValueError:
                assert False
            assert rn>=0
            assert rn<0x200
            #lea rcx, qword ptr [rdx+(<8*rn>))]
            tcode += b"\x48\x8D\x8A"+struct.pack("<I", rn*8)
            if reg=="rax":
                #mov rax, qword ptr[rcx]
                tcode += b"\x48\x8b\x01"
                #int3
                tcode += b"\xcc" + b"\x11" + b"\xcc"*5 #to check if rbx is "good" (<200, but <=0x200)
                #mov rax, qword ptr[rdx+rax*8]
                tcode += b"\x48\x8B\x04\xc2"
            elif reg=="rbx": #mov rbx, qword ptr[rdx+rbx*8]
                #mov rbx, qword ptr[rcx]
                tcode += b"\x48\x8b\x19"
                #int3
                tcode += b"\xcc" + b"\x22" + b"\xcc"*5 #to check if rbx is "good" (<200, but <=0x200)
                #mov rbx, qword ptr[rdx+rbx*8]
                tcode += b"\x48\x8B\x1c\xda"
        else:
            assert False
        return tcode

    def convert_r(v):
        tcode = b""
        if v[0] == ord(b"r"):
            try:
                rn = int(v[1:], 16)
            except ValueError:
                assert False
            assert rn>=0
            assert rn<0x200
            #lea rcx, qword ptr [rdx+(<8*rn>))]
            tcode += b"\x48\x8D\x8A"+struct.pack("<I", rn*8)
            #mov qword ptr[rcx], rax
            tcode += b"\x48\x89\x01"
        elif v[0] == ord(b"["):
            try:
                rn = int(v[2:], 16)
            except ValueError:
                assert False
            assert rn>=0
            assert rn<0x200
            #lea rcx, qword ptr [rdx+(<8*rn>))]
            tcode += b"\x48\x8D\x8A"+struct.pack("<I", rn*8)
            #mov rbx, qword ptr[rcx]
            tcode += b"\x48\x8b\x19"
            tcode += b"\xcc" + b"\x22" + b"\xcc"*5 #to check if rbx is "good" (<200, but <=0x200)
            #mov qword ptr[rbx*8+rdx], rax
            tcode += b"\x48\x89\x04\xDA"
        else:
            assert False
        return tcode

    def convert_w(w):
        tcode = b""
        try:
            rn = int(w, 10)
        except ValueError:
            assert False
        assert rn>=0
        assert rn<70
        #lea rbx, qword ptr [rsi+(<8*rn>))]
        tcode += b"\x48\x8D\x9E"+struct.pack("<I", rn*8)
        #mov rax, qword ptr[rbx]
        tcode += b"\x48\x8B\x03"
        tcode += b"\xcc" + b"\x03" + b"\xcc"*5  #to check if rbx is "good", except for exploitation it is not good if it is too big (but guranteed to be less than 70)
        return tcode




    icode = b""

    assert len(inst) < 200
    inst = inst.encode("utf-8")
    assert len(inst.split()) > 1
    op = inst.split()[0]
    assert op in [b"m", b"je", b"jb", b"j", b"a", b"s"]

    op = inst.split()[0]

    if op == b"m":
        assert len(inst.split()) == 3
        _, r, v1 = inst.split()
        icode += convert_v(v1, "rax")
        icode += convert_r(r)

    elif op == b"a" or op == b"s":
        assert len(inst.split()) == 4
        _, r, v1, v2 = inst.split()
        icode += convert_v(v1, "rax")
        icode += convert_v(v2, "rbx")
        if op == b"a":
            #add rax, rbx
            icode += b"\x48\x01\xd8"
        elif op == b"s":
            #sub rax, rbx
            icode += b"\x48\x29\xd8"
        icode += convert_r(r)

    elif op == b"jb":
        assert len(inst.split()) == 4
        _, w, v1, v2 = inst.split()
        icode += convert_v(v1, "rax")
        icode += convert_v(v2, "rbx")
        #cmp    rax,rbx 
        icode += b"\x48\x39\xd8"
        #ja + <something> (skip the code after). ja reg does not exist (opposite)
        icode += b"\x0F\x87\x13\x00\x00\x00"
        icode += convert_w(w)
        #jmp rax
        icode += b"\xff\xe0"

    elif op == b"je":
        assert len(inst.split()) == 4
        _, w, v1, v2 = inst.split()
        icode += convert_v(v1, "rax")
        icode += convert_v(v2, "rbx")
        #cmp    rax,rbx 
        icode += b"\x48\x39\xd8"
        #jne + <something> (skip the code after). jne reg does not exist (opposite)
        icode += b"\x0F\x85\x13\x00\x00\x00"
        icode += convert_w(w)
        #jmp rax
        icode += b"\xff\xe0"

    elif op == b"j":
        assert len(inst.split()) == 2
        _, w = inst.split()
        icode += convert_w(w)
        #jmp rax
        icode += b"\xff\xe0"

    else:
        assert False     

    return icode



def main():
    print("Welcome to the boilervm!")
    ninstr = int(input("how many instructions? "))
    assert ninstr>0 and ninstr<=70

    aslr = 0x6000000 + (random.randrange(0, pow(2,18)) * 0x1000)
    code = b""

    #munmap
    #rax = 0x11
    code += b"\x48\x31\xC0\xB0\x0B"
    #mov rdi, top of the region ot keep
    code += b"\x48\xC7\xC7" + struct.pack("<I", aslr+0x3000)
    #rsi = big value
    code += b"\x48\xBE\x00\x00\x00\x00\xff\x7f\x00\x00"
    #syscall
    code += b"\x0F\x05"

    #xor all common
    code += b"\x90\x48\x31\xC0\x48\x31\xDB\x48\x31\xC9\x48\x31\xD2\x48\x31\xE4\x48\x31\xED\x48\x31\xF6\x48\x31\xFF"
    #set rdx, rsi, rdi
    #rdx: top of register table
    #rsi: top of instr pointer table
    #rdi: top of code page (fully fixed wrt ASLR, ASLR is from Python) --> we need to read one of them, add something, and jump to it
    code += b"\x48\xC7\xC2" + struct.pack("<I", aslr+0x2000)
    code += b"\x48\xC7\xC6" + struct.pack("<I", aslr+0x1000)
    code += b"\x48\xC7\xC7" + struct.pack("<I", aslr)

    code += b"\x90"*8

    codeplist = []
    for _ in range(ninstr):
        codeplist.append(len(code))
        inst = input()
        inst = inst.split("#")[0]
        c = parse_inst(inst)
        #print(len(c)) #max seems to be 45
        #print(codeplist)
        code+=c

    #xor rax, rax
    #inc rax
    #xor rdi, rdi
    #inc rdi
    #mov rsi, rdx
    #xor rdx, rdx
    #mov dl, 0x8
    #syscall
    #xor rax, rax
    #mov al, 60
    #xor rdi, rdi
    #syscall
    code += b"\x90"*4
    assert len(code) < 0xfc0

    ttcode = b"\x90"
    endcode = ttcode + b"\x48\x31\xC0\x48\xFF\xC0\x48\x31\xFF\x48\xFF\xC7\x48\x89\xD6\x48\x31\xD2\xB2\x08\x0F\x05\x48\x31\xC0\xB0\x3C\x48\x31\xFF\x0F\x05"
    "\x48\x89\x04\x11"
    code = code.ljust(0x1000-len(endcode), b"\x90")
    code = code+endcode
    assert len(code) == 0x1000
    


    nvalues = int(input("how many values? "))
    assert nvalues>0 and nvalues<=4
    ivalues = []
    regs = b""
    for i in range(nvalues):
        vv = input()
        try:
            vv = int(vv, 16)
        except ValueError:
            assert False
        assert vv>=0 and vv<=0xffffffff
        regs += struct.pack("<Q", vv)
    regs = regs.ljust(0x1000, b"\x00")

    pointers = b""
    for p in codeplist:
        pointers += struct.pack("<Q", aslr+p)
    pointers = pointers.ljust(0x1000, b"\x00")

    buf = code+pointers+regs

    #with open("buf", "wb") as fp:
    #    fp.write(buf)

    fullargs = ["./stub", hex(aslr)[2:]]
    p = subprocess.Popen(fullargs, stdin=pipe, stdout=pipe, stderr=pipe, close_fds=True, preexec_fn=pkiller)
    pid = p.pid
    opid = pid
    #print(p, pid)
    pid, status = os.waitpid(-1, 0) # this will wait for the raise added at the beginning of the child

    #the following MUST happen after the child called tracme, but before it continues
    #therefore, the waitpid above is essential to call SETOPTIONS while the child is not terminated yet, but it has called traceme
    ptrace(PTRACE_SETOPTIONS, pid, 0, PTRACE_O_TRACESECCOMP | PTRACE_O_EXITKILL | PTRACE_O_TRACECLONE | PTRACE_O_TRACEVFORK)
    ptrace(PTRACE_CONT, pid, 0, 0)

    #print("---")

    p.stdin.write(buf)
    p.stdin.close()

    #print(pid)

    while True:
        pid, status = os.waitpid(-1, 0) # this will wait for the raise added at the beginning of the child
        pstatus = parse_status(status)
        #print(pstatus)
        #if pstatus[2] == "SIGSEGV":
        #    p.kill()
        #    break
        if pstatus[1] == "WIFEXITED":
            break
        else: # pstatus[2] == "SIGTRAP":
            res = ptrace(PTRACE_GETREGS, pid, 0, ctypes.addressof(ptrace_regs))
            #print(hex(ptrace_regs.rip), hex(ptrace_regs.rax), hex(ptrace_regs.rbx))
            v = readmem(pid, ptrace_regs.rip, 1)
            #print(hex(ord(v)))
            if v == b"\x03": #jump
                if ptrace_regs.rax not in [aslr + p for p in codeplist]:
                    print("Invalid jump target!")
                    sys.exit(1)
            elif v == b"\x11":
                #print("-", repr(ptrace_regs.rbx))
                if ptrace_regs.rax > 0x200:
                    print("Invalid register number!")
                    sys.exit(2)
            elif v == b"\x22":
                #print("-", repr(ptrace_regs.rbx))
                if ptrace_regs.rbx > 0x200:
                    print("Invalid register number!")
                    sys.exit(2)

            #elif v == b"\x77":
                #print(hex(ptrace_regs.rip), hex(ptrace_regs.rax), hex(ptrace_regs.rdi), hex(ptrace_regs.rsi), hex(ptrace_regs.rdx), hex(ptrace_regs.rbx))
                #input()

            prip = ptrace_regs.rip
            while True:
                #print(hex(prip))
                vmem = readmem(pid, prip, 4)
                #print(repr(vmem))
                if vmem == b"\xcc"*4:
                    break
                prip+=1
            ptrace_regs.rip = prip+4+1
            #if first:
            #    print("--------->", hex(ptrace_regs.rax))
                #ptrace_regs.rax = (0x2000000000000000-512)
            #first = False
            #print("->", hex(ptrace_regs.rip))
            #print(hex(ptrace_regs.rip), hex(ptrace_regs.rax), hex(ptrace_regs.rbx), hex(ptrace_regs.rdi), hex(ptrace_regs.rsi), hex(ptrace_regs.rdx))
            ptrace(PTRACE_SETREGS, pid, 0, ctypes.addressof(ptrace_regs))


        ptrace(PTRACE_CONT, pid, 0, 0)

    res = p.stdout.read(8)
    print("RESULT: " + str(struct.unpack("<Q", res)[0]))

    try:
        p.kill()
    except ProcessLookupError:
        pass



if __name__ == "__main__":
    sys.exit(main())



###TODO
#python -u
#xinitd without stderr and with timeout
#write file permissions

