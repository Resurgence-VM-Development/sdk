#!/usr/bin/python3
#
# RASM: Resurgence Assembler
# Python implementation of an assembler for RVM bytecode
# 
# Version 2
#

import sys
import struct

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)
    
def require_len(i, inst, params, size):
    if len(params) != size:
        fail(f"Invalid instruction {inst} at line {i} (requires {size} parameters, got {len(params)})")

def make_i32(i):
    return i.to_bytes(4, byteorder='big', signed=True)
def make_u32(i):
    return i.to_bytes(4, byteorder='big', signed=False)
def make_i64(i):
    return i.to_bytes(8, byteorder='big', signed=True)
def make_u64(i):
    return i.to_bytes(8, byteorder='big', signed=False)
def make_f32(i):
    return struct.pack('>f', i)
def make_f64(i):
    return struct.pack('>d', i)
def make_str(i):
    return make_u64(len(i)) + i.encode('utf8')

# resolves registers and aliases and outputs corresponding bytecode
def resolve(field):
    paramStart = field.find("(")
    if paramStart > -1: # this is NOT an alias
        paramEnd = field.find(")")
        if paramEnd == -1: fail(f"Bad field \"{field}\", mismatched parenthesis")
        t = field[:paramStart].lower() # type of register
        if t == "accumulator": # accumulator doesn't accept a parameter, only empty parenthesis ()
            return make_u32(0) + b'\x02'
        
        p = int(field[paramStart + 1:paramEnd]) # parameter value
        if t == "local":
            return make_u32(p) + b'\x04'
        elif t == "global":
            return make_u32(p) + b'\x03'
        elif t == "const":
            return make_u32(p) + b'\x01'
        else:
            fail(f"Bad field {field} while resolving")
    else: # uses an alias, need to recursively resolve
        if field in aliases:
            return resolve(aliases[field])
        # unknown alias or field
        fail(f"Unknown field or alias \"{field}\"")

# resolves a referenceable field; same as resolve() except it also processes and outputs rref byte
def resolveRef(field):
    if field[0] == '*':
        return resolve(field[1:]) + b'\x02'
    return resolve(field) + b'\x01'

####################
#
# MAIN CODE
#
####################



if len(sys.argv) < 3:
    print("ERROR: Invalid usage! Use ./rasm.py <rasm file> <dest rvm file>")
    sys.exit(1)

filename = sys.argv[1]
dest = sys.argv[2]

# info storage
constants = []
constantNum = 0
imports = []
exports = []
aliases = dict()
instructionData = b""
instPlaces = dict()
instNumber = 0

with open(filename, 'r') as file:
    imode = 0
    code = False
    
    for i, text in enumerate(file):
    
        parts = text.split("#")[0].split()
        
        # skip blank lines
        if len(parts) == 0:
            continue
            
        #print(parts)
        #print(f"MODE: {imode}")
        if code == False:
            if parts[0].lower() == 'section':
                # change interpretation mode
                if len(parts) < 2:
                    fail(f"Bad section declaration at line {i}")
                
                sec = parts[1].lower()
                if sec == 'constants':
                    imode = 1
                    continue
                elif sec == 'imports':
                    imode = 2
                    continue
                elif sec == 'exports':
                    imode = 3
                    continue
                elif sec == 'aliases':
                    imode = 4
                    continue
                elif sec == 'code':
                    # end header parts and go to the code
                    code = True
                    continue
                else:
                    fail(f"Bad section type at line {i}")
            elif imode == 0:
                fail(f"Invalid field for unknown section at line {i}")
            elif imode == 1:
                # process constants
                if len(parts) < 3 or parts[1] != "=>":
                    fail(f"Invalid constant at line {i}")
                
                # FIXME: constants parser currently breaks comments
                cparts = text.split(None, 2)
                pos = int(cparts[0])
                val = cparts[2].strip()
                
                if pos != constantNum:
                    fail(f"Bad constant index at line {i} (expected {constantNum}, got {pos})")
                
                # try to process string
                if (val[0] == '"' and val[-1] == '"') or (val[0] == "'" and val[-1] == "'"):
                    constants.insert(pos, val[1:-1])
                    constantNum += 1
                    continue

                # try to process boolean
                if val.lower() == "false":
                    constants.insert(pos, False)
                    constantNum += 1
                    continue
                elif val.lower() == "true":
                    constants.insert(pos, True)
                    constantNum += 1
                    continue
                
                # try to process int
                try:
                    constants.insert(pos, int(val))
                    constantNum += 1
                    continue
                except ValueError:
                    pass

                # try to process float
                try:
                    constants.insert(pos, float(val))
                    constantNum += 1
                    continue
                except ValueError:
                    # give up
                    fail(f"Could not determine type of constant at line {i}")
                    
            elif imode == 2:
                # process imports
                imports.append(parts[0])
            
            elif imode == 3:
                # process exports
                exports.append(parts[0])
            
            elif imode == 4:
                # process aliases
                if len(parts) < 3 or parts[1] != "=>":
                    fail(f"Invalid alias at line {i}")
                aliases[parts[0]] = parts[2]

        else:
            # process code
            if parts[0][0] == ".":
                # placeholders
                name = parts[0][1:]
                instPlaces[name] = instNumber
                print(f"Placeholder {name} at inst {instNumber}")
                continue
            
            # process instruction
            inst = parts[0].lower()
            params = []
            if len(parts) > 1:
                params = "".join(parts[1:]).split(",")
                
            print(f"Instruction {inst} with params {params}")
            
            data = b""
            
            # FIXME: CALL and JUMP only support previous placeholders currently
            # this is because of the way this loop is written
            # redesign this loop to fix
            
            if inst == 'alloc':
                require_len(i, inst, params, 1)
                data = b'\x01' + make_u32(int(params[0]))
            elif inst == 'framealloc':
                require_len(i, inst, params, 1)
                data = 'b\x15' + make_u32(int(params[0]))
            elif inst == 'free':
                require_len(i, inst, params, 1)
                data = b'\x02' + make_u32(int(params[0]))
            elif inst == 'framefree':
                require_len(i, inst, params, 1)
                data = b'\x16' + make_u32(int(params[0]))
            elif inst == 'jump':
                require_len(i, inst, params, 1)
                if params[0] not in instPlaces: fail(f"Invalid placeholder {params[0]} at line {i}")
                data = b'\x03' + make_i64(instPlaces[params[0]] - instNumber)
            elif inst == 'call':
                require_len(i, inst, params, 1)
                data = b'\x04' + make_u64(instPlaces[params[0]])
            elif inst == 'extcall':
                require_len(i, inst, params, 1)
                extcall = params[0]
                try:
                    data = b'\x05' + make_u64(imports.index(extcall))
                except ValueError:
                    fail(f"Invalid extcall \"{extcall}\" at line {i}")
            elif inst == 'ret':
                require_len(i, inst, params, 0)
                data = b'\x19'
            elif inst == 'mov':
                require_len(i, inst, params, 2)
                data = b'\x06' + resolveRef(params[0]) + resolveRef(params[1])
            elif inst == 'cpy':
                require_len(i, inst, params, 2)
                data = b'\x07' + resolveRef(params[0]) + resolveRef(params[1])
            elif inst == 'ref':
                require_len(i, inst, params, 2)
                data = b'\x08' + resolveRef(params[0]) + resolveRef(params[1])
            elif inst == 'stackpush':
                require_len(i, inst, params, 1)
                data = b'\x09' + resolveRef(params[0])
            elif inst == 'stackmov':
                require_len(i, inst, params, 1)
                data = b'\x17' + resolveRef(params[0])
            elif inst == 'stackpop':
                require_len(i, inst, params, 0)
                data = b'\x0A'
            elif inst == 'add':
                require_len(i, inst, params, 3)
                data = b'\x0B' + resolve(params[0]) + resolve(params[1]) + resolve(params[2])
            elif inst == 'sub':
                require_len(i, inst, params, 3)
                data = b'\x0C' + resolve(params[0]) + resolve(params[1]) + resolve(params[2])
            elif inst == 'mul':
                require_len(i, inst, params, 3)
                data = b'\x0D' + resolve(params[0]) + resolve(params[1]) + resolve(params[2])
            elif inst == 'div':
                require_len(i, inst, params, 3)
                data = b'\x0E' + resolve(params[0]) + resolve(params[1]) + resolve(params[2])
            elif inst == 'mod':
                require_len(i, inst, params, 3)
                data = b'\x18' + resolve(params[0]) + resolve(params[1]) + resolve(params[2])
            elif inst == 'equal':
                require_len(i, inst, params, 2)
                data = b'\x0F' + resolve(params[0]) + resolve(params[1])
            elif inst == 'notequal':
                require_len(i, inst, params, 2)
                data = b'\x10' + resolve(params[0]) + resolve(params[1])
            elif inst == 'greater':
                require_len(i, inst, params, 2)
                data = b'\x11' + resolve(params[0]) + resolve(params[1])
            elif inst == 'less':
                require_len(i, inst, params, 2)
                data = b'\x12' + resolve(params[0]) + resolve(params[1])
            elif inst == 'greaterequal':
                require_len(i, inst, params, 2)
                data = b'\x13' + resolve(params[0]) + resolve(params[1])
            elif inst == 'lessequal':
                require_len(i, inst, params, 2)
                data = b'\x14' + resolve(params[0]) + resolve(params[1])
            else:
                fail(f"Invalid instruction type {inst} at line {i}")
            
            print(f"Making {inst} at line {i} into {data.hex()}")
            instructionData += data
            instNumber += 1

print(f"Constants list: {constants}")
print(f"Imports list: {imports}")
print(f"Exports list: {exports}")
print(f"Aliases: {aliases}")

print("Final data")
print(instructionData.hex())


# Write bytecode file
with open(dest, 'wb') as out:
    out.write(b'RVM\x88' + b'\x00\x05') # header (magic + ver)
    
    # constants table
    out.write(make_u32(len(constants)))
    for i in constants:
        print(f"Constant: {i}")
        if isinstance(i, str):
            out.write(b'\x03' + make_str(i))
        elif isinstance(i, bool):
            if i: out.write(b'\x04\x01')
            else: out.write(b'\x04\x00')        
        elif isinstance(i, float):
            out.write(b'\x02' + make_f64(i))
        elif isinstance(i, int):
            out.write(b'\x01' + make_i64(i))
    
    # imports table
    out.write(make_u64(len(imports)))
    for i in imports:
        print(f"Import: {i}")
        out.write(make_str(i))
    
    # exports table
    out.write(make_u64(len(exports)))
    for i in exports:
        try:
            line = instPlaces[i]
            
            print(f"Export: {i} at {line}")
            out.write(make_str(i) + make_u64(line))
        except KeyError:
            fail(f"The placeholder \"{i}\" cannot be exported because it does not exist")
        
    # finally, write the code
    out.write(instructionData)

