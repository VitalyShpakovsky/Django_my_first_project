from django.db import models
from django.contrib.auth.models import User
from PIL import Image


def profile_avatar_directory_path(instance: "Profile", filename: str) -> str:
    return f"profile/user_{instance.user_id}/avatar/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(
        null=True, blank=True,
        upload_to=profile_avatar_directory_path,
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)


