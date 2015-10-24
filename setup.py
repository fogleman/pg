from setuptools import setup

setup(
    name='pg',
    version='0.1',
    description='Python OpenGL Graphics Framework',
    license='MIT',
    author='Michael Fogleman',
    author_email='michael.fogleman@gmail.com',
    url='https://github.com/fogleman/pg',
    packages=['pg'],
    install_requires=[
        'Pillow',
        'PyOpenGL',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
