from django.db import models
from django.urls import reverse
# Create your models here.

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id})
    
class Finch(models.Model):
    name= models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    #M:M relationship, here we're making the association
    toys = models.ManyToManyField(Toy)
    
    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    # A finch has many photos, a photo belong to a Finch
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for finch_id: {self.finch_id} @{self.url}"
    
    
    
    
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
)

class Feeding(models.Model):
    date = models.DateField()
    meals = models.CharField(max_length=1, choices= MEALS, default=MEALS[0][0])
    #Check if you use the same name variable for finch 
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']