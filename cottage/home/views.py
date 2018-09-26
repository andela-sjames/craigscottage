from django.views.generic.base import TemplateView
from django.shortcuts import render

from .models import CakeDisplay


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request):
        args = {}
        cakes = CakeDisplay.objects.all()
        args['page_title'] = "Craig's - cottage| Home"
        args['cakes'] = cakes

        return render(request, self.template_name, args)
