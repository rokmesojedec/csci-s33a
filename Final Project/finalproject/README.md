# Final Project for CSIC S33-a
Author: **Rok Mesojedec (rom0137@g.harvard.edu)**

## References
- Saving base64 to File [https://stackoverflow.com/questions/39576174/save-base64-image-in-django-file-field]
- Django ImageField [https://docs.djangoproject.com/en/3.0/ref/models/fields/]
- Login / Logout code taken from previous class project 4 [https://github.com/me50/rokmesojedec]
- Utils.js taken from Project 4 [https://github.com/me50/rokmesojedec]
- Square class and drawing methods taken from my personal project [https://github.com/rokmesojedec/comp-art/blob/master/src/index.js]

## Project Description 

Computed Art application lets users create, save, and persist configurations for generating repeating patterns in an HTML canvas.
Canvas image can be saved to the server and showcased on the main app page.

The script will produce an image from user adjusted parameters. Each generated image is unique and drawn while applying a set of
rules with chance and probabilities. This means that the chance of producing the same image from the same parameters is highly unlikely due the to probabilistic nature of this software.

- This project was inspired by computer generated arts and ideas of [Dr Edvard Zajec](http://www.mg-lj.si/si/obisk/2506/in-memoriam-edvard-zajec-1938-2018/)
- (https://www.atariarchives.org/artist/sec16.php)

## Project Files

### square.js
Square class is used by the program to define a single square shaped grid unit. These squares are tiled
inside of a canvas in a grid pattern. Eacg square can contain sub-elements such as a circle or four triangles, 
each taking 25% area of the square. Squares are rendered in a random sequence, using a backtracking algorithm.

### utils.js
Helper functions for creating DOM elements, making ajax calls and accessing API paths

### createconfig.js
This script adds ability to dynamically add and remove color pickers on viewconfig.html page.

### viewconfig.js
Contains logic for drawing on canvas. It also fetches configuration data from server and uses it to generate images.
It also adds onclick handlers for redrawing images and saving images on server. 

## Installation

Please run `pip3 install django-crispy-forms` and `pip3 install django` before running this app

## Start script

`python3 manage.py runserver`