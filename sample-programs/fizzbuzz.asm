# FizzBuzz
# This program implements the FizzBuzz challenge. It runs for 1 million
# iterations.
#
# Compile this using the "rasm" program included in the Resurgence SDK.

section constants
    0 => 1
    1 => 1000000
    2 => 0
    3 => "Fizz"
    4 => "Buzz"
    5 => 3
    6 => 5
    

section aliases
    one => const(0)
    zero => const(2)
    three => const(5)
    five => const(6)
    
    totalLoops => const(1)
    
    fizz => const(3)
    buzz => const(4)
    
    i => local(0)
    m => local(1)
    n => local(2)
    stackreg => local(3)

section imports
    printNumber
    printString

section exports
    main

section code
.printFizz
    STACKPUSH fizz
    EXTCALL printString
    STACKPOP
    RET
.printBuzz
    STACKPUSH buzz
    EXTCALL printString
    STACKPOP
    RET

.main
    ALLOC 4
    CPY i, one # dst, src

.loopstart
    # print the number
    # stackpush consumes the register, so we copy it to an otherwise unused register
    CPY stackreg, i
    STACKPUSH stackreg
    EXTCALL printNumber
    STACKPOP

    # do the math
    MOD m, i, three # m = i % 3
    MOD n, i, five # n = i % 5

    # Check fizz and buzz and print if necessary
    NOTEQUAL m, zero
    CALL printFizz
    NOTEQUAL n, zero
    CALL printBuzz
    
    # increment i and restart loop
    ADD i, i, one
    EQUAL i, totalLoops
    JUMP loopstart # not equal, restart loop
    RET # exit program

