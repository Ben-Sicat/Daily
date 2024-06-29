use std::io;
fn main() {
    
    chapter_3_1();
}

fn chapter_3_1(){
    // let x = 5;
    // println!("The value of x is: {}", x);
    // let x = 6;
    // println!("The value of x is: {}", x);
    // // this will cause errors cause variables are immutable by default in rust
    //code must be 
    let mut x = 6;
    println!("The value of x is: {}", x);
    x = 7;
    println!("The value of x is: {}", x);
    //expected output of x is 7
    
//#######################
// shadowing
//#######################
    //so shadowing in rust is when you declare a new variable with the same name as a previous variable
    //this is basically just reusing the variable name

    let y = 5;
    let y = y + 1;
    {
        let y = y * 2;
        println!("The value of y is: {}", y);
    }
    println!("The value of y is: {}", y);
   // expected output is 12 and then 6 
}

fn chapter_3_2(){
    //#######################
    // Data Types
    //#######################
    //Rust is a statically typed language, which means that it must know the types of all variables at compile time

    // scalar types represent a single value. Rust has four primary scalar types: integers, floating-point numbers, Booleans, and characters.   

    // examples
    //8 bit
    let x: i8 = 127; // -128 to 127
    let x: u8 = 255; // 0 to 255
    //16 bit
    let x: i16 = 32767; // -32768 to 32767
    let x: u16 = 65535; // 0 to 65535
    //32 bit
    let x: i32 = 2147483647; // -2147483648 to 2147483647
    let x: u32 = 4294967295; // 0 to 4294967295
    //64 bit
    let x: i64 = 9223372036854775807; // -9223372036854775808 to 9223372036854775807
    let x: u64 = 18446744073709551615; // 0 to 18446744073709551615
    //128 bit
    let x: i128 = 170141183460469231731687303715884105727; // -170141183460469231731687303715884105728 to 170141183460469231731687303715884105727
    let x: u128 = 340282366920938463463374607431768211455; // 0 to 340282366920938463463374607431768211455
    
    //############# 
    // Number Literals
    //#############
    // Number literals can be type annotated by adding the type as a suffix.
    // decimals
    let decimal = 98_222; // 98,222
    // hex
    let hex = 0xff; // 255
    // octal
    let octal = 0o77; // 63
    // binary
    let binary = 0b1111_0000; // 240
    // byte (u8 only)
    let byte = b'A'; // 65

    // note that if you mutate a variable it must be covered by the same type or it will result to an overflow
    // Tuples
    // A tuple is a general way of grouping together a number of values with a variety of types into one compound type. Tuples have a fixed length: once declared, they cannot grow or shrink in size.
    let tup: (i32, f64, u8) = (500, 6.4, 1);
    
    //arrays 
    // An array is a collection of multiple values of the same type. Arrays in Rust have a fixed length, like tuples.
    let a = [1, 2, 3, 4, 5];

    let a: [i32; 5] = [1, 2, 3, 4, 5];

    let a = [3; 5]; // [3, 3, 3, 3, 3]
    
    fn arrays(){
        let a = [1, 2, 3, 4, 5];
        
        println!("Please enter an array index.");

        let mut index = String::new();
        io::stdin().read_line(&mut index).expect("Failed to read line");
        let index: usize = index
        .trim()
        .parse()
        .expect("Index entered was not a number");
        
        let element = a[index];
        println!("the value is {element}");
    }
}
fn chapter3_3(){

    fn fn_with_parameter(x: i32){
        println!("The value of x is: {}", x);
    }
   // expressions
    // Expressions evaluate to something and return a value, while statements do not.
    // example of an expression
    let y = {
        let x = 3;
        x + 1
    };
    println!("The value of y is: {}", y);
    //expected output is 4
    

    // now let's talk about functions with return values

    fn five() -> i32{
        5

    }
    // the way functions work in rust is that the last line of the function is the return value
    // but it must match the data type of the function if you dont explicitly state a return statement
    fn is_even(num: i32) -> bool{
        if num % 2 == 0{
            return true;
        }
        false
    }

}
fn chapter3_5(){
    //control flow

    //if statements
    let number = 3;
    if number < 5 {
        println!("condition was true");
    } else {
        println!("condition was false");
    }

    //using if in a let statement
    let condition = true;
    let number = if condition { 5 } else { 6 };
    println!("The value of number is: {}", number);
    //expected output is 5
    // let cond = true;
    // let number = if cond { 5 } else { "six" };
    // println!("The value of number is: {}", number);
    //this will result in an error cause the data types are different
    

    //loops
    //loop
    //this is an infinite loop
    // loop {
    //     println!("again!");
       
    // }
    //while loop
    let mut number = 3;
    while number != 0 {
        println!("{}!", number);
        number = number - 1;
    }

    //for loop
    let a = [10, 20, 30, 40, 50];
    for element in a.iter() {
        println!("the value is: {}", element);
    }
    //expected output is 10, 20, 30, 40, 50

    //for loop with range
    for number in (1..10){
        println!("the value is: {}", number);
    }
    for number in (1..10).rev(){
        println!("the value is: {}", number);
    }

    //loop labels for disambiguation

    fn loop_disambiguation(){
        'outer: for x in 0..10{
            'inner: for y in 0..x{
                if x % y == 0{
                    continue 'outer;
                }
            }
        }
        let mut counter = 0;
        'counting_loop: loop{
            println!("the value is: {}", counter);
            let mut remaining = 10;
            loop{
                if remaining == 0{
                    break 'counting_loop;
                }
                remaining -= 1;
            }
        }
    }
}