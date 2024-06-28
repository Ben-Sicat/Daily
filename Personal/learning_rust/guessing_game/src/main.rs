use std:: io;
use rand::Rng;
use std::cmp::Ordering;
fn main() {
    println!("Guessing game!");

    println!("Enter a number : ");
    
    let secret_number = rand::thread_rng().gen_range(1..=10);
    loop{
        println!("Pleast enter a new number:");
            let mut number = String::new();
            io::stdin()
                .read_line(&mut number)
                .expect("Failed to read line");
            
            let number : u32 = match number.trim().parse(){
                Ok(num) => num,
                Err(_) => continue,
            };
            println!("Your guess is: {number}");
            println!("The secret number is: {secret_number}");
            match number.cmp(&secret_number){
                Ordering:: Less => println!("Too small!"),
                Ordering:: Greater => println!("Too big!"),
                Ordering:: Equal =>{
                   println!("You win!");
                   break; 
            }     
        }
    }
}
