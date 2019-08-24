import pyxel as px
from PIL import Image
from math import radians, cos, sin, sqrt
from copy import deepcopy


class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def length(self, origin):
        return sqrt(((self.x - origin.x) ** 2) + ((self.y - origin.y) ** 2))

    def add(self, vec):
        self.x += vec.x
        self.y += vec.y

    def sub(self, vec):
        self.x -= vec.x
        self.y -= vec.y

    def rotate(self, angle, origin):
        if self == origin:
            return
        self.sub(origin)
        tempx = self.x
        self.x = (tempx * cos(radians(angle))) - (self.y * sin(radians(angle)))
        self.y = (tempx * sin(radians(angle))) + (self.y * cos(radians(angle)))
        self.add(origin)


class Player:
    def __init__(self, pos):
        self.pos = pos
        self.angle = 0
        self.vel = Vec2d(1, 0)
        self.center = Vec2d(self.pos.x + 25, self.pos.y)

    def updatepos(self):
        if self.angle > 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360

        if px.btn(px.KEY_W):
            self.pos.add(self.vel)
            self.center.add(self.vel)
        if px.btn(px.KEY_S):
            self.pos.sub(self.vel)
            self.center.sub(self.vel)
        if px.btn(px.KEY_A):
            self.rotate(-2)
        if px.btn(px.KEY_D):
            self.rotate(2)

    def rotate(self, angle):
        self.angle += angle
        self.vel.rotate(angle, globalorigin)
        self.center.rotate(angle, self.pos)

    def draw(self):
        px.line(self.pos.x, self.pos.y, self.center.x, self.center.y, 9)
        px.pix(self.pos.x, self.pos.y, 8)


def importmap(img):
    mapimg = Image.open(img)
    map = list(mapimg.getdata())
    for x in range(len(map)):
        if map[x][0] == 0:
            map[x] = 0
        else:
            map[x] = 1
    width, height = mapimg.size
    map = [map[i * width:(i + 1) * width] for i in range(height)]
    return map


def drawmap():
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == 1:
                px.pix(x, y, 7)


def castray(angle, origin):
    basis = Vec2d(0.2, 0)
    basis.rotate(angle, globalorigin)
    ray = deepcopy(origin)
    while True:
        ray.add(basis)
        try:
            if map[int(ray.y)][int(ray.x)] == 1:
                return ray.length(origin)
        except Exception:
            return 0.1


map = importmap("map.png")
plr = Player(Vec2d(10, 10))
globalorigin = Vec2d(0, 0)

raybuffer = []
rayoffset = []
for x in range(64):
    raybuffer.append(None)
    rayoffset.append(None)


def update():
    plr.updatepos()

    for x in range(64):
        raybuffer[x] = castray(((plr.angle - 30) + ((0.2352941 * 4)) * x), plr.pos)
        if raybuffer[x] > 255:
            raybuffer[x] = 255
        raybuffer[x] = ((255 - raybuffer[x])) * 10 / raybuffer[x]
        if raybuffer[x] > 255:
            raybuffer[x] = 255
        rayoffset[x] = (abs(raybuffer[x] - 255) / 2)


def draw():
    px.cls(1)
    px.rect(0, 127, 255, 255, 2)
    for x in range(len(raybuffer)):
        px.rect(x * 4, rayoffset[x], x * 4 + 4, raybuffer[x] + rayoffset[x], 6)
    if px.btn(px.KEY_Q):
        
        drawmap()
        plr.draw()


px.init(255, 255)
px.run(update, draw)
