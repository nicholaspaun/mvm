#include <stdio.h>
#include <stdlib.h>

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
	SLTI = 0xA,
	SLTIU = 0xB,
	SB = 0x28,
	SC = 0x38,
	SH = 0x29,
	SW = 0x2B,
	LWC1 = 0x31,
	LDC1 = 0x35,
	SWC1 = 0x39,
	SDC1 = 0x39
} op_e;

typedef enum {
	ADD = 0x20,
	ADDU = 0x21,
	AND = 0x24,
	JR = 0x8,
	NOR = 0x27,
	OR = 0x25,
	SLT = 0x2A,
	SLTU = 0x2B,
	SLL = 0x0,
	SRL = 0x2,
	SUB = 0x22,
	SUBU = 0x23,
	DIV = 0x1A,
	DIVU = 0x1B,
	MFHI = 0x10,
	MFLO = 0x12,
	MULT = 0x18,
	MULTU = 0x19,
	SRA = 0x3
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


unsigned int mem[65536] = {0};
unsigned int regs[32] = {0};
unsigned int spec[3] = {0};
unsigned int pc = 0;
unsigned int lo = 0;
unsigned int hi = 0;

#define NEXT pc += 4; break;
#define RD regs[i.rd]
#define RS regs[i.rs]
#define RT regs[i.rt]

void exec_r(rfmt_s i) {
	long cheating = 0;

	switch(i.funct) {
		case ADD:
			RD = (int) RS + (int) RT;
			NEXT
		case ADDU:
			RD = RS + RT;
			NEXT

		case SUB:
			RD = (int) RS - (int) RT;
			NEXT
		case SUBU:
			RD = RS - RT;
			NEXT

		case AND:
			RD = RS & RT;
			NEXT

		case JR:
			pc = RS;
			break;

		case NOR:
			RD = ~(RS | RT);
			NEXT

		case OR:
			RD = RS | RT;
			NEXT

		case SLT:
			RD = ((int) RS < (int) RT) ? 1 : 0;
			NEXT
		
		case SLTU:
			RD = (abs((int) RS) < abs((int) RT)) ? 1 : 0;
			NEXT

		case SLL:
			RD = RT << i.shamt;
			NEXT

		case SRL:
			RD = RT >> i.shamt;
			NEXT


		case DIV:
		case DIVU:
			lo = RS/RT;
			hi = RS%RT;
			NEXT

		case MFHI:
			RD = hi;
			NEXT

		case MFLO:
			RD = lo;
			NEXT
		
		case MULT:
		case MULTU:
			cheating = RS * RT;
			hi = cheating >> 16; // Higher order bits remain
			lo = cheating & 0x0000FFFF; //Mask out higher order bits
			NEXT

		case SRA:
			RD = RT >> i.shamt; // Close enough
			NEXT;

	}
}

void decode(inst_u test) {
	printf("0x%08X\n",test.n);
	if (test.r.op == RFMT) {
		printf("<R> OP[%d] RS[%d] RT[%d] RD[%d] SHAMT[%d] FUNCT[%d]\n",test.r.op,test.r.rs,test.r.rt,test.r.rd,test.r.shamt,test.r.funct);
		exec_r(test.r);
	}
	else if (test.j.op == J || test.j.op == JAL)
		printf("<J> OP[%d] TARGET[%d]\n",test.j.op,test.j.target);
	else
		printf("<I> OP[%d] RS[%d] RT[%d] IMM[%d]\n",test.i.op,test.i.rs,test.i.rt,test.i.imm);
}


int main(int argc, char** argv) {
	mem[0] = 0x12A4020;
	regs[9] = 10;
	regs[10] = -5;


	decode((inst_u) mem[pc]);
	printf("%d\n",regs[8]);
}
