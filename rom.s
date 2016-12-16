boot:
	# We want to know that everything is working fine at the beginning.
	PYEVAL "sys.stdout.write('\033[1;35mROM Loaded.\033[0m\n')"

	# Set up the pointers so that important memory is not overwritten
	LI $sp 32760 #Initial stack pointer
	LI $gp 4000 #Abusing this register to store the point at which memory can be manipulated
	
	# Give main the arguments from the command-line
	PYEVAL "len(sys.argv)" # Ask Python -- How long is it?
	LI $t0 7 # This is the maximum argc we can handle because we have 4 arg registers

	BEQ $v0 $t0 argv_6 # Parse argv[6] and below
	SUBI $t0 $t0 1 # i--
	BEQ $v0 $t0 argv_5 # Parse argv[5] and below
	SUBI $t0 $t0 1 # i-- 
	BEQ $v0 $t0 argv_4 # You get the idea...
	SUBI $t0 $t0 1
	BEQ $v0 $t0 argv_3
	J argv_end

	argv_6:
		PYEVAL "sys.argv[6]" # Ask Python -- What is argv[6]?
		MOVE $a3 $v0 # Return values are in v0, v1. These become arguments to main.
	argv_5:
		PYEVAL "sys.argv[5]"
		MOVE $a2 $v0
	argv_4:
		PYEVAL "sys.argv[4]"
		MOVE $a1 $v0
	argv_3:
		PYEVAL "sys.argv[3]"
		MOVE $a0 $v0
	
	argv_end:

	LI $t0 0 # Blast the temporary variable, so everything is clean for main
 
	# Tell the user we're done doing the setup
	PYEVAL "sys.stdout.write('\033[35mInitialized registers.\033[0m\n')"

	# Cheating a bit... 
	# Call Python: Open the program file, parse it as JSON, and load it into memory at the right point
	PYEVAL "self.mem.rom(512,json.loads(open(sys.argv[2]).read()))"
	PYEVAL "sys.stdout.write('\033[1;32mProgram loaded at address 512.\033[0;35m Jumping.\033[0m\n\n')"

	# Bye-Bye
	JAL 512

halt:
	# We're back
	PYEVAL "sys.stdout.write('\n\033[1;32mProgram ended.\033[0;35m Halting.\033[0m\n')"
	# Tell Python to shut down
	PYEVAL "sys.exit(0)"
