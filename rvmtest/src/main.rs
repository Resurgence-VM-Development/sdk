use resurgence::bytecode;
use resurgence::CodeHolder;
use resurgence::ExecutionEngine;
use resurgence::Interpreter;
use resurgence::ResurgenceState;
use std::env;
use std::io::Error;

fn print_number(state: &mut ResurgenceState) -> Result<(), Error> {
    let num = state.get_i64()?;
    println!("printNumber called: {}", num);
    Ok(())
}

fn print_string(state: &mut ResurgenceState) -> Result<(), Error> {
    let s = state.get_string()?;
    println!("printString called: {}", s);
    Ok(())
}

fn main() {
    if let Some(filename) = env::args().nth(1) {
        let code: CodeHolder = bytecode::read_bytecode_file(filename.as_str()).unwrap();
        println!("Num of instructions: {}", code.instructions.len());

        let mut it = Interpreter::from(code);

        it.register_function(print_number, "printNumber".to_string());
        it.register_function(print_string, "printString".to_string());
        it.resolve_imports().unwrap();

        //it.execute_instruction(0).unwrap();
        it.execute_function(&"main".to_string()).unwrap();
    } else {
        println!("Usage: ./rvmtest [path to program]");
        return;
    }
}
