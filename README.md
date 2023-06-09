#Photo Index Generator

Simple gallery of photos intended to be printed as index cards for a collection.

## Usage
```
usage: pig.py [-h] --image_dir IMAGE_DIR --output_path OUTPUT_PATH
              [--title TITLE] [--description DESCRIPTION] [--row ROW]
              [--num NUM] [--ext EXT [EXT ...]]

Generate an HTML page from images.

optional arguments:
  -h, --help            show this help message and exit
  --image_dir IMAGE_DIR
                        Path to the images
  --output_path OUTPUT_PATH
                        Base path for the HTML files to generate
  --title TITLE         Title of the page
  --description DESCRIPTION
                        Description of the page
  --row ROW             Number of images per row
  --num NUM             Number of images to include in each set
  --ext EXT [EXT ...]   Extensions to use
```

## Example

```
python3 pig.py --image_dir /mnt/data/Photos/Wedding wedding.html --output_path wedding_photos --title "Wedding Photos" --note "Jan 2020 York"
```
This will create a set of HTML files named like "wedding_photos_1_10.html", each will contain --num photos (default 80) and will have links to navigate between them at the bottom.

By default paginates to 80 images in rows of 5 images. Around the size of an A4 page.