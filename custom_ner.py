import json
import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
from spacy import displacy
import random




# Load the JSON file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


annotation_file_1 = load_json('final_annotations\\annotations_a1.json')
annotation_file_2 = load_json('final_annotations\\annotations_s2.json')

# Convert data to spaCy format
def convert_data(data):
    training_data = []
    for text, annotations in data["annotations"]:


        entities = [(start, end, label) for start, end, label in annotations["entities"]]
        training_data.append((text, {"entities": entities}))
    return training_data

training_data = convert_data(annotation_file_1) + convert_data(annotation_file_2) 

# Create a blank spaCy model
nlp = spacy.blank("en")

# Create the NER component and add it to the pipeline
ner = nlp.add_pipe("ner")

# Add new labels to the NER component
for _, annotations in training_data:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# Disable other pipeline components (if any)
pipe_exceptions = ["ner"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

# Training the NER model

with nlp.disable_pipes(*unaffected_pipes):
    
    optimizer = nlp.begin_training()
    
    for iteration in range(200):
        random.shuffle(training_data)
        losses = {}
        batches = minibatch(training_data, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            examples = [Example.from_dict(nlp.make_doc(text), ann) for text, ann in zip(texts, annotations)]
            nlp.update(examples, drop=0.5, losses=losses)
        print(f"Iteration {iteration + 1}, Losses: {losses}")

# Save the trained model
nlp.to_disk("custom_climate_ner_model")

# Test the trained model
test_text = """They tell us that we are the primary forces controlling earth temperatures by the burning of fossil fuels and releasing their carbon dioxide.
The Great Barrier Reef is experiencing the most widespread bleaching ever recorded
it’s not a pollutant that threatens human civilization.
"If CO2 was so terrible for the planet, then installing a CO2 generator in a greenhouse would kill the plants."
"Sea level rise has been slow and a constant, pre-dating industrialization"
Earth about to enter 30-YEAR ‘Mini Ice Age’
"Volcanoes Melting West Antarctic Glaciers, Not Global Warming"
"the bushfires [in Australia] were caused by arsonists and a series of lightning strikes, not 'climate change'"
Discovery Of Massive Volcanic CO2 Emissions Discredits Global Warming Theory
Harvard study finds that wind turbines create MORE global warming than the fossil fuels they eliminate
"Ice berg melts, ocean level remains the same."""

doc = nlp(test_text)
for ent in doc.ents:
    print(ent.text, ent.label_)
displacy.render(doc, style="ent", jupyter=False)