from __future__ import annotations
import os, time, sys
from math import cos, sin, floor
from numpy import matmul


"""
Form of vertices is
[x, y, z]

"""
X = 0
Y = 1
Z = 2


def create_rot_x_matrix(theta: float):
    return [[1,0,0],[0,cos(theta), -sin(theta)], [0, sin(theta), cos(theta)]]

def create_rot_y_matrix(theta: float):
    return [[cos(theta), 0, sin(theta)],[0,1,0],[-sin(theta), 0, cos(theta)]]

def create_rot_z_matrix(theta: float):
    return [[cos(theta), -sin(theta), 0], [sin(theta),cos(theta),0], [0,0,1]]




class Cube():
    def __init__(self):
        self.SIZE = 14
        self.vertices = []
        options = [-self.SIZE, self.SIZE]
        for x in options:
            for y in options:
                for z in options:
                    self.vertices.append([x,y,z])

        self.faces = []

        for i in range(3):
            for val in options:
                self.faces.append([v for v in self.vertices if v[i] == val])

    def display(self, x_theta: float, y_theta: float, z_theta: float):

        radius = floor((3 * self.SIZE ** 2) ** 0.5)

        rot_matrix = self.create_rot_mat(x_theta, x_theta, z_theta)
        output = [["  " for _ in range(2 * (radius + 1))] for _ in range(2 * (radius + 1))]
        transformed_vertices = [matmul(rot_matrix, vertex) for vertex in self.vertices]
        transformed_vertices = sorted(transformed_vertices, key = lambda v: v[Z], reverse=True)
        symbols = [".", ".", "@", "@", "*", "*", "x", "x"]

        for symbol, t_vertex in zip(symbols, transformed_vertices):
            x_pos = floor(t_vertex[X]) + radius + 1
            y_pos = floor(t_vertex[Y]) + radius + 1

            assert(x_pos >= 0)
            assert(y_pos >= 0)
            output[y_pos][x_pos] = f"{symbol})"
        
        
        self._print(output, transformed_vertices)
        

    def display_faces(self, x_theta: float, y_theta: float, z_theta: float):


        radius = floor((3 * self.SIZE ** 2) ** 0.5)

        output = [["  " for _ in range(2 * (radius + 1))] for _ in range(2 * (radius + 1))]


        faces = self.get_transform_faces(x_theta, y_theta, z_theta)
        faces = sorted(faces, key = lambda face: max([v[Z] for v in face]))

        symbols = [".", ".", ".", ".", "@", "x"]

        for i, face in enumerate(faces):
            
            if self._check_vertical(face):
                continue
            
            u_min, u_max, l_min, l_max, top, bottom = self.calc_grad_bounds(face)


            for y, row in enumerate(output, start =-(radius+1)):
                for x, _ in enumerate(row, start =-(radius+1)):
                    # do some gradient stuff
                    pt = [x, y , 0]
                    if self.calc_within(u_min, u_max, pt, top) and \
                        self.calc_within(l_min, l_max, pt, bottom) and \
                        y <= top[Y] and y >= bottom[Y]:
                        output[y + radius + 1][x+radius + 1] = f"{symbols[i]} "


        self._print(output, [])
    
    # calculates whether p to v is within the "non convex angle" 
    # v is the "angle if you will"
    def calc_within(self, b_min, b_max, p, v):
        grad = self.calc_gradient(p, v)
        if b_min * b_max > 0:
            return grad > b_min and grad < b_max
        else:
            return grad < b_min or grad > b_max

        
        


    def calc_grad_bounds(self, face):
        top, mid1, mid2, bottom = sorted(face, key = lambda v: v[Y], reverse = True)

        u_min, u_max = sorted([self.calc_gradient(top, mid1), self.calc_gradient(top, mid2)])
        l_min, l_max = sorted([self.calc_gradient(bottom, mid1), self.calc_gradient(bottom, mid2)])

        return u_min, u_max, l_min, l_max, top, bottom   # negative

                    

    def calc_gradient(self, v1, v2):
        if v1[X] == v2[X]:
            return float("inf")
    
        return (v1[Y] - v2[Y])/(v1[X] - v2[X])


    def _check_vertical(self, face):
        # check for dupes
        s = set()

        for v in face:
            if v[X] in s:
                return True
            s.add(v[X])
        return False



    def get_transform_faces(self, x_theta: float, y_theta: float, z_theta: float):
        rot_matrix = self.create_rot_mat(x_theta, y_theta, z_theta)

        rotated = []
        for face in self.faces:
            rotated.append([matmul(rot_matrix, v) for v in face])
        
        return rotated
    
    def create_rot_mat(self, x_theta: float, y_theta: float, z_theta: float):
        x_rot = create_rot_x_matrix(x_theta)
        y_rot = create_rot_y_matrix(y_theta)
        z_rot = create_rot_z_matrix(z_theta)
        return matmul(matmul(x_rot, y_rot), z_rot)

    
    def _print(self, screen, vertices):
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')
        for v in vertices:
            print(f"({v[0]}, {v[1]}, {v[2]}) ")


        for row in screen:
            for val in row:
                print(val, end = "")

            print("")
        


def display_loop():
    cube = Cube()
    x, y, z = 0, 0, 0
    while x < 1000:
        # cube.display(x, y, z)
        cube.display_faces(x,y,z)
        x += 0.05
        y += 0.05
        z += 0.01
        time.sleep(0.2)


if __name__ == "__main__":
    display_loop()









    




