import os
import pygame

pygame.init()

# size of screen
WIDTH, HEIGHT = 1200, 1200
SCREEN_SIZE = (WIDTH, HEIGHT)

# images used in this simulation
IMAGE_NIGHTSKY = os.path.join("images", "galaxy-sky-stars-nebula-atmosphere-astronomy-93810-wallhere.com.jpg")
IMAGE_SUN      = os.path.join("images", "icons8-sun-96.png")
IMAGE_MERCURY  = os.path.join("images", "icons8-mercury-planet-96.png") 
IMAGE_VENUS    = os.path.join("images", "icons8-venus-planet-96.png")
IMAGE_EARTH    = os.path.join("images", "icons8-earth-planet-96.png")
IMAGE_MOON     = os.path.join("images", "icons8-moon-48.png")
IMAGE_MARS     = os.path.join("images", "icons8-mars-planet-96.png")
IMAGE_JUPITER  = os.path.join("images", "icons8-jupiter-planet-96.png")
IMAGE_SATURN   = os.path.join("images", "icons8-saturn-planet-96.png")

# colors used in this simulation
BEIGE = (245, 245, 220)
BLUE = (100, 149, 237)
DARK_GREY = (80, 78, 81)
ORANGE = (255, 165, 0)
RED = (188, 39, 50)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

def define_text_font():
  # pygame.font.SysFont("comicsans", 16)
  return pygame.font.SysFont("dejavusansmono", 16) 

# set astronomical constants
AU = 149.6e9 # astronomical unit [m]
G = 6.67428e-11 # gravitational force
# define scale of the screen and calculated timestep
SCALE = 300 / AU # scaling meters to pixels [px/m]
SCALE_OUT = 60 / AU # scaling to the outer planets [px/m]
TIMESTEP = 3600*24 # timestep [s]
