use serde::{Deserialize, Serialize};
use std::error::Error;
use std::fs::File;
use std::io;

#[derive(Debug, Serialize, Deserialize)]
struct Person {
    name: String,
    age: u32,
    city: String,
}

fn main() -> Result<(), Box<dyn Error>> {
    // 写入 CSV 文件
    let people = vec![
        Person { name: "Alice".to_string(), age: 30, city: "New York".to_string() },
        Person { name: "Bob".to_string(), age: 25, city: "Los Angeles".to_string() },
        Person { name: "Charlie".to_string(), age: 35, city: "Chicago".to_string() },
    ];

    let file = File::create("people.csv")?;
    let mut wtr = csv::Writer::from_writer(file);

    for person in people {
        wtr.serialize(person)?;
    }

    wtr.flush()?;

    // 读取 CSV 文件
    let file = File::open("people.csv")?;
    let mut rdr = csv::Reader::from_reader(file);

    for result in rdr.deserialize() {
        let person: Person = result?;
        println!("{:?}", person);
    }

    Ok(())
}