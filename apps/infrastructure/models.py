"""
Infrastructure models for Gadhawa Rural Municipality Digital Profile

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
    UNDER_15_MIN = "UNDER_15_MIN", _("१५ मिनेट भन्दा कम")
    UNDER_30_MIN = "UNDER_30_MIN", _("१५-३० मिनेट")
    UNDER_1_HOUR = "UNDER_1_HOUR", _("३०-६० मिनेट")
    ONE_HOUR_OR_MORE = "1_HOUR_OR_MORE", _("१ घण्टा वा बढी")


# House Map Passed Enums
class HouseMapStatusChoice(models.TextChoices):
    PASSED = "PASSED", _("पास भएको")
    NOT_PASSED = "NOT_PASSED", _("पास नभएको")
    IN_PROCESS = "IN_PROCESS", _("प्रक्रियामा")
    NOT_APPLICABLE = "NOT_APPLICABLE", _("लागू नहुने")


# =============================================================================
# PHYSICAL INFRASTRUCTURE MODELS (Chapter 7 - भौतिक विकासको अवस्था)
# =============================================================================

# ७.१ यातायात पूर्वाधार
# ७.१.१ सडक संजालको विद्यमान अवस्था


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


# ७.१.२ निर्माणाधीन गाउँ वा नगरस्तरीय सडकहरु
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


# ७.१.३ सवारी सुबिधा र रुट
# ७.१.४ गाउँ/नगर क्षेत्रभित्र चल्ने सवारी साधन


# ७.१.५ झोलुंगे पुल तथा पुलपुलेसा
class BridgeInfo(BaseModel):
    """Information about bridges (7.1.5)"""

    name = models.CharField(max_length=100, verbose_name=_("पुलको नाम"))
    ward_number = models.CharField(max_length=30, verbose_name=_("वडा नं"))
    address = models.CharField(
        max_length=150, verbose_name=_("ठेगाना"), blank=True, null=True
    )

    class Meta:
        verbose_name = _("झोलुंगे पुल तथा पुलपुलेसा")
        verbose_name_plural = _("झोलुंगे पुल तथा पुलपुलेसाहरू")

    def __str__(self):
        return f"{self.name} - {self.ward_number}"


# ७.१.६ टाढाको बस्तीबाट सम्बन्धित गाउँ/नगरपालिकाको केन्द्र पुग्न लाग्ने अनुमानित समय


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


# ७.१.७ वसपार्क तथा वस विसौनी सम्बन्धी विवरण


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


# ७.१.८ स्रोत नक्शा
# ७.२ विद्युत तथा बैकल्पिक उर्जा
# ७.२.१ इन्धन उपयोग विवरण (खाना पकाउने इन्धनको आधारमा घरपरिवार)
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


# ७.२.२ बत्ति बाल्ने इन्धनको प्रयोगको आधारमा घरपरिवार


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


# ७.२.३ जलविद्युत, सौर्य उर्जा, वायु उर्जाबाट विद्युत उत्पादन विवरण
# ७.२.४ विद्युत उपलब्ध घरपरिवार विवरण
# ७.२.५ वैकल्पिक उर्जा (लघु जल विद्युत, सोलार, वायोग्यास, सुधारिएको चुल्हो) प्रयोग गर्ने परिवार
# ७.२.६ स्रोत नक्शा
# ७.३ सञ्चार तथा प्रविधि
# ७.३.१ हुलाक तथा पत्रपत्रिका सम्बन्धी विवरण
# ७.३.२ दूरसंचार सम्बन्धी विवरण
# ७.३.३ रेडियो स्टेसन सम्बन्धी विवरण
# ७.३.४ आधुनिक सुबिधामा पहुँच सम्बन्धी विवरण
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


# ७.३.५ स्रोतनक्शाहरु
# ७.४ आवास तथा भवन


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


# ७.४.१ विद्यमान सतह ढलको अवस्था
# ७.४.२ छानोको प्रकारका आधारमा घरधुरी


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


# ७.४.३ गाउँ/नगरपालिका अन्तर्गतका सरकारी भवन सम्बन्धी विवरण
# ७.४.४ गाउँ/नगरपालिका कार्यालयदेखि प्रत्येक वडा केन्द्रसम्मको दूरी
# ७.४.५ पशुवधशालाको विवरण
# ७.४.६ शव दाहस्थल सम्बन्धी विवरण
# ७.४.८ स्रोत नक्शा
