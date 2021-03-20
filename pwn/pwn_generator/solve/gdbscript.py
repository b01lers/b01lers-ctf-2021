import gdb
from binascii import unhexlify

# gdb -ex "source gdbscript.py"
with open('datatransfer', 'r') as f:
    filename = f.read()

class ContinueReturn(gdb.Command):
    def __init__(self):
        super().__init__(
            'continue-return',
            gdb.COMMAND_RUNNING,
            gdb.COMPLETE_NONE,
            False
        )
    def invoke(self, arg, from_tty):
        thread = gdb.inferiors()[0].threads()[0]
        while thread.is_valid():
            gdb.execute('ni', to_string=True)
            frame = gdb.selected_frame()
            arch = frame.architecture()
            pc = gdb.selected_frame().pc()
            instruction = arch.disassemble(pc)[0]['asm']
            if instruction.startswith('ret '):
                break
ContinueReturn()

gdb.execute("file " + filename)
gdb.execute("b main")

gdb.execute("r < cyclic_input")
gdb.execute("continue-return")

with open('datatransfer', 'wb') as f:
    f.write(unhexlify(hex(gdb.parse_and_eval("*(void**)$rsp"))[2:])[::-1])
