from PIL import Image, ImageDraw, ImageFont
import pandas as pd

def get_text_width(text, font):
    """
    Get the width of a text string in pixels.

    Parameters:
    - text (str): The text string.
    - font (ImageFont.ImageFont): The font object.

    Returns:
    - Width of the text in pixels (int).
    """
    width, height = font.getsize(text)
    return width


def resize_image(photo_path, target_size=(100, 100)):
    """
    Resize the image while maintaining its aspect ratio.

    Parameters:
    - photo_path (str): Path to the photo file.
    - target_size (tuple): Target size as (width, height).

    Returns:
    - Resized image (PIL.Image.Image).
    """
    photo = Image.open(photo_path)
    photo.thumbnail(target_size)
    photo_w,photo_h = photo.size
    crop_box=(photo_w/2 - 128, photo_h/2 - 145 , photo_w/2 + 128, photo_h/2 + 145)
    photo = photo.crop(crop_box)
    return photo

# Load Excel sheet

# excel_path = 'staff.xlsx'
excel_path = 'small.xlsx'
df = pd.read_excel(excel_path)




font_size = 36  # Adjust the font size as needed
font = ImageFont.truetype("LEMONMILK-Medium.otf", font_size)
font_size1 = 32  # Adjust the font size as needed
font1 = ImageFont.truetype("LEMONMILK-Medium.otf", font_size1)

# Set the position to paste the photo and name on the template
x, y = 310, 365

# Process each row in the Excel sheet
for index, row in df.iterrows():
    player_name = row['PlayerName']
    photo_path = row['PhotoPath']
    college = row['College']
    sport = row['Sport']

# Load image template
    template_path = 'template.png'
    template = Image.open(template_path)
    template_w , template_h =template.size
    print(index)
    # Resize player photo
    resized_photo = resize_image('photos/' + photo_path, target_size=(500, 500))

    # Paste resized photo onto template
    width, height = resized_photo.size
    template.paste(resized_photo, (int(template_w/2 - width/2), 366))

    # Add player name
    draw = ImageDraw.Draw(template)
    player_name_width = get_text_width(player_name, font)
    college_width = get_text_width("IIT " + college, font1)
    sport_width = get_text_width(sport, font1)
    draw.text((template_w/2 - player_name_width/2, 836), player_name, font=font, fill="#ebb390")
    draw.text((template_w/2 - college_width/2, 880), "IIT " + college, font=font1, fill="#ebb390")
    draw.text((template_w/2 - sport_width/2, 770),  sport, font=font1, fill="#ebb390")

    
    # Update the position for the next card
    y += resized_photo.height + 30

    # Save the generated ID card
    template.save(f'output/{college}_{sport}_{player_name}_IDCard.png')
