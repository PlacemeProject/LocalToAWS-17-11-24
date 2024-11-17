from django import forms
from .models import Candidates

class CandidatePersonalUpdateForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = [
            'fullname', 'gender', 'dob', 'linkedin_profile', 'country', 'state', 'city',
            'marital_status','languages','work_status'
        ]

class CandidateUpdateForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = [
            'fullname', 'gender', 'dob', 'linkedin_profile', 'country', 'state', 'city', 'address',
            'marital_status', 'highest_qualification', 'specialization', 'year_of_graduation',
            'university_name', 'secondary_grade', 'higher_secondary_grade', 'diploma_grade',
            'bachelors_grade', 'masters_grade', 'doctorate_grade', 'present_ctc', 'present_take_home',
            'expected_ctc', 'expected_take_home', 'monthly_incentive', 'other_yearly_pay', 'skill',
            'present_designation', 'work_experience', 'notice_period', 'is_rotate_shift',
            'preferred_location', 'is_relocate', 'professional_summary'
        ]
