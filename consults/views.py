from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from .forms import (
    SectionAForm, 
    SectionBForm, 
    SectionCForm,
    SectionDForm,
    SectionEForm, 
    SectionFForm, 
    SectionGForm
)
from . models import ICUConsultation

# ------------------------------
# Section A: Patient Details
# ------------------------------
class SectionAView(View):
    def get(self, request):
        form = SectionAForm()
        return render(request, 'consults/section_a.html', {'form': form})

    def post(self, request):
        form = SectionAForm(request.POST)
        if form.is_valid():
            # Save Section A data and create a new ICUConsultation
            consult = form.save()
            
            # Store consult ID in session (optional, helps track multi-step forms)
            request.session['consult_id'] = consult.id
            
            # Redirect to Section B using the new consult's ID
            return redirect('consults:section_b', pk=consult.id)
        
        # If form is invalid, render the same page with errors
        return render(request, 'consults/section_a.html', {'form': form})


# ------------------------------
# Section B: Reason for ICU Consult
# ------------------------------
class SectionBView(View):
    def get(self, request, pk):
        consult = get_object_or_404(ICUConsultation, pk=pk)
        form = SectionBForm(instance=consult)
        return render(request, 'consults/section_b.html', {'form': form, 'consult': consult})

    def post(self, request, pk):
        consult = get_object_or_404(ICUConsultation, pk=pk)
        form = SectionBForm(request.POST, instance=consult)
        if form.is_valid():
            form.save()
            return redirect('consults:section_c', pk=consult.pk)
        return render(request, 'consults/section_b.html', {'form': form, 'consult': consult})


# ------------------------------
# Section C: Clinical Summary
# ------------------------------
class SectionCView(View):
    def get(self, request, pk):
        consult = get_object_or_404(ICUConsultation, pk=pk)
        form = SectionCForm(instance=consult)
        return render(request, 'consults/section_c.html', {'form': form, 'consult': consult})

    def post(self, request, pk):
        consult = get_object_or_404(ICUConsultation, pk=pk)
        form = SectionCForm(request.POST, instance=consult)
        if form.is_valid():
            form.save()
            return redirect('consults:section_d', pk=consult.pk)  # go to next section
        return render(request, 'consults/section_c.html', {'form': form, 'consult': consult})


# ------------------------------
# Section D: Current Clinical Status
# ------------------------------
class SectionDView(View):
    def get(self, request, pk):
        consult = get_object_or_404(ICUConsultation, pk=pk)
        form = SectionDForm(instance=consult)
        return render(request, 'consults/section_d.html', {
            'form': form, 
            'consult': consult
        })

    def post(self, request, pk):
        consult = get_object_or_404(ICUConsultation, pk=pk)
        form = SectionDForm(request.POST, instance=consult)
        
        if form.is_valid():
            form.save()
            print(f"Section D saved successfully for consult {consult.pk}")
            return redirect('consults:section_e', pk=consult.pk)
        else:
            print("Section D form invalid:", form)
            
        return render(request, 'consults/section_d.html', {
            'form': form, 
            'consult': consult
        })


# ------------------------------
# Section E: Investigations
# ------------------------------
class SectionEView(View):
    def get(self, request, pk):
        consult = get_object_or_404(ICUConsultation, pk=pk)
        form = SectionEForm(instance=consult)
        return render(request, 'consults/section_e.html', {'form': form, 'consult': consult})

    def post(self, request, pk):
        consult = get_object_or_404(ICUConsultation, pk=pk)
        form = SectionEForm(request.POST, instance=consult)
        if form.is_valid():
            form.save()
            return redirect('consults:section_f', pk=consult.pk)
        return render(request, 'consults/section_e.html', {'form': form, 'consult': consult})


# ------------------------------
# Section F: Planned Interventions
# ------------------------------
class SectionFView(View):
    def get(self, request, pk):
        consult = get_object_or_404(ICUConsultation, pk=pk)
        form = SectionFForm(instance=consult)
        return render(request, 'consults/section_f.html', {'form': form, 'consult': consult})

    def post(self, request, pk):
        consult = get_object_or_404(ICUConsultation, pk=pk)
        form = SectionFForm(request.POST, instance=consult)
        if form.is_valid():
            form.save()
            return redirect('consults:section_g', pk=consult.pk)
        return render(request, 'consults/section_f.html', {'form': form, 'consult': consult})


# ------------------------------
# Section G: ICU Doctor's Assessment
# ------------------------------
class SectionGView(View):
    def get(self, request, pk):
        consult = get_object_or_404(ICUConsultation, pk=pk)
        form = SectionGForm(instance=consult)
        return render(request, 'consults/section_g.html', {'form': form, 'consult': consult})

    def post(self, request, pk):
        consult = get_object_or_404(ICUConsultation, pk=pk)
        form = SectionGForm(request.POST, instance=consult)
        if form.is_valid():
            form.save()
            # Redirect to summary page for review before final submission
            return redirect('consults:consult_summary', pk=consult.pk)
        return render(request, 'consults/section_g.html', {'form': form, 'consult': consult})


# ------------------------------
# Summary Page
# ------------------------------
class ConsultSummaryView(View):
    def get(self, request, pk):
        consult = get_object_or_404(ICUConsultation, pk=pk)
        return render(request, 'consults/consult_summary.html', {'consult': consult})

    def post(self, request, pk):
        consult = get_object_or_404(ICUConsultation, pk=pk)
        # Mark as submitted
        consult.submitted = True
        consult.save()
        return render(request, 'consults/consult_complete.html', {'consult': consult})


# ------------------------------
# View All Submitted Summaries (Public)
# ------------------------------
def all_summaries(request):
    consultations = ICUConsultation.objects.filter(submitted=True).order_by('-id')
    return render(request, 'consults/all_summaries.html', {'summaries': consultations})


# ------------------------------
# Review Single Summary
# ------------------------------
def review_summary(request, id):
    consult =get_object_or_404(ICUConsultation, pk=id)
    return render(request, 'consults/review_summary.html', {'consult': consult})