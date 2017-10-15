import ctypes,struct,sys

class Rfmt_s (ctypes.BigEndianStructure):
    _fields_ = [
            ("op",ctypes.c_uint32,6),
            ("rs",ctypes.c_uint32,5),
            ("rt",ctypes.c_uint32,5),
            ("rd",ctypes.c_uint32,5),
            ("shamt",ctypes.c_uint32,5),
            ("funct",ctypes.c_uint32,6),
        ]

class Instruction (ctypes.Union):
    _anonymous_ = ["bits"]
    _fields_ = [
                ("bits", Rfmt_s),
                ("asInt",ctypes.c_uint32)
        ]


test = Instruction()

test.asInt = 0x03000011

print test.op,test.rs,test.rt,test.rd,test.shamt,test.funct
