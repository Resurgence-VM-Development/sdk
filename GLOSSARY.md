# Resurgence Glossary
This document aims to outline some of the terminology used in the Resurgence
project, since it might not be very intuitive.

## Bytecode
Bytecode is a portable representation of a codeholder in the form of a file.
Bytecode files are designed to work with different Resurgence versions and be
compatible with a wide variety of environments.

## Codeholders
A codeholder is a data structure used in Resurgence that contains the list of
instructions used by a program, list of requested extcall functions / features,
and all constant data values in the program.

## Frontend
In a hypothetical use case for Resurgence, A frontend is a host application
that provides an interpreted programming language to its users and translates
the language to Resurgence assembly instructions. Thus, in such a deployment,
Resurgence itself would be the Backend, responsible for executing those
instructions.

## Host Application / Embedding Application
The host application or embedding application is software that incorporates
(aka "hosts") a Resurgence Virtual Machine inside of it.

## Interpreter
An interpreter is a data structure that represents a Resurgence Virtual Machine
in its configured and operable state. It contains a codeholder, as well as
linking information that maps function registrations to extcall numbers, and
all active memory used by the virtual machine.

