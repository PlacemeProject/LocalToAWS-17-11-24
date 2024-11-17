from django import forms
from recruiters.models import Locations

class JobForm(forms.ModelForm):
    locations = forms.ModelMultipleChoiceField(
        queryset=Locations.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    # class Meta:
    #     model = Job
    #     fields = ['job_title', 'locations'] 