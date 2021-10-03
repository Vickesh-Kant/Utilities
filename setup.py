from setuptools import setup
from Utilities import __version__

setup(
    name='SDM-Utilities',
    version= __version__,    
    description='Shared Utilities Definitions',
    url='https://github.com/Vickesh-Kant/SDM-Utilities.git',
    author='Vickesh Kant',
    author_email='vickesh.kant@gmail.com',
    license='BSD 2-clause',
    packages=['SDM-Utilities'],
    install_requires=['pandas',
                      'teradata',
                      'pathlib',
                      'pypiwin32',
                      'os',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: WIN64 :: Windows',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)