from environs import Env

# Initialize the environment reader.
env = Env()
env.read_env()

ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES")
SECRET_KEY = env.str("API_SECRET_KEY")
DOCS = env.bool("DOCS")
