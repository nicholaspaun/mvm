main:
	addiu $sp $sp -4
	sw $ra ($sp)
	move $s1 $a0

	jal load
	jal debug
	move $a0 $s1 
	jal test
	jal print_array
	
	lw $ra ($sp)
	addiu $sp $sp 4
	jr $ra

load: # Load a series of values
	li $s0 1000
	li $t0 4
	sw $t0 4($s0)
	li $t1 2
	sw $t1 8($s0)
	li $t2 6
	sw $t2 12($s0)
	li $t3 9
	sw $t3 16($s0)
	li $t4 0
	sw $t4 20($s0)

	jr $ra

debug:
	no_args:
		LI $a0 0
		LI $a1 0
		LI $a2 0
		LI $a3 0

	call_python:
		PYJAL self.regs.display

	jr $ra

 
test:
	move $t0 $s0
	addi $t0 $t0 4
	li $t3 100
	loop:
		lw $t1 $t0
		
		slt $t2 $t1 $a0
		beq $t2 $0 end
		
		mult $t1 $t3
		mflo $t1
		sw $t1 $t0
		
		addiu $t0 $t0 4
		j loop
	end:
		jr $ra

print_array:
	move $t0 $s0
	addi $t0 $t0 4
	l2:
		lw $a0 $t0
		move $t1 $a0
		SYSCALL ml.putd
		
		li $a0 44
		SYSCALL ml.putc
		li $a0 32
		SYSCALL ml.putc

		beq $t1 $0 e2

		addiu $t0 $t0 4
		j l2
	e2:
		li $a0 10
		SYSCALL ml.putc
		jr $ra
