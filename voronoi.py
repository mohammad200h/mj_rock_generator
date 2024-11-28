import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import pyvista as pv


def voronoi3d():

  # Define grid dimensions
  grid_size = 100  # Define 3D grid size (100x100x100)
  num_points = 10  # Number of Voronoi seeds

  # Generate random 3D seed points
  seeds = np.random.rand(num_points, 3) * grid_size  # Scale to grid size

  # Create a 3D grid of points
  x, y, z = np.meshgrid(
      np.linspace(0, grid_size, grid_size),
      np.linspace(0, grid_size, grid_size),
      np.linspace(0, grid_size, grid_size),
  )
  grid_points = np.column_stack([x.ravel(), y.ravel(), z.ravel()])

  # Compute distance to nearest Voronoi seed for each voxel
  distances = distance.cdist(grid_points, seeds, 'euclidean')
  nearest_distances = distances.min(axis=1).reshape((grid_size, grid_size, grid_size))

  # Normalize the distances for better visualization
  texture = (nearest_distances - nearest_distances.min()) / (
      nearest_distances.max() - nearest_distances.min()
  )

  return texture


if __name__ == "__main__":

  texture = voronoi3d()

  # Visualize the 3D texture using PyVista
  grid = pv.ImageData()
  grid.dimensions = texture.shape
  grid.spacing = (1, 1, 1)  # Adjust spacing if needed
  grid.origin = (0, 0, 0)  # Grid starts at the origin
  grid.point_data["Distance Gradient"] = texture.ravel(order="F")  # Add texture data

  # Create PyVista plotter
  plotter = pv.Plotter()
  plotter.add_volume(
      grid, scalars="Distance Gradient", cmap="viridis",
      opacity=[0, 0.2, 0.5, 0.8, 1],  # Custom opacity transfer function
      show_scalar_bar=True
  )
  plotter.show()