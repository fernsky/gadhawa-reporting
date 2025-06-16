"""
Municipality Introduction models for Lungri Rural Municipality Digital Profile

This module contains models for Chapter 2 (गाउँ÷नगरपालिकाको चिनारी) including:
- 2.1 भौगोलिक अवस्थिति (Geographical Situation)
- 2.2 ऐतिहासिक चिनारी तथा नामाकरण (Historical Identity and Naming)
- 2.3 राजनीतिक अवस्थिति (Political Situation)
- 2.4 धरातलीय अवस्था (Topographical Situation)
- 2.5 प्राकृतिक सम्पदा (Natural Resources)
- 2.6 साँस्कृतिक उत्कृष्टता (Cultural Excellence)
- 2.7 विकासका संभावनाहरु (Development Possibilities)
- 2.8 गार्हस्थ्य उत्पादन (Domestic Production)
- 2.9 मानव विकास सूचकाङ्क (Human Development Index)
"""

import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """Abstract base model with common fields"""

    id = models.CharField(
        max_length=36, primary_key=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# =============================================================================
# MUNICIPALITY INTRODUCTION MODELS (Chapter 2 - गाउँ÷नगरपालिकाको चिनारी)
# =============================================================================


class WardWiseDemographicSummary(BaseModel):
    """Ward-wise demographic summary"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    ward_name = models.TextField(null=True, blank=True, verbose_name=_("वडाको नाम"))

    # Population statistics
    total_population = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("कुल जनसंख्या")
    )
    population_male = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("पुरुष जनसंख्या")
    )
    population_female = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("महिला जनसंख्या")
    )
    population_other = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("अन्य जनसंख्या")
    )

    # Household data
    total_households = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("कुल घरपरिवार")
    )
    average_household_size = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("औसत घरपरिवार आकार"),
    )

    # Demographic ratios
    sex_ratio = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("लिङ्ग अनुपात"),
    )

    class Meta:
        verbose_name = _("वडागत जनसांख्यिकीय सारांश")
        verbose_name_plural = _("वडागत जनसांख्यिकीय सारांश")
        unique_together = ["ward_number"]

    def __str__(self):
        return f"वडा {self.ward_number} - जनसंख्या: {self.total_population}"
