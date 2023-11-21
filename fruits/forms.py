from django.forms import ModelForm
from .models import Fruit, Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            'text',
        ]
        labels = {
            'text': 'Resenha',
        }