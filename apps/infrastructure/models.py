"""
Infrastructure models for Lungri Rural Municipality Digital Profile

This module contains models for Chapter 7 (भौतिक विकासको अवस्था) including:
- 7.1 यातायात पूर्वाधार (Transportation Infrastructure)
- 7.2 विद्युत तथा बैकल्पिक उर्जा (Electricity and Alternative Energy)
- 7.3 सञ्चार तथा प्रविधि (Communication and Technology)
- 7.4 आवास तथा भवन (Housing and Buildings)
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
# PHYSICAL INFRASTRUCTURE ENUMS (from TypeScript schemas)
# =============================================================================


# Common enums
class GenderChoice(models.TextChoices):
    MALE = "MALE", _("पुरुष")
    FEMALE = "FEMALE", _("महिला")
    OTHER = "OTHER", _("अन्य")


# Cooking Fuel Enums (from ward-wise-cooking-fuel.schema.ts)
class CookingFuelChoice(models.TextChoices):
    WOOD = "WOOD", _("काठ/दाउरा/कोइला")
    LP_GAS = "LP_GAS", _("एल.पी. ग्याँस")
    KEROSENE = "KEROSENE", _("मट्टितेल")
    ELECTRICITY = "ELECTRICITY", _("विद्युत")
    BIOGAS = "BIOGAS", _("गोबर ग्याँस/बायोग्याँस")
    DUNGCAKE = "DUNGCAKE", _("गोबर/गुँइठा")
    OTHER = "OTHER", _("अन्य")


# Electricity Source Enums (from ward-wise-electricity-source.schema.ts)
class ElectricitySourceChoice(models.TextChoices):
    ELECTRICITY = "ELECTRICITY", _("विद्युत")
    SOLAR = "SOLAR", _("सोलार")
    KEROSENE = "KEROSENE", _("मट्टितेल")
    BIOGAS = "BIOGAS", _("बायोग्याँस")
    OTHER = "OTHER", _("अन्य")


# Household Floor Enums (from ward-wise-household-floor.schema.ts)
class FloorTypeChoice(models.TextChoices):
    CONCRETE = "CONCRETE", _("सिमेन्ट ढलान")
    MUD = "MUD", _("माटो")
    WOOD = "WOOD", _("काठको फल्याक/बाँस")
    BRICK = "BRICK", _("इँटा/ढुङ्गा")
    TILE = "TILE", _("सेरामिक टायल")
    OTHER = "OTHER", _("अन्य")


# Household Roof Enums (from ward-wise-household-roof.schema.ts)
class RoofTypeChoice(models.TextChoices):
    CEMENT = "CEMENT", _("सिमेन्ट ढलान")
    TIN = "TIN", _("जस्ता/टिन")
    TILE = "TILE", _("टायल/खपडा/झिँगटी")
    STRAW = "STRAW", _("खर/पराल/छ्वाली")
    WOOD = "WOOD", _("काठ/फल्याक")
    STONE = "STONE", _("ढुङ्गा/स्लेट")
    OTHER = "OTHER", _("अन्य")


# Facilities Enums (from ward-wise-facilities.schema.ts)
class FacilityChoice(models.TextChoices):
    RADIO = "RADIO", _("रेडियो सुविधा")
    TELEVISION = "TELEVISION", _("टेलिभिजन")
    COMPUTER = "COMPUTER", _("कम्प्युटर/ल्यापटप")
    TELEPHONE = "TELEPHONE", _("टेलिफोन")
    MOBILE_PHONE = "MOBILE_PHONE", _("मोबाइल फोन")
    INTERNET = "INTERNET", _("इन्टरनेट")
    BICYCLE = "BICYCLE", _("साइकल")
    MOTORCYCLE = "MOTORCYCLE", _("मोटरसाइकल")
    CAR_JEEP_VAN = "CAR_JEEP_VAN", _("कार/जीप/भ्यान")
    TRACTOR = "TRACTOR", _("ट्याक्टर")
    OTHER = "OTHER", _("अन्य")


# Road Status Enums
class RoadStatusChoice(models.TextChoices):
    BLACKTOPPED = "BLACKTOPPED", _("कालोपत्रे")
    GRAVELED = "GRAVELED", _("ढुंगामाटो")
    EARTHEN = "EARTHEN", _("कच्ची")
    NO_ROAD = "NO_ROAD", _("सडक छैन")


# Time Duration Enums
class TimeDurationChoice(models.TextChoices):
    LESS_THAN_30_MIN = "LESS_THAN_30_MIN", _("३० मिनेट भन्दा कम")
    BETWEEN_30_60_MIN = "BETWEEN_30_60_MIN", _("३०-६० मिनेट")
    BETWEEN_1_2_HOURS = "BETWEEN_1_2_HOURS", _("१-२ घण्टा")
    BETWEEN_2_4_HOURS = "BETWEEN_2_4_HOURS", _("२-४ घण्टा")
    MORE_THAN_4_HOURS = "MORE_THAN_4_HOURS", _("४ घण्टा भन्दा बढी")


# House Map Passed Enums
class HouseMapStatusChoice(models.TextChoices):
    PASSED = "PASSED", _("पास भएको")
    NOT_PASSED = "NOT_PASSED", _("पास नभएको")
    IN_PROCESS = "IN_PROCESS", _("प्रक्रियामा")
    NOT_APPLICABLE = "NOT_APPLICABLE", _("लागू नहुने")


# =============================================================================
# PHYSICAL INFRASTRUCTURE MODELS (Chapter 7 - भौतिक विकासको अवस्था)
# =============================================================================


# 7.2 विद्युत तथा बैकल्पिक उर्जा (Electricity and Alternative Energy)
class WardWiseCookingFuel(BaseModel):
    """Ward wise cooking fuel usage (7.2.1 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    cooking_fuel = models.CharField(
        max_length=15,
        choices=CookingFuelChoice.choices,
        verbose_name=_("खाना पकाउने इन्धन"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत खाना पकाउने इन्धन")
        verbose_name_plural = _("वडागत खाना पकाउने इन्धन")
        unique_together = ["ward_number", "cooking_fuel"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_cooking_fuel_display()}"


class WardWiseElectricitySource(BaseModel):
    """Ward wise electricity source (7.2.2 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    electricity_source = models.CharField(
        max_length=15,
        choices=ElectricitySourceChoice.choices,
        verbose_name=_("बत्ति बाल्ने इन्धन"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत बत्ति बाल्ने इन्धन")
        verbose_name_plural = _("वडागत बत्ति बाल्ने इन्धन")
        unique_together = ["ward_number", "electricity_source"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_electricity_source_display()}"


# 7.3 सञ्चार तथा प्रविधि (Communication and Technology)
class WardWiseFacilities(BaseModel):
    """Ward wise facilities (7.3.4 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    facility = models.CharField(
        max_length=20,
        choices=FacilityChoice.choices,
        verbose_name=_("सुविधा"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत सुविधा")
        verbose_name_plural = _("वडागत सुविधाहरू")
        unique_together = ["ward_number", "facility"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_facility_display()}"


# 7.4 आवास तथा भवन (Housing and Buildings)
class WardWiseHouseholdFloor(BaseModel):
    """Ward wise household floor type (7.4.1 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    floor_type = models.CharField(
        max_length=15,
        choices=FloorTypeChoice.choices,
        verbose_name=_("भुइँको प्रकार"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत घरको भुइँको प्रकार")
        verbose_name_plural = _("वडागत घरको भुइँको प्रकार")
        unique_together = ["ward_number", "floor_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_floor_type_display()}"


class WardWiseHouseholdRoof(BaseModel):
    """Ward wise household roof type (7.4.2 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    roof_type = models.CharField(
        max_length=15,
        choices=RoofTypeChoice.choices,
        verbose_name=_("छानोको प्रकार"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत छानोको प्रकार")
        verbose_name_plural = _("वडागत छानोको प्रकार")
        unique_together = ["ward_number", "roof_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_roof_type_display()}"


class WardWiseHouseMapPassed(BaseModel):
    """Ward wise house map passed status (7.4.3 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    house_map_status = models.CharField(
        max_length=20,
        choices=HouseMapStatusChoice.choices,
        verbose_name=_("घरको नक्शा पास स्थिति"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत घरको नक्शा पास स्थिति")
        verbose_name_plural = _("वडागत घरको नक्शा पास स्थिति")
        unique_together = ["ward_number", "house_map_status"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_house_map_status_display()}"


# 7.1 यातायात पूर्वाधार (Transportation Infrastructure)
class WardWiseRoadStatus(BaseModel):
    """Ward wise road status (7.1.1 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    road_status = models.CharField(
        max_length=15,
        choices=RoadStatusChoice.choices,
        verbose_name=_("सडकको अवस्था"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत सडकको अवस्था")
        verbose_name_plural = _("वडागत सडकको अवस्था")
        unique_together = ["ward_number", "road_status"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_road_status_display()}"


class WardWiseTimeToActiveRoad(BaseModel):
    """Ward wise time to active road (7.1.6 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    time_duration = models.CharField(
        max_length=25,
        choices=TimeDurationChoice.choices,
        verbose_name=_("सक्रिय सडकमा पुग्न लाग्ने समय"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत सक्रिय सडकमा पुग्न लाग्ने समय")
        verbose_name_plural = _("वडागत सक्रिय सडकमा पुग्न लाग्ने समय")
        unique_together = ["ward_number", "time_duration"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_time_duration_display()}"


class WardWiseTimeToMarketCenter(BaseModel):
    """Ward wise time to market center (7.1.6 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    time_duration = models.CharField(
        max_length=25,
        choices=TimeDurationChoice.choices,
        verbose_name=_("बजार केन्द्रमा पुग्न लाग्ने समय"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत बजार केन्द्रमा पुग्न लाग्ने समय")
        verbose_name_plural = _("वडागत बजार केन्द्रमा पुग्न लाग्ने समय")
        unique_together = ["ward_number", "time_duration"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_time_duration_display()}"


class WardWiseTimeToPublicTransport(BaseModel):
    """Ward wise time to public transport (7.1.6 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    time_duration = models.CharField(
        max_length=25,
        choices=TimeDurationChoice.choices,
        verbose_name=_("सार्वजनिक यातायातमा पुग्न लाग्ने समय"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत सार्वजनिक यातायातमा पुग्न लाग्ने समय")
        verbose_name_plural = _("वडागत सार्वजनिक यातायातमा पुग्न लाग्ने समय")
        unique_together = ["ward_number", "time_duration"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_time_duration_display()}"
