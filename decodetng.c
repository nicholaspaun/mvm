#include <stdio.h>


typedef enum {
	RFMT = 0x0,
	ADDI = 0x8,
	ADDIU = 0x9,
	ANDI = 0xC,
	BEQ = 0x4,
	BNE = 0x5,
	J = 0x2,
	JAL = 0x3,
	LBU = 0x24,
	LHU = 0x25,
	LL = 0x30,
	LUI = 0xF,
	LW = 0x23,
	ORI = 0xD,
} op_e;

typedef enum {
	ADD = 0x20,
	ADDU = 0x21,
	AND = 0x24,
	JR = 0x8,
	NOR = 0x27,
	OR = 0x25,
	SLT = 0x2A,
} funct_e;

typedef struct {
	funct_e      funct: 6;
	unsigned int shamt: 5,
		     rd: 5,
		     rt: 5,
		     rs: 5;
	op_e	     op: 6;
} rfmt_s;

typedef struct {
	short imm;
	unsigned short rt: 5,
		       rs: 5;
	op_e	       op: 6;
} ifmt_s;

typedef struct {
	unsigned int target: 26;
	op_e	     op: 6;
} jfmt_s;

typedef union {
	rfmt_s r;
	ifmt_s i;
	jfmt_s j;
	unsigned int n;
} inst_u;



void decode(inst_u test) {
	printf("0x%08X\n",test.n);
	if (test.r.op == RFMT) 
		printf("<R> OP[%d] RS[%d] RT[%d] RD[%d] SHAMT[%d] FUNCT[%d]\n",test.r.op,test.r.rs,test.r.rt,test.r.rd,test.r.shamt,test.r.funct);
	else if (test.j.op == J || test.j.op == JAL)
		printf("<J> OP[%d] TARGET[%d]\n",test.j.op,test.j.target);
	else
		printf("<I> OP[%d] RS[%d] RT[%d] IMM[%d]\n",test.i.op,test.i.rs,test.i.rt,test.i.imm);
}


int main(int argc, char** argv) {
	inst_u test;
	test.n = 0x0005402A;
	decode(test);
}
