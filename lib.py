import numpy
from stl import mesh
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

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

def plot_points_3d(points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(points.size // 3):
        ax.scatter(points[i][0], points[i][1], points[i][2], color='b')
        ax.text(points[i][0], points[i][1], points[i][2], f'{i}', size=10, zorder=1, color='k')
    plt.show()

def plot_points_2d(points):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(points.size // 2):
        ax.scatter(points[i][0], points[i][1], color='b')
        ax.text(points[i][0], points[i][1], f'{i}', size=10, zorder=1, color='k')
    plt.show()

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

def stereographic_projection(points_3d, radius=1.0):
    projected_points = []
    for point in points_3d:
        x, y, z = point
        if z == radius:
            projected_points.append((float('inf'), float('inf')))
        else:
            xp = radius * x / (radius - z)
            yp = radius * y / (radius - z)
            projected_points.append((xp, yp))
    return numpy.array(projected_points)

def delaunay_triangulation(points_2d):
    #TODO: I'd like to try implementing this myself  
    out = Delaunay(points_2d)
    return out.simplices

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

def generate_dodecahedron(side_length): #FIXME: Not working
    base_sides = 5
    num_sides = 12
    num_facets = 12 * (base_sides - 2)
    
    dodecahedron = create_empty_mesh(num_facets)

    d_vert = numpy.zeros((20, 3))
    d_vert = fibonacci_sphere(20) * (side_length / numpy.sqrt(3))

    return dodecahedron

def generate_sphere(num_facets, radius):
    sphere = create_empty_mesh(num_facets)
    points = fibonacci_sphere(num_facets) * radius # FIXME: How does num points relate to num facets?
    
    # Map points onto 2D plane for easier triangulation
    projected_points = stereographic_projection(points, radius)

    # Deluney triangulation 
    triangles = delaunay_triangulation(projected_points)

    # Invert points to create facets and build mesh
    for i, triangle in enumerate(triangles):
        print(i)
        sphere.vectors[i] = [points[triangle[2]], points[triangle[1]], points[triangle[0]]]

    return sphere

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