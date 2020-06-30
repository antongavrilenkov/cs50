"""
Import modules
"""
import uuid
import os
from PIL import Image, ImageDraw, ImageFont

def prepare_slide_text(text):
    '''Prepare text / Insert line breakes'''
    chars_since_last_break = 0
    max_char_in_line = 14
    previous_word_end_idx = 0
    start = 0
    trav = 0
    result = ''
    while True: 
        # Return result after the end of the line reached
        if trav > len(text) - 1:
            result += text[start:trav] 
            return result
        # Track index of the end of previous word
        if text[trav] == ' ' or (previous_word_end_idx == 0 and trav > len(text) - 2):
            previous_word_end_idx = trav + 1
        # Insert line break
        if chars_since_last_break > max_char_in_line:
            result += text[start:previous_word_end_idx] + "\n"
            start = previous_word_end_idx
            trav = previous_word_end_idx
            chars_since_last_break = 0
        # Traverse the next character
        else:
            trav += 1
            chars_since_last_break += 1


def hex_to_rgb(value):
    '''Convert HEX color to RGB color'''
    value = value.lstrip('#')
    value_length = len(value)
    return tuple(int(value[i:i + value_length // 3], 16) for i
                 in range(0, value_length, value_length // 3))

# text, folder_name, filename, text_color, bg_color
def create_slide(params):
    '''create slide image'''
    max_characters = 100

    if len(params.get("text")) <= max_characters and params.get("text") != '':
        try:
            if not os.path.exists(params.get("slide_folder")):
                os.mkdir(params.get("slide_folder"))
        except OSError:
            print("Creation of the directory %s failed" % params.get("slide_folder"))
            return None
        else:
            print("Successfully created the directory %s " % params.get("slide_folder"))
            image_width = 1080
            image_height = 1080
            img = Image.new('RGB', (image_width, image_height), hex_to_rgb(params.get("bg_color")))
            draw = ImageDraw.Draw(img)
            font_path = "static/fonts/RobotoMono-VariableFont_wght.ttf"
            font_size = 100
            font = ImageFont.truetype(font_path, font_size)
            text = prepare_slide_text(params.get("text"))
            text_width, text_height = draw.textsize(text, font=font)
            draw.text(((image_width - text_width) / 2, (image_height - text_height) / 2), text,
                      fill=hex_to_rgb(params.get("text_color")), font=font)
            file_dest = params.get("slide_folder") + params.get("filename") + '.png'
            img.save(file_dest)
            return 1
    else:
        return None


def generator(params):
    '''Generate a video slideshow from text''' 
    folder_name = str(uuid.uuid4())
    temp_folder = 'static/temp/'
    slide_folder = temp_folder + folder_name + '/'

    # Create temp folder
    try:
        if not os.path.exists(temp_folder):
            os.mkdir(temp_folder)
    except OSError:
        print("Creation of the directory %s failed" % slide_folder)
    else:
        print("Successfully created the directory %s " % slide_folder)

        # Create slide's image from text
        slides_created = len(params.get("texts"))
        for idx, text in enumerate(params.get("texts")):
            create_slide({'text': text.get("text"), 'slide_folder': slide_folder,
                          'filename': str(idx),
                          'text_color': text.get("text_color"),
                          'bg_color': text.get("bg_color")})  

        # Convert images to output video
        os.system("ffmpeg -framerate 1/{1} -i {0}%d.png -r 25 -pix_fmt yuv420p {0}out.mp4"
                  .format(slide_folder, params.get("slide_duration")))

        # Add background music
        if params.get("bg_music") != "none":
            video_duration = slides_created * int(params.get("slide_duration")) 
            os.system("mv {0}out.mp4 {0}tmp.mp4".format(slide_folder))
            os.system("cp static/audio/bg-music/{1}.mp3 {0}tmp.mp3"
                      .format(slide_folder, params.get("bg_music"))) 
            os.system("ffmpeg -i {0}tmp.mp3 -t {1} {0}out.mp3"
                      .format(slide_folder, video_duration))
            os.system("ffmpeg -i {0}tmp.mp4 -i {0}out.mp3 -shortest {0}out.mp4"
                      .format(slide_folder))

        # Return result video file path
        return slide_folder + 'out.mp4'
