"""Project startup configuration."""

# PyMySQL is a pure-Python MySQL driver, so deployment does not require native
# compiler packages. Django loads it through the standard MySQLdb interface.
try:
    import pymysql
    pymysql.version_info = (2, 2, 1, "final", 0)
    pymysql.install_as_MySQLdb()
except ImportError:
    # SQLite development remains usable before optional production packages are installed.
    pass
