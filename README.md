# Spotify Keychain 3D Model

This repository contains the code and 3D model files needed to create a custom Spotify keychain. This keychain is designed to incorporate a Spotify code of your favorite song, album, artist, or playlist, which can be scanned to play music directly from Spotify.

// Remix of [ricdigi](https://github.com/ricdigi/spotify_keychain_3D_model)

## How to Use the Code

The script in this repository uses `cadquery` to modify a base 3D model of the keychain by adding a Spotify code to it. Follow these steps to use the code:

1. **Setup Python Environment**:
   - Ensure you have Python installed on your system. ([install here](https://www.python.org/downloads/release/python-396/))
   - Install required packages: `cadquery`, `requests`, `pillow`.
   - Install these packages using `pip install cadquery requests pillow`.
   - Install thease upgrades: `pip install nptyping --upgrade`, `pip install numpy --upgrade`

2. **Running the Script**:
   - Go to the application folder. click at folder path
   - click here (folder path), delete this line and write `cmd`
   - Run the script (`python main.py`) It will prompt you to enter the link of the song, album, artist, or playlist from Spotify.

3. **Input URL Parsing**:
   - The script parses the provided Spotify link and prepares a URL to fetch the corresponding Spotify code.

4. **Downloading the Spotify Code**:
   - The script downloads the Spotify code as an image based on the parsed data.

5. **Loading the Code Image**:
   - The code image is loaded and processed to determine the bar lengths which are essential to generate the Spotify code's pattern.

6. **Editing the Base Model**:
   - The script then takes a base model of the keychain (in STEP format) and modifies it by adding the Spotify code pattern.
   - The model is updated with extrusions representing the unique barcode of your Spotify link.

7. **Exporting the Final Model**:
   - According to the information displayed, the script will download a ready-made .stl model, the file will be located in the `models` folder in the application folder.

8. **3D Printing**:
   - Use the exported STL file to 3D print your custom Spotify keychain.

## Customization

You can customize the keychain by using different Spotify links. Each link will generate a unique code that represents the specific song, album, artist, or playlist.

