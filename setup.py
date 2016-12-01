from setuptools import setup

setup(
    name='blender_file',
    version='1.0',
    description='Blender File',
    url='https://developer.blender.org/diffusion/BBF/',
    author='At Mind B.V. - Jeroen Bakker, Blender Foundation - Campbell Barton',
    author_email='foundation@blender.org',
    license='GNU General Public License v2 or later (GPLv2+)',
    packages=['blender_file'],
    tests_require=[
        'pytest',
    ],
    zip_safe=False,
)
