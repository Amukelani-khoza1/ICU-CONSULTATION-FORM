from django import forms
from .models import ICUConsultation
from datetime import date

# ------------------------------
# Section A: Patient & Requesting Team Details
# ------------------------------
class SectionAForm(forms.ModelForm):
    class Meta:
        model = ICUConsultation
        fields = [
            'patient_name', 'date_of_birth', 'age', 'gender', 'hospital_number',
            'ward','request_datetime', 'requesting_discipline', 'requesting_dr',
            'requesting_dr_contact', 'requesting_dr_speed_dial'
        ]
        widgets = {
            'request_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    # Ensure all fields are required
    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get("date_of_birth")
        age = cleaned_data.get("age")
        
        # If DOB provided -> calculate age automatically
        if dob:
            today = date.today()
            calculated_age = (
                today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            )
            cleaned_data["age"] = calculated_age  # overwrite manual entry if any
            
        # If neither age nor DOB provided -> raise error
        if not dob and not age:
            raise forms.ValidationError("Please provide either Age or Date of Birth.")
        
        return cleaned_data


# ------------------------------
# Section B: Reason for ICU Consult
# ------------------------------
REASON_CHOICES = [
    ('haemodynamic_instability', 'Haemodynamic instability'),
    ('respiratory_failure', 'Respiratory failure'),
    ('altered_level_of_consciousness', 'Altered level of consciousness'),
    ('post_op_management', 'Post-operative management'),
    ('sepsis_syndrome', 'Sepsis Syndrome'),
    ('multi_organ_dysfunction', 'Multi-organ dysfunction'),
    ('other', 'Other')
]

class SectionBForm(forms.ModelForm):
    reason = forms.MultipleChoiceField(
        choices=REASON_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    reason_other = forms.CharField(required=False)

    class Meta:
        model = ICUConsultation
        fields = ['reason', 'reason_other']

    def clean(self):
        cleaned_data = super().clean()
        reasons = cleaned_data.get('reason', [])
        reason_other = cleaned_data.get('reason_other')

        if 'other' in reasons and not reason_other:
            self.add_error('reason_other', 'Please specify the "Other" reason.')
            
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.reason = self.cleaned_data['reason']  # store list in JSONField
        if commit:
            instance.save()
        return instance


# ------------------------------
# Section C: Clinical Summary
# ------------------------------
class SectionCForm(forms.ModelForm):
    class Meta:
        model = ICUConsultation
        fields = ['clinical_summary']
        widgets = {
            'clinical_summary':forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter clinical summary here...'}),
        }

    def clean_clinical_summary(self):
        data = self.cleaned_data.get('clinical_summary')
        if not data:
            raise forms.ValidationError("This field is required.")
        
        return data


# ------------------------------
# Section D: Current Clinical Status
# ------------------------------
class SectionDForm(forms.ModelForm):
    # Airway
    airway_patent = forms.BooleanField(
        required=False, 
        label="Patent"
        )
    
    airway_threatened = forms.BooleanField(
        required=False, 
        label="Threatened"
        )
    
    def intubated(self):
        value = self.cleaned_data.get('Intubated')
        if value =='yes': 
            return True
        elif value == 'no':
            return False
        return value  
        
        # = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')],
        # widget=forms.RadioSelect,
        # required=False,
        # label="Intubated?"
        # )


    # Breathing
    breathing_spo2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-underline text-center', 'size': 3}),
        required=False,
        label='SpO2 (%)'
        )
    def breathing_distress(self):
        value = self.cleaned_data.get('Distress')
        if value =='yes': 
            return True
        elif value == 'no':
            return False
        return value  
    
    
    # = forms.ChoiceField(
    #     choices=[('yes', 'Yes'), ('no', 'No')], 
    #     widget=forms.RadioSelect, 
    #     required=False,
    #     label="Distress")
    breathing_device = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-underline text-center', 'size': 3}),
        required=False, 
        label="O2 Device"
        )


    # Circulation
    bp_systolic = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-underline text-center', 'size': 3}), 
        required=False,
        label="systolic"
        )
    
    bp_diastolic = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-underline text-center', 'size': 3}), 
        required=False,
        label="Diastolic"
        )

    def clean_circulation_inotropes(self):
        value = self.cleaned_data.get('circulation_intropes')
        if value =='yes': 
            return True
        elif value == 'no':
            return False
        return value  


    def circulation_anti_hpt(self):
        value = self.cleaned_data.get('circulation_anti_hpt')
        if value == 'yes':
            return True
        elif value == 'no':
            return False
        return value 


    # Heart
    heart_rate = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-underline text-center', 'size': 3}),
        required=False,
        label=' bpm'
    )
    
    heart_rhythm = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-underline text-center', 'size': 3}),
        required=False, 
        label="Rhythm"
    )


    # Fluids
    fluid_type = forms.ChoiceField(
        choices=[
            ('', ''),
            ('fluid_type1', 'Fluid1'),
            ('fluid_type2', 'Fluid2'),
            ('fluid_type3', 'Fluid3'),
        ],
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        required=False,
        label="Fluid Type"
    )
    fluid_urine_output = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-underline text-center', 'size': 3}), 
        required=False,
        label="Urine Output (ml/hr)"
        )


    # Temperature
    temperature = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-underline text-center', 'size': 3}),
        required=False,
        label="Temperature (℃)"
        )
    
    measures = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-underline text-center', 'size': 3}),
        required=False,
        label="Temperature control measures"
        )


    # Neuro
    gcs = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-underline text-center', 'size': 3}),
        required=False,
        label="GCS"
        )

    def sedation(self):
        value = self.cleaned_data.get('Sedation')
        if value =='yes': 
            return True
        elif value == 'no':
            return False
        return value  
        
        # = forms.ChoiceField(
        # choices=[('yes','Yes'), ('no','No')], 
        # widget=forms.RadioSelect, 
        # required=False,
        # label="Sedation"
        # )


    # Pupils
    pupil_left_size = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-underline text-center', 'size': 3}),
        required=False, 
        label="left Size"
        )
    pupil_left_reactivity = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-underline text-center', 'size': 3}),
        required=False, 
        label="left Reactivity"
        )
    pupil_right_size = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-underline text-center', 'size': 3}),
        required=False,                          
        label="Right Size")
    pupil_right_reactivity = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-underline text-center', 'size': 3}),
        required=False, 
        label="Right Reactivity")

    class Meta:
        model = ICUConsultation
        fields = [
            'airway_patent', 'airway_threatened', 'intubated',
            'breathing_spo2', 'breathing_distress', 'breathing_device',
            'bp_systolic', 'bp_diastolic', 'circulation_inotropes', 'circulation_anti_hpt',
            'heart_rate', 'heart_rhythm', 'fluid_type', 'fluid_urine_output',
            'temperature', 'measures', 'gcs', 'sedation',
            'pupil_left_size', 'pupil_left_reactivity',
            'pupil_right_size', 'pupil_right_reactivity'
        ]

circulation_inotropes = forms.BooleanField(required=False, widget=forms.CheckboxInput())
circulation_anti_hpt = forms.BooleanField(required=False, widget=forms.CheckboxInput())
# ------------------------------
# Section E: Investigations
# ------------------------------
class SectionEForm(forms.ModelForm):
    latest_abg = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'class': 'form-control'}), required=False)
    key_labs = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'class': 'form-control'}), required=False)
    imaging_findings = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'class': 'form-control'}), required=False)
    time_tests_done = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}), required=False,
                                        input_formats=['%Y-%m-%dT%H:%M'])

    class Meta:
        model = ICUConsultation
        fields = ['latest_abg', 'key_labs', 'imaging_findings', 'time_tests_done']


# ------------------------------
# Section F: Current (Planned) Interventions
# ------------------------------
class SectionFForm(forms.ModelForm):
    airway = forms.CharField(required=False)
    ventilation = forms.CharField(label='Ventilation / Oxygen Support', required=False)
    iv_fluids = forms.CharField(label='IV Fluids', required=False)
    inotropes = forms.CharField(label='Inotropes / Vasopressors', required=False)
    antibiotics = forms.CharField(label='Antibiotics', required=False)
    other_interventions = forms.CharField(label='Other Critical Interventions', required=False)

    class Meta:
        model = ICUConsultation
        fields = [
            'airway', 'ventilation', 'iv_fluids',
            'inotropes', 'antibiotics', 'other_interventions'
        ]


# ------------------------------
# Section G: ICU Doctor's Assessment
# ------------------------------
DECISION_CHOICES = [
    ('admit', 'Admit to ICU'),
    ('not_for_icu', 'Not for ICU'),
    ('review_later', 'Review Later')
]

class SectionGForm(forms.ModelForm):
    assessment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    decision = forms.ChoiceField(choices=DECISION_CHOICES, widget=forms.RadioSelect)
    plan_comments = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    consultant_name = forms.CharField(required=True)
    signature = forms.CharField(required=True)
    datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}), required=True)
    contact_no = forms.CharField(required=False)

    class Meta:
        model = ICUConsultation
        fields = [
            'assessment', 'decision', 'plan_comments',
            'consultant_name', 'signature', 'datetime', 'contact_no'
        ]
