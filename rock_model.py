import mujoco as mj
import typing
import random
import numpy as np

from rock import rock

class Rock:
  def __init__(self,texture,smooth = False,name="rock"):
    self.spec = mj.MjSpec()
    self.model = self.spec.worldbody
    self.spec.compiler.degree = False

    main = self.spec.default()
    main.mesh.scale = [random.random()]*3

    tex = self.spec.add_texture(
        name="rock", type=mj.mjtTexture.mjTEXTURE_2D,
        file = texture,
        width=300, height=300)
    self.spec.add_material(
        name='rock',  reflectance=.2
        ).textures[mj.mjtTextureRole.mjTEXROLE_RGB] = 'rock'
    # defaults
    main = self.spec.default()
    main.geom.type = mj.mjtGeom.mjGEOM_MESH

    mesh = None
    deformed_mesh , smoothed_mesh = rock()
    if smooth:
      mesh  = smoothed_mesh
    else:
      mesh = deformed_mesh

    self.spec.add_mesh(
        name = name,
        uservert = np.array(mesh.points).flatten()

    )
    self.model.add_geom(meshname = name , material = "rock")
    # self.model.add_geom(meshname = name )



