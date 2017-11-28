from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime
  # Create your models here.
NAME_REGEX = re.compile(r"(^[A-Z][-a-zA-Z]+$)")
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
PASS_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
  # uploaded_by_id = models.ForeignKey(users, related_name = "uploader")
  # likes = models.ManyToManyField(users, related_name = "likes")

class usersManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}

        name = postData['name']
        username = postData['username']
        pw1 = postData['pw1']
        pw2 = postData['pw2']

        if not NAME_REGEX.match(name):
            errors['name'] = "Name input is invalid"

        if len(name) < 4 or len(username) < 4:
            errors['name_len'] = "Name and username must be more than 3 characters"

        if len(name) == 0 or len(username) == 0:
            errors['name_blank'] = "Name or username cannot be empty"

        try:
            users.objects.get(username=username)
            errors['username_taken'] = "Username is taken"
        except:
            pass

        if not PASS_REGEX.match(pw1):
            errors['pw1'] = "Password is invalid"

        if pw1 != pw2:
            errors['pw2'] = "Password does not match"

        return errors

    def log_validator(self, postData):
        errors = {}

        log_user = postData['log_user']
        log_pw = postData['pw']

        try:
            users.objects.get(username=log_user)
            db_pw = users.objects.get(username=log_user).pw
            if not bcrypt.checkpw(log_pw.encode(), db_pw.encode()):
                errors['not_match'] = "Invalid password"
        except:
            errors['not_user'] = "Invalid username"

        return errors

class tripsManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        tripname = postData['tripdest']
        desc = postData['description']
        strdate = str(postData['strdate'])
        enddate = str(postData['enddate'])
        nowdate = str(datetime.now())

        if len(tripname) < 4:
            errors['shortname'] = "Destination name has to be more than 3 characters"
        if len(tripname) > 50:
            errors['longname'] = "Destination name is too long, max 50 characters"
        if len(tripname) == 0:
            errors['noname'] = "Please enter a destination"

        if len(desc) == 0:
            errors['nodesc'] = "Please enter a Description"
        if len(desc) > 255:
            errors['nodesc'] = "Description is too long, max 300 characters"

        print strdate
        print enddate
        print nowdate

        if not strdate:
            errors['nostrdate'] = "Please input a start date"
        if not enddate:
            errors['noenddate'] = "Please input a start date"

        if strdate <= nowdate or enddate <= nowdate:
            errors['pastdate'] = "Trip start/end dates must be in the future"
        if enddate <= strdate:
            errors['wrongstartend'] = "End date cannot be before start date"

        return errors

class users(models.Model):
  name = models.CharField(max_length=50)
  username = models.CharField(max_length=30)
  pw = models.CharField(max_length=30)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  objects = usersManager()

class trips(models.Model):
  destination = models.CharField(max_length=50)
  desc = models.CharField(max_length=300)
  str_date= models.DateField(default=datetime.now())
  end_date= models.DateField(default=datetime.now())
  created_by = models.ForeignKey(users, null=True, related_name='created_trip')
  tripgoers = models.ManyToManyField(users, related_name='wishedtrip')
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  objects = tripsManager()
