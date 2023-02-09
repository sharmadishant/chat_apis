from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','email','username','password1','password2']
        labels = {'first_name':'Name'}

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args,**kwargs)

        for name, field in self.fields.items():
            print(field, name)
            field.widget.attrs.update({'class':'input'})
            # field.widget.attrs.update({'placeholder':'input'})
            if name == "first_name":
                field.widget.attrs.update({'placeholder':'Full Name'})
            elif name == "email":
                field.widget.attrs.update({'placeholder':'Email'})
            elif name == "username":
                field.widget.attrs.update({'placeholder':'Username'})
            elif name == "password1":
                field.widget.attrs.update({'placeholder':'Enter Password'})
            elif name == "password2":
                field.widget.attrs.update({'placeholder':'Confirm Password'})

