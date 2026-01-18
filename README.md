# STL-generation
## Background

I've been doing quite a bit of 3D printing since I started working on **[PATT](https://github.com/SamBaker101/PATT_MK0)**. I'm fairly confident using parametric CAD tools but have started to encounter situations where it would be convenient to generate or modify simple STL files directly from the commandline without the overhead of those programs. I am thinking of situations similar to what is supported by the **[Gridfinity Generator](https://gridfinitygenerator.com/en)**, where you have a standard set of geometries but want to quickly create a number of variations. Additionally the ability to make standard edits to models created in CAD (or generated) such as adding uniform fillets, champfers, textures ect. 

## Usage
At this point the program is really just a set of functions defined in lib.py. These are divided into three categories:

### Basic STL Operations
File and print operations and create empty mesh. Any conversion functions will also fall into this category if created.

### Manipulation Functions
Scale, translate and rotate functions.

### Generation Functions
These are functions used to generate shapes and geometries.

## Roadmap
- [x] Open and Close STL Files
- [x] Scale an STL file
- [x] Rotate an STL file
- [x] Generate simple shapes (Cube, Pyramid)
- [ ] Generate a sphere at a given resolution
- [ ] Add champfers to simple shapes
- [ ] Add fillets to simple shapes
- [ ] Stitch models together
- [ ] Selectively scale more complex models (eg. Scale overall dimensions while maintaining wall thickness)

