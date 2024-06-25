import json


def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def clean_annotations(data):
    cleaned_annotations = []
    
    for item in data["annotations"]:
        try:
            # Ensure each item is a tuple with two elements
            if not isinstance(item, list) or len(item) != 2:
                print(f"Skipping invalid entry: {item}")
                continue
            
            text, annotations = item
            
            # Ensure annotations is a dictionary and contains "entities" key
            if not isinstance(annotations, dict) or "entities" not in annotations:
                print(f"Skipping invalid entry: {annotations}")
                continue
            
            # Ensure entities is a list
            if not isinstance(annotations["entities"], list):
                print(f"Skipping invalid 'entities' value: {annotations['entities']}")
                continue
            
            # Skip entries with empty entities
            if not annotations["entities"]:
                print(f"Skipping entry with empty entities: {item}")
                continue
            
            cleaned_annotations.append(item)
        
        except ValueError as e:
            print(f"Skipping invalid entry: {e}")
            continue
    
    data["annotations"] = cleaned_annotations
    return data

# File paths
input_filepath = '13.json'
output_filepath = '13_clean.json'

# Load, clean, and save data
data = load_json(input_filepath)
cleaned_data = clean_annotations(data)
save_json(cleaned_data, output_filepath)

print(f"Cleaned data saved to {output_filepath}")
