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

#load_stl("not_valid.stl")    
mesh_data = load_stl("./input/cube_10mm.stl")
print_mesh_info(mesh_data)
save_stl(mesh_data, "./out/cube_10mm_copy.stl")