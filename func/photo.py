from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime
import random 
from pilmoji import Pilmoji
import os

def gen_image(text="???"):
    ImgPath = ["src/kiu1.jpg", "src/left1.png", "src/left2.jpg"];
    pickImg = random.choice(ImgPath)
    img = Image.open(pickImg)
    I1 = ImageDraw.Draw(img)
   
    box = (100, 100, 1300, 700)
    color = (255, 255, 255)  

    font_size = 100
    line_height_factor = 1.2  # Adjust the line height factor as desired
    size = None
    while (size is None or size[0] > box[2] - box[0] or size[1] > box[3] - box[1]) and font_size > 0:
        font = ImageFont.truetype("NotoSansTC-Bold.ttf", font_size)
        wrapped_text = textwrap.wrap(text, width=40)
        lines = []
        for line in wrapped_text:
            line_size = font.getsize(line)
            if line_size[0] > box[2] - box[0]:
                # Line too long, wrap it to the next line
                words = line.split()
                new_line = words[0]
                for word in words[1:]:
                    if font.getsize(new_line + ' ' + word)[0] <= box[2] - box[0]:
                        new_line += ' ' + word
                    else:
                        lines.append(new_line)
                        new_line = word
                lines.append(new_line)
            else:
                lines.append(line)
        
        line_height = int(font_size * line_height_factor)
        size = (max(font.getsize(line)[0] for line in lines), sum(line_height for _ in lines))
        font_size -= 1
    
    position = (box[0], box[1])
    for line in lines:
        I1.text(position, line, color, font=font)
        position = (position[0], position[1] + line_height)

    font = ImageFont.truetype("NotoSansTC-Bold.ttf", 100)

    if "kiu" in pickImg:
        I1.text((600,800), "kiu GOD", font=font, fill=color)
    else:
        I1.text((600,800), "left GOD", font=font, fill=color)

    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_file = f'{current_time}.png'
    img.save(output_file)

    return output_file


def gen_image2(text="???", image_name=None):
    # Available images with their full paths
    ImgPath = ["src/kiu1.jpg", "src/left1.png", "src/left2.jpg"]
    
    # Build a mapping from simple name -> full path
    name_to_path = {}
    for path in ImgPath:
        base = os.path.basename(path)               # e.g. "kiu1.jpg"
        name, _ = os.path.splitext(base)            # e.g. "kiu1"
        name_to_path[name.lower()] = path           # store lowercase for case‑insensitivity
    
    # Select image based on image_name
    if image_name is not None:
        key = image_name.lower()
        if key in name_to_path:
            pickImg = name_to_path[key]
        else:
            available = ', '.join(name_to_path.keys())
            raise ValueError(f"Unknown image name '{image_name}'. Available: {available}")
    else:
        pickImg = random.choice(ImgPath)
    
    # Open image
    img = Image.open(pickImg)
    
    # Text box dimensions (left, top, right, bottom)
    box = (100, 100, 1300, 700)
    max_width = box[2] - box[0]
    max_height = box[3] - box[1]
    
    color = (255, 255, 255)   # white text
    
    # Try different font sizes until the text fits
    font_size = 100
    line_height_factor = 1.2
    font_path = "NotoSansTC-Bold.ttf"   # make sure this font file exists
    
    while font_size > 0:
        try:
            font = ImageFont.truetype(font_path, font_size)
        except OSError:
            # Fallback to default font if the specific one isn't found
            font = ImageFont.load_default()
            # With default font, we can't reduce size; break after one try
            break
        
        line_height = int(font_size * line_height_factor)
        
        # Split text into words (preserve spaces)
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            # Measure the width of the word with the current font
            bbox = font.getbbox(word)
            word_width = bbox[2] - bbox[0]
            
            # Build a test line including this word
            test_line = ' '.join(current_line + [word])
            bbox_test = font.getbbox(test_line)
            test_width = bbox_test[2] - bbox_test[0]
            
            if not current_line:
                # First word on the line
                current_line.append(word)
            elif test_width <= max_width:
                # Word fits on current line
                current_line.append(word)
            else:
                # Start a new line
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate total height of all lines
        total_height = len(lines) * line_height
        
        if total_height <= max_height:
            # Text fits with current font size
            break
        else:
            font_size -= 1
            lines = []   # reset lines for next iteration
    
    # If font_size became 0, fallback to smallest possible (but still try)
    if font_size <= 0:
        font_size = 10
        try:
            font = ImageFont.truetype(font_path, font_size)
        except OSError:
            font = ImageFont.load_default()
        line_height = int(font_size * line_height_factor)
        # Recompute lines with the tiny font (simplified fallback)
        lines = textwrap.wrap(text, width=40)   # rough fallback
    
    # Draw text with emoji support
    with Pilmoji(img) as pilmoji:
        y = box[1]
        for line in lines:
            pilmoji.text((box[0], y), line, fill=color, font=font)
            y += line_height
    
    # Add footer text
    try:
        footer_font = ImageFont.truetype(font_path, 100)
    except OSError:
        footer_font = ImageFont.load_default()
    
    with Pilmoji(img) as pilmoji:
        if "kiu" in pickImg:
            pilmoji.text((600, 800), "kiu GOD", fill=color, font=footer_font)
        else:
            pilmoji.text((600, 800), "left GOD", fill=color, font=footer_font)
    
    # Save with timestamp
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_file = f'{current_time}.png'
    img.save(output_file)
    
    return output_file

# gen_image2("GPA is not important 🤓 🤓 🤓", "left1")