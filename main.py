"""
This simulation is inspired by Tech with Tim: https://www.youtube.com/watch?v=WTLPmUHTPqo
night sky image from https://wallhere.com/de/wallpaper/93810
planet symbols were gained from https://icons8.com/icons
<a target="_blank" href="https://icons8.com/icon/62034/moon">Moon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a> 
"""

import pygame
import math
import numpy as np
from objects import *
from globals import *

# initialization
pygame.init()

# create window with the size of the coordinates
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Planet Simulation - Running")

# Set background and screen
background = pygame.image.load(IMAGE_NIGHTSKY)
background_scaled = pygame.transform.scale(background, SCREEN_SIZE)

def zoom_in_and_out(planets, scale, func):
  for planet in planets:
    adjusted_scale = scale / planet.AU
    if planet.SCALE != adjusted_scale: planet.radius = func(planet.radius, 2)
    planet.SCALE = adjusted_scale

def main():
  # booleans for running, stopping and pausing the simulation
  running = True
  active = True

  # setting the sun
  sun = Planet(0, 0, 25, YELLOW, 1.98892 * 10**30, IMAGE_SUN, "Sun")
  sun.sun = True 
  # setting the planets
  mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 0.330e24, IMAGE_MERCURY, "Mercury")
  mercury.y_vel = -47.4e3
  venus = Planet(0.723 * Planet.AU, 0, 12, WHITE, 4.8685e24, IMAGE_VENUS, "Venus")
  venus.y_vel = 35.02e3
  earth = Planet(-1 * Planet.AU, 0, 12, BLUE, 5.9742e24, IMAGE_EARTH, "Earth")
  earth.y_vel = 29.783e3
  mars = Planet(-1.524 * Planet.AU, 0, 10, RED, 0.639e24, IMAGE_MARS, "Mars")
  mars.y_vel = 24.077e3
  jupiter = Planet(5.203 * Planet.AU, 0, 20, DARK_GREY, 1898.13e24, IMAGE_JUPITER, "Jupiter")
  jupiter.y_vel = -13.06e3
  saturn = Planet(9.537 * Planet.AU, 0, 20, DARK_GREY, 568.32e24, IMAGE_SATURN, "Saturn")
  saturn.y_vel = -9.67e3
  # list of used planets
  planets = [mercury, venus, earth, mars, jupiter, saturn, sun]

  # setting game spped and create object and event to track time
  CLOCK = pygame.time.Clock()
  TIMEREVENT = pygame.USEREVENT + 1
  trigger_event_rate = 1000 # trigger TIMEEVENT ever millisecond
  pygame.time.set_timer(TIMEREVENT, trigger_event_rate)
  start_ticks = pygame.time.get_ticks()
  seconds1 = seconds2 = 0

  while running:

    # update clock every second
    CLOCK.tick(60)
    # time since start
    gametime = (pygame.time.get_ticks()-start_ticks)/1000

    # set background of the screen
    SCREEN.blit(background_scaled, (0, 0))

    # writing distance information in the left upper corner
    distance_info_text = FONT.render(f"Distance in million Km", 1, WHITE)
    SCREEN.blit(distance_info_text, (10, 15))

    for event in pygame.event.get():
        if event.type == TIMEREVENT:
            seconds1 = seconds2
            seconds2 = gametime
            # display time interval days per second on screen
            timestep_text = FONT.render(f"timestep: {round(1/(seconds2-seconds1),1)} days per second", 1, BLUE)
            SCREEN.blit(timestep_text, (10, 160))
            #print("seconds elapsed", gametime, trigger_event_rate, seconds2 - seconds1)

            # update planet positions if event is triggered
            for i in range(len(planets)):
              planet = planets[i]
              if planet.name != "Sun":
                distance_text = FONT.render(f"{planet.name}: {round(planet.distance_to_sun/1e9, 3)}", 1, WHITE)
                SCREEN.blit(distance_text, (10, 35+20*i))
            # update planet positions and draw them on the screen
              if active: planet.update_position(planets)
              planet.draw(SCREEN)
              
            # title of the screen
            if active:
              pygame.display.set_caption("Planet Simulation - Running")
            else:
              pygame.display.set_caption("Planet Simulation - Paused")

            pygame.display.update()

        # stops the simulation when ESC is pressed
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
          running = False
        elif event.type == pygame.KEYDOWN:
        # pauses or continue when SPACE is pressed
          if event.key == pygame.K_SPACE:
            active = not active
          # zoom in when "i" is pressed
          elif event.key == pygame.K_i:
            zoom_in_and_out(planets, 300, np.multiply)
          # zoom out when "o" is pressed
          elif event.key == pygame.K_o:
            zoom_in_and_out(planets, 60, np.divide)
        # modify trigger rate of TIMEEVENT on the event queue betwwen 1000ms and 50ms
          elif event.key == pygame.K_UP:
            trigger_event_rate = np.max([25, int(trigger_event_rate/2)])
            pygame.time.set_timer(TIMEREVENT, trigger_event_rate)
          elif event.key == pygame.K_DOWN:
            trigger_event_rate = np.min([1000, int(trigger_event_rate*2)])
            pygame.time.set_timer(TIMEREVENT, trigger_event_rate)
        # elif event.type == pygame.MOUSEBUTTONDOWN: 
        #   if event.button == 4:
        #   elif event.button == 5:

  pygame.quit


if __name__ == '__main__': 
  main()




