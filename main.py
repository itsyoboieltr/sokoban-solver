from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
import re
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import BFS
import time

def main():
    # Headless browser setup for webscraping the Sokoban map
    driverPath = chromedriver_autoinstaller.install()
    service = Service(driverPath)
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(service=service, options=options)

    # Get map url
    sokobanSource = input('\nEnter URL of Sokoban game: ') or 'https://www.sokobanonline.com/play/web-archive/marti-homs-caussa/choriban/86887_choriban-20'
    
    print('\n<Downloading map...>\n')

    # Open headless browser
    driver.get(sokobanSource)

    # Wait until JavaScript loads and canvas appears
    canvas = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.TAG_NAME, 'canvas')))

    # Inject JavaScript to download the html canvas of the game map
    canvasBase64 = driver.execute_script('return arguments[0].toDataURL("image/png").replace("image/png", "image/octet-stream");', canvas)
    
    # Close headless browser
    driver.quit()

    # Sanitize image data to make it suitable for PIL
    canvasData = re.sub('^data:image/.+;base64,', '', canvasBase64)

    # Convert base64 to Image format
    canvasImage = Image.open(BytesIO(base64.b64decode(canvasData)))

    # True = white pixels, False = black pixels
    canvasImageBW = canvasImage.convert('L').point(lambda x: 255 if x > 200 else 0, mode='1')

    # Save image as B&W np array
    raw_map = np.asarray(canvasImageBW)

    # Get dimensions for cutting
    height, width = len(raw_map), len(raw_map[0])

    # Cut left part of the map
    cut_left = 0
    done = False
    for i in range(width):
        if done: break
        for j in range(40):
            if raw_map[height // 2 + j][i] == True:
                cut_left = i
                done = True
                break

    # Cut top part of the map
    cut_top = 0
    done = False
    for i in range(height):
        if done: break
        for j in range(40):
            if raw_map[i][width // 2 + j] == True:
                cut_top = i
                done = True
                break

    # Insert pixels into reduced_map list
    reduced_map = []
    for i in range(cut_top, height):
        row = []
        for j in range(cut_left, width):
            pixel = raw_map[i][j]
            row.append('#' if pixel else ' ')
        reduced_map.append(row)

    SOKOBAN_MAP = []
    block_size = 64
    N, M = len(reduced_map), len(reduced_map[0])

    def map_squares(x, y):
        '''
        Count the number of white and black pixels in one block square and
        create a map readable for the computer.
        '''
        black_no, white_no = 0, 0
        for i in range(block_size):
            for j in range(block_size):
                if reduced_map[x + i][y + j] == '#': white_no += 1
                else: black_no += 1
        ratio = black_no - white_no
        if 1700 <= ratio <= 1800: return '#'  # wall block
        elif ratio >= 4001: return '#'  # empty field outside of the map
        elif ratio <= -4000: return '.'  # empty block
        elif -4001 <= ratio <= -3800: return 'G'  # goal
        elif 3800 <= ratio <= 3850: return 'C'  # chest
        elif 3858 <= ratio <= 4000: return '*'  # chest on goal
        elif -1500 <= ratio <= -900: return 'P'  # Player
        else: return '@'

    # Iterate through all blocks to create a compact map
    for i in range(0, N, block_size):
        row = []
        for j in range(0, M, block_size):
            if i + block_size < N and j + block_size < M:
                pixels = map_squares(i, j)
                row.append(pixels)
        SOKOBAN_MAP.append(row)

    # Filter empty arrays
    SOKOBAN_MAP = [x for x in SOKOBAN_MAP if x != []]

    # Run with selected algorithm: BFS
    solution = BFS.run_bfs(SOKOBAN_MAP)

    # Print solution
    print(f'Number of steps needed: {len(solution)}\n')
    print(solution)
    print()

    # Map the directions to keyboard keys for testing
    def mapDirectionToKey(direction):
        if direction == 'up': return Keys.ARROW_UP
        elif direction == 'down': return Keys.ARROW_DOWN
        elif direction == 'left': return Keys.ARROW_LEFT
        elif direction == 'right': return Keys.ARROW_RIGHT
        else: raise Exception('Invalid direction!')
    
    solutionKeys = list(map(mapDirectionToKey, solution))

    # Browser setup for testing the solution
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(service=service, options=options)

    # Test in the browser
    driver.get(sokobanSource)

    # Wait until JavaScript loads and canvas appears
    canvas = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.TAG_NAME, 'canvas')))

    # Set up ActionChains for keyboard key sends
    actions = ActionChains(driver)

    # Execute key presses with sleeps between
    for key in solutionKeys:
        actions.send_keys(key)
        actions.perform()
        time.sleep(0.1)
    
    input('Press Enter to end...')
    
    # Close headless browser
    driver.quit()

if __name__ == '__main__':
    main()
