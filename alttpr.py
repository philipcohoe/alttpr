import random
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

# set romDir to where you keep your "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc" file
romDir = "/home/philip/Downloads/"
# set downloadsDir to your downloads folder
downloadsDir = "/home/philip/Downloads/"
# set gameDir to where you want the game files to eventually go
gameDir = "/home/philip/Downloads/"

# Here's the seed
random.seed(0)

entrance = random.randint(0, 1) == 1
enemize = random.randint(0, 1) == 1
boss = random.randint(0, 1) == 1
pots = random.randint(0, 1) == 1
palette = random.randint(0, 1) == 1
variation = random.choice(["None", "Keysanity", "Retro"])
heart = random.choice(["Blue", "Green", "Red", "Yellow"])
goals = ["Defeat Ganon", "All Dungeons", "Master Sword Pedestal", "Triforce Pieces"]
if entrance:
    goals.append("Crystals")
    shuffle = random.choice(["Simple", "Restricted", "Full", "Crossed", "Insanity"])
else:
    state = random.choice(["Open", "Inverted"])
goal = random.choice(goals)

#options = Options()
#options.headless = True
#driver = webdriver.Chrome(chrome_options = options)
driver = webdriver.Chrome()

def setOption(key, value):
    driver.find_element_by_xpath("//div[@id='" + key + "']").click()
    driver.find_element_by_xpath("//div[@id='" + key + "']//span[contains(text(), '" + value + "')]").click()

def setToggle(key):
    driver.find_element_by_xpath("//div[@id='" + key + "']").click()

driver.get("https://alttpr.com/en/randomizer")
driver.find_element_by_tag_name("input").send_keys(romDir + "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc")
WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.NAME, "generate")))
if entrance:
    driver.find_element_by_xpath("//a[contains(text(), 'Switch to Entrance Randomizer')]").click()
    setOption("shuffle", shuffle)
else:
    setOption("weapons", "Randomized")
    setOption("mode-state", state)
if enemize or boss or pots or palette:
    driver.find_element_by_xpath("//button[contains(text(), 'Enable Enemizer')]").click()
    if boss:
        setOption("enemizer-boss", "Simple")
    if pots:
        setToggle("enemizer-pot_shuffle")
    if palette:
        setToggle("enemizer-palette_shuffle")
    if not enemize:
        setToggle("enemizer-enemy")
setOption("variation", variation)
setOption("goal", goal)
driver.find_element_by_name("generate").click()
WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Save Spoiler')]")))
setToggle("quickswap")
setOption("heart-color", heart)
setOption("sprite-gfx", "Random")
time.sleep(0.1)
driver.find_element_by_xpath("//button[contains(text(), 'Save Spoiler')]").click()
driver.find_element_by_xpath("//button[contains(text(), 'Save Rom')]").click()
time.sleep(0.1)

for filename in os.listdir(downloadsDir):
    if filename.startswith("ALttP"):
        os.rename(downloadsDir + filename, gameDir + "ALttP" + filename[-4:])

driver.close()