import hashlib
from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, resolve_url as r
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def new(request):
    if request.method == 'POST':
        return create(request)

    return empty_form(request)


def empty_form(request):
    context = {'form': SubscriptionForm()}
    template_name = 'subscriptions/subscription_form.html'
    return render(request, template_name, context)


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html',
                      {'form': form})

    # Save BD
    subscription = form.save()
    subscription.hash_url = hashlib.md5(subscription.name.encode()).hexdigest()
    subscription.save()

    # Send email
    _send_mail(
        'Confirmação de inscrição',
        settings.DEFAULT_FROM_EMAIL,
        subscription.email,
        'subscriptions/subscription_email.txt',
        {'subscription': subscription})

    return HttpResponseRedirect(r('subscriptions:detail', subscription.hash_url))


def detail(request, hash_url):
    try:
        subscription = Subscription.objects.get(hash_url=hash_url)
    except Subscription.DoesNotExist:
        raise Http404
    return render(request, 'subscriptions/subscription_detail.html', {'subscription': subscription})


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])


