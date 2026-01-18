import numpy
from stl import mesh
from lib import *

def main():
    #mesh_data = load_stl("./input/cube_10mm.stl")
    #detailed_print(mesh_data)
    #scale_mesh(mesh_data, 2.0)
    #translate_mesh(mesh_data, numpy.array([5.0, 0.0, 0.0]))
    #rotate_mesh(mesh_data, [0.0, 0.0, 1.0], numpy.radians(45))
    #scale_mesh_non_uniform(mesh_data, [1.0, 2.0, 0.5])
    
    mesh_data = generate_cube([5.0, 3.0, 1.0])

    detailed_print(mesh_data)
    save_stl(mesh_data, "./out/out_cube.stl")

if __name__ == "__main__":
    main()