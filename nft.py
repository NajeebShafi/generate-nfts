# Import required libraries
import datetime
import json
from collections import defaultdict, Counter
from math import comb
from PIL import Image
import time
import os
import glob
import random

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
def generate_meta_json(traits, album,image_name, config):
    import json
    meta_data = {
        "name": f"{album} #{image_name}",
        "description": f"{config['description']}" ,
        "image": f"{config['base_image_url']}.png",
        "edition": 1,
        "date": datetime.datetime.now().timestamp(),
        "attributes":traits,
    }
    json_object = json.dumps(meta_data, indent=4)
    with open(os.path.join("output", album, image_name + ".json"), "w") as outfile:
        outfile.write(json_object)


def generate_single_image(filepaths, output_filename=None):
    bg = Image.open(os.path.join(filepaths[0]))

    for filepath in filepaths[1:]:
        if filepath.endswith('.png'):
            img = Image.open(os.path.join(filepath))
            bg.paste(img, (0, 0), img)

    if output_filename is not None:

        bg.save(output_filename)
    else:
        if not os.path.exists(os.path.join('output', 'test_images')):
            os.makedirs(os.path.join('output', 'test_images'))
        bg.save(os.path.join('output', 'test_images', str(int(time.time())) + '.png'))

def load_config():
    f = open('config.json')
    data = json.load(f)
    return data

def total_combinations(total_images, layers):
    return comb(total_images, layers)

def get_traits(layers):
    traits = defaultdict()

    image_count = 0
    for layer in layers:
        image_list = os.listdir(os.path.join("assets", layer["directory"]))
        image_count += len(image_list)
        traits[layer['name']] = [f"assets/{layer['directory']}/{image}" for image in image_list]

    return traits, image_count

def generate_nfts(traits, number_of_images, album, config, remove_duplicates=True, generate_rarity_table=False, generate_commons_table=False):
    start = time.time()

    rarity_table = {}
    used_traits = []
    for i in range(number_of_images):
        file_name = f"{i}"
        image_traits = []
        image_traits_dict = []
        for trait_key, trait_value in traits.items():
            image = trait_value[random.randint(0, len(trait_value) - 1)]
            image_traits.append(image)
            image_traits_dict.append({"trait_type":trait_key,"value":image.split("/")[2]})
            if rarity_table.get(f"{trait_key}"):
                rarity_table[f"{trait_key}"].append(image.split("/")[2])
            else:
                rarity_table[f"{trait_key}"] = [image.split("/")[2]]

        if image_traits in used_traits:
            file_name += f"duplicate_of_{used_traits.index(image_traits)}"
        else:
            used_traits.append(image_traits)

        if not os.path.exists(os.path.join("output", album)):
            os.makedirs(os.path.join("output", album))

        generate_single_image(image_traits, os.path.join("output", album, file_name + ".png"))
        generate_meta_json(image_traits_dict, album, file_name, config)

    if remove_duplicates:
        print("in duplicates")
        for filename in glob.glob(f"output/{album}/*duplicate_of_*"):
            os.remove(filename)

    end = time.time()
    elapsed_seconds = float("%.2f" % (end - start))
    print(f"Time took generate nfts is {elapsed_seconds} seconds")
    if generate_rarity_table:
        print()
        print(f"Generating Rarity Table")
        for key, value in rarity_table.items():
            print(f"{key}: {dict(Counter(value))}")

    if generate_commons_table:
        print()
        print(f"Generating Common Table")
        for key, value in rarity_table.items():
            print(f"{key}: {Counter(value).most_common(1)[0][0]}")


def main():
    # load config
    config = load_config()

    layers = config['layers']
    number_of_nfts = config['number_of_nfts']
    album = config['name']

    print("No. of layers:",len(layers))
    print("")

    traits, image_count = get_traits(layers)
    for trait, images in traits.items():
        print(f"trait:{trait} , image_count:{len(images)}")
    print("")

    print(f"total number of unique images that can be produced from this set is {total_combinations(image_count,len(layers))}")
    print("generating a test image using random traits")

    if image_count <= 0:
        print("Kindly add assets to run this command")
    else:
        generate_nfts(traits, number_of_nfts, album, config, generate_rarity_table=True, generate_commons_table=True)


# Run the main function
main()