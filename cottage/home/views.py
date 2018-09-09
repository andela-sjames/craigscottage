from django.views.generic.base import TemplateView
from django.shortcuts import render


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request):
        args = {}
        args['page_title'] = "Craig's - cottage| Home"

        return render(request, self.template_name, args)
