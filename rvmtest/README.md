# Resurgence Test VM
RVMTest is a sample implementation of using the Resurgence VM in a
host program. It is used for executing the sample programs in the SDK, and
for benchmarking different components of Resurgence.

## Building
RVMTest requires the Rust toolchain to build. Once this need is met, build
the program using the following command:
```
cargo build --release
```

If you want debugging features to be available, and don't care about
performance, compile in debug mode:
```
cargo build
```

## Usage
To use RVMTest, the syntax is as follows:
```
./target/release/rvmtest [path to rvm bytecode file]
```
If you compiled in debug mode, invoke `./target/debug/rvmtest` instead.

RVMTest works out-of-box with any of the sample programs provided in the
`sample-programs` directory of the Resurgence SDK.

## Built-in External Calls
RVMTest provides the following external calls which may be used by sample
programs:
- `printNumber`: accepts an integer from the stack and prints a number to
  STDOUT and a new line character (\n)
- `printString`: accepts a string from the stack and prints it to STDOUT along
  with a new line character (\n)

