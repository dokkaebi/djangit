from django import http
from django import template
from django.conf import settings
from mainsite.forms import LoginForm
from django.contrib import auth
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def error500(request, template_name='500.html'):
    t = template.loader.get_template(template_name)
    context = template.Context({
        'STATIC_URL': settings.STATIC_URL,
    })
    return http.HttpResponseServerError(t.render(context))

def error404(request, template_name='404.html'):
    t = template.loader.get_template(template_name)
    context = template.Context({
        'STATIC_URL': settings.STATIC_URL,
    })
    return http.HttpResponseNotFound(t.render(context))

class LoginView(FormView):
    form_class=LoginForm
    success_url='/admin/'
    template_name='login.html'

    def get_success_url(self):
        return self.request.GET.get('next', getattr(self,'success_url','/'))

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return http.HttpResponseRedirect(self.get_success_url())
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.data.get('username',None)
        password = form.data.get('password',None)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(self.request, user)
            return http.HttpResponseRedirect(self.get_success_url())
        return super(LoginView, self).form_invalid(form)

class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
