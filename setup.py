from setuptools import find_packages, setup

setup(
    name="mj_rock_generator",
    packages=find_packages(),
    include_package_data=False,
    python_requires='>=3',
    url="https://github.com/mohammad200h/mj_rock_generator",
    author="Mohammad Hamid",
    license="MIT",
    install_requires=[
        "numpy>=1.15"
        "pyvista==0.44.2"
    ],
    zip_safe=False
)
