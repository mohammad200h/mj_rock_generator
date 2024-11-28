from voronoi import voronoi3d
import pyvista as pv
import numpy as np

from rock import rock


# Generate the Voronoi texture
grid_size = 100
texture = voronoi3d()

# Create a sphere as the base shape for the rock
sphere = pv.Sphere(radius=1.0, center=(0.5, 0.5, 0.5), theta_resolution=200, phi_resolution=200)

sphere = sphere.scale([1.0, 1.0, 0.5])

# Map the sphere's vertices into the texture's coordinate space
points = sphere.points  # Sphere vertices in 3D space
scaled_points = (points + 0.1) * grid_size  # Scale sphere to fit the texture grid

# Sample the texture for each vertex
texture_values = []
for point in scaled_points:
    x, y, z = np.clip(point.astype(int), 0, grid_size - 1)  # Ensure within bounds
    texture_values.append(texture[x, y, z])

# Convert texture values to a NumPy array
texture_values = np.array(texture_values)

# Add noise for more natural rock-like features
noise = np.random.normal(scale=0.05, size=texture_values.shape)  # Small random noise
combined_values = texture_values + noise  # Combine Voronoi texture with noise

# Displace vertices based on the combined texture
displacement_strength = 0.3  # Strength of deformation
normals = sphere.point_normals  # Sphere vertex normals
new_points = points + normals * (combined_values[:, None] * displacement_strength)

# Create a new mesh with displaced vertices
deformed_sphere = pv.PolyData(new_points, sphere.faces)

# Smooth the mesh to create a more natural rock shape
smoothed_sphere = deformed_sphere.smooth(n_iter=50, relaxation_factor=0.2)

# Visualize the rock-like shape
plotter = pv.Plotter()
plotter.add_mesh(smoothed_sphere, color="gray", show_scalar_bar=False)
plotter.add_mesh(sphere, style="wireframe", color="black", label="Original Mesh")
plotter.add_legend()
plotter.show()



