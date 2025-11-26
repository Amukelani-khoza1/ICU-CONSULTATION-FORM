from django.db import models
from datetime import date

# ------------------------------
# ICU Consultation Model
# ------------------------------
class ICUConsultation(models.Model):
    # ------------------------------
    # Section A: Patient & Requesting Team Details
    # ------------------------------
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    
    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    WARD_CHOICES = [
        ('emergency unit', 'Emergency Unit'),
        ('ward a', 'Ward A'),
        ('ward b', 'Ward B'),
        ('ward c', 'Ward C'),
        ('ward d', 'Ward D'),
        ('ward e', 'Ward E'),
        ('ward f', 'Ward F'),
        ('ward g', 'Ward G'),
        ('ward h', 'Ward H'),
        ('ward i', 'Ward I'),
        ('ward j', 'Ward J'),
        ('ward k', 'Ward K'),
        ('ward l', 'Ward L'),
        ('ward m', 'Ward M'),
        ('ward n', 'Ward N'),
        ('ward o', 'Ward O'),
        ('ward p', 'Ward P'),
        ('ward q', 'Ward Q'),
        ('ward r', 'Ward R'),
        ('ward s', 'Ward S'),
        ('ward t', 'Ward T')
    ]
    
    REQUESTING_DISCIPLINE_CHOICES = [
        ('anaesthesia', 'Anaesthesia'),
        ('cardiology', 'Cardiology'),
        ('cardiothoracic surgery', 'Cardiothoracic Surgery'),
        ('dermatology', 'Dermatology'),
        ('ent surgery', 'ENT Surgery'),
        ('gastroenterology surgery', 'Gastroenterology Surgery'),
        ('General Surgery', 'General Surgery'),
        ('internal medicine', 'Internal Medicine'),
        ('maxillofacial surgery', 'Maxillofacial Surgery'),
        ('nephrology', 'Nephrology'),
        ('neurology', 'Neurology'),
        ('neurosurgery', 'Neurosurgery'),
        ('obstetrics and gynaecology', 'Obstetrics and Gynaecology'),
        ('oncology', 'Oncology'),
        ('orthopaedics surgery', 'Orthopaedics Surgery'),
        ('paediatrics', 'Paediatrics'),
        ('urology', 'Urology')
    ]

    patient_name = models.CharField(max_length=255)
    
    # Either Age OR Date of Birth can be provided
    age = models.PositiveIntegerField(null=True, blank=True, help_text="Enter if DOB is not known")
    date_of_birth = models.DateField(null=True, blank=True, help_text="Enter if available, system can calculate age")
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    hospital_number = models.CharField(max_length=50)
    ward = models.CharField(max_length=100, choices=WARD_CHOICES)
    request_datetime = models.DateTimeField()
    requesting_discipline = models.CharField(max_length=100, choices=REQUESTING_DISCIPLINE_CHOICES)
    requesting_dr = models.CharField(max_length=200, null=True, blank=True)
    requesting_dr_contact = models.CharField(max_length=50, null=True, blank=True, help_text="Enter the requesting doctor's contact info")
    requesting_dr_speed_dial = models.CharField(max_length=20, null=True, blank=True, help_text="Enter the requesting doctor's speed dial")

    
    # ------------------------------
    # Utility method to get age from DOB
    # ------------------------------
    def get_calculated_age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                - (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth)
            )
        return self.age # fallback if DOB not given
    
    def __str__(self):
        return f"{self.patient_name} ({self.get_calculated_age()} yrs)"

    # ------------------------------
    # Section B: Reason for ICU Consult
    # ------------------------------
    reason = models.JSONField(default=list)  # store multiple ticked reasons as list
    reason_other = models.CharField(max_length=255, blank=True)

    # ------------------------------
    # Section C: Clinical Summary
    # ------------------------------
    clinical_summary = models.TextField(null=True, blank=True)

    # ------------------------------
    # Section D: Current Clinical Status
    # ------------------------------
    airway_patent = models.BooleanField(default=False)
    airway_threatened = models.BooleanField(default=False)
    intubated = models.CharField(
        max_length=3, 
        choices=YES_NO_CHOICES, 
        blank=True, 
        null=True, 
        verbose_name="intubated?"
        )

    breathing_spo2 = models.PositiveIntegerField(null=True, blank=True)
    breathing_distress = models.CharField(max_length=3, choices=[('yes','Yes'),('no','No')], blank=True, null=True)
    breathing_device = models.CharField(max_length=100, blank=True)

    bp_systolic = models.PositiveIntegerField(null=True, blank=True)
    bp_diastolic = models.PositiveIntegerField(null=True, blank=True)

    circulation_inotropes = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        blank=True,
        null=True,
        verbose_name="On inotropes?"
    )

    circulation_anti_hpt = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        blank=True,
        null=True,
        verbose_name="Antihypertensives?"
    )

    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    heart_rhythm = models.CharField(max_length=100, null=True, blank=True)

    FLUID_CHOICES = [
        ('fluid_type1', 'Fluid Type 1'),
        ('fluid_type2', 'Fluid Type 2'),
        ('fluid_type3', 'Fluid Type 3'),
    ]
    fluid_type = models.CharField(max_length=100, choices=FLUID_CHOICES, blank=True)
    fluid_urine_output = models.FloatField(null=True, blank=True)

    temperature = models.FloatField(null=True, blank=True)
    measures = models.CharField(max_length=255, blank=True)

    gcs = models.CharField(max_length=10, blank=True)

    sedation = models.CharField(max_length=3, choices=[('yes','Yes'), ('no','No')], blank=True, null=True)

    pupils = models.CharField(max_length=50, blank=True)

    # ------------------------------
    # Section E: Investigations
    # ------------------------------
    latest_abg = models.TextField(blank=True)
    key_labs = models.TextField(blank=True)
    imaging_findings = models.TextField(blank=True)
    time_tests_done = models.DateTimeField(null=True, blank=True)

    # ------------------------------
    # Section F: Current (Planned) Interventions
    # ------------------------------
    airway = models.CharField(max_length=100, blank=True)
    ventilation = models.CharField(max_length=100, blank=True)
    iv_fluids = models.CharField(max_length=100, blank=True)
    inotropes = models.CharField(max_length=100, blank=True)
    antibiotics = models.CharField(max_length=100, blank=True)
    other_interventions = models.CharField(max_length=255, blank=True)

    # ------------------------------
    # Section G: ICU Doctor's Assessment
    # ------------------------------
    DECISION_CHOICES = [
        ('admit', 'Admit to ICU'),
        ('not_for_icu', 'Not for ICU'),
        ('review_later', 'Review Later')
    ]

    assessment = models.TextField(blank=True)
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES, blank=True)
    plan_comments = models.TextField(blank=True)
    consultant_name = models.CharField(max_length=255, blank=True)
    signature = models.CharField(max_length=255, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    contact_no = models.CharField(max_length=20, blank=True)

    # ------------------------------
    # Submission Flag
    # ------------------------------
    submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient_name} - {self.request_datetime.strftime('%Y-%m-%d %H:%M')}"
