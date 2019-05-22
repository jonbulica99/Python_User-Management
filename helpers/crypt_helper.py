import os

if 'posix' in os.name:
    import crypt
else:
    import pcrypt as crypt
