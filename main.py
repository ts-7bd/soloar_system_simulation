"""
This program simulates the orbiting planets in our solar system. By startup it shows the inner planets.
Planet positions are calculated for Sun, Mercury, Venus, Earth, Mars, Jupiter, and Saturn#
Zooming in and out enables the view of the outer planets and inner planets or only the inner planets.
You can also launch comets with the mass of the Halley's comet and view its way through the solar system.
If it does not crash with one of the object you may be lucky and it is orbiting around the sun.
Also the simulation speed can be adapted.

This simulation is inspired by the Youtube channel from Tech with Tim: https://www.youtube.com/watch?v=WTLPmUHTPqo
night sky image from https://wallhere.com/de/wallpaper/93810
planet symbols were gained from https://icons8.com/icons
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

# change scale and increase displayed radius of the planet
def zoom_in_and_out(objects, new_scale, func):
  for object in objects:
    old_scale = object.scale
    # change radius only if new scale is different from the current scale
    if old_scale != new_scale: object.radius = func(object.radius, 2)
    object.scale = new_scale
    # if object.__class__.__name__ == "Comet":
    #   print("Comet", object.scale*AU, new_scale*AU, old_scale*AU, object.radius)

# create comet, get velocities, and define radius of displayed circle
def create_comet(comets, current_scale, first_position, second_position):
  first_x, first_y = first_position
  second_x, second_y = second_position
  vel_x = (second_x - first_x) / 1e6
  vel_y = (second_y - first_y) / 1e6
  radius = 4 if current_scale == SCALE else 2
  comet = Comet(first_x, first_y, vel_x, vel_y, current_scale, radius, 1e4)

  comets.append(comet)

def comet_is_gone(comet):
  x_screen = comet.x * SCALE_OUT + WIDTH / 2
  y_screen = comet.y * SCALE_OUT + HEIGHT / 2
  off_screen = x_screen < 0 or x_screen > WIDTH or y_screen < 0 or y_screen > HEIGHT
  return off_screen

def comet_collided(self, comets, planets):
  objects = comets + planets
  for object in objects:
    if object == self:
      continue
    distance = np.sqrt((object.x - self.x)**2 + (object.y - self.y)**2)
    if distance*object.scale < object.radius:
      # print(distance, distance*object.scale, object.radius)
      return True
  
def main():
  # booleans for running, stopping and pausing the simulation
  running = True
  active = True

  comets = []
  temp_obj_pos = None



  # setting the sun
  sun = Planet(0, 0, 25, YELLOW, 1.98892 * 10**30, IMAGE_SUN, "Sun")
  sun.y_vel = 0
  sun.sun = True 
  # setting the planets
  mercury = Planet(0.387 * AU, 0, 8, DARK_GREY, 0.330e24, IMAGE_MERCURY, "Mercury")
  mercury.y_vel = -47.4e3
  venus = Planet(0.723 * AU, 0, 12, WHITE, 4.8685e24, IMAGE_VENUS, "Venus")
  venus.y_vel = 35.02e3
  earth = Planet(-1 * AU, 0, 12, BLUE, 5.9742e24, IMAGE_EARTH, "Earth")
  earth.y_vel = 29.783e3
  mars = Planet(-1.524 * AU, 0, 10, RED, 0.639e24, IMAGE_MARS, "Mars")
  mars.y_vel = 24.077e3
  jupiter = Planet(5.203 * AU, 0, 20, ORANGE, 1898.13e24, IMAGE_JUPITER, "Jupiter")
  jupiter.y_vel = -13.06e3
  saturn = Planet(9.537 * AU, 0, 20, DARK_GREY, 568.32e24, IMAGE_SATURN, "Saturn")
  saturn.y_vel = -9.67e3
  
  # list of used planets
  planets = [mercury, venus, earth, mars, jupiter, saturn, sun]

  # for playing with Jupiters mass
  # mass_multiplier = 1 # Jupiter is a planet
  mass_multiplier = 20 # Jupiter is a brown dwarf
  #mass_multiplier = 100 # Jupiter is a red dwarf
  jupiter.mass = jupiter.mass * mass_multiplier # increasing the mass
  # Sun rotates around the common mass center
  nom, denom = 0, 0
  for planet in planets:
    nom += planet.x*planet.mass
    denom += planet.mass
  mass_center = nom/denom
  # sun need and it planets need to be shifted to the distance from the mass center
  for planet in planets:
    if planet.name == "Jupiter": continue # 
    planet.x = planet.x - mass_center
  print("mass center: ", mass_center)
  if mass_multiplier == 20: sun.y_vel = 2.5e2
  if mass_multiplier == 100: sun.y_vel = 12e2

  # setting game spped and create object and event to track time
  CLOCK = pygame.time.Clock()
  TIMEREVENT = pygame.USEREVENT + 1
  trigger_event_rate : int = 50 # trigger TIMEEVENT ever millisecond
  pygame.time.set_timer(TIMEREVENT, trigger_event_rate)
  start_ticks = pygame.time.get_ticks()
  seconds1 = seconds2 = np.float64(0.)

  while running:

    # update clock every second
    CLOCK.tick(60)
    # time since start
    gametime = np.float64(pygame.time.get_ticks()-start_ticks)/1000.

    # set background of the screen
    SCREEN.blit(background_scaled, (0, 0))

    # writing distance information in the left upper corner
    distance_info_text = FONT.render(f"Distance in million Km", 1, WHITE)
    SCREEN.blit(distance_info_text, (10, 15))

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
      # update positions only when timerevent occurs
      if event.type == TIMEREVENT:
          seconds1 = seconds2
          seconds2 = gametime
          # display time interval days per second on screen
          timestep_text = FONT.render(f"timestep: {round(1/(seconds2-seconds1+0.0001),1)} days per second", 1, BLUE)
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
            
          # title of the screen: running - paused
          if active:
            pygame.display.set_caption("Planet Simulation - Running")
          else:
            pygame.display.set_caption("Planet Simulation - Paused")
          
          # line and circle for launching the comet
          if temp_obj_pos:
            pygame.draw.line(SCREEN, WHITE, temp_obj_pos, mouse_pos, 1)
            r = 4 if planets[0].scale == SCALE else 2 
            pygame.draw.circle(SCREEN, BEIGE, temp_obj_pos, r)  

          # drawing comets
          for comet in comets:
            if active: comet.update_position(planets)
            comet.draw(SCREEN)

            if comet_is_gone(comet) or comet_collided(comet, comets, planets): 
              comets.remove(comet)

          pygame.display.update()

      # stops the simulation when ESC is pressed
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        running = False
      if event.type == pygame.KEYDOWN:
      # pauses or continue when SPACE is pressed
        if event.key == pygame.K_SPACE:
          active = not active
        # zoom in when "i" is pressed
        elif event.key == pygame.K_i:
          zoom_in_and_out(planets, SCALE, np.multiply)
          zoom_in_and_out(comets, SCALE, np.multiply)
        # zoom out when "o" is pressed
        elif event.key == pygame.K_o:
          zoom_in_and_out(planets, SCALE_OUT, np.divide)
          zoom_in_and_out(comets, SCALE_OUT, np.divide)
      # modify trigger rate of TIMEEVENT on the event queue betwwen 1000ms and 50ms
        elif event.key == pygame.K_UP:
          trigger_event_rate = np.max([25, int(trigger_event_rate/2)])
          pygame.time.set_timer(TIMEREVENT, trigger_event_rate)
        elif event.key == pygame.K_DOWN:
          trigger_event_rate = np.min([800, int(trigger_event_rate*2)])
          pygame.time.set_timer(TIMEREVENT, trigger_event_rate)
      if event.type == pygame.MOUSEBUTTONDOWN: 
        if temp_obj_pos:
          # get current scale of the screen and draw comet
          current_scale = planets[0].scale
          create_comet(comets, current_scale, temp_obj_pos, mouse_pos)
          temp_obj_pos = None
        else:
          temp_obj_pos = mouse_pos


  pygame.quit


if __name__ == '__main__': 
  main()




