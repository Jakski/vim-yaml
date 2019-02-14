from setuptools import setup


# This file is used only for development
setup(
    name='vim-yaml',
    description='ruamel.yaml based highlighting extension for Neovim',
    url='https://github.com/Jakski/vim-yaml',
    author='Jakub Pieńkowski',
    author_email='jakub@jakski.name',
    license='MIT',
    packages=['vim_yaml'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Text Editors',
    ],
    python_requires='>=3',
    install_requires=[
        'pynvim',
        'ruamel.yaml'
    ]
)
