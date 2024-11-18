from krita import Krita, InfoObject
import json
import os
import random
import time
import glob

# Initialize Krita instance and active document
KI = Krita.instance()
doc = KI.activeDocument()

# Define rarity names and counts
rarity_names = [
    'Common',
    'Uncommon',
    'Rare',
    'Epic',
    'Legendary',
]

rarity_counts = {
    'Legendary': 20,
    'Epic': 96,
    'Rare': 192,
    'Uncommon': 480,
    'Common': 1132,  # Adjusted to total 1920 images
}

# Total number of images to generate
num_images = sum(rarity_counts.values())

# Define attributes with possible values and their weights (rarity)
attributes = {
    'color': {
        'values': ['red', 'green', 'blue', 'yellow', 'purple', 'black', 'white'],
        'weights': [50, 30, 10, 7, 3, 1, 1],  # Adjust weights as needed
        'rare_values': ['gold', 'silver'],
    },
    'exampleTrait1': {
        'values': ['trait1Variation1', 'trait1Variation2', 'trait1Variation3'],
        'weights': [70, 20, 10],
        'rare_values': ['trait1RareVariation1', 'trait1RareVariation2'],
    },
    'exampleTrait2': {
        'values': ['trait2Variation1', 'trait2Variation2'],
        'weights': [80, 20],
        'rare_values': [],
    },
    # Add more traits as needed
}

def choose_weighted(values, weights):
    """Randomly choose an item from values list based on weights."""
    return random.choices(values, weights=weights, k=1)[0]

def set_layer_active(name, state):
    """Set the visibility of a layer by its name."""
    layer = doc.nodeByName(name)
    if layer:
        layer.setVisible(state)

def set_all_layers_inactive():
    """Set all layers in the document to invisible."""
    for node in doc.topLevelNodes():
        node.setVisible(False)
        for child in node.childNodes():
            child.setVisible(False)

# List to keep track of unique images
unique_images = []

# Directory placeholders (replace with your desired directories)
output_image_dir = "/path/to/output/images"      # Replace with your output images directory
frames_dir = "/path/to/output/frames"            # Replace with your frames directory
gif_dir = "/path/to/output/gifs"                 # Replace with your GIFs directory
metadata_output_file = "/path/to/metadata.json"  # Replace with your metadata output file

# Ensure output directories exist
os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(frames_dir, exist_ok=True)
os.makedirs(gif_dir, exist_ok=True)

# Flag to control animation generation
generate_animation = True  # Set to False if you do not want to generate animations

# Data dictionary to store metadata
data = {}

# Prepare the list of rarities for images
rarity_list = []
for rarity, count in rarity_counts.items():
    rarity_list.extend([rarity] * count)
random.shuffle(rarity_list)

def generate_random_image(index, rarity):
    """Generate a random image with unique traits and export it."""
    traits = {}
    # Randomly select traits based on weights
    for attr, attr_info in attributes.items():
        # Decide if we should include a rare value for this attribute
        include_rare = False
        rare_chance = {
            'Common': 0,
            'Uncommon': 0.1,
            'Rare': 0.2,
            'Epic': 0.3,
            'Legendary': 0.5,
        }
        if attr_info.get('rare_values') and random.random() < rare_chance[rarity]:
            # Choose a rare value
            value = random.choice(attr_info['rare_values'])
        else:
            # Choose a common value
            value = choose_weighted(attr_info['values'], attr_info['weights'])
        traits[attr] = value

    # Ensure uniqueness
    if traits in unique_images:
        # Duplicate found, regenerate
        return generate_random_image(index, rarity)
    unique_images.append(traits.copy())

    # Set layers based on traits
    set_all_layers_inactive()
    for attr, value in traits.items():
        layer_name = f"{attr}_{value}"
        set_layer_active(layer_name, True)

    # Export the image
    output_filename = os.path.join(output_image_dir, f"image_{index}.png")
    doc.refreshProjection()
    doc.exportImage(output_filename, InfoObject())

    # Save metadata
    image_data = {
        'name': f'GeneratedImage_{index}',
        'metadata': {
            'traits': traits,
            'rarity': rarity,
        }
    }
    data[str(index)] = image_data

    # Optionally, render frames and create animated GIF
    if generate_animation:
        render_frames(traits, index)

def render_frames(traits, index):
    """Render frames for animation and create an animated GIF using ffmpeg."""
    frame_count = 25  # Number of frames in the animation

    # Ensure the layers are set according to traits
    set_all_layers_inactive()
    for attr, value in traits.items():
        layer_name = f"{attr}_{value}"
        set_layer_active(layer_name, True)

    # Export frames
    for i in range(frame_count):
        doc.setCurrentTime(i)
        doc.refreshProjection()
        time.sleep(0.1)  # Adjust timing as needed
        frame_filename = os.path.join(frames_dir, f"frame_{i}.png")
        doc.exportImage(frame_filename, InfoObject())

    # Create animated GIF using ffmpeg
    output_gif = os.path.join(gif_dir, f"animation_{index}.gif")
    ffmpeg_command = f"ffmpeg -y -f image2 -framerate 24 -i {frames_dir}/frame_%d.png {output_gif}"
    os.system(ffmpeg_command)

    # Clean up frames
    files = glob.glob(f'{frames_dir}/*')
    for f in files:
        os.remove(f)

# Generate images
for index in range(1, num_images + 1):
    rarity = rarity_list[index - 1]
    generate_random_image(index, rarity)

# Write metadata to JSON file
with open(metadata_output_file, 'w', encoding='utf8') as outfile:
    json.dump(data, outfile, indent=4)
