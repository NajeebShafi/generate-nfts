# Generate-NFTs

## Installation 🛠️

If you are cloning the project then run this first, otherwise you can download the source code on the release page and skip this step.

```sh
git clone https://github.com/NajeebShafi/generate-nfts.git
```

Go to the root of your folder and run this command if you have python installed.

```sh
python nft.py
```

Alternatively if above dont work, you to run these command.

```sh
poetry install
```

## Usage ℹ️

Create your different layers as folders in the 'assets' directory, and add all the layer assets in these directories. You can name the assets anything as long as it has a rarity weight attached in the file name like so: `example element#70.png`.

Once you have all your layers, go into `config.json` and update the `layer` objects `layers` array to be your layer folders name in order of the back layer to the front layer.

_Example:_ If you were creating a portrait design, you might have a background, then a head, a mouth, eyes, eyewear, and then headwear, so your `layersOrder` would look something like this:

```json
{
  "layers" : [
    {
      "id": 1,
      "name": "background",
      "directory": "Background"
    },
    {
      "id": 2,
      "name": "face_color",
      "directory": "Face Color"
    },
    {
      "id": 3,
      "name": "face_shape",
      "directory": "Face Shape"
    },
    {
      "id": 4,
      "name": "eye_color",
      "directory": "Eye Color"
    },
    {
      "id": 5,
      "name": "eye_shape",
      "directory": "Eye Shape"
    },
    {
      "id": 6,
      "name": "nose",
      "directory": "Nose"
    },
    {
      "id": 7,
      "name": "lips",
      "directory": "Lips"
    }
  ]
}
```

The `directory` of each layer object represents the name of the folder (in `/assets/`) that the images reside in.

The program will output all the images in the `output/{you-config-file-name}` directory. i am still working on metadata creation.

