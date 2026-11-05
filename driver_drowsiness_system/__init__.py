"""Project startup configuration."""

# PyMySQL is a pure-Python MySQL driver, so deployment does not require native
# compiler packages. Django loads it through the standard MySQLdb interface.
try:
    import pymysql
except ImportError:
    # SQLite development remains usable before optional production packages are installed.
    pass
else:
    pymysql.install_as_MySQLdb()
