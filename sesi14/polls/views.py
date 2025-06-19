from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to the Polls Index Page!")

def address(request):
    return HttpResponse("JL.Caringin Ngumbang, Sukabumi")

def phone(request):
    return HttpResponse("0857-2369-3415")
