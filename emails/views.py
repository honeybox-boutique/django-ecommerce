from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm

def send_email_view(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            from_email = form.cleaned_data.get('from_email')
            message = form.cleaned_data.get('message')
            phone_num = form.cleaned_data.get('phone_num')
            subject = 'Contact-Us Email - %s - %s - %s' % (name, from_email, phone_num)
            try:
                send_mail(subject, message, settings.EMAIL_HOST_ALIAS_CONTACT, [settings.EMAIL_HOST_ALIAS_CONTACT], auth_user=settings.EMAIL_HOST_USER, auth_password=settings.EMAIL_HOST_PASSWORD)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact_thanks')
    return render(request, 'contact-us.html', {'form': form})




def email_success_view(request):
    return render(request, 'contact-us_thanks.html')

