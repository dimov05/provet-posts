import json
import os

# --- КОНФИГУРАЦИЯ ---
TRELLO_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trello_export.json")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts")
# --------------------

def parse_trello():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not os.path.exists(TRELLO_JSON_PATH):
        print(f"Грешка: Файлът {TRELLO_JSON_PATH} не е намерен.")
        return

    with open(TRELLO_JSON_PATH, "r", encoding="utf-8") as f:
        trello_data = json.load(f)
        
    cards = trello_data.get("cards", [])
    count = 0
    
    for card in cards:
        # Пропускаме архивираните (затворени) карти
        if card.get("closed"):
            continue
            
        name = card.get("name", "Untitled")
        desc = card.get("desc", "")
        
        # Извличане на датата (Due Date), ако има такава
        due = card.get("due")
        if due:
            # Trello формат: 2023-10-15T14:30:00.000Z
            date_str = due[:10]
            time_str = due[11:16]
        else:
            date_str = "TBD"
            time_str = "TBD"
            
        # Генериране на уникално име за файла
        filename = f"Trello_{date_str}_{card['id'][:6]}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Запазване на файла
        with open(filepath, "w", encoding="utf-8") as md_file:
            md_file.write("---\n")
            md_file.write(f"status: planned\n") # Маркираме ги като планирани
            md_file.write(f"date: {date_str}\n")
            md_file.write(f"time: {time_str}\n")
            md_file.write(f"trello_title: \"{name}\"\n")
            md_file.write("---\n\n")
            md_file.write(desc.strip())
            
        count += 1
        
    print(f"Успех! {count} активни карти от Trello бяха превърнати в Markdown.")

if __name__ == "__main__":
    parse_trello()