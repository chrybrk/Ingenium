import pygame, sys, math, random, time, os, json, csv
import numpy as np
from pygame.locals import *
from enum import Enum
from PIL import Image

true = True; false = False; nil = None
clock = pygame.time.Clock()

def fpsLock(fps): return clock.tick(fps)

def sine_wave(time, period, amplitude, midpoint): return math.sin(time * 2 * math.pi / period) * amplitude + midpoint
