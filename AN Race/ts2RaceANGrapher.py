from cProfile import label
import numpy as np
import matplotlib.pyplot as plt


ax = plt.axes()
# it's all rotated :(
ax.axes.set_xlabel('Z')
ax.axes.set_ylabel('X')

less4_Zline = 0x25342
less4_Xline = 0x3cc17
ax.axline((less4_Zline, 0), (less4_Zline, 1), label=f'1st Progression Z-Line  (Z = {less4_Zline})', c='orange')
ax.axline((0, less4_Xline), (1, less4_Xline), label=f'2nd Progression X-Line (X = {less4_Xline})', c='red')


more4_Zline = 0xb9c2
more4_Xline = -0x42069
ax.axline((more4_Zline, 0), (more4_Zline, 1), label=f'3rd Progression Z-Line (Z = {more4_Zline})', c='green')
ax.axline((0, more4_Xline), (1, more4_Xline), label=f'4th Progression X-Line (X = {more4_Xline})', c='blue')

finish_lineX = -0x24269
ax.axline((0, finish_lineX), (1, finish_lineX), label=f'Finish Line (X = {finish_lineX})', c='black')

race_start = (6496, -156704)
ax.scatter(race_start[0], race_start[1], label=f'Race Star Position')

plt.title("The Essentials of Andy's Neighborhood Race")

plt.grid()

ax.legend(loc='right')
plt.show()