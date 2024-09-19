import os

# Set environment variables manually for testing
os.environ['CLOUDINARY_CLOUD_NAME'] = 'dnldfoz08'
os.environ['CLOUDINARY_API_KEY'] = '889244259294162'
os.environ['CLOUDINARY_API_SECRET'] = 'ZWpou1IJRUWh_MDVYVIPqUAlrSg'

# Print environment variables to verify
print("Cloudinary Config:")
print("Cloud Name:", os.getenv('CLOUDINARY_CLOUD_NAME'))
print("API Key:", os.getenv('CLOUDINARY_API_KEY'))
print("API Secret:", os.getenv('CLOUDINARY_API_SECRET'))