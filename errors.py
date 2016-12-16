class MVMErr:
    reg_invalid = {0: "Invalid register name"}
    reg_ro = {1: "Register cannot be written to"}
    reg_forbidden = {6: "Writing to this register is invalid."}
    operand_type = {2: "Operand is not an integer"}
    operand_overflow = {5: "Operand is larger than 1 word"}
    addr_invalid = {3: "Invalid memory address"}
    addr_align = {4: "Address not correctly aligned for size of read/write"}
