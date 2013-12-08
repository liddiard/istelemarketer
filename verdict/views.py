import re
import json
from django.http import HttpResponse
from django.views.generic.base import View, TemplateView
from verdict import scrapers

class FrontPageView(TemplateView):

    template_name = "front.html"


class AjaxView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            return super(AjaxView, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404

    def json_response(self, **kwargs):
        return HttpResponse(json.dumps(kwargs), content_type="application/json")

    def success(self, message):
        return self.json_response(result=0, message=message)

    def error(self, error_type, message):
        return self.json_response(result=1, error=error_type, message=message)


class CheckPhoneNumberView(AjaxView):
    
    def post(self, request):
        number = request.POST.get('number')
        pattern = re.compile("^[0-9]+$")
        if number is None:
            return self.error('KeyError', 'Required key (number) not found in '
                                          'request.')
        elif not pattern.match(number):
            return self.error('ValidationError', 'Field (number) contains '
                                              'characters other than numbers.')
        elif len(number) != 10:
            return self.error('ValidationError', 'Field (number) is not 10 '
                                                 'characters long.')
        else:
            scrapers.eight_hundred_notes(number)
            return self.success(number)
