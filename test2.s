LI $t0 4
SLTI $t1 $t0 5 # 4 < 5
BEQ $t1 $0 err # if 4 < 5 is false, we've got a problem

LI $t0 5 
SLTI $t1 $t0 5 # 5 < 5
BNE $t1 $0 err # if 5 < 5 isn't false, we've got a problem

LI $t0 6
SLTI $t1 $t0 5 # 6 < 5
BNE $t1 $0 err # if 6 < 5 isn't false, we've got a problem

J ok # If the previous tests didn't fail, assume we did ok

err: # Print something to show we've got a problem.
	LI $a0 64
	ADDI $a0 $a0 6
	SYSCALL ml.putc
	jr $ra

ok: # Print something to show we don't
	LI $a0 64
	ADDI $a0 $a0 20
	SYSCALL ml.putc

	jr $ra
