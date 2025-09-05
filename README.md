ReadMe – WPlace.live Screenbot.py

Overview
--------
This script automatically captures and stitches together map screenshots from wplace.live into one large image. It uses undetected-chromedriver with Selenium to browse the map, hides unwanted UI elements, and saves the final stitched image with a timestamp.

Requirements
------------
- Python 3.8+ → Download here: https://www.python.org/downloads/
- Google Chrome (latest version)
- The following Python packages:

pip install undetected-chromedriver pillow tqdm setuptools

How to Use
----------

1. Install Python
   If you don’t already have it, install Python 3.8+: https://www.python.org/downloads/
   
2. Press Windows+R -> type cmd -> hit enter
   Paste this -> "pip install undetected-chromedriver pillow tqdm setuptools" and hit enter.

3. Download the Script and place "WPlace.live Screenbot.py" in a folder of your choice.

4. Adjust Settings
   Open WPlace.live Screenbot.py and check the CONFIGURATION section:
   - GRID_WIDTH & GRID_HEIGHT → Number of tiles to capture horizontally and vertically.
   - START_URL = "https://wplace.live/?lat=40.800703958993395&lng=-74.14584994072266&zoom=13" 
     ZOOM has to be 13!!   Latitude and longitude can be changed.

   By default, it starts with a 2x2 grid at the given coordinates.

5. Run the Script
   Navigate to the folder, and run: WPlace.live Screenbot.py

6. Process
   - The script will open a Chrome browser (via undetected-chromedriver).
   - It captures tiles one by one, hides interface elements, and saves them to the tiles/ folder.
   - Once complete, it stitches the tiles into a single large image.
   - The final stitched image is saved inside a Finished/ folder, with a timestamped filename like:

     Wplace2x2_2025-09-05_14-30-10.png


Notes
-----
- If the page takes too long to load, you may increase TIMEOUT_PER_TILE.
- Make sure Google Chrome is installed and up to date.
- The script hides several UI elements defined in ELEMENTS_TO_HIDE – you can adjust this list if needed.
- Larger grids (e.g., GRID_WIDTH=5, GRID_HEIGHT=5) will take more time and storage.

That's it! After running, check the Finished/ folder for your stitched map images.
