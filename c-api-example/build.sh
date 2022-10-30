#!/bin/sh

# build the program
gcc -g -o main main.c -I../../resurgence/ -L../../resurgence/target/debug -lresurgence || exit 1

# run with
# LD_LIBRARY_PATH=target/debug ./main
