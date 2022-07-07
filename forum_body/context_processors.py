from django.conf import settings
from .forms import SearchForm

def search(request):
    """Implements discussion search button in base.html"""

    search_form = SearchForm()
    return search_form
