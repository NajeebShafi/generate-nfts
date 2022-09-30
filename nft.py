# Import required libraries
import json
from collections import defaultdict
from math import comb
from PIL import Image
import time
import os
import glob
import random
from progressbar import progressbar

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

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

def generate_nfts(traits, number_of_images, album, remove_duplicates=False):
    start = time.time()

    used_traits = []
    for i in range(number_of_images):
        file_name = f"{i}"
        image_traits = []
        for trait_value in traits.values():
            image = trait_value[random.randint(0, len(trait_value) - 1)]
            image_traits.append(image)

        if image_traits in used_traits:
            file_name += f"duplicate_of_{used_traits.index(image_traits)}"
        else:
            used_traits.append(image_traits)

        if not os.path.exists(os.path.join("output", album)):
            os.makedirs(os.path.join("output", album))

        generate_single_image(image_traits, os.path.join("output", album, file_name + ".png"))

    if remove_duplicates:
        print("in duplicates")
        for filename in glob.glob(f"output/{album}/*duplicate_of_*"):
            os.remove(filename)

    end = time.time()
    elapsed_seconds = float("%.2f" % (end - start))
    print(f"Time took generate nfts is {elapsed_seconds} seconds")


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
        generate_nfts(traits, number_of_nfts, album)


# Run the main function
main()