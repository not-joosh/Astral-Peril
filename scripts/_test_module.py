
import pygame
from entities import UFO

# Create a test UFO object
ufo = UFO(100, 100, [], [])

# Test the launch method
ufo.launch((200, 200), True)

# Test the update method
ufo.update()

# Test the start_drag method
ufo.start_drag()

# Test the end_drag method
ufo.end_drag()
