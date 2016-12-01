from setuptools import setup, find_packages

setup(
    name='blender-file',
    version='1.0',
    description='Blender File',
    url='https://developer.blender.org/diffusion/BBF/',
    author='At Mind B.V. - Jeroen Bakker, Blender Foundation - Campbell Barton',
    author_email='foundation@blender.org',
    license='GNU General Public License v2 or later (GPLv2+)',
    packages=find_packages('.', exclude=['tests']),
    tests_require=[
        'pytest',
    ],
    zip_safe=False,
)
