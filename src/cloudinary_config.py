import cloudinary
from dotenv import load_dotenv

load_dotenv('.env')

config = cloudinary.config(
    secure=True)

print(config)