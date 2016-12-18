from errors import MVMErr

class Registers:
    REGS_SPECIAL = 32
    REGS_TOTAL = 35
    VALUE_MAX = 2**32 - 1

    def __init__(self):
        self.regs = [0] * self.REGS_TOTAL

    def number(self,reg):
        if reg[0] == '$' and reg[1:].isdigit():
            return int(reg[1:])
        else:
            try:
                if reg[0] == '$':
                    return self.number.map.index(reg[1:])
                else:
                    return self.number.special.index(reg) + self.REGS_SPECIAL
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

        if val > self.VALUE_MAX:
            raise ValueError(MVMErr.operand_overflow,val)

        reg = self.number(reg)
        if reg >= self.REGS_SPECIAL and not special:
            raise Exception(MVMErr.reg_forbidden,reg)
        elif reg == 0:
            raise TypeError(MVMErr.reg_ro,reg)
        else:
            self.regs[reg] = val
        
    def reset(self):
        self.__init__()

    def display(self):
        print "\033[34m"
        for i in range(0,self.REGS_SPECIAL):
            print "%2d\t$%2s\t%10d" % (i,self.number.map[i],self.regs[i])

        for i in range(0,3):
            print "%2d\t %2s\t%10d" % (i + self.REGS_SPECIAL, self.number.special[i],self.regs[i + self.REGS_SPECIAL])
        print "\033[0m\n"
