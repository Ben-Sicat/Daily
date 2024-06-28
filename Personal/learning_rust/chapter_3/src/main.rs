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
