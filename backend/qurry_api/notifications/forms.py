from django import forms
from qurry_api.forms import BOOL_CHOICES, BaseActionForm


class NotificationActionForm(BaseActionForm):
    read = forms.ChoiceField(choices=BOOL_CHOICES, required=False)

    def _save_read(self):
        read = self.cleaned_data.get('read')
        if read:
            if read == 'true':
                self.instance.delete()
