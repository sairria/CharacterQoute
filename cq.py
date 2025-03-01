from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import csv
import random
import pandas as pd

# Define the data
data = {
    "Character": ["Barbie", "Ken", "Raquelle", "Skipper", "Stacie", "Chelsea", "Nikki", "Midge", "Terry", "Simba"],
    "Quote": [
        "I can do anything I set my mind to!",
        "I'm just going to go ahead and say it: I'm awesome.",
        "Oh, this? It's just a little something I threw together.",
        "I don't think that's such a great idea.",
        "I'm just going to try to make things better.",
        "Let's have some fun!",
        "It's so much fun to try new things!",
        "I’m all about the adventure.",
        "You got it, Barbie! I'm your number one fan!",
        "Woof!"
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("barbie_living_in_the_dreamhouse_quotes.csv", index=False)

print("CSV file created successfully!")

app = FastAPI()

# Define a Pydantic model for characters
class Character(BaseModel):
    name: str
    quote: str

# Load characters and quotes from CSV files
characters = []
with open('barbie_living_in_the_dreamhouse_quotes.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        characters.append(Character(name=row['Character'], quote=row['Quote']))

#Create quotes.csv
with open('quotes.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for quote in data['Quote']:
        writer.writerow([quote])

quotes = []
with open('quotes.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        quotes.append(row[0])

# Define routes
@app.get("/characters")
async def get_characters():
    """Return a list of all characters."""
    return [character.dict() for character in characters]

@app.get("/characters/{name}")
async def get_character(name: str):
    """Return a specific character by name."""
    for character in characters:
        if character.name == name:
            return character.dict()
    raise HTTPException(status_code=404, detail="Character not found")

@app.post("/create_characters")
async def create_character(character: Character):
    """Create a new character and add it to the CSV file."""
    with open('barbie_living_in_the_dreamhouse_quotes.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Character', 'Quote'])
        writer.writerow({'Character': character.name, 'Quote': character.quote})
    characters.append(character)
    return {"message": "Character created"}

@app.get("/quote")
async def get_quote():
    """Return a random quote."""
    return {"quote": random.choice(quotes)}