from django import forms
from .models import Post, Comment
from django.utils.translation import ugettext as _  
import cv2 
from PIL import Image
import numpy as np
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from .models import Profile
  

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            'likes': forms.HiddenInput(),
            'profile': forms.HiddenInput(),
            'published_date': forms.HiddenInput()
        }
    def clean_main_image(self):

            img1 = self.cleaned_data.get('main_image', False)
            try:
                img = Image.open(img1)
            except Exception as e:
                return img1
            img.save("temp.jpg") 
            img = cv2.imread("C:/Users/sgriffiths/nofacebook/temp.jpg")
            grayscale_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_cascade = cv2.CascadeClassifier('C:/Users/sgriffiths/nofacebook/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
            detected_faces = face_cascade.detectMultiScale(grayscale_image)
            faces = "no"
            imgblank = np.zeros([100,100,3],dtype=np.uint8)
            poppp=Image.fromarray(imgblank)
            poppp.save("temp.jpg")
            for (column, row, width, height) in detected_faces:
                cv2.rectangle(
                    img,
                    (column, row),
                    (column + width, row + height),
                    (0, 255, 0),
                    2
                )
                faces = "yes"
            if faces == "yes":
                raise forms.ValidationError("The picture you tried to upload mayb contain faces, please try another.")
            return img1


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)


class CustomUserCreationForm(forms.ModelForm):  
    class Meta:
        model = User
        fields = ('username', 'password')


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']