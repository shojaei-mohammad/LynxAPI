from environs import Env

# Initialize the environment variables reader
env = Env()
# Load the .env file into the environment
env.read_env()

# Server host and port configuration for Uvicorn
UVICORN_HOST = env.str(
    "UVICORN_HOST", "0.0.0.0"
)  # Default to '0.0.0.0' if not specified
UVICORN_PORT = env.int("UVICORN_PORT", 8081)  # Default to 8081 if not specified

# Access token settings for authentication
ACCESS_TOKEN_EXPIRE_MINUTES = env.int(
    "ACCESS_TOKEN_EXPIRE_MINUTES", 30
)  # Token expiry time

# Application secret key for cryptographic operations
API_SECRET_KEY = env.str("API_SECRET_KEY")  # API secret key

# Aplication security algorithm
API_ALGORITHM = env.str("API_ALGORITHM")

# Enable or disable API documentation
DOCS = env.bool("DOCS", False)  # Whether to generate API docs

# Path to the scripts used by the application
SCRIPTS_PATH = env.str("SCRIPTS_PATH")  # Path to network-config script

# Database configuration
SQLALCHEMY_DATABASE_URL = env.str("SQLALCHEMY_DATABASE_URL")  # Database connection URL
