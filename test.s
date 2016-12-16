main: 
	# We don't really automatically go to the main label, the way we should.
	# Instead, we start at the top of the file

	main__stack_save:
	# Save values to the stack
		addiu $sp $sp -8 # Bring the stack pointer down 2 words

		sw $ra ($sp) # Put in 1 word at the stack pointer
		# When a subroutine calls another subroutine, 
		# we need to save the original ra we were supposed to return from, 
		#so that when the subroutine returns to us, we know where to go.

		sw $s1 4($sp) # Put in 1 word at the stack pointer + 4
		# We always have to put back the saved registers the way we found them.
		# So, we make a copy we can restore at the end.

	main__arg_save:
	# Save our argument, because each subroutine call might need arguments, and so we'd have to overwrite a0
		move $s1 $a0

	jal load # Call the load subroutine
	jal debug # Call the debug subroutine

	move $a0 $s1 # Prepare a0 for test
	jal test # Call it

	jal print_array

	
	main__stack_restore:
		#Put back the stack, and the stuff we changed.
		lw $ra ($sp) # Bring back the return address
		lw $s1 4($sp) # Bring back $s1
		addiu $sp $sp 4 # Restore the tack pointer

	# Jump to the return address
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

	jr $ra # We don't call anything, so we can just do jr $ra, and have it work

debug:
	no_args:
		LI $a0 0
		LI $a1 0
		LI $a2 0
		LI $a3 0

	call_python:
		PYJAL self.regs.display # This isn't real MIPS code. Just something I made to call python from MIPS

	jr $ra # Return

 

# This subroutine will multiply any number in an array < a0 by 100. When the first element >= a0 is reached, it stops.
test:
	move $t0 $s0 # Copy the array address
	addi $t0 $t0 4 # We started storing at base + 4
	li $t3 100 # $t3 = 100
	loop:
		lw $t1 $t0 # Load the word from the address
		
		slt $t2 $t1 $a0 # t2 = t1 < a0
		beq $t2 $0 end # t2 != 0, goto end (so a0 >= t1 means goto end)
		
		mult $t1 $t3 # t1 * t3
		mflo $t1 # Get the lowest 32 bits of the answer
		sw $t1 $t0 # Put the word back in memory
		
		addiu $t0 $t0 4 # Increment the address by 4
		j loop # Repeat the loop
	end: # At the end of the loop
		jr $ra # Return to caller

# This prints out an array, stopping after element 0 is reached.
print_array:
	move $t0 $s0 # Copy array address
	addi $t0 $t0 4 # Start at $t0 + 4
	l2:
		lw $a0 $t0 # Load the number into a0
		move $t1 $a0 # Make a copy
		SYSCALL ml.putd # Print the number (syscall syntax isn't really like this)
		
		li $a0 44 # Set a0 = 44
		SYSCALL ml.putc # Print ASCII Char 44 (,)
		li $a0 32 # Set a0 = 32
		SYSCALL ml.putc # Print ASCII Char 32 (sapce)

		beq $t1 $0 e2 # When we find an element = 0, stop

		addiu $t0 $t0 4 # Increment address by 4
		j l2 # Repeat loop
	e2:
		li $a0 10 # ASCII 10 is newline
		SYSCALL ml.putc
		jr $ra # Return
