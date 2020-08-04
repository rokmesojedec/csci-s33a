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
    """ Configuartion Model """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_author", editable=False
    )
    title = models.CharField(max_length=256)
    square_size = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(4), MaxValueValidator(200)]
    )
    grid_width = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )
    grid_height = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )
    circle_chance = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    color_chance = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    four_part_chance = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created = models.DateTimeField(auto_now_add=True, blank=True)
    image_file = models.ImageField(upload_to="images/%Y/%m/%d/", blank=True, null=True)
    animate = models.BooleanField()


class ConfigurationForm(ModelForm):
    """ Configuratio  model form """

    def __init__(self, *args, **kwargs):
        super(ConfigurationForm, self).__init__(*args, **kwargs)
        self.fields["square_size"].initial = 24
        self.fields["grid_width"].initial = 32
        self.fields["grid_height"].initial = 16
        self.fields["animate"].initial = False
        self.fields["circle_chance"].initial = 0
        self.fields["color_chance"].initial = 0
        self.fields["four_part_chance"].initial = 100

    class Meta:
        """ Post form meta class """

        model = Configuration
        fields = [
            "title",
            "square_size",
            "grid_width",
            "grid_height",
            "animate",
            "circle_chance",
            "color_chance",
            "four_part_chance",
        ]
        labels = {
            "square_size": "Square Size (in px)",
            "grid_width": "Grid Width (number of squares)",
            "grid_height": "Grid Height (number of squares)",
            "animate": "Animate Rendering",
            "circle_chance": "% Chance that a circle shape is rendered. 0 won't render any circles.",
            "color_chance": "% Chance that color is inhereted from previous element. 0 means color is always picked randomly",
            "four_part_chance": "% Chance that a non-circle element will contain 4 sub-parts. 0 means that element will contain 2 sub-parts",
        }


class Color(models.Model):
    """ Color Model """

    configuration = models.ForeignKey(
        Configuration, on_delete=models.CASCADE, related_name="config_color"
    )
    color = models.CharField(max_length=100)
