import numpy
from stl import mesh

##### Basic STL Operations #####

def load_stl(file_path):
    #Load an STL file and return the mesh object
    return mesh.Mesh.from_file(file_path)
    
def save_stl(mesh_obj, file_path):
    #Save the mesh object to an STL file
    mesh_obj.save(file_path)

def create_empty_mesh(num_facets):
    #Create an empty mesh with a specified number of facets
    return mesh.Mesh(numpy.zeros(num_facets, dtype=mesh.Mesh.dtype))

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

##### Manipulation Functions #####

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

##### Generation Functions #####

def generate_cube(size):
    cube = create_empty_mesh(12) 
    
    #Theres probably a cleaner way to do this but going through the process seemed important
    cube_faces = numpy.array([
        [[0,0,0], [1, 0, 0], [1, 1, 0], [0, 1, 0]],
        [[0,0,0], [1, 0, 0], [1, 0, 1], [0, 0, 1]],
        [[0,0,0], [0, 1, 0], [0, 1, 1], [0, 0, 1]],
        [[1,1,1], [0, 1, 1], [0, 0, 1], [1, 0, 1]],
        [[1,1,1], [0, 1, 1], [0, 1, 0], [1, 1, 0]],
        [[1,1,1], [1, 0, 1], [1, 0, 0], [1, 1, 0]]])

    for face in cube_faces:
        face[0] = face[0] * size
        face[1] = face[1] * size
        face[2] = face[2] * size
        face[3] = face[3] * size
        
    i = 0;
    for face in cube_faces:
        cube.vectors[i]   = face[0:3]
        cube.vectors[i+1] = [face[0], face[2], face[3]]
        i += 2
    
    return cube

def generate_prism(base_sides, side_length, height):
    if base_sides < 3:
        raise ValueError("Please provide a valid number of sides (3 or more) for the prism base.")
    
    num_facets = base_sides * 2 + (base_sides - 2) * 2
    prism = create_empty_mesh(num_facets)

    base_vertices = numpy.zeros((base_sides, 3))
    base_vertices[0] = [0, 0, 0]
    
    for i in range(1, base_sides):
        base_vertices[i] = [base_vertices[i-1][0] + (side_length * numpy.cos(2 * numpy.pi * i / base_sides)),
                            base_vertices[i-1][1] + (side_length * numpy.sin(2 * numpy.pi * i / base_sides)),
                            0]
        
    top_vertices = base_vertices + numpy.array([0, 0, height]) 
    
    print(base_vertices)
    print(top_vertices)