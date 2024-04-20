import pygame
import math
from globals import *

FONT = define_text_font()

class Planet:
  AU = (149.6e6 * 1000) # astronomical unit
  G = 6.67428e-11 # gravitational force
  SCALE = 60 / AU # scaling meters to pixels - 1AU = 100px?
  TIMESTEP = 3600*24

  def __init__(self, x, y, radius, color, mass, figure="", name=""):
    self.x = x
    self.y = y
    self.radius = radius
    self.color = color
    self.mass = mass
    self.figure = figure
    self.name = name

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
