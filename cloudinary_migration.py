import os
import cloudinary.uploader
import cloudinary.api
import cloudinary
from cloudinary import CloudinaryImage

# Set configuration parameter: return "https" URLs by setting secure=True
config = cloudinary.config(secure=True)
# Log the configuration
print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")


def uploadImage():
    try:
        # Upload an image from a URL to Cloudinary
        result = cloudinary.uploader.upload(
            "https://cloudinary-devs.github.io/cld-docs-assets/assets/images/butterfly.jpeg",
            public_id="quickstart_butterfly",
            unique_filename=False,
            overwrite=True
        )
        # Build the URL for the uploaded image and save it in the variable 'srcURL'
        srcURL = CloudinaryImage("quickstart_butterfly").build_url()
        # Log the image URL to the console
        print("****2. Upload an image****\nDelivery URL: ", srcURL, "\n")
    except Exception as e:
        print("Error uploading image:", e)


def getAssetInfo():
    try:
        # Get and use details of the uploaded image
        image_info = cloudinary.api.resource("quickstart_butterfly")
        # Log the image information to the console
        print("****3. Get and use details of the image****\nUpload response:\n", image_info, "\n")

        # Assign tags to the uploaded image based on its width
        if image_info["width"] > 900:
            update_resp = cloudinary.api.update("quickstart_butterfly", tags="large")
        elif image_info["width"] > 500:
            update_resp = cloudinary.api.update("quickstart_butterfly", tags="medium")
        else:
            update_resp = cloudinary.api.update("quickstart_butterfly", tags="small")

        # Log the new tag to the console
        print("New tag: ", update_resp["tags"], "\n")
    except Exception as e:
        print("Error getting asset info:", e)


def createTransformation():
    try:
        # Transform the image (resize and crop)
        transformedURL = CloudinaryImage("quickstart_butterfly").build_url(width=100, height=150, crop="fill")
        # Log the transformation URL to the console
        print("****4. Transform the image****\nTransformation URL: ", transformedURL, "\n")
    except Exception as e:
        print("Error creating transformation:", e)


def main():
    uploadImage()
    getAssetInfo()
    createTransformation()


main()
