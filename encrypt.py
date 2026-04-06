import hashlib
import json
import unicodedata

def normalize(text):
    text = text.upper().replace(" ", "")
    # Remove accents/diacritics
    return "".join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

names = ["EINSTEIN", "ADA LOVELACE", "ALAN TURING", "TESLA"]
hashed_data = []

for name in names:
    clean_name = normalize(name)
    h = hashlib.sha256(clean_name.encode()).hexdigest()
    hashed_data.append({"length": len(clean_name), "hash": h, "hint": name[0]})

with open("names.json", "w") as f:
    json.dump(hashed_data, f)
