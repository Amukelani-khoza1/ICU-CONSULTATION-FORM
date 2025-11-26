from django.urls import path
from . import views
from .views import (
    SectionAView, SectionBView, SectionCView,
    SectionDView, SectionEView, SectionFView,
    SectionGView, ConsultSummaryView, 
)
from django.views.generic import RedirectView
app_name = 'consults'

urlpatterns = [
    path('', RedirectView.as_view(url='/section_a/', permanent=False)),  # redirect root of app to Section A
    path('section_a/', SectionAView.as_view(), name='section_a'),
    path('section_b/<int:pk>/', SectionBView.as_view(), name='section_b'),
    path('section_c/<int:pk>/', SectionCView.as_view(), name='section_c'),
    path('section_d/<int:pk>/', SectionDView.as_view(), name='section_d'),
    path('section_e/<int:pk>/', SectionEView.as_view(), name='section_e'),
    path('section_f/<int:pk>/', SectionFView.as_view(), name='section_f'),
    path('section_g/<int:pk>/', SectionGView.as_view(), name='section_g'),
    path('consult_summary/<int:pk>/', ConsultSummaryView.as_view(), name='consult_summary'),
    
    path('all_summaries/', views.all_summaries, name='all_summaries'),
    path('review_summary/<int:id>/', views.review_summary, name='review_summary')
]
