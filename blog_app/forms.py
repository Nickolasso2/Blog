from django import forms
from  .models import Comment
from mptt.forms import TreeNodeChoiceField
from django.contrib.auth.forms import AuthenticationForm

class NewComment(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset= Comment.objects.all(),       required = False,
            widget = forms.Select(attrs={'style':'display:none'}), label='') # <=
                        # interchangable
                        # =>
                        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.fields['parent'].required = False
    #     self.fields['parent'].widget.attrs.update(
    #         {'style': 'display:none'})
    #     self.fields['parent'].label = ''


    # widgets can be written down here or in class  Meta
    # content = forms.CharField(widget= forms.Textarea(attrs={'rows':3, 'cols':60}))
   
 
    class Meta:
        model= Comment
        fields = ['content', 'post', 'parent']
        widgets = {
            'content' : forms.Textarea(attrs={'rows':3, 'cols':60, 'class':'form-control'}),
            'post' : forms.TextInput(attrs={'style':'display:none'})
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
