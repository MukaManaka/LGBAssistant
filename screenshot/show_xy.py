import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import math
import time
import os




fig = plt.figure()

img = np.array(Image.open('screenshot_temp.jpg'))

im = plt.imshow(img, animated=True)

ani = animation.FuncAnimation(fig, im, interval=50, blit=True)

plt.show()
