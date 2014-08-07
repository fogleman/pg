from distutils.core import setup

setup(
    name='pg',
    version='0.1',
    description='Python Distribution Utilities',
    author='Michael Fogleman',
    author_email='fogleman@gmail.com',
    url='https://github.com/fogleman/pg',
    packages=['pg'],
    install_requires=[
        'glfw',
        'Pillow',
        'PyOpenGL',
    ],
)
