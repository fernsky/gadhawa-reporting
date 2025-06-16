"""
Environment models for Lungri Rural Municipality Digital Profile

This module contains models related to forests, water resources, biodiversity,
parks, and disaster risk management as specified in Chapter 6 of the report structure.
"""

import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """Abstract base model with common fields"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("सिर्जना मिति"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("अपडेट मिति"))

    class Meta:
        abstract = True


# Forest and Environment Enums
class ForestTypeChoice(models.TextChoices):
    """Forest types"""

    DECIDUOUS = "DECIDUOUS", _("पातलो वन")
    CONIFEROUS = "CONIFEROUS", _("कोणधारी वन")
    MIXED = "MIXED", _("मिश्रित वन")
    SHRUBLAND = "SHRUBLAND", _("झाडीखण्ड")
    GRASSLAND = "GRASSLAND", _("घाँसे मैदान")
    BAMBOO = "BAMBOO", _("बाँसको वन")


class ForestManagementChoice(models.TextChoices):
    """Forest management types"""

    GOVERNMENT = "GOVERNMENT", _("सरकारी व्यवस्थित")
    COMMUNITY = "COMMUNITY", _("सामुदायिक")
    COLLABORATIVE = "COLLABORATIVE", _("कबुलियती")
    RELIGIOUS = "RELIGIOUS", _("धार्मिक")
    PRIVATE = "PRIVATE", _("निजी")
    LEASEHOLD = "LEASEHOLD", _("पट्टा")


class WaterSourceTypeChoice(models.TextChoices):
    """Water source types"""

    SPRING = "SPRING", _("मुहान")
    RIVER = "RIVER", _("नदी")
    STREAM = "STREAM", _("खोला")
    LAKE = "LAKE", _("ताल")
    POND = "POND", _("पोखरी")
    WELL = "WELL", _("इनार")
    WETLAND = "WETLAND", _("सीमसार")


class DisasterTypeChoice(models.TextChoices):
    """Disaster types"""

    EARTHQUAKE = "EARTHQUAKE", _("भूकम्प")
    LANDSLIDE = "LANDSLIDE", _("पहिरो")
    FLOOD = "FLOOD", _("बाढी")
    FIRE = "FIRE", _("आगलागी")
    DROUGHT = "DROUGHT", _("खडेरी")
    HAILSTORM = "HAILSTORM", _("असिना")
    WIND_STORM = "WIND_STORM", _("आंधीबतास")
    LIGHTNING = "LIGHTNING", _("चट्याङ")


class BiodiversityTypeChoice(models.TextChoices):
    """Biodiversity types"""

    MAMMALS = "MAMMALS", _("स्तनधारी")
    BIRDS = "BIRDS", _("चराचुरुंगी")
    REPTILES = "REPTILES", _("सरीसृप")
    AMPHIBIANS = "AMPHIBIANS", _("उभयचर")
    FISH = "FISH", _("माछा")
    INSECTS = "INSECTS", _("कीराकीट")
    PLANTS = "PLANTS", _("वनस्पति")
    MEDICINAL_PLANTS = "MEDICINAL_PLANTS", _("जडिबुटी")


# Forest Models
class ForestArea(BaseModel):
    """Forest areas and types"""

    name = models.CharField(max_length=200, verbose_name=_("वनको नाम"))
    name_nepali = models.CharField(
        max_length=200, blank=True, verbose_name=_("वनको नाम (नेपाली)")
    )
    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    forest_type = models.CharField(
        max_length=20, choices=ForestTypeChoice.choices, verbose_name=_("वनको प्रकार")
    )
    management_type = models.CharField(
        max_length=20,
        choices=ForestManagementChoice.choices,
        verbose_name=_("व्यवस्थापन प्रकार"),
    )
    area_hectares = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("क्षेत्रफल (हेक्टेयर)")
    )
    canopy_cover_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("वृक्ष ढकावना प्रतिशत"),
    )
    is_protected = models.BooleanField(default=False, verbose_name=_("संरक्षित छ"))
    has_management_plan = models.BooleanField(
        default=False, verbose_name=_("व्यवस्थापन योजना छ")
    )
    last_survey_year = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("अन्तिम सर्वेक्षण वर्ष")
    )

    class Meta:
        verbose_name = _("वन क्षेत्र")
        verbose_name_plural = _("वन क्षेत्रहरू")

    def __str__(self):
        return f"{self.name} - वडा {self.ward_number}"


class ForestProduction(BaseModel):
    """Forest products and production"""

    forest_area = models.ForeignKey(
        ForestArea, on_delete=models.CASCADE, verbose_name=_("वन क्षेत्र")
    )
    product_type = models.CharField(
        max_length=30,
        choices=[
            ("TIMBER", _("काठ")),
            ("FUELWOOD", _("दाउरा")),
            ("BAMBOO", _("बाँस")),
            ("MEDICINAL_PLANTS", _("जडिबुटी")),
            ("NTFP", _("गैर काठ वन पैदावार")),
            ("FODDER", _("घाँसपात")),
            ("FRUITS", _("जंगली फलफूल")),
            ("HONEY", _("मह")),
        ],
        verbose_name=_("उत्पादनको प्रकार"),
    )
    annual_production_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("वार्षिक उत्पादन मात्रा"),
    )
    unit = models.CharField(max_length=20, default="KG", verbose_name=_("एकाइ"))
    market_value_npr = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("बजार मूल्य (रुपैयाँ)"),
    )
    harvesting_season = models.CharField(
        max_length=50, blank=True, verbose_name=_("संकलन मौसम")
    )

    class Meta:
        verbose_name = _("वन उत्पादन")
        verbose_name_plural = _("वन उत्पादन")
        unique_together = ["forest_area", "product_type"]

    def __str__(self):
        return f"{self.forest_area.name} - {self.get_product_type_display()}"


# Water Resources Models
class WaterResource(BaseModel):
    """Water sources and resources"""

    name = models.CharField(max_length=200, verbose_name=_("जलस्रोतको नाम"))
    name_nepali = models.CharField(
        max_length=200, blank=True, verbose_name=_("जलस्रोतको नाम (नेपाली)")
    )
    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    source_type = models.CharField(
        max_length=20,
        choices=WaterSourceTypeChoice.choices,
        verbose_name=_("स्रोतको प्रकार"),
    )
    is_perennial = models.BooleanField(default=True, verbose_name=_("वर्षभरि पानी छ"))
    flow_rate_lps = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("प्रवाह दर (लिटर प्रति सेकेन्ड)"),
    )
    water_quality = models.CharField(
        max_length=20,
        choices=[
            ("EXCELLENT", _("उत्कृष्ट")),
            ("GOOD", _("राम्रो")),
            ("FAIR", _("मध्यम")),
            ("POOR", _("खराब")),
            ("POLLUTED", _("दूषित")),
        ],
        default="GOOD",
        verbose_name=_("पानीको गुणस्तर"),
    )
    is_used_for_drinking = models.BooleanField(
        default=False, verbose_name=_("खानेपानीका लागि प्रयोग")
    )
    is_used_for_irrigation = models.BooleanField(
        default=False, verbose_name=_("सिंचाइका लागि प्रयोग")
    )
    households_served = models.PositiveIntegerField(
        default=0, verbose_name=_("सेवा पाउने घरपरिवार")
    )
    has_conservation_measures = models.BooleanField(
        default=False, verbose_name=_("संरक्षण उपायहरू छन्")
    )

    class Meta:
        verbose_name = _("जलस्रोत")
        verbose_name_plural = _("जलस्रोतहरू")

    def __str__(self):
        return f"{self.name} - वडा {self.ward_number}"


class WatershedArea(BaseModel):
    """Watershed and sub-watershed areas"""

    name = models.CharField(max_length=200, verbose_name=_("जलाधार क्षेत्रको नाम"))
    name_nepali = models.CharField(
        max_length=200, blank=True, verbose_name=_("जलाधार क्षेत्रको नाम (नेपाली)")
    )
    ward_numbers = models.CharField(max_length=50, verbose_name=_("वडा नं.हरू"))
    area_hectares = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("क्षेत्रफल (हेक्टेयर)")
    )
    is_main_watershed = models.BooleanField(
        default=False, verbose_name=_("मुख्य जलाधार हो")
    )
    forest_coverage_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("वन क्षेत्र प्रतिशत"),
    )
    degradation_level = models.CharField(
        max_length=20,
        choices=[
            ("LOW", _("कम")),
            ("MODERATE", _("मध्यम")),
            ("HIGH", _("उच्च")),
            ("SEVERE", _("गम्भीर")),
        ],
        default="LOW",
        verbose_name=_("क्षरण स्तर"),
    )
    has_conservation_activities = models.BooleanField(
        default=False, verbose_name=_("संरक्षण गतिविधिहरू छन्")
    )

    class Meta:
        verbose_name = _("जलाधार क्षेत्र")
        verbose_name_plural = _("जलाधार क्षेत्रहरू")

    def __str__(self):
        return f"{self.name}"


# Biodiversity Models
class BiodiversityRecord(BaseModel):
    """Biodiversity and wildlife records"""

    species_name = models.CharField(max_length=200, verbose_name=_("प्रजातिको नाम"))
    species_name_nepali = models.CharField(
        max_length=200, blank=True, verbose_name=_("प्रजातिको नाम (नेपाली)")
    )
    scientific_name = models.CharField(
        max_length=200, blank=True, verbose_name=_("वैज्ञानिक नाम")
    )
    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    biodiversity_type = models.CharField(
        max_length=20,
        choices=BiodiversityTypeChoice.choices,
        verbose_name=_("जैविक विविधताको प्रकार"),
    )
    population_estimate = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("जनसंख्या अनुमान")
    )
    conservation_status = models.CharField(
        max_length=30,
        choices=[
            ("ABUNDANT", _("प्रचुर")),
            ("COMMON", _("सामान्य")),
            ("RARE", _("दुर्लभ")),
            ("ENDANGERED", _("लोपोन्मुख")),
            ("CRITICALLY_ENDANGERED", _("अति लोपोन्मुख")),
            ("EXTINCT", _("लुप्त")),
        ],
        default="COMMON",
        verbose_name=_("संरक्षण स्थिति"),
    )
    habitat_description = models.TextField(blank=True, verbose_name=_("बासस्थान विवरण"))
    economic_importance = models.TextField(blank=True, verbose_name=_("आर्थिक महत्व"))
    threats = models.TextField(blank=True, verbose_name=_("खतराहरू"))
    is_endemic = models.BooleanField(default=False, verbose_name=_("स्थानीय प्रजाति हो"))

    class Meta:
        verbose_name = _("जैविक विविधता अभिलेख")
        verbose_name_plural = _("जैविक विविधता अभिलेखहरू")

    def __str__(self):
        return f"{self.species_name} - वडा {self.ward_number}"


class ProtectedArea(BaseModel):
    """Protected areas and conservation zones"""

    name = models.CharField(max_length=200, verbose_name=_("संरक्षित क्षेत्रको नाम"))
    name_nepali = models.CharField(
        max_length=200, blank=True, verbose_name=_("संरक्षित क्षेत्रको नाम (नेपाली)")
    )
    ward_numbers = models.CharField(max_length=50, verbose_name=_("वडा नं.हरू"))
    protection_type = models.CharField(
        max_length=30,
        choices=[
            ("NATIONAL_PARK", _("राष्ट्रिय निकुञ्ज")),
            ("WILDLIFE_RESERVE", _("वन्यजन्तु आरक्ष")),
            ("CONSERVATION_AREA", _("संरक्षण क्षेत्र")),
            ("BUFFER_ZONE", _("मध्यवर्ती क्षेत्र")),
            ("COMMUNITY_FOREST", _("सामुदायिक वन")),
            ("SACRED_GROVE", _("धार्मिक वन")),
            ("WETLAND", _("सीमसार क्षेत्र")),
        ],
        verbose_name=_("संरक्षणको प्रकार"),
    )
    area_hectares = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("क्षेत्रफल (हेक्टेयर)")
    )
    establishment_year = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("स्थापना वर्ष")
    )
    management_authority = models.CharField(
        max_length=200, blank=True, verbose_name=_("व्यवस्थापन निकाय")
    )
    conservation_objectives = models.TextField(
        blank=True, verbose_name=_("संरक्षण उद्देश्यहरू")
    )
    has_management_plan = models.BooleanField(
        default=False, verbose_name=_("व्यवस्थापन योजना छ")
    )

    class Meta:
        verbose_name = _("संरक्षित क्षेत्र")
        verbose_name_plural = _("संरक्षित क्षेत्रहरू")

    def __str__(self):
        return f"{self.name}"


# Parks and Gardens Models
class ParkGarden(BaseModel):
    """Parks and garden facilities"""

    name = models.CharField(max_length=200, verbose_name=_("पार्क/उद्यानको नाम"))
    name_nepali = models.CharField(
        max_length=200, blank=True, verbose_name=_("पार्क/उद्यानको नाम (नेपाली)")
    )
    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    park_type = models.CharField(
        max_length=20,
        choices=[
            ("PUBLIC_PARK", _("सार्वजनिक पार्क")),
            ("BOTANICAL_GARDEN", _("वनस्पति उद्यान")),
            ("CHILDREN_PARK", _("बाल पार्क")),
            ("COMMUNITY_GARDEN", _("सामुदायिक बगैंचा")),
            ("MEMORIAL_PARK", _("स्मारक पार्क")),
        ],
        verbose_name=_("पार्कको प्रकार"),
    )
    area_square_meters = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("क्षेत्रफल (वर्ग मिटर)")
    )
    establishment_year = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("स्थापना वर्ष")
    )
    has_playground = models.BooleanField(default=False, verbose_name=_("खेलमैदान छ"))
    has_walking_trail = models.BooleanField(default=False, verbose_name=_("पैदल बाटो छ"))
    has_seating_areas = models.BooleanField(default=False, verbose_name=_("बस्ने ठाउँ छ"))
    has_water_facility = models.BooleanField(
        default=False, verbose_name=_("पानीको सुविधा छ")
    )
    maintenance_status = models.CharField(
        max_length=20,
        choices=[
            ("EXCELLENT", _("उत्कृष्ट")),
            ("GOOD", _("राम्रो")),
            ("FAIR", _("मध्यम")),
            ("POOR", _("खराब")),
        ],
        default="GOOD",
        verbose_name=_("मर्मतको अवस्था"),
    )

    class Meta:
        verbose_name = _("पार्क तथा उद्यान")
        verbose_name_plural = _("पार्क तथा उद्यानहरू")

    def __str__(self):
        return f"{self.name} - वडा {self.ward_number}"


# Disaster Risk Management Models
class DisasterRiskArea(BaseModel):
    """Disaster risk and vulnerable areas"""

    area_name = models.CharField(max_length=200, verbose_name=_("क्षेत्रको नाम"))
    area_name_nepali = models.CharField(
        max_length=200, blank=True, verbose_name=_("क्षेत्रको नाम (नेपाली)")
    )
    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    disaster_type = models.CharField(
        max_length=20,
        choices=DisasterTypeChoice.choices,
        verbose_name=_("विपद्को प्रकार"),
    )
    risk_level = models.CharField(
        max_length=20,
        choices=[
            ("LOW", _("कम")),
            ("MODERATE", _("मध्यम")),
            ("HIGH", _("उच्च")),
            ("VERY_HIGH", _("अति उच्च")),
        ],
        verbose_name=_("जोखिम स्तर"),
    )
    vulnerable_households = models.PositiveIntegerField(
        default=0, verbose_name=_("जोखिममा रहेका घरपरिवार")
    )
    vulnerable_population = models.PositiveIntegerField(
        default=0, verbose_name=_("जोखिममा रहेको जनसंख्या")
    )
    seasonal_months = models.CharField(
        max_length=100, blank=True, verbose_name=_("जोखिमको मौसम")
    )
    mitigation_measures = models.TextField(blank=True, verbose_name=_("न्यूनीकरण उपायहरू"))
    early_warning_system = models.BooleanField(
        default=False, verbose_name=_("पूर्व चेतावनी प्रणाली छ")
    )

    class Meta:
        verbose_name = _("विपद् जोखिम क्षेत्र")
        verbose_name_plural = _("विपद् जोखिम क्षेत्रहरू")
        unique_together = ["area_name", "ward_number", "disaster_type"]

    def __str__(self):
        return f"{self.area_name} - {self.get_disaster_type_display()} - वडा {self.ward_number}"


class DisasterIncident(BaseModel):
    """Historical disaster incidents and damages"""

    incident_date = models.DateField(verbose_name=_("घटना मिति"))
    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    disaster_type = models.CharField(
        max_length=20,
        choices=DisasterTypeChoice.choices,
        verbose_name=_("विपद्को प्रकार"),
    )
    affected_households = models.PositiveIntegerField(
        default=0, verbose_name=_("प्रभावित घरपरिवार")
    )
    affected_population = models.PositiveIntegerField(
        default=0, verbose_name=_("प्रभावित जनसंख्या")
    )
    human_casualties = models.PositiveIntegerField(
        default=0, verbose_name=_("मानवीय हानि")
    )
    injured_count = models.PositiveIntegerField(default=0, verbose_name=_("घाइते संख्या"))
    houses_damaged = models.PositiveIntegerField(
        default=0, verbose_name=_("क्षतिग्रस्त घर")
    )
    economic_loss_npr = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("आर्थिक हानि (रुपैयाँ)"),
    )
    crops_damaged_hectares = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("बाली क्षति (हेक्टेयर)"),
    )
    livestock_lost = models.PositiveIntegerField(default=0, verbose_name=_("पशु हानि"))
    description = models.TextField(blank=True, verbose_name=_("घटना विवरण"))

    class Meta:
        verbose_name = _("विपद् घटना")
        verbose_name_plural = _("विपद् घटनाहरू")

    def __str__(self):
        return f"{self.get_disaster_type_display()} - {self.incident_date} - वडा {self.ward_number}"


class EmergencyResource(BaseModel):
    """Emergency resources and preparedness"""

    resource_name = models.CharField(max_length=200, verbose_name=_("स्रोतको नाम"))
    resource_name_nepali = models.CharField(
        max_length=200, blank=True, verbose_name=_("स्रोतको नाम (नेपाली)")
    )
    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    resource_type = models.CharField(
        max_length=30,
        choices=[
            ("AMBULANCE", _("एम्बुलेन्स")),
            ("FIRE_TRUCK", _("फायर ब्रिगेड")),
            ("RESCUE_VEHICLE", _("उद्धार गाडी")),
            ("EMERGENCY_SHELTER", _("आपतकालीन आश्रय")),
            ("RELIEF_STORE", _("राहत भण्डार")),
            ("COMMUNICATION_EQUIPMENT", _("सञ्चार उपकरण")),
            ("MEDICAL_SUPPLIES", _("चिकित्सा सामग्री")),
            ("WATER_TANKER", _("पानी ट्यांकर")),
            ("GENERATOR", _("जेनेरेटर")),
            ("RESCUE_EQUIPMENT", _("उद्धार उपकरण")),
        ],
        verbose_name=_("स्रोतको प्रकार"),
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("संख्या"))
    condition = models.CharField(
        max_length=20,
        choices=[
            ("EXCELLENT", _("उत्कृष्ट")),
            ("GOOD", _("राम्रो")),
            ("FAIR", _("मध्यम")),
            ("POOR", _("खराब")),
            ("OUT_OF_ORDER", _("बिग्रिएको")),
        ],
        default="GOOD",
        verbose_name=_("अवस्था"),
    )
    is_operational = models.BooleanField(default=True, verbose_name=_("सञ्चालनमा छ"))
    responsible_organization = models.CharField(
        max_length=200, blank=True, verbose_name=_("जिम्मेवार संस्था")
    )
    contact_person = models.CharField(
        max_length=100, blank=True, verbose_name=_("सम्पर्क व्यक्ति")
    )
    contact_number = models.CharField(
        max_length=20, blank=True, verbose_name=_("सम्पर्क नम्बर")
    )

    class Meta:
        verbose_name = _("आपतकालीन स्रोत")
        verbose_name_plural = _("आपतकालीन स्रोतहरू")

    def __str__(self):
        return f"{self.resource_name} - वडा {self.ward_number}"
