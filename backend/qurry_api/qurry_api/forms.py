from django import forms

from qurry_api.decorators import call_methods_starting_with


class BaseActionForm(forms.Form):
    @call_methods_starting_with('_validate_')
    def clean(self):
        return super().clean()

    @call_methods_starting_with('_save_')
    def save(self, commit=True):
        pass


class BaseModelForm(forms.ModelForm):
    def __init__(self, data, *args, instance=None, **kwargs):
        super().__init__(data, *args, instance=instance, **kwargs)

        if instance:
            # remove uneditable
            if hasattr(self.Meta, 'uneditable'):
                for field_name in self.Meta.uneditable:
                    del self.fields[field_name]

            # remove unprovided fields
            for field_name in self.fields:
                if field_name not in data:
                    del self.fields[field_name]

        # change default required error message
        for field in self.fields.values():
            field.error_messages = {'required': f'{field.label} is required'}
