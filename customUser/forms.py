from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "password1", "password2",'email','first_name','last_name']

    # def form_valid(self, form):
    #     form.instance.is_active = False
    #     response = super(UserRegister, self).form_valid(form)
    #     activation_message, activation_message_html = self.create_activation_message(form)
        # send_mail(
        #     'Registration Confirmation',
        #     activation_message,
        #     settings.EMAIL_HOST_USER,
        #     [form.instance.email],
        #     fail_silently=False,
        #     html_message = activation_message_html
        # )
        # return response
    
    # def create_activation_message(self,form):
    #     link = request.META['HTTP_HOST']+"/accounts/activation/abcd"+str(form.instance.id)
    #     activation_message = f''' 
    #     Hi {form.instance.first_name} {form.instance.last_name},
                                  
    #     Please Click the linke here to activate your account.
    #     http://{link}{link}
                                          
    #     Regards,
    #     Blog Team.
    #     '''

    #     activation_message_html = f''' 
    #     <p>Hi {form.instance.first_name} {form.instance.last_name},</p>
                                  
    #     <p>Please Click the linke here to activate your account.</p>
    #     <a href=http://{link}>http://{link}</a>
                                          
    #     <p>Regards,</p>
    #     <p>Blog Team.</p>
    #     '''
    #     return activation_message, activation_message_html