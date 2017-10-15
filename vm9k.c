#include <stdio.h>
#include <stdlib.h>


#define FETCH(base) (unsigned int)(mem[(base)] << 24 | mem[(base) + 1] << 16 | mem[(base) + 2] << 8 | mem[(base) + 3])
#define PUT(data,base) mem[(base)] = ((data) & 0xFF000000) >> 24; mem[(base) + 1] = ((data) & 0x00FF0000) >> 16; mem[(base) + 2] = ((data) & 0x0000FF00) >> 8; mem[(base) + 3] = ((data) & 0x000000FF) >> 0;
#define NPUT(a,b,c,d,base) mem[(base)] = a; mem[(base) + 1] = b; mem[(base) + 2] = c; mem[(base) + 3] = d;

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
	SDC1 = 0x3d
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
	SRA = 0x3,
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


unsigned char mem[1048576] = {0};
unsigned int regs[32] = {0};
unsigned int spec[3] = {0};
unsigned int pc = 0;
unsigned int lo = 0;
unsigned int hi = 0;

#define NEXT pc += 4; break;
#define RD regs[i.rd]
#define RS regs[i.rs]
#define RT regs[i.rt]
#define IMM i.imm

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
			RD = (RS < RT) ? 1 : 0;
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

void exec_j(jfmt_s i) {
	switch (i.op) {
		case J:
			pc = (pc & 0xF0000000) | (i.target << 2);
			break;
		case JAL:
			regs[31] = pc + 8; // Textbook says 8 but seems wrong
			pc = (pc & 0xF0000000) | (i.target << 2);
			break;
	}
}

void exec_i(ifmt_s i) {
	switch (i.op) {
		case ADDI:
			printf("%d\n",(int) IMM);
			RT = (int) RS + (int) IMM;
			NEXT
		case ADDIU:
			RT = RS + IMM;
			NEXT

		case ANDI:
			RT = RS & IMM;
		      	NEXT

		case BEQ:
			pc += 4 + (((RS == RT) ? IMM : 0) << 2);
			break;

		case BNE:
			pc += 4 + (((RS != RT) ? IMM : 0) << 2);
			break;

		case LBU:
			RT = FETCH(RS + IMM) >> 24;
			NEXT

		case LHU:
			RT = FETCH(RS + IMM) >> 16;
			NEXT

		case LL:
			NEXT

		case LUI:
			RT = FETCH(RS + IMM) << 16;
			NEXT
		
		case LW:
			RT = FETCH(RS + IMM);
			NEXT

		case ORI:
			RT = RS | IMM;
			NEXT

		case SLTI:
			RT = (int) RS < (short) IMM ? 1 : 0;
			NEXT

		case SLTIU:
			RT = RS < IMM ? 1 : 0;
			NEXT

		case SB:
			NEXT

		case SC:
			NEXT

		case SH:
			NEXT


		case SW:
			PUT(RT,RS + IMM)
			NEXT

		case LWC1:
			printf("$$$ FLOATING POINT COPROCESSOR NOT INSTALLED\n");
			NEXT

		case LDC1:
			printf("$$$ FLOATING POINT COPROCESSOR NOT INSTALLED\n");
			NEXT

		case SWC1:
			printf("$$$ FLOATING POINT COPROCESSOR NOT INSTALLED\n");
			NEXT


		case SDC1:
			printf("$$$ FLOATING POINT COPROCESSOR NOT INSTALLED\n");
			NEXT

	}
}

void show_regs(void) {
	for (int i = 0; i < 32; i++) {
		printf("%2d = %8x %8d\n",i,regs[i],(int) regs[i]);
	}
}

void exec(inst_u test) {
	printf("0x%08X\n",test.n);
	if (test.n == 0xFFFFFFFF) {
		show_regs();
		printf("$$$ VM HALTED $$$\n");
		exit(0);
	}

	if (test.r.op == RFMT) 
		exec_r(test.r);
	else if (test.j.op == J || test.j.op == JAL)
		exec_j(test.j);
	else
		exec_i(test.i);
}


int main(int argc, char** argv) {
	NPUT(0x01,0x2a,0x40,0x20,0);
	NPUT(0x20,0xa5,0xff,0xff,4);
	NPUT(0xff,0xff,0xff,0xff,8);

	for (;;) {
		printf("[%x] \t",pc);
		exec((inst_u) FETCH(pc));
	}
}
