import pygame
import math
import numpy as np
from globals import *

FONT = define_text_font()

class Planet:
  AU = 149.6e9 # astronomical unit [m]
  G = 6.67428e-11 # gravitational force
  SCALE = 300 / AU # scaling meters to pixels [px/m]
  TIMESTEP = 3600*24 # timestep [s]

  def __init__(self, x, y, radius, color, mass, figure="", name=""):
    self.x = x # [m]
    self.y = y # [m]
    self.radius = radius # [px]
    self.color = color # string
    self.mass = mass # [kg]
    self.figure = figure # jpg/png
    self.name = name # string

    self.orbit = []
    self.sun = False
    self.distance_to_sun = 0

    self.x_vel = 0
    self.y_vel = 0
  
  # draw image of the planet with pygame
  def draw(self, screen):

    # location of the planet
    x = self.x * self.SCALE + WIDTH / 2
    y = self.y * self.SCALE + HEIGHT / 2
    
		# draw orbit
    if len(self.orbit) > 2:
      updated_points = []
      for point in self.orbit[-5000:]:
        x, y = point
        x = x * self.SCALE + WIDTH / 2
        y = y * self.SCALE + HEIGHT / 2
        updated_points.append((x, y))

      pygame.draw.lines(screen, self.color, False, updated_points, 2)

    # distinguish between painted circle and inserted figure
    if self.figure == "":
      pygame.draw.circle(screen, self.color, (x,y), self.radius)
    else:
			# adjust image position
      x -= self.radius
      y -= self.radius 
      image = pygame.image.load(self.figure)
      image_scaled = pygame.transform.scale(image, (self.radius*2, self.radius*2))
      screen.blit(image_scaled, (x, y))  

    # if not self.sun:
    #   distance_text = FONT.render(f"{round(self.distance_to_sun/1e9, 2)}", 1, WHITE)
    #   screen.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

  # calculate gravitational force between this planet and the other object
  def attraction(self, other):
    distance_x = other.x - self.x
    distance_y = other.y - self.y
    distance = math.sqrt(distance_x**2 + distance_y**2)

    # save updated distance to the sun
    if other.sun:
      self.distance_to_sun = distance

    # attraction in x and y direction
    force = self.G * self.mass * other.mass / distance**2
    theta = math.atan2(distance_y, distance_x)
    force_x = math.cos(theta) * force
    force_y = math.sin(theta) * force

    return force_x, force_y
  
	# calculated new position as a result of the total force of all other planets on this planets
  def update_position(self, planets):
    total_fx = total_fy = 0
    
    for planet in planets:
      if self == planet:
        continue
			
      fx, fy = self.attraction(planet)
      total_fx += fx
      total_fy += fy

    self.x_vel += total_fx / self.mass * self.TIMESTEP
    self.y_vel += total_fy / self.mass * self.TIMESTEP

    self.x += self.x_vel * self.TIMESTEP
    self.y += self.y_vel * self.TIMESTEP

    self.orbit.append((self.x, self.y))


class Comet:
  AU = 149.6e9 # astronomical unit [m]
  G = 6.67428e-11 # gravitational force
  SCALE = 300 / AU # scaling meters to pixels [px/m]
  TIMESTEP = 3600*24 # timestep [s]
  DENSITY = 550 # mean density of Halley's comet [kg/m³]

  # initialization with x [px], y [px], x_vel [px/s], y_vel [px/s], size [px], d [m]
  def __init__(self, x, y, x_vel, y_vel, radius, diameter=5000):
    self.x = (x - WIDTH/2) / self.SCALE # x-distance to sun [m]
    self.y = (y - HEIGHT/2) / self.SCALE # y-distance to sun [m]
    self.x_vel = x_vel / self.SCALE # x-velocity [m/s]
    self.y_vel = y_vel / self.SCALE # y-velocity [m/s]

    self.radius = radius if self.SCALE * self.AU >= 200 else int(radius/2) # displayed radius on the screen [px]
    self.diameter = diameter # diameter of the object [m]
    print("initialisierter Radius", self.radius)
    print(radius, self.SCALE * self.AU)
    
    self.volume = 4/3.*np.pi*(self.diameter/2.)**3 # volume [m³]
    self.mass = self.volume * self.DENSITY
    print("position",x, y, self.x/1e9, self.y/1e9)
    print("velocity", x_vel, y_vel, np.sqrt(self.x_vel**2+self.y_vel**2)/1e3)
    print("mass", self.mass/1e12)
  
  # draw comit on the given screen
  def draw(self, screen):
    # location of the comiet and draw a circle
    x = self.x * self.SCALE + WIDTH / 2
    y = self.y * self.SCALE + HEIGHT / 2  
    pygame.draw.circle(screen, BEIGE, (x, y), self.radius)

  def move(self, planets):
    self.x += self.x_vel * self.TIMESTEP
    self.y += self.y_vel * self.TIMESTEP


  


    

  