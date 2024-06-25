import json
import os
import matplotlib.pyplot as plt

# Define the classes
classes = [
    "CLIMATE EVENT",
    "LIVING BEING",
    "CURRENCY",
    "DISASTER",
    "CAUSE",
    "LOCATION",
    "YEAR",
    "ORGANIZATION",
    "TEMPERATURE"
]

# Initialize a dictionary to hold entity counts
entity_counts = {cls: 0 for cls in classes}

# Directory containing the annotation files
directory_path = 'final_annotations'

# Iterate through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.json'):  # Assuming annotation files are in JSON format
        with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Iterate through the annotations to count entities
            if 'annotations' in data:
                for item in data['annotations']:
                    text, annotation = item
                    if 'entities' in annotation:
                        for entity in annotation['entities']:
                            entity_type = entity[2]
                            if entity_type in entity_counts:
                                entity_counts[entity_type] += 1

# Print the counts of each entity type
print(entity_counts)

# Extract data for plotting
entity_types = list(entity_counts.keys())
counts = list(entity_counts.values())

# Create the bar chart
plt.figure(figsize=(12, 8))
plt.bar(entity_types, counts, color='skyblue')

# Add labels and title
plt.xlabel('Entity Types')
plt.ylabel('Counts')
plt.title('Entity Counts in Training Data')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha="right")

# Save the plot to a file
plt.savefig('entity_counts.png')

# Show the plot
plt.show()
