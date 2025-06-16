from django.urls import path
from .views.religion import (
    ReligionDemographicsView, 
    ReligionDataAPIView, 
    ReligionReportPartialView
)

app_name = 'demographics'
urlpatterns = [
    # Religion demographics URLs
    path('religion/', ReligionDemographicsView.as_view(), name='religion_analysis'),
    path('religion/data/', ReligionDataAPIView.as_view(), name='religion_data_api'),
    path('religion/report-partial/', ReligionReportPartialView.as_view(), name='religion_report_partial'),
]
