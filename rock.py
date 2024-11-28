import pyvista as pv

def rock():

  # Create a sphere mesh
  cube = pv.Cube().triangulate()
  # sphere = pv.Sphere()

  cube = cube.scale([1.0, 1.0, 0.5])

  # https://docs.pyvista.org/examples/01-filter/subdivide.html#subdivide-cells
  # subfilter -> linear | butterfly | loop
  subdivided_sphere = cube.subdivide(2, subfilter="loop")

  return subdivided_sphere




if __name__ == "__main__":
  subdivided_sphere = rock()

  # Plot the original and subdivided meshes
  p = pv.Plotter()
  # p.add_mesh(cube, color='red', style='wireframe', label='Original Mesh')
  p.add_mesh(subdivided_sphere,style='wireframe', color='blue', label='Subdivided Mesh')
  # p.add_legend()
  p.show()