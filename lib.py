import numpy
from stl import mesh

def load_stl(file_path):
    #Load an STL file and return the mesh object
    return mesh.Mesh.from_file(file_path)
    
def save_stl(mesh_obj, file_path):
    #Save the mesh object to an STL file
    mesh_obj.save(file_path)

def print_mesh_info(mesh_obj):
    #Print basic information about the mesh
    print(f"Number of facets: {len(mesh_obj.vectors)}")
    print(f"Bounding box min: {mesh_obj.min_}")
    print(f"Bounding box max: {mesh_obj.max_}")

def detailed_print(mesh_obj):
    #Print detailed information about each facet
    print_mesh_info(mesh_obj)
    for i, vector in enumerate(mesh_obj.vectors):
        print(f"Facet {i}:")
        print(f"  Vertex 1: {vector[0]}")
        print(f"  Vertex 2: {vector[1]}")
        print(f"  Vertex 3: {vector[2]}")

def scale_mesh(mesh_obj, scale_factor):
    #Scale the mesh by a given factor
    mesh_obj.vectors *= scale_factor

def scale_mesh_non_uniform(mesh_obj, scale_factors):
    #Scale the mesh non-uniformly by given factors for each axis
    mesh_obj.vectors *= numpy.array(scale_factors)

def translate_mesh(mesh_obj, translation_vector):
    #Translate the mesh by a given vector
    mesh_obj.vectors += translation_vector

def rotate_mesh(mesh_obj, axis, radians):
    #Rotate the mesh using a given rotation matrix
    return mesh_obj.rotate(axis,radians)