from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'bcrypt', # cryptography tools for hashing
    'alembic', # migration of sqls
    'deform', # tool for creating and validating forms
    'gitpython',
    'pyramid',  # main pyramid
    'pyramid_jinja2', # jinja2 rendering engine
    'pyramid_retry',
    'pyramid_tm', # transaction manager
    'sqlalchemy', # our orm mapper
    'transaction',
    'typing'
    'waitress', # our server
    'zope.sqlalchemy', # integrates the sqlalchemy transaction manager with the pyramid transaction manager
]

# List of dependencies installed via `pip install -e ".[dev]"`
# by virtue of the Setuptools `extras_require` value in the Python
# dictionary below.
dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'webtest',
]

setup(
    name='gitswitch',
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
)