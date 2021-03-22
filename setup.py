from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'git',
    'typing',
]

# List of dependencies installed via `pip install -e ".[dev]"`
# by virtue of the Setuptools `extras_require` value in the Python
# dictionary below.
dev_requires = [
    'pytest',
]

setup(
    name='gitswitch',
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
)