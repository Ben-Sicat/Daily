fn main() {
    borrowing();
}
fn borrowing(){
    //refferencing and borrowing

    // so  here's how refferencing works in rust
    //  theres a concept called ownership in rust
    // ownership is a concept that is used to manage memory in rust
    // here's how it works

    let s1 = String::from("hello");
    let s2  = s1;
    //now s1 and s2 are pointing to the same memory location
    // this is because rust uses the concept of ownership
    // so if i do this
    // println!("{s1} world!");
    // this will give me an error because s1 is no longer valid


    // to work around this you can clone s1 to s2
    let s1 = String::from("hello");
    let s2 = s1.clone();
    println!("s1: {}, s2: {}", s1, s2);
    // but integers are stored on the stack so they are copied instead of moved
    let x = 5;
    let y = x;
    println!("x: {}, y: {}", x, y);
    // this will work because integers are stored on the stack

   fn functiong_ownership(){
       let s1 = gives_ownership();         // gives_ownership moves its return
                                        // value into s1

    let s2 = String::from("hello");     // s2 comes into scope

    let s3 = takes_and_gives_back(s2);  // s2 is moved into
                                        // takes_and_gives_back, which also
                                        // moves its return value into s3
    } // Here, s3 goes out of scope and is dropped. s2 was moved, so nothing
    // happens. s1 goes out of scope and is dropped.

    fn gives_ownership() -> String {             // gives_ownership will move its
                                                // return value into the function
                                                // that calls it

        let some_string = String::from("yours"); // some_string comes into scope

        some_string                              // some_string is returned and
                                                // moves out to the calling
                                                // function
    }

    // This function takes a String and returns one
    fn takes_and_gives_back(a_string: String) -> String { // a_string comes into
                                                        // scope

        a_string  // a_string is returned and moves out to the calling function
    }
    functiong_ownership();
}
