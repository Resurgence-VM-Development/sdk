# Fibonacci Sequence
# This program prints the entire fibonacci sequence up to the maximum possible
# integer, and repeats the entire sequence calculation a total of 1024 times.
#
# Compile this using the "rasm" program included in the Resurgence SDK.

section constants
    0 => 1
    1 => 1024
    2 => 7540113804746346429
    3 => 0

section aliases
    one => const(0)
    maxTries => const(1)
    maxValue => const(2)
    zero => const(3)
    
    a => local(0)
    b => local(1)
    c => local(2)
    tempreg => local(3)
    triesCounter => local(4)

section imports
    printNumber

section exports
    main

section code
.main
    ALLOC 5
    CPY local(4), zero # dst, src

.calculator
    ADD local(4), local(4), one # increment r4
    CPY a, one
    CPY b, one
.somewhere
    ADD c, a, b # add A and B and store in C
    CPY a, b # copy B to A
    CPY b, c # copy C to B
    # print the answer
    CPY tempreg, b # copy answer to tempreg
    STACKPUSH tempreg
    EXTCALL printNumber
    STACKPOP
    
    # check if answer has reached the max value
    EQUAL c, maxValue
    JUMP somewhere # false
    # TRUE
    EQUAL local(4), maxTries # check if we should quit
    JUMP calculator # false
    RET # true, end program

