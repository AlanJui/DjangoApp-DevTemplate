from django.shortcuts import redirect, render
from django.views.generic import ListView

from datetime import datetime

from .forms import LogMessageForm
from .models import LogMessage


class HomeListView(ListView):
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context


def log_message(request):
    form = LogMessageForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect('home')
        else:
            return render(request,
                          'log_msg/log_message.html',
                          {'form': form})
    else:
        return render(request,
                      'log_msg/log_message.html',
                      {'form': form})


def about(request):
    return render(request, 'log_msg/about.html')


def contact(request):
    return render(request, 'log_msg/contact.html')
