from django.views.generic.base import View, TemplateView


class FrontPageView(TemplateView):

    template_name = "front.html"


class AjaxView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            return super(AjaxView, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404


class CheckPhoneNumberView(AjaxView):
    
    def post(self, request):
        pass
