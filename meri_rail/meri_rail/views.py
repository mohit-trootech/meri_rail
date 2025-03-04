from django.views.generic import TemplateView
from utils.constants import Templates


class SuccessView(TemplateView):
    template_name = Templates.SUCCESS_TEMPLATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.request.session.get("context"))
        return context


success_view = SuccessView.as_view()


class ErrorView(TemplateView):
    template_name = Templates.ERROR_TEMPLATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.request.session.get("context"))
        return context


error_view = ErrorView.as_view()
