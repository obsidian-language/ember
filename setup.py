from setuptools import setup

setup(
    name='ember',
    version='0.1.0-beta',
    author='Codezz-ops',
    author_email='codezz-ops@obsidian.cc',
    description='A command-line interface for managing tools like Obsidian, Cinder, and Ember.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/obsidian-language/ember',
    py_modules=['cli', 'downloader', 'installer', 'ui', 'utils'],
    entry_points={
        'console_scripts': [
            'ember = cli:main',
        ],
    },
    package_dir={'': 'src'},
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)