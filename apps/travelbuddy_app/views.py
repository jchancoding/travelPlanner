# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Q
from models import *
import bcrypt
from datetime import date
from datetime import datetime

def index(request):
    return render(request, 'travelbuddy_app/index.html')

def registration(request):
    errors = users.objects.reg_validator(request.POST)
    hashedpw = bcrypt.hashpw(request.POST['pw1'].encode(), bcrypt.gensalt())

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        user = users.objects.create(name=request.POST['name'], username=request.POST['username'], pw=hashedpw)
        user.save()
        request.session['name'] = user.name
        request.session['username'] = user.username
        request.session['userid'] = user.id
        return redirect('/success')

def login(request):
    log_username = request.POST['log_user']
    errors = users.objects.log_validator(request.POST)
    print errors
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        request.session['name']=users.objects.get(username=log_username).name
        request.session['username']=users.objects.get(username=log_username).username
        request.session['userid']=users.objects.get(username=log_username).id
        return redirect('/success')

def success(request):
        if 'name' not in request.session:
            return redirect ("/")

        context = {
        "name": request.session['name']
        }
        return render(request, 'travelbuddy_app/success.html', context)

def delete(request):
    if 'name' not in request.session:
        return redirect ("/")

    username = request.session['username']
    users.objects.filter(username=log_username).delete()
    messages.success(request, 'Deleted yourself')
    return redirect('/')

def dashboard(request):
    if 'name' not in request.session:
        return redirect ("/")

    logged_user = users.objects.get(id=request.session['userid'])
    all_trips = trips.objects.all()
    my_trips = logged_user.wishedtrip.all()

    print logged_user
    print all_trips
    print my_trips

    context = {
    "current_user": logged_user,
    "name": request.session['name'],
    "all_trips": all_trips,
    "my_trips": my_trips
    }

    return render(request, 'travelbuddy_app/dashboard.html', context)

def trippage(request, url_id):
    if 'name' not in request.session:
        return redirect ("/")

    trip = trips.objects.get(id=url_id)
    logged_username = request.session['username']
    logged_user = users.objects.get(username=logged_username)
    attendees= trip.tripgoers.all()
    context = {
    'user': logged_user,
    'trip': trip,
    'attendees': attendees
    }
    return render(request, 'travelbuddy_app/trippage.html', context)

def newtrip(request):
    if 'name' not in request.session:
        return redirect ("/")

    return render(request, 'travelbuddy_app/newtrip.html')

def createtrip(request):
    errors = trips.objects.trip_validator(request.POST)
    current_user = users.objects.get(username=request.session['username'])

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/tripgroups/create')
    else:
        trip = trips.objects.create(destination=request.POST['tripdest'], desc=request.POST['description'], str_date=request.POST['strdate'], end_date=request.POST['enddate'],  created_by=current_user)
        trip.save()
        current_user.wishedtrip.add(trip)

        return redirect('/dashboard')

def logout(request):
    if 'name' not in request.session:
        return redirect ("/")
    # if 'username' not in request.session: redirect to home
    # request.session['name'] = False
    # request.session['username'] = False
    # messages.success(request, 'You have logged out')
    request.session.clear()
    return redirect('/')

def change_trip(request, operation, trip_id):
    if 'name' not in request.session:
        return redirect ("/")

    current_user = users.objects.get(username=request.session['username'])
    tripgroup = trips.objects.get(id=trip_id)

    if operation == 'add':
        current_user.wishedtrip.add(tripgroup)
    elif operation == 'delete':
        tripgroup.delete()

    # if operation == 'add':
    #     users.make_friend(current_user, new_friend)
    # elif operation == 'remove':
    #     users.remove_friend(current_user, new_friend)

    return redirect('/dashboard')
