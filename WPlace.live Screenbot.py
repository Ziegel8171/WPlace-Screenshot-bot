import os
import time
import undetected_chromedriver as uc
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tqdm import tqdm
from datetime import datetime # Use datetime for timestamps

# ==============================================================================
# CONFIGURATION
# ==============================================================================
GRID_WIDTH = 15
GRID_HEIGHT = 15
START_URL = "https://wplace.live/?lat=41.08882474886046&lng=-74.56825228447266&zoom=13" # Zoom has to be 13!
WINDOW_WIDTH = 1280 # Don't touch
WINDOW_HEIGHT = 800 # Don't touch

# Final calibrated STEP values. Don't touch
LAT_STEP = -0.04600 # Don't touch
LNG_STEP = 0.10850 # Don't touch

# Max time to wait for the page to load
TIMEOUT_PER_TILE = 0.5

ELEMENTS_TO_HIDE = [
    'div.absolute:nth-child(5)', 'div.absolute:nth-child(6)', '.left-2',
    'div.absolute:nth-child(7)', '.right-2', '.MuiButtonBase-root',
    '.main-wrapper', 'div.absolute:nth-child(8)'
]
# ==============================================================================

def capture_tiles(start_lat, start_lng, zoom):
    print("Starting capture with visible browser...")
    
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, use_subprocess=True)
    driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)

    if not os.path.exists("tiles"):
        os.makedirs("tiles")

    hide_script = """
    var selectors = arguments[0];
    for (const selector of selectors) {
        const elements = document.querySelectorAll(selector);
        for (const element of elements) { element.style.display = 'none'; }
    }
    """
    
    wait = WebDriverWait(driver, TIMEOUT_PER_TILE)

    all_tiles = [(x, y) for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH)]
    
    for x, y in tqdm(all_tiles, desc="Capturing Tiles"):
        current_lat = start_lat + (y * LAT_STEP)
        current_lng = start_lng + (x * LNG_STEP)
        url = f"https://wplace.live/?lat={current_lat}&lng={current_lng}&zoom={zoom}"

        driver.get(url)

        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "leaflet-container")))
        except Exception as e:
            print(f"\nWarning: Page took too long to load for tile ({x+1}, {y+1}). Error: {e}")

        if ELEMENTS_TO_HIDE:
            driver.execute_script(hide_script, ELEMENTS_TO_HIDE)

        filename = f"tiles/tile_{y}_{x}.png"
        driver.save_screenshot(filename)

    print("\nCapture phase complete.")
    driver.quit()

def stitch_tiles():
    print("Starting stitching phase...")
    first_tile_path = "tiles/tile_0_0.png"
    if not os.path.exists(first_tile_path):
        print("Error: No tiles were captured. Cannot stitch.")
        return
    with Image.open(first_tile_path) as first_tile:
        tile_width, tile_height = first_tile.size
    final_width = tile_width * GRID_WIDTH
    final_height = tile_height * GRID_HEIGHT
    stitched_image = Image.new('RGB', (final_width, final_height))
    print(f"Creating final image with dimensions {final_width}x{final_height}...")
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile_path = f"tiles/tile_{y}_{x}.png"
            try:
                with Image.open(tile_path) as tile:
                    paste_x = x * tile_width
                    paste_y = y * tile_height
                    stitched_image.paste(tile, (paste_x, paste_y))
            except FileNotFoundError:
                print(f"Warning: Tile not found at {tile_path}. Skipping.")
    
    # --- UPDATED FILENAME LOGIC ---
    folder_name = "Finished"
    
    # 1. Get the current date and time
    now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # 2. Create the unique filename with the timestamp
    dynamic_filename = f"Wplace{GRID_WIDTH}x{GRID_HEIGHT}_{now_str}.png"
    
    os.makedirs(folder_name, exist_ok=True)
    full_save_path = os.path.join(folder_name, dynamic_filename)
    
    stitched_image.save(full_save_path)
    print(f"Stitching complete! Image saved as {full_save_path}")
    
    print("Removing temporary tile files...")
    for y in range(GRID_WIDTH):
        for x in range(GRID_HEIGHT):
            tile_path = f"tiles/tile_{y}_{x}.png"
            if os.path.exists(tile_path):
                os.remove(tile_path)
    os.rmdir("tiles")
    print("Cleanup complete.")

if __name__ == "__main__":
    try:
        parts = START_URL.split('?')[1].split('&')
        lat = float(next(p for p in parts if p.startswith('lat=')).split('=')[1])
        lng = float(next(p for p in parts if p.startswith('lng=')).split('=')[1])
        zoom = float(next(p for p in parts if p.startswith('zoom=')).split('=')[1])
        capture_tiles(lat, lng, zoom)
        stitch_tiles()
    except Exception as e:
        print(f"An error occurred: {e}")