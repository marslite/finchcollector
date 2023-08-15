from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch


# finches = [
#   {'name': 'Damian', 'color':'yellow' , 'description': ' yellow medium-sized passerine', 'age': 1},
#   {'name': 'Brulè', 'color':'silver', 'description': ' silver medium-sized passerine', 'age': 2},
  
# ]

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def finch_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {
        'finches' : finches
    })

def finch_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    return render(request, 'finches/detail.html', {'finch': finch})


class FinchCreate(CreateView):
    model = Finch
    fields = '__all__'
    # success_url = '/finches'

class FinchUpdate(UpdateView):
    model = Finch
    fields = ['color', 'description', 'age']

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches'
