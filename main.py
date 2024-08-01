import cadquery as cq
import requests
import io
from PIL import Image
import utils
import os

BRIGHT_GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def get_next_filename(directory, prefix='model', extension='stl'):
    """Generate a unique filename with an incrementing number."""
    i = 1
    while True:
        filename = f"{prefix}_{i}.{extension}"
        if not os.path.exists(os.path.join(directory, filename)):
            return filename
        i += 1

def print_ascii_art():
    print(BRIGHT_GREEN + r"""



   _____                   __     _     ____                           __              _         
  / ___/    ____   ____   / /_   (_)   / __/   __  __         _____   / /_   ____ _   (_)   ____ 
  \__ \    / __ \ / __ \ / __/  / /   / /_    / / / /        / ___/  / __ \ / __ `/  / /   / __ \
 ___/ /   / /_/ // /_/ // /_   / /   / __/   / /_/ /        / /__   / / / // /_/ /  / /   / / / /
/____/   / .___/ \____/ \__/  /_/   /_/      \__, /         \___/  /_/ /_/ \__,_/  /_/   /_/ /_/ 
        /_/                                 /____/                                               


                                                                                                                      
             """ + RESET)

def print_completion_message(filename):
    print(BRIGHT_GREEN + r"""
 


   __  __                                                                                      __          __    __
  / / / /   _____  ___           __  __  ____   __  __   _____          ____ ___   ____   ____/ /  ___    / /   / /
 / / / /   / ___/ / _ \         / / / / / __ \ / / / /  / ___/         / __ `__ \ / __ \ / __  /  / _ \  / /   / / 
/ /_/ /   (__  ) /  __/        / /_/ / / /_/ // /_/ /  / /            / / / / / // /_/ // /_/ /  /  __/ / /   /_/  
\____/   /____/  \___/         \__, /  \____/ \__,_/  /_/            /_/ /_/ /_/ \____/ \__,_/   \___/ /_/   (_)   
                              /____/                                                                               

                                                                                                                        
                                              """ + RESET)
    print(YELLOW + f"File {filename} created successfully! The file is located in the models folder" + RESET)

URL = "https://www.spotifycodes.com/downloadCode.php?uri=jpeg%2F000000%2Fwhite%2F640%2Fspotify%3Aalbum%3A4m2880jivSbbyEGAKfITCa"

if __name__ == '__main__':

    print_ascii_art()

    models_dir = 'models'
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    share_link = input(YELLOW + "Enter link of song, album, artist or playlist: " + RESET)

    data = utils.get_link_data(share_link)

    if len(data) != 2:
        print(YELLOW + "Something went wrong while parsing the URL." + RESET)
        exit(-1)

    code_URL = f"https://www.spotifycodes.com/downloadCode.php?uri=jpeg%2F000000%2Fwhite%2F640%2Fspotify%3A{data[0]}%3A{data[1]}"
    r = requests.get(code_URL)

    if not r.ok or not r.content:
        print(YELLOW + "Something went wrong while fetching the Spotify code." + RESET)
        exit(-1)

    try:
        img = Image.open(io.BytesIO(r.content)).crop((160, 0, 640-31, 160))
    except Exception as e:
        print(YELLOW + f"Error loading image: {e}" + RESET)
        exit(-1)

    width, height = img.size
    pix = img.load()

    bar_heights = []
    max_height_of_single_bar = 0

    for x in range(width):
        at_bar = False
        curr_height = 0

        for y in range(height):
            if pix[x, y][0] > 20 or pix[x, y][1] > 20 or pix[x, y][2] > 20:
                at_bar = True
                curr_height += 1

        if at_bar and curr_height > max_height_of_single_bar:
            max_height_of_single_bar = curr_height / 20
        elif not at_bar and max_height_of_single_bar > 0:
            bar_heights.append(max_height_of_single_bar)
            max_height_of_single_bar = 0

    print(YELLOW + f"There are {len(bar_heights)} bars of heights {bar_heights}" + RESET)

    try:
        model = cq.importers.importStep('base_model.step')
    except Exception as e:
        print(YELLOW + f"Error importing base model: {e}" + RESET)
        exit(-1)

    curr_bar = 0

    for bar in bar_heights:
        model = (
            model.pushPoints([(15.5 + curr_bar * 1.88, 7.5)])
            .sketch()
            .slot(9 / 5 * bar, 1, 90)
            .finalize()
            .extrude(4)
        )
        curr_bar += 1

    filename = get_next_filename(models_dir, 'model', 'stl')

    try:
        cq.exporters.export(model, os.path.join(models_dir, filename))
    except Exception as e:
        print(YELLOW + f"Error exporting model: {e}" + RESET)
        exit(-1)

    print_completion_message(filename)
