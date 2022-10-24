from dataclasses import dataclass
import struct
from tkinter import Y
from tokenize import Special
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import animation
from itertools import permutations

from BigBool import isInSomeRange


@dataclass
class ZoneBoundaries:
    numEntires: int = 0
    unknown: int = 0
    A_Z: np.int16 = 0
    A_Y: np.int16 = 0
    A_X: np.int16 = 0
    zoneOrigZ: np.int16 = 0
    zoneOrigY: np.int16 = 0
    zoneOrigX: np.int16 = 0
    B_Z: np.int16 = 0
    B_Y: np.int16 = 0
    B_X: np.int16 = 0
    U_Z: np.int16 = 0
    U_Y: np.int16 = 0
    U_X: np.int16 = 0
    C_Z: np.int16 = 0
    C_Y: np.int16 = 0
    C_X: np.int16 = 0
    V_Z: np.int16 = 0
    V_Y: np.int16 = 0
    V_X: np.int16 = 0
    D_Z: np.int16 = 0
    D_Y: np.int16 = 0
    D_X: np.int16 = 0
    W_Z: np.int16 = 0
    W_Y: np.int16 = 0
    W_X: np.int16 = 0

    # TODO these don't do anything?
    def getA(self):
        return (np.int16(self.A_X), np.int16(self.A_Y), np.int16(self.A_Z))

    def getOrig(self):
        return (np.int16(self.zoneOrigX), np.int16(self.zoneOrigY), np.int16(self.zoneOrigZ))

    def getB(self):
        return (np.int16(self.B_X), np.int16(self.B_Y), np.int16(self.B_Z))

    def getC(self):
        return (np.int16(self.C_X), np.int16(self.C_Y), np.int16(self.C_Z))

    def getD(self):
        return (np.int16(self.D_X), np.int16(self.D_Y), np.int16(self.D_Z))

    def getU(self):
        return (np.int16(self.U_X), np.int16(self.U_Y), np.int16(self.U_Z))

    def getV(self):
        return (np.int16(self.V_X), np.int16(self.V_Y), np.int16(self.V_Z))

    def getW(self):
        return (np.int16(self.W_X), np.int16(self.W_Y), np.int16(self.W_Z))

    def getLists(self, option_str=None):
        x_data = []
        y_data = []
        z_data = []

        all_data = True if option_str is None else False
        if all_data or 'A' in option_str:
            x, y, z = self.getA()
            x_data.append(x)
            y_data.append(y)
            z_data.append(z)

        if all_data or 'O' in option_str:
            x, y, z = self.getOrig()
            x_data.append(x)
            y_data.append(y)
            z_data.append(z)

        if all_data or 'B' in option_str:
            x, y, z = self.getB()
            x_data.append(x)
            y_data.append(y)
            z_data.append(z)

        if all_data or 'C' in option_str:
            x, y, z = self.getC()
            x_data.append(x)
            y_data.append(y)
            z_data.append(z)

        if all_data or 'D' in option_str:
            x, y, z = self.getD()
            x_data.append(x)
            y_data.append(y)
            z_data.append(z)

        if all_data or 'U' in option_str:
            x, y, z = self.getU()
            x_data.append(x)
            y_data.append(y)
            z_data.append(z)

        if all_data or 'V' in option_str:
            x, y, z = self.getV()
            x_data.append(x)
            y_data.append(y)
            z_data.append(z)

        if all_data or 'W' in option_str:
            x, y, z = self.getW()
            x_data.append(x)
            y_data.append(y)
            z_data.append(z)

        return x_data, y_data, z_data

    def origDistCalc(self, buzz_pos, y_sub=True):
        small_x, small_y, small_z = buzz_pos
        smallX = np.int32(small_x >> 7)
        smallY = np.int32((small_y - (0x2000 if y_sub else 0)) >> 7)
        smallZ = np.int32(small_z >> 7)

        botLefX, botLefY, botLefZ = self.A_X, self.A_Y, self.A_Z
        botLefX = np.int32(botLefX)
        botLefY = np.int32(botLefY)
        botLefZ = np.int32(botLefZ)

        the_x = np.int32(np.int32(smallX - botLefX) * self.zoneOrigX)
        the_y = np.int32(np.int32(smallY - botLefY) * self.zoneOrigY)
        the_z = np.int32(np.int32(smallZ - botLefZ) * self.zoneOrigZ)

        return np.int32(the_x + the_y + the_z), the_x, the_y, the_z

    def dist_diff(self, cur_pos, old_pos):
        cur_x, cur_y, cur_z = cur_pos
        old_x, old_y, old_z = old_pos
        cur_dist = self.origDistCalc(cur_pos)
        old_dist = self.origDistCalc(old_pos)

        #print('dist', cur_dist, old_dist, old_dist - cur_dist)
        diff = old_dist - cur_dist
        try:
            calc_z = np.int32((((cur_z - old_z) * old_dist) // diff + (old_z >> 7)) - self.A_Z)
            calc_y = np.int32((((cur_y - old_y) * old_dist) // diff + (old_y >> 7)) - self.A_Y)
            calc_x = np.int32((((cur_x - old_x) * old_dist) // diff + (old_x >> 7)) - self.A_X)
        except:
            print(cur_pos, old_pos)
            print(cur_dist, old_dist, diff, (old_z >> 7))

        return (calc_z, calc_y, calc_x)

    def inRange(self, cur_pos, old_pos, dist=400, cprint=False):
        cz, cy, cx = self.dist_diff(cur_pos, old_pos)
        blx, bly, blz = self.getA()
        tlx, tly, tlz = self.getB()
        trx, t_y, trz = self.getC()
        brx, bry, brz = self.getD()
        sx, sy, sz = self.getOrig()

        if cprint:
            print(f'    // {old_pos}\n'
                  f'    vec3short sVec = {{ {sz}, {sy}, {sx} }};\n'
                  f'    return isInSomeRange({cz}, {cy}, {cx}, {(tlz-blz)}, {(tly-bly)}, {(tlx-blx)}, {(trz-blz)}, {(t_y-bly)}, {(trx-blx)}, &sVec, {dist}) ||\n'
                  f'           isInSomeRange({cz}, {cy}, {cx}, {(trz-blz)}, {(t_y-bly)}, {(trx-blx)}, {(brz-blz)}, {(bry-bly)}, {(brx-blx)}, &sVec, {dist});')

        return (isInSomeRange(cz, cy, cx, (tlz-blz), (tly-bly), (tlx-blx), (trz-blz), (t_y-bly), (trx-blx), sz, sy, sx, dist) or
                isInSomeRange(cz, cy, cx, (trz-blz), (t_y-bly), (trx-blx), (brz-blz), (bry-bly), (brx-blx), sz, sy, sx, dist))


def readZoneObjects(filename='zones.txt'):
    zones = []
    with open(filename, 'r') as zone_file:
        for i, line in enumerate(zone_file):
            s = line.split(' ')
            def _c(hex_str):
                return struct.unpack('>h', bytes.fromhex(hex_str))[0]
            # there is a near 100% chance there is a better way to do this ;(
            a_zone = ZoneBoundaries(_c(s[0]), _c(s[1]),              # some info
                                    _c(s[2]), _c(s[3]), _c(s[4]),    # A
                                    _c(s[5]), _c(s[6]), _c(s[7]),    # origin?
                                    _c(s[8]), _c(s[9]), _c(s[10]),   # B
                                    _c(s[11]), _c(s[12]), _c(s[13]), # U
                                    _c(s[14]), _c(s[15]), _c(s[16]), # C
                                    _c(s[17]), _c(s[18]), _c(s[19]), # V
                                    _c(s[20]), _c(s[21]), _c(s[22]), # D
                                    _c(s[23]), _c(s[24]), _c(s[25])) # W
            #print(i, a_zone)
            zones.append(a_zone)

    return zones

def cubify(data, size=0x4000):
    x_data = []
    y_data = []
    z_data = []

    def _add_cube(x, y, z):
        for x_c in range(x - size, x + size*2, size):
            for y_c in range(y - size, y + size*2, size):
                for z_c in range(z - size, z + size*2, size):
                    x_data.append(x_c)
                    y_data.append(y_c)
                    z_data.append(z_c)

    #print(type(data), data)
    xs, ys, zs = data
    for x, y, z in zip(xs, ys, zs):
        _add_cube(x, y, z)

    return x_data, y_data, z_data

def premuteData(data):
    permuted = []

    indicies = list(range(0, len(data)))
    for (a, b) in list(permutations(indicies, 2)):
        permuted.append(data[a])
        permuted.append(data[b])

    return permuted

def generateZoneGraph(zones,
                      zone_numbers=None,
                      draw_lines=False,
                      all_lines=False,
                      buzz_pos=None,
                      y_sub=True,
                      savefile=None,
                      animate=False):
    fig = plt.figure(figsize=(16,9))
    ax = plt.axes(projection='3d')

    colors = ['gold', 'lime', 'red', 'dodgerblue', 'olive', 'hotpink', 'orange', 'sienna', 'darkolivegreen', 'darkslategray', 'blueviolet', 'indigo', 'violet', 'navy', 'crimson', 'black']
    #colors = ['red', 'orange', 'yellow', 'green', 'dodgerblue', 'navy', 'indigo', 'hotpink']
    #colors.sort()
    color = iter(colors)
    for i, zone in enumerate(zones):
        if zone_numbers is not None and i not in zone_numbers:
            continue
        c = next(color)

        # swap in game Y data with graph Z data so it's the on vertical axis
        (x_data, z_data, y_data) = zone

        # dirty hack to draw the other lines
        if all_lines:
            x_data = premuteData(x_data)
            y_data = premuteData(y_data)
            z_data = premuteData(z_data)

        ax.scatter3D(x_data, y_data, z_data, color=c, label=f'Zone Boundary Id: {hex(i+65)}')
        #ax.scatter3D(x_data, y_data, z_data, color=c)
        ax.axes.set_xlabel('X')
        ax.axes.set_ylabel('Z')
        ax.axes.set_zlabel('Y')
        #print(x_data, y_data, z_data)

        if draw_lines:
            ax.plot(x_data, y_data, z_data, color=c, linestyle='-')

    if buzz_pos:
        bx, bz, by = buzz_pos
        bx = bx / 128.0
        by = (by - (0x2000 if y_sub else 0)) / 128.0
        #by = (by) / 128.0
        bz = bz / 128.0
        ax.scatter3D(bx, by, bz, c='black', label=f'Buzz Spawn Location')
    ax.set_title("Al's Space Land - Unique Zone Boundaries (With Scalars)")
    #ax.set_title("Al's Space Land - Unique Zone Boundaries")
    ax.legend(bbox_to_anchor=(1.60, 0.5), loc='right')
    plt.gca().invert_zaxis()


    if savefile is not None:
        plt.savefig(fname=savefile)

    if not animate:
        plt.show()
    else:
        def rotate_iso(angle):
            ax.view_init(azim=angle, elev=45)

        def rotate_ver(angle):
            ax.view_init(azim=0, elev=(180 - angle))

        def rotate_hor(angle):
            ax.view_init(azim=angle, elev=0)

        angle = 3

        ani = animation.FuncAnimation(fig, rotate_iso, frames=np.arange(0, 360, angle), interval=50)
        ani.save('boundaries_with_scalars.gif', writer=animation.PillowWriter(fps=20))
        #ani.save('boundaries.gif', writer=animation.PillowWriter(fps=20))

        #ani = animation.FuncAnimation(fig, rotate_hor, frames=np.arange(0, 360, angle), interval=50)
        #ani.save('zones_h.gif', writer=animation.PillowWriter(fps=20))

        #ani = animation.FuncAnimation(fig, rotate_ver, frames=np.arange(0, 360, angle), interval=50)
        #ani.save('zones_v.gif', writer=animation.PillowWriter(fps=20))

def inequality_graph_test():
    zone_objs = readZoneObjects()
    zone = zone_objs[9]
    spawn = (315274, 61, -4082)
    old_pos = (0, 14000000 - 0x2000, 0)
    cur_pos = spawn


    good_dist = []
    bad_dist = []
    # don't care about the bad ones
    space = 80000000
    step = int(space / 10.0)
    #y_space = 10000000
    y_space = 10000000
    y_step = int(y_space / 13.0)
    #y_step = int(step / 200)
    for x in range(-space, space, step):
    #for x in [0]:
        for y in range(-y_space, 0, y_step):
        #for y in range(int(-5e6), int(14e6), int(1e4)):
            #for z in [0]:
            for z in range(-space, space, step):
                old_pos = (x,y,z)
                cur_dist = zone.origDistCalc(cur_pos)
                old_dist = zone.origDistCalc(old_pos)
                # avoid div 0
                if cur_pos == old_pos:
                    continue
                inRange = zone.inRange(cur_pos, old_pos)
                if (cur_dist < 0 and old_dist > -1 and inRange):
                    good_dist.append(old_pos)
                else:
                    bad_dist.append(old_pos)

    #for x in [0]:
    #    for y in [13000000,14000000]:
    #        for z in [0]:
    #            old_pos = (x,y,z)
    #            cur_dist = zone.origDistCalc(cur_pos)
    #            old_dist = zone.origDistCalc(old_pos)
    #            # avoid div 0
    #            if cur_pos == old_pos:
    #                continue
    #            inRange = zone.inRange(cur_pos, old_pos)
    #            if (cur_dist < 0 and old_dist > -1 and inRange):
    #                good_dist.append(old_pos)
    #            else:
    #                bad_dist.append(old_pos)

    # swap in game Y data with graph Z data so it's the on vertical axis
    good_x, good_z, good_y = zip(*good_dist)
    bad_x, bad_z, bad_y = zip(*bad_dist)
    for _, y, _ in good_dist:
        print(y)

    ax = plt.axes(projection='3d')

    ax.scatter3D(good_x, good_y, good_z, color='green', label=f'Good')
    #ax.scatter3D(bad_x, bad_y, bad_z, color='red', label=f'Bad')
    ax.axes.set_xlabel('X')
    ax.axes.set_ylabel('Z')
    ax.axes.set_zlabel('Y')
    ax.set_title("Valid Boss Warp Locations for Al's Space Land")
    ax.legend(bbox_to_anchor=(1.60, 0.5), loc='right')
    plt.gca().invert_zaxis()
    plt.show()

def isInSomeRangeTest(old_pos = (0, 14000000, 0)):
    zone_objs = readZoneObjects()
    zone = zone_objs[9]
    cur_pos = (315274, 61, -4082)
    #old_pos = (0, 14000000, 0)
    #old_pos = (315274, 61-0x2000, -4082)
    print(zone.inRange(cur_pos, old_pos, cprint=True))

def main():
    #inequality_graph_test()
    #isInSomeRangeTest((42714, 7159543, 586147))

    #zone_objs = readZoneObjects()
    #zone = zone_objs[9]
    #spawn = (315274, 61, -4082)
    ##old_pos = (0, 14000000, 0)
    #old_pos = (0, 0, 0)
    #cur_pos = spawn
    #cur_dist = zone.origDistCalc(cur_pos)
    #print(cur_dist, cur_dist < 0)
    #old_dist = zone.origDistCalc(old_pos)
    #print(old_dist, old_dist > -1)
    #inRange = zone.inRange(cur_pos, old_pos)
    #print(inRange)
    #return

    zones = []
    zone_objs = readZoneObjects()
    spawn = (315274, 61, -4082)
    warp = (0, 14000000, 0)
    outside_4 = (342526, 59, 149138)
    inside_4 = (321150, 63, 275781)
    #buzz_pos = inside_4
    #buzz_pos = outside_4
    buzz_pos = spawn
    old_buzz_pos = (0, 13000000, 0)

    for i, zone in enumerate(zone_objs):
        #objs = zone.getLists('O')
        objs = zone.getLists('ABCDO')
        zones.append(objs)
        dist, x, y, z = zone.origDistCalc(buzz_pos)
        orig_dist, x, y, z = zone.origDistCalc(old_buzz_pos)
        if i == 9:
            print(zone.getA())
            print(zone.getOrig())
            print(f'{hex(i+65)}) {1 if (dist < 0 and orig_dist > -1) else 0} all | dist: {1 if dist < 0 else 0} orig_dist: {1 if orig_dist > -1 else 0} x: {x}, y: {y}, z: {z}')

    generateZoneGraph(zones,
                     draw_lines=True,
                     all_lines=True,
                     buzz_pos=spawn,
                     y_sub=False,
                     savefile=None,
                     animate=False,
                     zone_numbers=[5,7,10,11,12,13,14,15,16])
                     #zone_numbers=range(0,9))
                     #zone_numbers=range(0,9))#,
                     #zone_numbers=[6])

if __name__ == "__main__":
    main()