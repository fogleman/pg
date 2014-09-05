from setuptools import setup

setup(
    name='pg',
    version='0.1',
    description='Python OpenGL Graphics Framework',
    author='Michael Fogleman',
    author_email='michael.fogleman@gmail.com',
    url='https://github.com/fogleman/pg',
    packages=['pg'],
    install_requires=[
        'Pillow',
        'PyOpenGL',
    ],
)
