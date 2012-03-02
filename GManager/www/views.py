from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello you are now at the main index!')
