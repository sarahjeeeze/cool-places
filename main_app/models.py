from django.db import models
from django.utils import timezone

from django.db import models
from django.utils import timezone
from mapbox_location_field.models import LocationField
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver #add this
from django.db.models.signals import post_save 


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    liked = models.ManyToManyField(User, related_name='likes', blank=True, default=0)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(username=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender,instance,**kwargs):
        instance.profile.save()
    
    def __str__(self):
        return str(self.username)

class Post(models.Model):
        #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        profile = models.ForeignKey('main_app.Profile', on_delete=models.CASCADE, related_name="posts", default="")
        title = models.CharField(max_length=200, null=True, blank=True, default="None")
        likes = models.ManyToManyField(User, related_name='liked', blank=True, null=True)
        description = models.TextField(null=True, blank=True, default="None")
        place_name = models.CharField(default="UK", max_length=400, null=False, blank=True)
        picture_type = models.CharField(default="None", max_length=50, null=True, blank=True)
        published_date = models.DateTimeField(blank=True, null=True)
        main_image = models.ImageField(default='image01.png',null=True, blank=True, upload_to="media/static/images")
        location = LocationField(
        map_attrs={"style": "mapbox://styles/mapbox/streets-v11", "readonly": False, "center": (-0.631764294,51.237738)}, default="(-0.631764294,51.45629072)", null=True)
        
    
        def publish(self):
            self.published_date = timezone.now()
            self.save()

        def approved_comments(self):
            return self.comments.filter(approved_comment=True)

        def __str__(self):
            return self.title

class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey('main_app.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
   
    def __str__(self):
        return self.text
    
