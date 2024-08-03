from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime
import random 

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

# gen_image("Left教教徒1號)")