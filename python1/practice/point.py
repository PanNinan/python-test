from math import sqrt

class Point(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move_to(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def move_by(self, move_x, move_y):
        self.x += move_x
        self.y += move_y

    def distance_to(self, other):
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        distance = sqrt(dx ** 2 + dy ** 2)
        return distance

def main():
    p1 = Point(1, 1)
    p1.move_by(1, 2)
    
    p0 = Point()
    p0.move_to(4, -1)
    dis = p1.distance_to(p0)
    print(dis)


if __name__ == "__main__":
    main()
