use std::io;
fn main() {
    println!("Guessing game!");

    println!("Enter a number : ");

    let mut number = String::new();
    io::stdin()
        .read_line(&mut number)
        .expect("Failed to read line");

    println!("You entered : {}", number);


}
