from django.core.files.storage import FileSystemStorage
from cloudinary_storage.storage import MediaCloudinaryStorage


class CloudinaryMediaStorage(MediaCloudinaryStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.local_storage = FileSystemStorage()

    def save(self, name, content, max_length=None):
        if name.startswith("avatar.svg"):
            # Save the default avatar to the local filesystem
            return self.local_storage.save(name, content)
        # Save user-uploaded avatars to Cloudinary
        return super().save(name, content)

    def url(self, name):
        if name.startswith("avatar.svg"):
            # Serve default avatars from the local filesystem
            return self.local_storage.url(name)
        # Serve user-uploaded avatars from Cloudinary
        return super().url(name)
