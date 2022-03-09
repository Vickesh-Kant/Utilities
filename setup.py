import setuptools

# Version Control
__version__ = '0.1.22'

setuptools.setup(
    name='Utilities',
    version= __version__,    
    description='Shared Utilities Definitions',
    url='https://github.com/Vickesh-Kant/Utilities.git',
    author='Vickesh Kant',
    author_email='vickesh.kant@gmail.com',
    license='BSD 2-clause',
    packages= setuptools.find_packages(),
    include_package_data = True,
    install_requires=['pandas',
                      'teradata',
                      'pyodbc',
                      'pathlib2',
                      'pyautogui',
                      'numpy',
                      'teradatasql',                     
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
