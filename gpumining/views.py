from django.shortcuts import render

# Create your views here.
def gpumining(request):
    return render(request, 'gpumining/gpumining.html', {})
    