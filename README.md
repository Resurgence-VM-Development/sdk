# Resurgence SDK
This repository contains the software development kit (SDK) for working with
Resurgence, either for developing programs that run inside of Resurgence, or
for developing host projects that incorporate a
[Resurgence Virtual Machine](https://github.com/Resurgence-VM-Development/Resurgence).

## Contents
The Resurgence SDK contains the following:
- `rasm`: a basic implementation of an assembly compiler and bytecode generator
  that is compatible with Resurgence
- `rvmtest`: a sample implementation of a host program that executes Resurgence
  code using a Resurgence Virtual Machine
- `sample-programs`: Examples of programs that can be compiled with `rasm` and
  executed using the `rvmtest` program

Each directory contains its own explanation of its contents and how to use
them.
