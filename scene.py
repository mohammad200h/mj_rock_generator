from rock_model import Rock
from arena import Arena

import tempfile
from PIL import Image

import mujoco as mj
import mujoco.viewer

from perlin_numpy import generate_perlin_noise_2d

if __name__ =="__main__":

  texture = generate_perlin_noise_2d((256, 256), (8, 8))

  with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
    temp_file_path = temp_file.name
     # "L" mode for grayscale
    pil_image = Image.fromarray(texture, mode="L")
    pil_image.save(temp_file_path, format="png")

    print(f"temp_file_path::{temp_file_path}")

    arena = Arena()
    rock = Rock(temp_file_path,smooth=True)

    arena.add_movable_asset(rock,[0,0,0.23])

    model = arena.spec.compile()
    data = mj.MjData(model)

    print(arena.spec.to_xml())

    # visualization
    with mj.viewer.launch_passive(
          model=model, data=data, show_left_ui=False, show_right_ui=False
      ) as viewer:
          mj.mjv_defaultFreeCamera(model, viewer.cam)

          mj.mj_forward(model, data)

          while viewer.is_running():
              mj.mj_step(model, data)
              viewer.sync()
