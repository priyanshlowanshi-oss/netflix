from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class addemploye(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    roll_CHOICES = [
        ('DM/A', 'DATA monitor / Analyst'),
        ('CM', 'content moderator'),
        ('HR', 'hr manager'),
    ]

    roll = models.CharField(max_length=100, choices=roll_CHOICES, default='select')
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} | {self.email}"
        # return f"{self.name}, + ,{self.email}"



class aadmovies(models.Model):

    category_id=models.CharField(max_length=50)
    movie_name=models.CharField(max_length=100)
    movie_genre_CHOICES = [
       ('A/T' ,'Action / Thriller') ,
       ('DR','Drama'),
       ('C','Comedy'),
       ('H','Horror'),
       ('D','Documentary')

    ]
    movie_genre=models.CharField(max_length=100 ,choices=movie_genre_CHOICES,default='A/T')

    def __str__(self):
        return f"{self.movie_name}|{self.movie_genre}"




class user(models.Model):

    
    def __str__(self):
        self




from django.db import models
from django.contrib.auth.models import User


class MyList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"       