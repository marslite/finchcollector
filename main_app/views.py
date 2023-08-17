import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Finch, Toy, Photo
from .forms import FeedingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin




def add_photo(request, finch_id):
    print('Testing inside views')
    photo_file = request.FILES.get('photo-file', None)
    print(photo_file, "Check here")
    if photo_file:
        s3 = boto3.client('s3')
        #using uuid to generate unique key for S3
        key = 'pupstagram-ga/' + uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        #the rfind('.') is grabbing the extension at the end of the photo_file.name

        try:
            bucket = os.environ['BUCKET_NAME']
            s3.upload_fileobj(photo_file, bucket, key)
            #Here we are building the full URL string 
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, finch_id= finch_id)
        except Exception as e:
            print('An error has occurred while uploading file to S3 ')
            print(e)

    return redirect('detail', finch_id=finch_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = "Invalid sign-up try one more time"
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

        
              

# finches = [
#   {'name': 'Damian', 'color':'yellow' , 'description': ' yellow medium-sized passerine', 'age': 1},
#   {'name': 'Brulè', 'color':'silver', 'description': ' silver medium-sized passerine', 'age': 2},
  
# ]

# Create your views here.


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def finch_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {
        'finches' : finches
    })

@login_required
def finch_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)

    id_list = finch.toys.all().values_list('id')
    toys_finch_doesnt_have = Toy.objects.exclude(id__in=id_list)

    feeding_form = FeedingForm()

    return render(request, 'finches/detail.html', {
        'finch': finch,
        'feeding_form' : feeding_form,
        'toys': toys_finch_doesnt_have
        })

class FinchCreate(LoginRequiredMixin, CreateView):
    model = Finch
    fields = '__all__'
    # success_url = '/finches'

class FinchUpdate(LoginRequiredMixin,UpdateView):
    model = Finch
    fields = ['color', 'description', 'age']

class FinchDelete(LoginRequiredMixin,DeleteView):
    model = Finch
    success_url = '/finches'

@login_required
def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', finch_id= finch_id)

@login_required
def assoc_toy(request, finch_id, toy_id):
    finch = Finch.objects.get(id = finch_id)
    finch.toys.add(toy_id)
    return redirect('detail', finch_id = finch_id)

class ToyList(LoginRequiredMixin,ListView):
    model = Toy

class ToyDetail(LoginRequiredMixin,DetailView):
    model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin,DeleteView):
    model = Toy
    success_url = '/toys'



