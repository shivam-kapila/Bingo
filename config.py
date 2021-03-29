# Secret key
SECRET_KEY = "CHANGE_ME"

# Databases
SQLALCHEMY_DATABASE_URI = "postgresql://bingo:bingo@localhost:5432/bingo"
POSTGRES_ADMIN_URI = "postgresql://postgres:postgres@localhost/postgres"

# Set to True if Less should be compiled in browser. Set to False if styling is pre-compiled.
COMPILE_LESS = True

# expiration of 'Remember me' cookie
SESSION_REMEMBER_ME_DURATION = 365

# List of user email IDs that are allowed to access the admin views
ADMINS = []

# No. of days till which the tickets are valid
TICKET_VALIDITY = 7
