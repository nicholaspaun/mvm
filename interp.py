#!/usr/bin/env python
from registers import Registers
from memory import Memory
from errors import MVMErr
import sys
import ml

class Interp:

    def __init__(self):

        self.cmds = {
                'ADD': self.add, 'ADDU': self.add, 'SUB': self.add, 'SUBU': self.add,
                'OR': self.add, 'AND': self.add, 'NOR': self.add, 'XOR': self.add,
                'ADDI': self.addi,'ADDIU': self.addi,'SUBI': self.addi,'SUBIU': self.addi,
                'ANDI': self.addi, 'ORI': self.addi, 'XORI': self.addi,
                'LI': self.li, 'MOVE': self.move,
                'SLT': self.slt, 'SLTU': self.slt,
                'SLL': self.sll, 'SRL': self.sll,
                'J': self.j,
                'JAL': self.jal,
                'JR': self.jr,
                'BEQ': self.beq, 'BNE': self.beq,
                'MULT': self.mult, 'MULTU': self.mult,
                'DIV': self.div, 'DIVU': self.div,
                'MFLO': self.mfhi, 'MFHI': self.mfhi,
                'NOP': self.nop,
                'PYEVAL': self.pyeval,
                'PYJAL': self.pycall,
                'SYSCALL': self.pysyscall,
                'PYEXEC': self.pyexec,
                'LW': self.lw,
                'SW': self.lw,
        }
        self.regs = Registers()
        self.mem = Memory(32)

    def pcinc(self):
        pc = self.regs.get('pc')
        pc += 4
        self.regs.set('pc',pc,special=True)

    def add(self,name,d,s,t):
        sval = self.regs.get(s)
        tval = self.regs.get(t)

        if name == 'SUB' or name == 'SUBU':
            sval -= tval
        elif name == 'OR':
            sval |= tval
        elif name == 'AND':
            sval &= tval
        elif name == 'XOR':
            sval ^= tval
        elif name == 'NOR':
            sval = ~(sval | tval)
        else:
            sval += tval

        if name == 'ADDU' or name == 'SUBU':
            sval = abs(sval)

        self.regs.set(d,sval)
        self.pcinc()

    def addi(self,name,d,s,i):
        val = self.regs.get(s)

        if name == 'SUBI' or name == 'SUBIU':
            val -= i
        elif name =='ADDI' or name == 'ADDIU':
            val += i
        elif name == 'ANDI':
            val &= i
        elif name == 'ORI':
            val |= i
        elif name == 'XORI':
            val ^= i

        if name == 'ADDIU' or name == 'SUBIU':
            val = abs(val)

        self.regs.set(d,val)
        self.pcinc()



    def li(self,name,d,i):
        self.addi('ADDI',d,'$0',i)

    def move(self,name,d,s):
        self.add('ADD',d,s,'$0')

    def slt(self,name,d,a,b):
        aval = self.regs.get(a)
        bval = self.regs.get(b)

        if name == 'SLTU':
            aval = abs(aval)
            bval = abs(bval)

        if aval < bval:
            val = 1
        else:
            val = 0

        self.regs.set(d,val)
        self.pcinc()

    def sll(self,name,d,s,i):
        val = self.regs.get(s)

        if i > 5:
            i = 5

        if name == 'SLL':
            val <<= i
        elif name == 'SRL':
            val >>= i

        self.regs.set(d,val)
        self.pcinc()

    def j(self,name,addr):
        self.regs.set('pc',addr,special = True)

    def jr(self,name,r):
        self.regs.set('pc',self.regs.get(r), special = True)

    def jal(self,name,addr):
        self.regs.set('$ra',self.regs.get('pc') + 4)
        self.j('J',addr)

    def beq(self,name,a,b,addr):
        aval = self.regs.get(a)
        bval = self.regs.get(b)

        if name == 'BEQ':
            truth = (aval == bval)
        elif name == 'BNE':
            truth = (bval != aval)

        if truth:
            self.j('J',addr)
        else:
            self.pcinc()
    
    def mult(self,name,a,b):
        aval = self.regs.get(a)
        bval = self.regs.get(b)

        if name == 'MULT' or name == 'MULTU':
            aval *= bval
            
        # We're going to store high and low just cause
        hi = (aval & 0xFFFFFFFF00000000) >> 0x20
        lo = (aval & 0x00000000FFFFFFFF)
        self.regs.set('hi',int(hi),special = True)
        self.regs.set('lo',lo, special = True)
        self.pcinc()


    def div(self,name,a,b):
        aval = self.regs.get(a)
        bval = self.regs.get(b)

        if name == 'DIV' or name == 'DIVU':
            hi = aval / bval
            lo = aval % bval
       
        self.regs.set('hi',hi, special = True)
        self.regs.set('lo',lo, special = True)
        self.pcinc()

    def mfhi(self,name,to):
        if name == 'MFHI':
            val = self.regs.get('hi')
        elif name == 'MFLO':
            val = self.regs.get('lo')

        self.regs.set(to,val)
        self.pcinc()

    def nop(self,name):
        self.pcinc()


    def _ret_conv(self,val):
        if type(val) == int:
            return val
        try:
            res = int(val)
        except:
            res = 0xdeadbeef

        return res



    def pyeval(self,name,code):
        code = code[1:-1]
        res = eval(code)
        if type(res) in [list,tuple]:
            res0,res1 = res
            res0 = self._ret_conv(res0)
            res1 = self._ret_conv(res1)
            self.regs.set('$v0',res0)
            self.regs.set('$v1',res1)
        else:
            res = self._ret_conv(res)
            self.regs.set('$v0',res)

        self.pcinc()

    def pycall(self,name,func):
        args = [self.regs.get('$a0'),self.regs.get('$a1'),self.regs.get('$a2'),self.regs.get('$a3')]
        args = repr(tuple(filter(lambda x: x != 0,args)))
        code = '"' + func + args + '"'
        self.pyeval("PYEVAL",code)
    
    def pyexec(self,name,code):
        eval(code)
        self.pcinc()

    def pysyscall(self,name,func):
        args = (self.regs.get('$a0'),self.regs.get('$a1'),self.regs.get('$a2'),self.regs.get('$a3'))
        code = '"' + func + '(self,' + repr(args) + ')"'
        self.pyeval("PYEVAL",code)
       



    def _addr_decode(self,addr):
        import re
        match = re.match("((\d+)?\((.*?)\)|(.*))",addr)
        if match:
            g = match.groups()
            if g[1]:
                offset = int(g[1])
            else:
                offset = 0

            if g[2]:
                reg = g[2]
            elif g[3]:
                reg = g[3]

        else:
            offset = 0
            reg = '$0'

        return offset,reg


    def lw(self,name,reg,addr):
        off,srcreg = self._addr_decode(addr)
        addr = self.regs.get(srcreg) + off

        if name == 'LW':
            self.regs.set(reg,self.mem.get(addr,4))
        elif name == 'SW':
            self.mem.set(addr,4,self.regs.get(reg))

        self.pcinc()


    def loader(self,code):
        self.mem.rom(0,code)

    def execute(self,args):
        inst = args[0]
        self.cmds[inst](*args)

    def run(self):
        while True:
            pc = self.regs.get('pc')
            inst = self.mem.rawget(pc)
            ij = []
            for e in inst:
                ij.append(str(e))
            ij[0] = "\033[1m" + ij[0] + "\033[0m"

            dbg = "\t\033[30m\033[1;34m*\033[0;37m%5d:\033[0m\t%s\033[0m\n" % (pc, " ".join(ij))
            sys.stderr.write(dbg)
            self.execute(inst)


print "*************** MVM *********************"
print "* ROM file....\t\t%s\t\t*" % (sys.argv[1]) 
cpu = Interp()

import json

f = open(sys.argv[1]).read()
f = json.loads(f)

cpu.loader(f)

print "* CPU...\t\tInterp          *"
print "* Coprocessor 0....\tNone\t\t*"
print "* Coprocessor 1....\tNone\t\t*"
print "*****************************************"
print ""
cpu.run()

