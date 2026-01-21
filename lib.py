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

##### Math Helpers #####

def get_base_polygon_vertices(sides, side_length):
    vertices = numpy.zeros((sides, 3))
    vertices[0] = [0, 0, 0]
    
    for i in range(1, sides):
        vertices[i] = [vertices[i-1][0] + (side_length * numpy.cos(2 * numpy.pi * i / sides)),
                       vertices[i-1][1] + (side_length * numpy.sin(2 * numpy.pi * i / sides)),
                       0]
    return vertices

def fibonacci_sphere(samples):
    points = []
    phi = numpy.pi * (3. - numpy.sqrt(5.))  # golden angle in radians

    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
        radius = numpy.sqrt(1 - y * y)  # radius at y

        theta = phi * i  # golden angle increment

        x = numpy.cos(theta) * radius
        z = numpy.sin(theta) * radius

        points.append((x, y, z))

    return numpy.array(points)

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

def generate_prism(base_sides, side_length, height):
    if base_sides < 3:
        raise ValueError("Please provide a valid number of sides (3 or more) for the prism base.")
    
    num_facets = base_sides * 2 + (base_sides - 2) * 2
    prism = create_empty_mesh(num_facets)

    base_vertices = get_base_polygon_vertices(base_sides, side_length)
        
    top_vertices = base_vertices + numpy.array([0, 0, height]) 
    
    for i in range(base_sides - 2):
        prism.vectors[i]                = [base_vertices[0], base_vertices[i + 1], base_vertices[i + 2]]
        prism.vectors[i + base_sides-2] = prism.vectors[i] + numpy.array([0, 0, height])

    for i in range(base_sides):
        next_i = (i + 1) % base_sides
        prism.vectors[2 * (base_sides - 2) + i] = [base_vertices[i], base_vertices[next_i], top_vertices[next_i]]
        prism.vectors[2 * (base_sides - 2) + i + base_sides] = [base_vertices[i], top_vertices[next_i], top_vertices[i]]

    return prism

def generate_pyramid(base_sides, side_length, height):
    if base_sides < 3:
        raise ValueError("Please provide a valid number of sides (3 or more) for the pyramid base.")
    
    num_facets = base_sides + (base_sides - 2)
    pyramid = create_empty_mesh(num_facets)

    base_vertices = get_base_polygon_vertices(base_sides, side_length)
        
    apex = numpy.array([numpy.mean(base_vertices[:,0]), numpy.mean(base_vertices[:,1]), height])
    
    for i in range(base_sides - 2):
        pyramid.vectors[i]                = [base_vertices[0], base_vertices[i + 1], base_vertices[i + 2]]

    for i in range(base_sides):
        next_i = (i + 1) % base_sides
        pyramid.vectors[base_sides - 2 + i] = [base_vertices[i], base_vertices[next_i], apex]

    return pyramid

def generate_tetrahedron(side_length):
    return generate_pyramid(3, side_length, side_length * numpy.sqrt(6)/3)

def generate_cube(size):
    return generate_prism(4, size, size)

def generate_octahedron(side_length):
    num_facets = 8
    base_sides = 4
    height = (side_length * numpy.sqrt(2)) / 2
    octahedron = create_empty_mesh(num_facets)

    base_vertices = get_base_polygon_vertices(base_sides, side_length)
        
    upper_apex = numpy.array([numpy.mean(base_vertices[:,0]), numpy.mean(base_vertices[:,1]), height])
    lower_apex = numpy.array([numpy.mean(base_vertices[:,0]), numpy.mean(base_vertices[:,1]), - height])
    
    for i in range(base_sides):
        next_i = (i + 1) % base_sides
        octahedron.vectors[i]              = [base_vertices[i], base_vertices[next_i], upper_apex]
        octahedron.vectors[base_sides + i] = [base_vertices[next_i], base_vertices[i], lower_apex]
    return octahedron

def generate_dodecahedron(side_length):
    base_sides = 5
    num_sides = 12
    num_facets = 12 * (base_sides - 2)
    
    dodecahedron = create_empty_mesh(num_facets)

    d_vert = numpy.zeros((20, 3))
    d_vert = fibonacci_sphere(20) * (side_length / numpy.sqrt(3))
    
    #This is ungraceful
    #This also doesn't work... FIXME:
    dodecahedron_faces = [
        [d_vert[0], d_vert[1], d_vert[2],  d_vert[3], d_vert[4],],
        [d_vert[0], d_vert[5], d_vert[10], d_vert[6], d_vert[1],],
        [d_vert[1], d_vert[6], d_vert[11], d_vert[7], d_vert[2],],
        [d_vert[2], d_vert[7], d_vert[12], d_vert[8], d_vert[3],],
        [d_vert[3], d_vert[8], d_vert[13], d_vert[9], d_vert[4],],
        [d_vert[4], d_vert[9], d_vert[14], d_vert[5], d_vert[0],],
        [d_vert[15], d_vert[10], d_vert[5 ], d_vert[14], d_vert[19]],
        [d_vert[16], d_vert[11], d_vert[6 ], d_vert[10], d_vert[15]],
        [d_vert[17], d_vert[12], d_vert[7 ], d_vert[11], d_vert[16]],
        [d_vert[18], d_vert[13], d_vert[8 ], d_vert[12], d_vert[17]],
        [d_vert[19], d_vert[14], d_vert[9 ], d_vert[13], d_vert[18]],
        [d_vert[19], d_vert[18], d_vert[17], d_vert[16], d_vert[15]]
    ]

    for i, face in enumerate(dodecahedron_faces):
        for j in range(base_sides - 2):
            dodecahedron.vectors[i * (base_sides - 2) + j] = face[0] , face[j + 1], face[j + 2]

    return dodecahedron


def generate_icosahedron(side_length):
    raise NotImplementedError("Icosahedron generation is not implemented yet.")

def generate_platonic(num_sides, side_length):
    if num_sides == 4:
        return generate_tetrahedron(side_length)
    elif num_sides == 6:
        return generate_cube(side_length)
    elif num_sides == 8:
        return generate_octahedron(side_length)
    elif num_sides == 12:
        return generate_dodecahedron(side_length) 
    elif num_sides == 20:
        return generate_icosahedron(side_length) 
    else:
        raise ValueError("Unsupported number of sides for Platonic solid.")