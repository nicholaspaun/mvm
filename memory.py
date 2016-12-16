from errors import MVMErr

class Memory():
    def __init__(self,size):
        self.size = (size * 2**10)
        self.mem = [0] * self.size

    def get(self,base,sz):
        if base % sz != 0:
            raise KeyError(MVMErr.addr_align,base,sz)

        try:
            return self.unbyte(self.mem[base:base + sz])
        except ValueError:
            raise KeyError(MVMErr.addr_invalid,addr)


    def unbyte(self,data):
        work = 0
        sz = len(data) - 1

        for i in range(0,sz + 1):
            work |= data[sz - i] << (i * 8)

        return work

    def debug(self,addr,sz):
        print self.mem[addr:addr + sz]

    def byteify(self,sz,val):
        data = [0] * sz
        data[sz - 1] = val & 0xFF

        i = sz - 2
        while val != 0:
            val >>= 8
            byte = val & 0xFF
            data[i] = byte
            i -= 1

        return data

    def set(self,base,sz,val):
        if base % sz != 0:
             raise KeyError(MVMErr.addr_align,base,sz)

        self.mem[base:base + sz] = self.byteify(sz,val)

    def reset(self):
        self.mem = [0] * self.size()

    # Cheating....
    def rawget(self,addr):
        return self.mem[addr]

    def rom(self,base,roml):
        self.mem[base: base + 4 * len(roml):4] = roml

