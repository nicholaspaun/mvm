from errors import MVMErr

class Registers:
    def __init__(self):
        self.regs = [0] * 35

    def number(self,reg):
        if reg[0] == '$' and reg[1:].isdigit():
            return int(reg[1:])
        else:
            try:
                if reg[0] == '$':
                    return self.number.map.index(reg[1:])
                else:
                    return self.number.special.index(reg) + 32
            except ValueError:
                raise KeyError(MVMErr.reg_invalid,reg)

        
        raise KeyError(MVMErr.reg_invalid,reg)

    number.map = [
            'zero','at','v0','v1','a0','a1','a2','a3',
            't0','t1','t2','t3','t4','t5','t6','t7',
            's0','s1','s2','s3','s4','s5','s6','s7',
            't8','t9','k0','k1','gp','sp','fp','ra'
            ]

    number.special = ['pc','hi','lo']

    def get(self,reg):
        return self.regs[self.number(reg)]

    def set(self,reg,val,special = False):
        if type(val) != int:
            raise TypeError(MVMErr.operand_type,val)

        if val > (2**32 - 1):
            raise ValueError(MVMErr.operand_overflow,val)

        reg = self.number(reg)
        if reg > 31 and not special:
            raise Exception(MVMErr.reg_forbidden,reg)


        if reg == 0:
            raise TypeError(MVMErr.reg_ro,reg)
        else:
            self.regs[reg] = val
        
    def reset(self):
        self.regs = [0] * 35

    def display(self):
        print "\033[34m"
        for i in range(0,32):
            print "%2d\t$%2s\t%10d" % (i,self.number.map[i],self.regs[i])

        for i in range(0,3):
            print "%2d\t %2s\t%10d" % (i + 32, self.number.special[i],self.regs[i + 32])
        print "\033[0m\n"
