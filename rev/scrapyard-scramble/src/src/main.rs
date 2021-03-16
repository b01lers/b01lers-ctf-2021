use std::io::{stdin, stdout, Write};
use rand::Rng;

static FLAG: &[u8; 33] = include_bytes!("flag.enc");

struct Customer<'a> {
    money_to_spend: u32,
    items: Vec<(&'a str, u32)>
}

impl<'a> Customer<'a> {
    pub fn new(budget: u32) -> Self {
        Customer {
            money_to_spend: budget,
            items: Vec::new()
        }
    }
    pub fn add_item(&mut self, item: &'a str, price: u32) {
        self.items.push((item, price))
    }

    fn total_price(&self) -> u32 {
        self.items.iter().map(|(_, price)| price).sum::<u32>()
    }

    pub fn in_budget(&self) -> bool {
        self.total_price() <= self.money_to_spend
    }

    pub fn remove_item(&mut self, idx: usize) -> Result<(&'a str, u32), ()> {
        if idx < self.items.len() {
            return Ok(self.items.remove(idx));
        }
        Err(())
    }

    pub fn print_cart(&self) {
        for item in self.items.iter().enumerate() {
            println!("{}: {}, ${}", item.0, item.1.0, item.1.1);
        }
        println!("Total: ${}", self.total_price())
    }

    pub fn wallet(&self) -> u32 {
      self.money_to_spend
    }
}


fn main() {
    let mut rng = rand::thread_rng();
    let mut shopper = Customer::new(200);
    println!("Welcome to the scrapyard, choose whatever catches your eye");
    let items = [("Engine block", 100), ("Old fridge", 100), ("Shiny tea kettle", 25), ("Car battery", 30), ("A big mirror", 75)];
    loop {
        print_menu();
        let choice = get_choice();
        match choice {
          0 => { // Search and maybe add an item
            let item = items[rng.gen_range(0..items.len())];
            println!("You found a {} for ${}, ya want it?", item.0, item.1);
            println!("[0] No");
            println!("[1] Yes");
            let mut choice = -1;
            while choice < 0 {
              choice = match get_choice() {
                0 => 0,
                1 => 1,
                _ => -1
              }
            }
            if choice == 1 {
              shopper.add_item(item.0, item.1);
            }
          },
          1 => { // Print cart
            shopper.print_cart();
          },
          2 => { // Checkout
            if shopper.in_budget() {
              println!("Thank you for shopping");
              std::process::exit(0);
            } else {
              println!("Either come back later with more money, or remove some items from your cart");
            }

          },
          3 => { // Remove item
            print!("Which item do you wanna remove");
            stdout().flush().unwrap_or(());
            let idx = get_choice();
            if idx < 0 {
              println!("You what!?!??!");
            }
            match shopper.remove_item(idx as usize) {
              Ok(item) => println!("Good bye to the {}", item.0),
              Err(()) => println!("What are you doing?"),
            }

          },
          4 => {
            println!("You have ${} in your wallet", shopper.wallet())
          }
          5 => { // Leave
            println!("Bye!!");
            std::process::exit(0);
          },
          1337 => { // Apply discount
            print!("What's the discount code: ");
            stdout().flush().unwrap_or(());
            let input = get_input();
            if check_input(input.as_str(), FLAG) {
              std::process::exit(0);
            } else {

              std::process::exit(1);
            }
          },
          _ => println!("Not a valid choice")
        }


    }

}

fn print_menu() {
    println!("\nWould you like to:");
    println!("[0] Search for an item");
    println!("[1] Check your cart");
    println!("[2] Checkout");
    println!("[3] Remove an item from your cart");
    println!("[4] Check wallet");
    println!("[5] Leave\n");
}


fn get_choice() -> i32 {
  print!("What do you wanna do? ");
  stdout().flush().unwrap_or(());
  let mut choice = -1;
  while choice < 0 {
      choice = get_input().parse::<i32>().unwrap_or(-1);
      if choice < 0 {
          println!("Ya gotta give me a number");
      }
  }
  choice
}

fn get_input<'a>() -> String {
  let mut input = String::new();
  stdin().read_line(&mut input).expect("Ya gotta gimme something to work with");
  if let Some('\n') = input.chars().next_back() {
      input.pop();
  }
  if let Some('\r') = input.chars().next_back() {
      input.pop();
  }
  input
}

fn check_input(input: &str, flag: &[u8; 33]) -> bool {
    if input.len() != flag.len() {
        println!("You think you're slick huh?");
        false
    } else if input.chars().enumerate().map(|(i, c)| ((c as usize) ^ (i * i) % 256) as u8 == flag[i] ).all(|e| e) {
        println!("Your cart's on the house today!");
        true
    } else {
        println!("You think you're slick huh?");
        false
    }

}
