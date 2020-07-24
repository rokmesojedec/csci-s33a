from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm

# Using Crispy forms to generate bootstrap forms
# https://django-crispy-forms.readthedocs.io/en/latest/index.html

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from crispy_forms.bootstrap import PrependedText


class User(AbstractUser):
    """ User model """

    followers = models.ManyToManyField("User", blank=True)

    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    """ Post Model """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_author", editable=False
    )
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.content}"


class PostForm(ModelForm):
    """ Post model form """

    class Meta:
        """ Post form meta class """

        model = Post
        fields = ["content"]

    helper = FormHelper()
    helper.form_class = "form-group"
    helper.form_show_labels = False
    helper.layout = Layout(
        Field("content", rows="3", css_class="form-control mt-2 mb-3"),
        Submit("add_post", "Post"),
    )
