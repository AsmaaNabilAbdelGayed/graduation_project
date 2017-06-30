from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from users.models import UserAccount

class RegistrationForm(ModelForm):
    username = forms.CharField(label=(u'User Name'))
    email = forms.EmailField(label=(u'Email Address'))
    password = forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label=(u'Verify Password'),widget=forms.PasswordInput(render_value=False))

    class Meta:
        '''hena ba2olo el ModelForm bta3 el RegistrationForm hwa
        el UserAccount w beltaly by3mel elform de ll model da
        ma5sos... execlude de bet2olo hatla2u 3ndak fel UserAccount
        tuple esmaha usermat7otha4 m3aya felform'''
        model = UserAccount
        exclude = ('user',)

    ''' 34an ne3mel check 3la kol field fel form hal el input
        elly d5alo m72a2 el4root elly talebha wla l2a... fabne3mel
        function lkol field 34an nhandel el input'''
    def clean_username(self):
        ''' el try bet4of lw fe username zay el input keda keda mwgood
        wla l2a... lw mafe4 hta5do 3ady... w lw feh hattlob username
        8ero'''
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("That username is already taken, please select another.")

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError("The passwords did not match. Please try again.")
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label=(u'User Name'))
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
