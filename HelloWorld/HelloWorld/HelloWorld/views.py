# Create your views here.
from django.http import HttpResponse
def Home(request):
	return HttpResponse('<html><body>Hello World</html></body>')

