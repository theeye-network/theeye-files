from flask import Flask, render_template
import os
from PIL import Image, ImageDraw, ImageFont
import time
from pdf2image import convert_from_path

app = Flask(__name__)

def generate_watermarked_image(image_path, watermark_text):
    if image_path.lower().endswith(".pdf"):
        images = convert_from_path(image_path, poppler_path=f'{os.getcwd()}/poppler-23.08.0/Library/bin')
        img = images[0].convert("RGBA")
    else:
        img = Image.open(image_path).convert("RGBA")
    # Define a threshold value for brightness
    threshold = 128  # You can adjust this threshold as needed
    pixels = list(img.getdata())

    # Initialize counters for light and dark colors
    light_count = 0
    dark_count = 0


    for pixel in pixels:
        # Calculate brightness (average of RGB values)
        brightness = sum(pixel) / 3  # Assuming RGB channels have equal weight

        # Check if the pixel is light or dark based on the threshold
        if brightness > threshold:
            light_count += 1
        else:
            dark_count += 1

    if dark_count>light_count:
        txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    else:
        txt = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt)
    monospace = font = ImageFont.truetype("Alegreya.ttf",100)
    text_width, text_height = draw.textsize(watermark_text, font=font)
    img_width, img_height = img.size
    x = img_width - text_width - 900
    y = img_height - text_height - 540
    if dark_count>light_count:
        draw.text((x, y), watermark_text, font=monospace, fill=(255, 255, 255, 64))
    else:
        draw.text((x, y), watermark_text, font=monospace, fill=(0, 0, 0, 64))
    out = Image.alpha_composite(img, txt).convert('RGB')
    return out

@app.route('/<path:route>')
def render_certificate(route):
    if os.path.exists(os.path.join(app.root_path, 'temp-imgs', route + '.pdf')):
        image_path = os.path.join(app.root_path, 'temp-imgs', route + '.pdf')
    else:
        image_path = os.path.join(app.root_path, 'temp-imgs', route + '.jpg')
    if not os.path.exists(image_path):
        return "Certificate not found", 404
    
    creation_time = os.path.getctime(image_path)
    creation_datetime = time.ctime(creation_time)

    watermark_text = f"This is a valid certificate as created on {creation_datetime} by The Eye"
    
    watermarked_image = generate_watermarked_image(image_path, watermark_text)
    
    temp_path = os.path.join(app.root_path, 'static', 'temp_certificate.jpg')
    watermarked_image.save(temp_path,'JPEG')
    
    return render_template('certificate.html')

if __name__ == '__main__':
    app.run()
