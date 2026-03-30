import os
import random
from PIL import Image, ImageDraw, ImageFont
import math

# We will import RAW_PRODUCTS from app to know exactly what products to generate images for
from app import RAW_PRODUCTS

def draw_sparks(draw, width, height):
    # Draw some "sparks" to give a firework feel
    colors = [(255, 69, 0), (255, 140, 0), (255, 215, 0), (0, 191, 255), (148, 0, 211), (255, 20, 147)]
    for _ in range(40):
        x = random.randint(0, width)
        y = random.randint(0, height)
        c = random.choice(colors)
        size = random.randint(2, 6)
        draw.ellipse((x, y, x+size, y+size), fill=c)
        # draw a tiny trail
        draw.line((x+size/2, y+size/2, x+size/2 + random.randint(-15, 15), y+size/2 + random.randint(10, 30)), fill=c, width=1)

def generate_product_image(text, filepath):
    width, height = 500, 500
    # Choose a nice dark background color slightly randomized per item
    base_r = random.randint(10, 30)
    base_g = random.randint(10, 30)
    base_b = random.randint(20, 50)
    
    img = Image.new('RGB', (width, height), color=(base_r, base_g, base_b))
    draw = ImageDraw.Draw(img)
    
    draw_sparks(draw, width, height)
    
    # Try to load a generic font or fallback to default
    try:
        # Windows typically has arial.ttf
        font = ImageFont.truetype("arialbd.ttf", 36)
    except:
        try:
            font = ImageFont.truetype("tahoma.ttf", 36)
        except:
            font = ImageFont.load_default()

    # Draw the text in the center
    # Split text into two lines if it's too long
    words = text.split()
    lines = []
    if len(words) >= 3:
        mid = len(words) // 2
        lines.append(' '.join(words[:mid]))
        lines.append(' '.join(words[mid:]))
    else:
        lines.append(text)

    # Calculate total height of text block
    line_spacing = 10
    total_text_height = 0
    font_heights = []
    
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        h = bbox[3] - bbox[1]
        font_heights.append(h)
        total_text_height += h + line_spacing
        
    y = (height - total_text_height) // 2
    
    # Draw shadow then text
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (width - w) // 2
        
        # shadow
        draw.text((x+2, y+2), line, font=font, fill=(0, 0, 0))
        # text
        draw.text((x, y), line, font=font, fill=(255, 255, 255))
        
        y += font_heights[i] + line_spacing

    # Make target directory
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath, 'JPEG', quality=90)


if __name__ == '__main__':
    base_dir = os.path.join('static', 'images', 'products')
    count = 0
    for cat, items in RAW_PRODUCTS:
        for item in items:
            # We'll sanitize the item name for filename
            safe_name = item.replace(' ', '_').replace('/', '_') + '.jpg'
            filepath = os.path.join(base_dir, safe_name)
            generate_product_image(item, filepath)
            count += 1
            
    print(f"Successfully generated {count} product images locally in {base_dir}")
