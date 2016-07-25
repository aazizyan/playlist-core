import os


DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://postgres:postgres@localhost:5432/postgres')

DATABASE_CONNECTION = 'DATABASE_CONNECTION'
