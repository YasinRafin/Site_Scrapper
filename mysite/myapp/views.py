from django.shortcuts import render,HttpResponseRedirect
from requests.exceptions import MissingSchema, InvalidURL, RequestException
import requests
from bs4 import BeautifulSoup
from .models import Link
# Create your views here.
def scrape(request):
    if request.method == "POST":
        site = request.POST.get('site', '')

        if not site:
            return render(request, 'myapp/scrapper.html', {'error': 'No URL provided', 'data': Link.objects.all()})

        try:
            page = requests.get(site)
            page.raise_for_status() 

        except (MissingSchema, InvalidURL):
            return render(request, 'myapp/scrapper.html', {'error': 'Invalid URL', 'data': Link.objects.all()})

        except RequestException as e:
            return render(request, 'myapp/scrapper.html', {'error': f'Error fetching the URL: {e}', 'data': Link.objects.all()})

        soup = BeautifulSoup(page.text, 'html.parser')

        for link in soup.find_all('a'):
            link_address = link.get('href')
            link_text = link.string if link.string else link.get('title', 'No text')
            if link_address:
                Link.objects.create(address=link_address, name=link_text)

        return HttpResponseRedirect('/')

    else:
        data = Link.objects.all()

    return render(request, 'myapp/scrapper.html', {'data': data})

def clear(request):
    if request.method == "POST":
        Link.objects.all().delete()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'myapp/scrapper.html')