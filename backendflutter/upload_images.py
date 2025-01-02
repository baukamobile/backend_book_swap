import os
import cloudinary.uploader
import environ
env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env()

cloud_name = env("cloud_name")
api_key = env("api_key")
api_secret = env("api_secret")

print("api_secret:", os.environ.get("api_secret"))
print("api_key:", os.environ.get("api_key"))

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name="cloud_name",
    api_key="api_key",
    api_secret="api_secret"
)
folder_path = '/Users/001/PycharmProjects/backendflutter/app/media/book_img/'

# Загружаем файлы
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    if os.path.isfile(file_path):  # Убедимся, что это файл
        try:
            # Загружаем каждый файл на Cloudinary
            upload_result = cloudinary.uploader.upload(file_path)
            print(f"success {filename} uploaded to {upload_result['url']}")
        except Exception as e:
            print(f"Error uploading {filename}: {e}")








