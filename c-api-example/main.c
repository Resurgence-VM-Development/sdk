#include <stdio.h>
#include "resurgence.h"
#include <stdint.h>

/*
 * printString extcall
 * Accepts a string from the Stack and prints it to the terminal.
 */
uint8_t print_string(struct RVMState* state) {
  char* value;
  
  // Retrive a string value from the VM's stack.
  if(rvm_state_get_string(state, &value)) {
    // No string on the stack
    printf("printString called, but failed to get value\n");
    // Returning anything other than 0 triggers a fault and halts VM execution
    return 1;
  }

  printf("printString called: %s\n", value);
  
  // Free the string's memory
  rvm_string_free(value);
  
  // Indicate success and return execution to the program
  return 0;
}

/*
 * printNumber extcall
 * Accepts a number from the Stack and prints it to the terminal.
 */
uint8_t print_number(struct RVMState* state) {
  int64_t value;
  
  // retrieve an integer value from the VM's stack.
  if(rvm_state_get_integer(state, &value)) {
    // No integer on the stack
    printf("printNumber called, but failed to get value\n");
    // Returning anything other than 0 triggers a fault and halts VM execution
    return 1;
  }

  printf("printNumber called: %ld\n", value);
  
  // Indicate success and return execution to the program
  return 0;
}


int main(int argc, char* argv[]) {
  if(argc < 2) {
    printf("Usage: main [path to rvm file]\n");
    return 1;
  }

  char* path = argv[1];
  printf("File path to execute: %s\n", path);


  // Read a bytecode file and create a Codeholder
  struct RVMCodeHolder* ch = rvm_read_bytecode_file(path);
  if(ch == 0) {
    printf("Failed to read bytecode and create codeholder\n");
    return 1;
  }

  printf("CodeHolder ptr: %p\n", ch);

  // Create an Interpreter using the Codeholder
  // after this point, the Codeholder instance must not be used.
  struct RVMInterpreter* inter = rvm_interpreter_new(ch);
  if(inter == 0) {
    printf("Failed to create interpreter instance\n");
    return 1;
  }
  printf("Interpreter ptr: %p\n", inter);

  // Register the "printNumber" extcall
  if(rvm_interpreter_register_function(inter, print_number, "printNumber")) {
    printf("Failed to register print_number\n");
    return 1;
  }
  printf("pn registered\n");

  // Register the "printString" extcall
  if(rvm_interpreter_register_function(inter, print_string, "printString")) {
    printf("Failed to register print_string\n");
    return 1;
  }
  printf("ps registered\n");

  // Force extcalls to resolve (optional step)
  if(rvm_interpreter_resolve_imports(inter)) {
    printf("Failed to resolve imports\n");
    return 1;
  }

  printf("Everything succeeded, starting VM!\n");

  // Execute the "main" function inside the VM
  if(rvm_interpreter_execute_function(inter, "main")) {
    printf("Execution of main() failed\n");
    return 1;
  }

  printf("Successfully executed! Cleaning up now\n");

  // Clean up
  rvm_interpreter_destroy(inter);

  printf("All done!\n");

  return 0;
}
