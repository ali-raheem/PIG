import os
import base64
import argparse
from datetime import datetime
from PIL import Image
from io import BytesIO


def create_thumbnail(image_path):
    with Image.open(image_path) as img:
        img.thumbnail((128, 128))
        with BytesIO() as buffer:
            img.save(buffer, 'JPEG')
            return base64.b64encode(buffer.getvalue()).decode()

def get_head():
    return """<!DOCTYPE html>
    <html>
    <head>
    <style>
    img { max-width: 128px; }
    .gallery {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        flex-wrap: wrap;
    }
    .row {
        display: flex;
        justify-content: space-evenly;
    }
    .controls {
    	display: flex;
    	justify-content: center;
    }
    </style>
    </head>
    <body>"""
def get_footer():
	return """
    Made with PhotoIndexGenerator (PIG) 0.1.0 <a href='https://github.com/ali-raheem/PIG'>Source</a>
    </body>
    </html>
    """
def generate_gallery_html(images, title, description, num_images_per_row):
    html =""
    
    html = f"""<div class='metadata'>
        <h1>{title}</h1>
        <p>{description}</p>
        <p>First image: {images[0]}</p>
        <p>Last image: {images[-1]}</p>
    </div>
    <div class='gallery'>
        <div class='row'>
    """

    image_count = 0
    for i, image in enumerate(images):
        if i > 0 and i % num_images_per_row == 0:
            html += "</div><div class='row'>"
        thumbnail_b64 = create_thumbnail(image)
        html += f"""
        <div class="thumbnail">
            <img src="data:image/jpeg;base64,{thumbnail_b64}" /><br/>
            {os.path.basename(image)}
        </div>
        """
    image_count += 1
    html += """
        </div>
    </div>
    """
    return html


def main(image_dir: str, output_path: str, title: str, description: str, num: int, ext: list, num_images_per_row: int):
    # Find all images in the image_dir with matching extensions
    images = [os.path.join(image_dir, file) for file in os.listdir(image_dir)
              if file.lower().endswith(tuple(ext))]

    # Sort images by filename
    images.sort()

    num_sets = (len(images)+1) // num

    for i in range(num_sets):
        gallery_html = get_head()
        start_index = i * num
        end_index = start_index + num
        set_images = images[start_index:end_index]
        set_title = f"{title} {i+1}/{num_sets}"
        gallery_html += generate_gallery_html(set_images, set_title, description, num_images_per_row)
        gallery_html += "<div class='controls'>"
        if i > 0:
            gallery_html += f"<a href='{output_path}_{i}_{num_sets}.html'>Previous</a> "
        gallery_html += f"<span>Page {i+1} of {num_sets}</span>"
        if i + 1 < num_sets:
            gallery_html += f" <a href='{output_path}_{i+2}_{num_sets}.html'>Next</a>"
        gallery_html += "</div><br/>"+get_footer()
        with open(f"{output_path}_{i+1}_{num_sets}.html", 'w') as f:
            f.write(gallery_html)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate an HTML page from images.')
    parser.add_argument('--image_dir', required=True, help='Path to the images')
    parser.add_argument('--output_path', required=True, help='Base path for the HTML files to generate')
    parser.add_argument('--title', default='', help='Title of the page')
    parser.add_argument('--description', default='', help='Description of the page')
    parser.add_argument('--row', type=int, default=5, help='Number of images per row')
    parser.add_argument('--num', type=int, default=80, help='Number of images to include in each set')
    parser.add_argument('--ext', nargs='+', default=['jpg', 'png'], help='Extensions to use')

    args = parser.parse_args()

    main(args.image_dir, args.output_path, args.title, args.description, args.num, args.ext, args.row)
