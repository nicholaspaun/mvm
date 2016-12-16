#!/usr/bin/env python
import sys

lines = open(sys.argv[1]).readlines()
labels = {}
pc = int(sys.argv[2])
prog = []

for l in lines:
    l = l.strip()
    if l == '':
        continue

    data = l.split("#")
    if len(data) == 2:
        code,comment = data
        code = code.strip()
    else:
        code, = data

    if code == '':
        continue

    if code[-1] == ':': #This is a label
        labels[code[:-1]] = pc
    else:
        if code[0:2] == "PY":
            inst = code.split(" ",1)
        else:
            inst = code.split(" ")

        inst[0] = inst[0].upper()
        for i in range(0,len(inst)):
            if inst[i].isdigit():
                inst[i] = int(inst[i])
            elif inst[i][0] == '-' and inst[i][1:].isdigit():
                inst[i] = int(inst[i])

        prog.append(inst)

        pc += 4

def label_replace(val):
    try:
        return labels[val]
    except:
        return val

for i in prog:
    opcode = i[0]
    if opcode == 'J' or opcode == 'JAL':
        i[1] = label_replace(i[1])

    if opcode == 'BEQ' or opcode == 'BNE':
        i[3] = label_replace(i[3])

import json

dest = open(sys.argv[1].replace(".s","") + ".o",'w')
dest.write(json.dumps(prog))
dest.close()

