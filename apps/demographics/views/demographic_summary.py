"""
Demographic Summary Views

Views for handling demographic summary (population distribution) related requests.
"""

from django.shortcuts import render
from django.http import JsonResponse
from apps.demographics.processors.demographic_summary import DemographicSummaryProcessor


def demographic_summary_report(request):
    """Generate demographic summary report for PDF"""
    processor = DemographicSummaryProcessor()
    data = processor.get_data()

    if not data:
        return JsonResponse(
            {"error": "No demographic summary data available"}, status=404
        )

    content = processor.generate_report_content(data)

    context = {
        "content": content,
        "section_title": processor.get_section_title(),
        "section_number": processor.get_section_number(),
    }

    return render(
        request,
        "demographics/demographic_summary/demographic_summary_report_partial.html",
        context,
    )


def demographic_summary_data(request):
    """API endpoint for demographic summary data"""
    processor = DemographicSummaryProcessor()
    data = processor.get_data()

    if not data:
        return JsonResponse(
            {"error": "No demographic summary data available"}, status=404
        )

    # Convert model instance to dictionary for JSON response
    data_dict = {
        "total_population": data.total_population,
        "population_male": data.population_male,
        "population_female": data.population_female,
        "population_other": data.population_other,
        "sex_ratio": float(data.sex_ratio) if data.sex_ratio else None,
        "total_households": data.total_households,
        "average_household_size": (
            float(data.average_household_size) if data.average_household_size else None
        ),
        "population_density": (
            float(data.population_density) if data.population_density else None
        ),
        "population_0_to_14": data.population_0_to_14,
        "population_15_to_59": data.population_15_to_59,
        "population_60_and_above": data.population_60_and_above,
        "growth_rate": float(data.growth_rate) if data.growth_rate else None,
        "literacy_rate_above_15": (
            float(data.literacy_rate_above_15) if data.literacy_rate_above_15 else None
        ),
        "literacy_rate_15_to_24": (
            float(data.literacy_rate_15_to_24) if data.literacy_rate_15_to_24 else None
        ),
    }

    return JsonResponse(data_dict)
