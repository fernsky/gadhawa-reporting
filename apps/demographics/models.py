"""
Demographics models for Lungri Rural Municipality Digital Profile

This module contains models related to population, households, and demographic information
as specified in the SQL schema files and report structure.
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


# Enums for Demographics based on attached schema files
class GenderChoice(models.TextChoices):
    MALE = "MALE", _("पुरुष")
    FEMALE = "FEMALE", _("महिला")
    OTHER = "OTHER", _("अन्य")


class AgeGroupChoice(models.TextChoices):
    AGE_0_4 = "AGE_0_4", _("०-४ वर्ष")
    AGE_5_9 = "AGE_5_9", _("५-९ वर्ष")
    AGE_10_14 = "AGE_10_14", _("१०-१४ वर्ष")
    AGE_15_19 = "AGE_15_19", _("१५-१९ वर्ष")
    AGE_20_24 = "AGE_20_24", _("२०-२४ वर्ष")
    AGE_25_29 = "AGE_25_29", _("२५-२९ वर्ष")
    AGE_30_34 = "AGE_30_34", _("३०-३४ वर्ष")
    AGE_35_39 = "AGE_35_39", _("३५-३९ वर्ष")
    AGE_40_44 = "AGE_40_44", _("४०-४४ वर्ष")
    AGE_45_49 = "AGE_45_49", _("४५-४९ वर्ष")
    AGE_50_54 = "AGE_50_54", _("५०-५४ वर्ष")
    AGE_55_59 = "AGE_55_59", _("५५-५९ वर्ष")
    AGE_60_64 = "AGE_60_64", _("६०-६४ वर्ष")
    AGE_65_69 = "AGE_65_69", _("६५-६९ वर्ष")
    AGE_70_74 = "AGE_70_74", _("७०-७४ वर्ष")
    AGE_75_AND_ABOVE = "AGE_75_AND_ABOVE", _("७५ वर्षभन्दा माथि")


class AbsenteeAgeGroupChoice(models.TextChoices):
    AGE_0_4 = "AGE_0_4", _("०-४ वर्ष")
    AGE_5_9 = "AGE_5_9", _("५-९ वर्ष")
    AGE_10_14 = "AGE_10_14", _("१०-१४ वर्ष")
    AGE_15_19 = "AGE_15_19", _("१५-१९ वर्ष")
    AGE_20_24 = "AGE_20_24", _("२०-२४ वर्ष")
    AGE_25_29 = "AGE_25_29", _("२५-२९ वर्ष")
    AGE_30_34 = "AGE_30_34", _("३०-३४ वर्ष")
    AGE_35_39 = "AGE_35_39", _("३५-३९ वर्ष")
    AGE_40_44 = "AGE_40_44", _("४०-४४ वर्ष")
    AGE_45_49 = "AGE_45_49", _("४५-४९ वर्ष")
    AGE_50_AND_ABOVE = "AGE_50_AND_ABOVE", _("५० वर्षभन्दा माथि")


class MarriedAgeGroupChoice(models.TextChoices):
    AGE_BELOW_15 = "AGE_BELOW_15", _("१५ वर्षभन्दा कम")
    AGE_15_19 = "AGE_15_19", _("१५-१९ वर्ष")
    AGE_20_24 = "AGE_20_24", _("२०-२४ वर्ष")
    AGE_25_29 = "AGE_25_29", _("२५-२९ वर्ष")
    AGE_30_34 = "AGE_30_34", _("३०-३४ वर्ष")
    AGE_35_39 = "AGE_35_39", _("३५-३९ वर्ष")
    AGE_40_AND_ABOVE = "AGE_40_AND_ABOVE", _("४० वर्षभन्दा माथि")


class MaritalStatusChoice(models.TextChoices):
    SINGLE = "SINGLE", _("अविवाहित")
    MARRIED = "MARRIED", _("विवाहित")
    DIVORCED = "DIVORCED", _("सम्बन्धविच्छेद")
    WIDOWED = "WIDOWED", _("विधवा/विधुर")
    SEPARATED = "SEPARATED", _("छुट्टिएको")
    NOT_STATED = "NOT_STATED", _("उल्लेख नगरिएको")


class CasteTypeChoice(models.TextChoices):
    BRAHMIN = "BRAHMIN", _("ब्राह्मण")
    CHHETRI = "CHHETRI", _("क्षेत्री")
    MAGAR = "MAGAR", _("मगर")
    TAMANG = "TAMANG", _("तामाङ")
    NEWAR = "NEWAR", _("नेवार")
    THARU = "THARU", _("थारु")
    GURUNG = "GURUNG", _("गुरुङ")
    RAI = "RAI", _("राई")
    LIMBU = "LIMBU", _("लिम्बु")
    SHERPA = "SHERPA", _("शेर्पा")
    DALIT = "DALIT", _("दलित")
    MADHESI = "MADHESI", _("मधेसी")
    MUSLIM = "MUSLIM", _("मुस्लिम")
    OTHER = "OTHER", _("अन्य")


class LanguageTypeChoice(models.TextChoices):
    NEPALI = "NEPALI", _("नेपाली")
    LIMBU = "LIMBU", _("लिम्बु")
    RAI = "RAI", _("राई")
    HINDI = "HINDI", _("हिन्दी")
    NEWARI = "NEWARI", _("नेवारी")
    SHERPA = "SHERPA", _("शेर्पा")
    TAMANG = "TAMANG", _("तामाङ")
    MAITHILI = "MAITHILI", _("मैथिली")
    BHOJPURI = "BHOJPURI", _("भोजपुरी")
    THARU = "THARU", _("थारु")
    BAJJIKA = "BAJJIKA", _("बज्जिका")
    MAGAR = "MAGAR", _("मगर")
    DOTELI = "DOTELI", _("डोटेली")
    URDU = "URDU", _("उर्दू")
    AWADI = "AWADI", _("अवधी")
    GURUNG = "GURUNG", _("गुरुङ")
    ENGLISH = "ENGLISH", _("अंग्रेजी")
    OTHER = "OTHER", _("अन्य")


class ReligionTypeChoice(models.TextChoices):
    HINDU = "HINDU", _("हिन्दू")
    BUDDHIST = "BUDDHIST", _("बौद्ध")
    KIRANT = "KIRANT", _("किरात")
    CHRISTIAN = "CHRISTIAN", _("क्रिश्चियन")
    ISLAM = "ISLAM", _("इस्लाम")
    NATURE = "NATURE", _("प्रकृति")
    BON = "BON", _("बोन")
    JAIN = "JAIN", _("जैन")
    BAHAI = "BAHAI", _("बहाई")
    SIKH = "SIKH", _("सिख")
    OTHER = "OTHER", _("अन्य")


class DisabilityCauseChoice(models.TextChoices):
    CONGENITAL = "CONGENITAL", _("जन्मजात")
    ACCIDENT = "ACCIDENT", _("दुर्घटना")
    MALNUTRITION = "MALNUTRITION", _("कुपोषण")
    DISEASE = "DISEASE", _("रोगको कारण")
    CONFLICT = "CONFLICT", _("द्वन्द्वको कारण")
    OTHER = "OTHER", _("अन्य")


class BirthPlaceChoice(models.TextChoices):
    SAME_MUNICIPALITY = "SAME_MUNICIPALITY", _("यहि गापा/नपा")
    SAME_DISTRICT_ANOTHER_MUNICIPALITY = "SAME_DISTRICT_ANOTHER_MUNICIPALITY", _(
        "यहि जिल्लाको अर्को गा.पा./न.पा"
    )
    ANOTHER_DISTRICT = "ANOTHER_DISTRICT", _("अर्को जिल्ला")
    ABROAD = "ABROAD", _("विदेश")


class MigratedFromChoice(models.TextChoices):
    ANOTHER_DISTRICT = "ANOTHER_DISTRICT", _("नेपालको अर्को जिल्ला")
    SAME_DISTRICT_ANOTHER_MUNICIPALITY = "SAME_DISTRICT_ANOTHER_MUNICIPALITY", _(
        "यही जिल्लाको अर्को स्थानीय तह"
    )
    ABROAD = "ABROAD", _("विदेश")


class EducationalLevelChoice(models.TextChoices):
    CHILD_DEVELOPMENT_CENTER = "CHILD_DEVELOPMENT_CENTER", _("बाल विकास केन्द्र")
    NURSERY = "NURSERY", _("नर्सरी")
    CLASS_1 = "CLASS_1", _("कक्षा १")
    CLASS_2 = "CLASS_2", _("कक्षा २")
    CLASS_3 = "CLASS_3", _("कक्षा ३")
    CLASS_4 = "CLASS_4", _("कक्षा ४")
    CLASS_5 = "CLASS_5", _("कक्षा ५")
    CLASS_6 = "CLASS_6", _("कक्षा ६")
    CLASS_7 = "CLASS_7", _("कक्षा ७")
    CLASS_8 = "CLASS_8", _("कक्षा ८")
    CLASS_9 = "CLASS_9", _("कक्षा ९")
    CLASS_10 = "CLASS_10", _("कक्षा १०")
    SLC_LEVEL = "SLC_LEVEL", _("एसएलसी तह")
    CLASS_12_LEVEL = "CLASS_12_LEVEL", _("कक्षा १२ तह")
    BACHELOR_LEVEL = "BACHELOR_LEVEL", _("स्नातक तह")
    MASTERS_LEVEL = "MASTERS_LEVEL", _("स्नातकोत्तर तह")
    PHD_LEVEL = "PHD_LEVEL", _("पी.एच.डी. तह")
    OTHER = "OTHER", _("अन्य")
    INFORMAL_EDUCATION = "INFORMAL_EDUCATION", _("अनौपचारिक शिक्षा")
    EDUCATED = "EDUCATED", _("शिक्षित")
    UNKNOWN = "UNKNOWN", _("अज्ञात")


# Core Demographics Models based on attached schemas
# ३.१ बस्ती र घरपरिवार विवरण


# ३.१.१ मुख्य बस्ती
class WardSettlement(BaseModel):
    """Ward-wise settlement information"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    settlement_areas = models.JSONField(
        default=list, blank=True, verbose_name=_("मुख्य बस्तीहरु")
    )

    class Meta:
        verbose_name = _("वडागत बस्ती विवरण")
        verbose_name_plural = _("वडागत बस्ती विवरण")
        unique_together = ["ward_number"]

    def __str__(self):
        return f"वडा {self.ward_number} बस्ती विवरण"


# ३.१.२ घरपरिवारको विवरण
class WardTimeSeriesPopulation(BaseModel):
    """Ward time series population data"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    ward_name = models.TextField(null=True, blank=True, verbose_name=_("वडाको नाम"))

    # Census year (e.g., 2068, 2078)
    year = models.PositiveIntegerField(verbose_name=_("वर्ष"))

    # Population statistics
    total_population = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("कुल जनसंख्या")
    )
    male_population = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("पुरुष जनसंख्या")
    )
    female_population = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("महिला जनसंख्या")
    )
    other_population = models.PositiveIntegerField(
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

    # Age demographics
    population_0_to_14 = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("०-१४ वर्ष जनसंख्या")
    )
    population_15_to_59 = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("१५-५९ वर्ष जनसंख्या")
    )
    population_60_and_above = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("६० वर्षभन्दा माथि जनसंख्या")
    )

    # Literacy data
    literacy_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("साक्षरता दर"),
    )
    male_literacy_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("पुरुष साक्षरता दर"),
    )
    female_literacy_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("महिला साक्षरता दर"),
    )

    # Growth rate
    growth_rate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("वृद्धि दर")
    )

    # Geographic data
    area_sq_km = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("क्षेत्रफल (वर्ग कि.मी.)"),
    )
    population_density = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("जनसंख्या घनत्व"),
    )

    # Sex ratio
    sex_ratio = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("लिङ्ग अनुपात"),
    )

    class Meta:
        verbose_name = _("वडागत समयश्रृंखला जनसंख्या")
        verbose_name_plural = _("वडागत समयश्रृंखला जनसंख्या")
        unique_together = ["ward_number", "year"]

    def __str__(self):
        return f"वडा {self.ward_number} - वर्ष {self.year}"


# ३.२ जनसंख्या वितरणको अवस्था
class DemographicSummary(BaseModel):
    """Demographic summary - singleton record for overall statistics"""

    # Using "singleton" as the id since there will only be one record
    id = models.CharField(max_length=36, primary_key=True, default="singleton")

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

    # Absentee population
    population_absentee_total = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("कुल अनुपस्थित जनसंख्या")
    )
    population_male_absentee = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("अनुपस्थित पुरुष जनसंख्या")
    )
    population_female_absentee = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("अनुपस्थित महिला जनसंख्या")
    )
    population_other_absentee = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("अनुपस्थित अन्य जनसंख्या")
    )

    # Demographic ratios and averages
    sex_ratio = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("लिङ्ग अनुपात"),
    )
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
    population_density = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("जनसंख्या घनत्व"),
    )

    # Age groups
    population_0_to_14 = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("०-१४ वर्ष जनसंख्या")
    )
    population_15_to_59 = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("१५-५९ वर्ष जनसंख्या")
    )
    population_60_and_above = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("६० वर्षभन्दा माथि जनसंख्या")
    )

    # Growth and literacy rates (percentages)
    growth_rate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("वृद्धि दर")
    )
    literacy_rate_above_15 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("१५ वर्षभन्दा माथि साक्षरता दर"),
    )
    literacy_rate_15_to_24 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("१५-२४ वर्ष साक्षरता दर"),
    )

    class Meta:
        verbose_name = _("जनसांख्यिकीय सारांश")
        verbose_name_plural = _("जनसांख्यिकीय सारांश")

    def __str__(self):
        return f"जनसांख्यिकीय सारांश - कुल जनसंख्या: {self.total_population}"


# ३.३ उमेर तथा लिङ्गको आधारमा जनसंख्या विवरण
class WardAgeWisePopulation(BaseModel):
    """Ward age wise population"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    age_group = models.CharField(
        max_length=20, choices=AgeGroupChoice.choices, verbose_name=_("उमेर समूह")
    )
    gender = models.CharField(
        max_length=10, choices=GenderChoice.choices, verbose_name=_("लिङ्ग")
    )
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत उमेरगत जनसंख्या")
        verbose_name_plural = _("वडागत उमेरगत जनसंख्या")
        unique_together = ["ward_number", "age_group", "gender"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_age_group_display()} - {self.get_gender_display()}"


# ३.४ मातृभाषाको आधारमा जनसंख्या विवरण
class WardWiseMotherTonguePopulation(BaseModel):
    """Ward wise mother tongue population"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    language_type = models.CharField(
        max_length=50, choices=LanguageTypeChoice.choices, verbose_name=_("मातृभाषा")
    )
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत मातृभाषा जनसंख्या")
        verbose_name_plural = _("वडागत मातृभाषा जनसंख्या")
        unique_together = ["ward_number", "language_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_language_type_display()}"


# ३.५ धर्म अनुसार जनसंख्या विवरण
class WardWiseReligionPopulation(BaseModel):
    """Ward wise religion population"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    religion_type = models.CharField(
        max_length=20, choices=ReligionTypeChoice.choices, verbose_name=_("धर्म")
    )
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत धार्मिक जनसंख्या")
        verbose_name_plural = _("वडागत धार्मिक जनसंख्या")
        unique_together = ["ward_number", "religion_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_religion_type_display()}"


# ३.६ जातिगत आधारमा जनसंख्या विवरण
class WardWiseCastePopulation(BaseModel):
    """Ward wise caste population"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    caste_type = models.CharField(
        max_length=100, choices=CasteTypeChoice.choices, verbose_name=_("जातजाति")
    )
    population = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("जनसंख्या")
    )

    class Meta:
        verbose_name = _("वडागत जातीय जनसंख्या")
        verbose_name_plural = _("वडागत जातीय जनसंख्या")
        unique_together = ["ward_number", "caste_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_caste_type_display()}"


# ३.७ घरमूलीको विवरण
class WardWiseHouseheadGender(BaseModel):
    """Ward wise househead gender"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    ward_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("वडाको नाम")
    )
    gender = models.CharField(
        max_length=10, choices=GenderChoice.choices, verbose_name=_("घरमुखियाको लिङ्ग")
    )
    population = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार संख्या"))

    class Meta:
        verbose_name = _("वडागत घरमुखियाको लिङ्ग")
        verbose_name_plural = _("वडागत घरमुखियाको लिङ्ग")
        unique_together = ["ward_number", "gender"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_gender_display()} मुखिया"


# ३.८ पेशाका आधारमा जनसंख्या विवरण
class WardWiseMajorOccupation(BaseModel):
    """Ward wise major occupation"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    occupation = models.TextField(verbose_name=_("पेशा"))
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत मुख्य पेशा")
        verbose_name_plural = _("वडागत मुख्य पेशा")
        unique_together = ["ward_number", "occupation"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.occupation}"


# ३.९ आर्थिक रुपले सक्रिय जनसंख्या विवरण
class WardAgeWiseEconomicallyActivePopulation(BaseModel):
    """Ward age wise economically active population"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    age_group = models.CharField(
        max_length=20, choices=AgeGroupChoice.choices, verbose_name=_("उमेर समूह")
    )
    population = models.PositiveIntegerField(
        default=0, verbose_name=_("आर्थिक रूपमा सक्रिय जनसंख्या")
    )

    class Meta:
        verbose_name = _("वडागत उमेरअनुसार आर्थिक रूपमा सक्रिय जनसंख्या")
        verbose_name_plural = _("वडागत उमेरअनुसार आर्थिक रूपमा सक्रिय जनसंख्या")
        unique_together = ["ward_number", "age_group"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_age_group_display()}"


# ३.१० अपाङ्गताको आधारमा जनसंख्या विवरण
class WardWiseDisabilityCause(BaseModel):
    """Ward wise disability cause"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    disability_cause = models.CharField(
        max_length=20,
        choices=DisabilityCauseChoice.choices,
        verbose_name=_("अपाङ्गताको कारण"),
    )
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत अपाङ्गताको कारण")
        verbose_name_plural = _("वडागत अपाङ्गताको कारण")
        unique_together = ["ward_number", "disability_cause"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_disability_cause_display()}"


# ३.११ बसाइंसराइ सम्बन्धी विवरण
# क) जन्म स्थानको आधारमा जनसंख्या विवरण
class WardWiseBirthplaceHouseholds(BaseModel):
    """Ward wise birthplace households"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    birth_place = models.CharField(
        max_length=50, choices=BirthPlaceChoice.choices, verbose_name=_("जन्मस्थान")
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार संख्या"))

    class Meta:
        verbose_name = _("वडागत जन्मस्थानअनुसार घरपरिवार")
        verbose_name_plural = _("वडागत जन्मस्थानअनुसार घरपरिवार")
        unique_together = ["ward_number", "birth_place"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_birth_place_display()}"


# ख) बसाईसराई गरी आउने संख्याको आधारमा जनसंख्याको विवरण
class WardWiseMigratedHouseholds(BaseModel):
    """Ward wise migrated households"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    migrated_from = models.CharField(
        max_length=50,
        choices=MigratedFromChoice.choices,
        verbose_name=_("बसाइसराइको स्थान"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार संख्या"))

    class Meta:
        verbose_name = _("वडागत बसाइसराइ गरेका घरपरिवार")
        verbose_name_plural = _("वडागत बसाइसराइ गरेका घरपरिवार")
        unique_together = ["ward_number", "migrated_from"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_migrated_from_display()}"


# ३.१२ व्यक्तिगत घटना सम्बन्धी विवरण
# क) पाँच वर्षमुनिका बालबालिकाको जन्मदर्ताको आधारमा वडागत विवरण
class WardWiseBirthCertificatePopulation(BaseModel):
    """Ward wise birth certificate population"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    with_birth_certificate = models.PositiveIntegerField(
        default=0, verbose_name=_("जन्म दर्ता भएका")
    )
    without_birth_certificate = models.PositiveIntegerField(
        default=0, verbose_name=_("जन्म दर्ता नभएका")
    )
    total_population_under_5 = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("५ वर्षमुनिका कुल बालबालिका")
    )

    class Meta:
        verbose_name = _("वडागत जन्म दर्ता जनसंख्या")
        verbose_name_plural = _("वडागत जन्म दर्ता जनसंख्या")
        unique_together = ["ward_number"]

    def __str__(self):
        return f"वडा {self.ward_number} - जन्म दर्ता तथ्याङ्क"


# ख) विगत १२ महिनाको मृत्यु सम्बन्धी विवरण
# ग) लिङ्ग र उमेर समूह अनुसार विगत १२ महिनामा मृत्यु भएकाको विवरण
class WardAgeGenderWiseDeceasedPopulation(BaseModel):
    """Ward age gender wise deceased population"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    age_group = models.CharField(
        max_length=20, choices=AgeGroupChoice.choices, verbose_name=_("उमेर समूह")
    )
    gender = models.CharField(
        max_length=10, choices=GenderChoice.choices, verbose_name=_("लिङ्ग")
    )
    deceased_population = models.PositiveIntegerField(
        default=0, verbose_name=_("मृत्यु जनसंख्या")
    )

    class Meta:
        verbose_name = _("वडागत उमेर लिङ्गअनुसार मृत्यु जनसंख्या")
        verbose_name_plural = _("वडागत उमेर लिङ्गअनुसार मृत्यु जनसंख्या")
        unique_together = ["ward_number", "age_group", "gender"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_age_group_display()} - {self.get_gender_display()} (मृत्यु)"


# घ) मृत्युको कारण अनुसार मृतकको संख्या
class WardWiseDeathCause(BaseModel):
    """Ward wise death cause"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    death_cause = models.TextField(verbose_name=_("मृत्युको कारण"))
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत मृत्युको कारण")
        verbose_name_plural = _("वडागत मृत्युको कारण")
        unique_together = ["ward_number", "death_cause"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.death_cause}"
