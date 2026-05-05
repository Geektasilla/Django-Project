# Create your views here.
from django.http import HttpResponse, HttpRequest

def greetings(request: HttpRequest) -> HttpResponse:
  return HttpResponse('HELLO FROM OUR FIRST VIEW!!!')
