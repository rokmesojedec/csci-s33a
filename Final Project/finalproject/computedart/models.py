from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ModelForm

# Using Crispy forms to generate bootstrap forms
# https://django-crispy-forms.readthedocs.io/en/latest/index.html

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class User(AbstractUser):
    pass

class Configuration(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_author", editable=False
    )
    title = models.CharField(max_length=256)
    grid = models.PositiveSmallIntegerField(validators=[MinValueValidator(4),
                                       MaxValueValidator(200)])
    created = models.DateTimeField(auto_now_add=True, blank=True)


class ConfigurationForm(ModelForm):
    """ Configuratio  model form """

    class Meta:
        """ Post form meta class """

        model = Configuration
        fields = ["title", "grid"]

    helper = FormHelper()
    helper.form_class = "form-group"
    helper.form_show_labels = True
    helper.layout = Layout(
        Field("title", css_class="form-control mt-2 mb-3"),
        Field("grid", css_class="form-control mb-3")
    )


class Color(models.Model):
    configuration  = models.ForeignKey(
        Configuration, on_delete=models.CASCADE, related_name="config_color")
    color = models.CharField(max_length=100)

