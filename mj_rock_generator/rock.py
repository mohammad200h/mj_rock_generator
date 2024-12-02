import pyvista as pv
from .voronoi import voronoi3d

import numpy as np


def apply_texture(texture, voronoi_grid, mesh):
  # Note to self: I dont have a good understanding of this

  # Map the sphere's vertices into the texture's coordinate space
  points = mesh.points  # Sphere vertices in 3D space
  scaled_points = (points + 0.1) * voronoi_grid  # Scale sphere to fit the texture grid


  # Sample the texture for each vertex
  texture_values = []
  for point in scaled_points:
      x, y, z = np.clip(point.astype(int), 0, voronoi_grid - 1)  # Ensure within bounds
      texture_values.append(texture[x, y, z])

  # Convert texture values to a NumPy array
  texture_values = np.array(texture_values)

  # Add noise for more natural rock-like features
  noise = np.random.normal(scale=0.05, size=texture_values.shape)  # Small random noise
  combined_values = texture_values + noise  # Combine Voronoi texture with noise

  # Displace vertices based on the combined texture
  displacement_strength = 0.3  # Strength of deformation
  normals = mesh.point_normals  # mesh vertex normals
  new_points = points + normals * (combined_values[:, None] * displacement_strength)

  # Create a new mesh with displaced vertices
  deformed_mesh = pv.PolyData(new_points, mesh.faces)
  # Smooth the mesh to create a more natural rock shape
  smoothed_mesh = deformed_mesh.smooth(n_iter=50, relaxation_factor=0.2)

  return deformed_mesh,smoothed_mesh

def rock(base_shape="sphere",subdivide=2,subfilter="loop",
         scale=[1.0, 0.2, 0.5],voronoi_grid=100):
  """
  base_shape : base shape used for mesh generation: cube | sphere
    default: sphere
  subdivide: Increase the number of triangles in a single, connected triangular mesh
    default: 2
  subfilter: subdivide filter: linear | butterfly | loop
    default: loop
  scale : scaling base_shape shape
    default : [1.0, 1.0, 0.5]
  voronoi_grid: define 3D grid size

  """
  # base shape
  mesh = None
  if base_shape == "cube":
    mesh = pv.Cube( center=(0.5, 0.5, 0.5)).triangulate()
  elif base_shape == "sphere":
    mesh = pv.Sphere( center=(0.5, 0.5, 0.5))
  else:
    raise ValueError("wrong base_shape. choose:  cube | sphere ")

  # scale
  mesh = mesh.scale(scale)

  # applying subdivision
  if subfilter not in ["linear", "butterfly" , "loop"]:
    raise ValueError("wrong base_shape. choose:  linear | butterfly | loop ")

  mesh = mesh.subdivide(subdivide, subfilter=subfilter)

  # voronoi 3D texture
  texture = voronoi3d(voronoi_grid)

  mesh = apply_texture(texture,voronoi_grid,mesh)

  return mesh










if __name__ == "__main__":
  rock = rock(base_shape="sphere",scale=[1.0, 0.8, 0.5],subdivide=4)

  print(f"rock::{rock}")
  print(f"rock::vertices::{rock.points}")

  # rock.faces = [n_points_in_face, vertex1, vertex2, ..., vertex_n, ...]
  slice = rock.faces[0]
  faces = rock.faces[1:]

  print(f"rock::faces::{faces}")

  # Visualize the rock-like shape
  plotter = pv.Plotter()
  plotter.add_mesh(rock, color="gray", show_scalar_bar=False)
  plotter.show()