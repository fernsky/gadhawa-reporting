"""
Social models for Lungri Rural Municipality Digital Profile

This module contains models for Chapter 5 (सामाजिक अवस्था) including:
- 5.1 शैक्षिक तथा मानव संशाधन विकास (Education and Human Resource Development)
- 5.2 स्वास्थ्य तथा पोषण (Health and Nutrition)
- 5.3 खानेपानी तथा सरसफाई (Water and Sanitation)
- 5.4 महिला, बालबालिका तथा सामाजिक समावेशीकरण (Women, Children and Social Inclusion)
- 5.5 युवा तथा खेलकूद र मनोरञ्जन (Youth, Sports and Recreation)
- 5.6 कला, भाषा तथा संस्कृति (Arts, Language and Culture)
- 5.7 शान्ति तथा सुरक्षाको अवस्था (Peace and Security)
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
# SOCIAL ENUMS (from TypeScript schemas)
# =============================================================================


# Common enums
class GenderChoice(models.TextChoices):
    MALE = "MALE", _("पुरुष")
    FEMALE = "FEMALE", _("महिला")
    OTHER = "OTHER", _("अन्य")


# Social Marriage Age Groups (from ward-age-gender-wise-first-marriage-age.ts)
class FirstMarriageAgeGroupChoice(models.TextChoices):
    AGE_0_14 = "AGE_0_14", _("०-१४ वर्ष")
    AGE_15_19 = "AGE_15_19", _("१५-१९ वर्ष")
    AGE_20_24 = "AGE_20_24", _("२०-२४ वर्ष")
    AGE_25_29 = "AGE_25_29", _("२५-२९ वर्ष")
    AGE_30_34 = "AGE_30_34", _("३०-३४ वर्ष")
    AGE_35_39 = "AGE_35_39", _("३५-३९ वर्ष")
    AGE_40_44 = "AGE_40_44", _("४०-४४ वर्ष")
    AGE_45_49 = "AGE_45_49", _("४५-४९ वर्ष")
    AGE_50_54 = "AGE_50_54", _("५०-५४ वर्ष")
    AGE_55_59 = "AGE_55_59", _("५५-५९ वर्ष")
    AGE_60_AND_ABOVE = "AGE_60_AND_ABOVE", _("६० वर्ष र माथि")


# Water and Sanitation Enums (from water-and-sanitation schemas)
class DrinkingWaterSourceChoice(models.TextChoices):
    TAP_INSIDE_HOUSE = "TAP_INSIDE_HOUSE", _("घर भित्र पानी ट्याप")
    TAP_OUTSIDE_HOUSE = "TAP_OUTSIDE_HOUSE", _("घर बाहिर पानी ट्याप")
    TUBEWELL = "TUBEWELL", _("ट्यूबवेल")
    COVERED_WELL = "COVERED_WELL", _("ढाकेको इनार")
    OPEN_WELL = "OPEN_WELL", _("खुला इनार")
    AQUIFIER_MOOL = "AQUIFIER_MOOL", _("भुमिगत जलश्रोत मूल")
    RIVER = "RIVER", _("नदी")
    JAR = "JAR", _("जार")
    OTHER = "OTHER", _("अन्य")


class WaterPurificationChoice(models.TextChoices):
    BOILING = "BOILING", _("उमालेर")
    FILTERING = "FILTERING", _("छानेर")
    CHEMICAL_PIYUSH = "CHEMICAL_PIYUSH", _("रसायनिक पियुष")
    NO_ANY_FILTERING = "NO_ANY_FILTERING", _("कुनै छनौट नगर्ने")
    OTHER = "OTHER", _("अन्य")


class ToiletTypeChoice(models.TextChoices):
    FLUSH_WITH_SEPTIC_TANK = "FLUSH_WITH_SEPTIC_TANK", _("सेप्टिक ट्यांक सहित फ्लश")
    NORMAL = "NORMAL", _("सामान्य")
    PUBLIC_EILANI = "PUBLIC_EILANI", _("सार्वजनिक ऐलानी")
    NO_TOILET = "NO_TOILET", _("शौचालय छैन")
    OTHER = "OTHER", _("अन्य")


class SolidWasteManagementChoice(models.TextChoices):
    HOME_COLLECTION = "HOME_COLLECTION", _("घर संकलन")
    WASTE_COLLECTING_PLACE = "WASTE_COLLECTING_PLACE", _("फोहोर संकलन ठाउँ")
    BURNING = "BURNING", _("जलाउने")
    DIGGING = "DIGGING", _("गाड्ने")
    RIVER = "RIVER", _("नदी")
    ROAD_OR_PUBLIC_PLACE = "ROAD_OR_PUBLIC_PLACE", _("सडक वा सार्वजनिक ठाउँ")
    COMPOST_MANURE = "COMPOST_MANURE", _("कम्पोस्ट मल")
    OTHER = "OTHER", _("अन्य")


# =============================================================================
# SOCIAL MODELS (Chapter 5 - सामाजिक अवस्था)
# =============================================================================


# ५.१ शैक्षिक तथा मानव संशाधन विकास
# ५.१.१ पाँच वर्षभन्दा माथि र १५ बर्षभन्दा माथिको साक्षरता विवरण
# Literacy enums
class LiteracyTypeChoice(models.TextChoices):
    BOTH_READING_AND_WRITING = "BOTH_READING_AND_WRITING", _("पढ्न र लेख्न दुवै")
    READING_ONLY = "READING_ONLY", _("पढ्न मात्र")
    ILLITERATE = "ILLITERATE", _("निरक्षर")


class WardWiseLiteracyStatus(BaseModel):
    """Ward wise literacy status (5.1.1 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    literacy_type = models.CharField(
        max_length=25,
        choices=LiteracyTypeChoice.choices,
        verbose_name=_("साक्षरता प्रकार"),
    )
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत साक्षरता अवस्था")
        verbose_name_plural = _("वडागत साक्षरता अवस्था")
        unique_together = ["ward_number", "literacy_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_literacy_type_display()}"


# ५.१.२ पाँच वर्ष र सोभन्दा माथिको शैक्षिक अवस्था


class MajorSubjectTypeChoice(models.TextChoices):
    ENGLISH = "ENGLISH", _("अंग्रेजी")
    ECONOMICS = "ECONOMICS", _("अर्थशास्त्र")
    ENGINEERING = "ENGINEERING", _("इन्जिनियरिङ")
    HISTORY = "HISTORY", _("इतिहास")
    HOME_ECONOMICS = "HOME_ECONOMICS", _("गृह अर्थशास्त्र")
    RURAL_DEVELOPMENT = "RURAL_DEVELOPMENT", _("ग्रामीण विकास")
    MEDICINE = "MEDICINE", _("चिकित्सा")
    POPULATION_STUDY = "POPULATION_STUDY", _("जनसंख्या अध्ययन")
    BIOLOGY = "BIOLOGY", _("जैविक विज्ञान")
    STATISTICS = "STATISTICS", _("तथ्यांक")
    NEPALI = "NEPALI", _("नेपाली")
    TOURISM = "TOURISM", _("पर्यटन")
    GEOGRAPHY = "GEOGRAPHY", _("भूगोल")
    PHYSICS = "PHYSICS", _("भौतिकशास्त्र")
    PSYCHOLOGY = "PSYCHOLOGY", _("मनोविज्ञान")
    HUMANITIES = "HUMANITIES", _("मानविकी")
    CHEMISTRY = "CHEMISTRY", _("रसायनशास्त्र")
    POLITICAL_SCIENCE = "POLITICAL_SCIENCE", _("राजनीति विज्ञान")
    FORESTRY_AND_AGRICULTURE = "FORESTRY_AND_AGRICULTURE", _("वन तथा कृषि")
    BOTANY = "BOTANY", _("वनस्पति विज्ञान")
    COMMERCE = "COMMERCE", _("वाणिज्य")
    SCIENCE = "SCIENCE", _("विज्ञान")
    MANAGEMENT = "MANAGEMENT", _("व्यवस्थापन")
    EDUCATION = "EDUCATION", _("शिक्षा")
    EDUCATIONAL_SCIENCE = "EDUCATIONAL_SCIENCE", _("शिक्षा विज्ञान")
    SANSKRIT = "SANSKRIT", _("संस्कृत")
    ARTS = "ARTS", _("कला")
    SOCIAL_SCIENCES = "SOCIAL_SCIENCES", _("सामाजिक विज्ञान")
    INFORMATION_TECHNOLOGY = "INFORMATION_TECHNOLOGY", _("सूचना प्रविधि")
    HINDI = "HINDI", _("हिन्दी")
    OTHER = "OTHER", _("अन्य")


class WardWiseMajorSubject(BaseModel):
    """Ward wise major subject (5.1.2 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    subject_type = models.CharField(
        max_length=30,
        choices=MajorSubjectTypeChoice.choices,
        verbose_name=_("मुख्य विषय प्रकार"),
    )
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत मुख्य विषय")
        verbose_name_plural = _("वडागत मुख्य विषय")
        unique_together = ["ward_number", "subject_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_subject_type_display()}"


# ५.१.३ तहगत रुपमा शैक्षिक संस्था/विद्यालय (सामुदायिक, संस्थागत, मदरसा, गुम्बा) र विद्यार्थी विवरण
# School/Institution type enums
class SchoolTypeChoice(models.TextChoices):
    COMMUNITY = "COMMUNITY", _("सामुदायिक")
    INSTITUTIONAL = "INSTITUTIONAL", _("संस्थागत")
    MADRASA = "MADRASA", _("मदरसा")
    GUMBA = "GUMBA", _("गुम्बा")
    BOARDING = "BOARDING", _("बोर्डिङ")


class School(BaseModel):
    """School master data"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    school_name = models.CharField(max_length=200, verbose_name=_("विद्यालयको नाम"))
    school_type = models.CharField(
        max_length=15,
        choices=SchoolTypeChoice.choices,
        default=SchoolTypeChoice.COMMUNITY,
        verbose_name=_("विद्यालयको प्रकार"),
    )

    class Meta:
        verbose_name = _("विद्यालय")
        verbose_name_plural = _("विद्यालयहरू")
        unique_together = ["ward_number", "school_name"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.school_name}"


class SchoolStudentData(BaseModel):
    """School student data by year (5.1.3 - from table data)"""

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="student_data",
        verbose_name=_("विद्यालय"),
    )
    year = models.CharField(max_length=10, verbose_name=_("वर्ष"))
    female_students = models.PositiveIntegerField(default=0, verbose_name=_("छात्रा"))
    male_students = models.PositiveIntegerField(default=0, verbose_name=_("छात्र"))

    class Meta:
        verbose_name = _("विद्यालय विद्यार्थी तथ्यांक")
        verbose_name_plural = _("विद्यालय विद्यार्थी तथ्यांक")
        unique_together = ["school", "year"]

    def __str__(self):
        return f"{self.school.school_name} - {self.year}"

    @property
    def total_students(self):
        return self.female_students + self.male_students


# ५.१.४ विद्यालयमा अध्ययन गरिरहेका तहगत छात्रछात्राको विवरण


class EducationalLevelTypeChoice(models.TextChoices):
    CHILD_DEVELOPMENT_CENTER = "CHILD_DEVELOPMENT_CENTER", _("बाल विकास केन्द्र")
    NURSERY = "NURSERY", _("नर्सरी")
    GRADE_1 = "GRADE_1", _("कक्षा १")
    GRADE_2 = "GRADE_2", _("कक्षा २")
    GRADE_3 = "GRADE_3", _("कक्षा ३")
    GRADE_4 = "GRADE_4", _("कक्षा ४")
    GRADE_5 = "GRADE_5", _("कक्षा ५")
    GRADE_6 = "GRADE_6", _("कक्षा ६")
    GRADE_7 = "GRADE_7", _("कक्षा ७")
    GRADE_8 = "GRADE_8", _("कक्षा ८")
    GRADE_9 = "GRADE_9", _("कक्षा ९")
    GRADE_10 = "GRADE_10", _("कक्षा १०")
    SLC_LEVEL = "SLC_LEVEL", _("एसएलसी तह")
    CLASS_12_LEVEL = "CLASS_12_LEVEL", _("कक्षा १२ तह")
    BACHELOR_LEVEL = "BACHELOR_LEVEL", _("स्नातक तह")
    MASTERS_LEVEL = "MASTERS_LEVEL", _("स्नातकोत्तर तह")
    PHD_LEVEL = "PHD_LEVEL", _("पीएचडी तह")
    INFORMAL_EDUCATION = "INFORMAL_EDUCATION", _("अनौपचारिक शिक्षा")
    OTHER = "OTHER", _("अन्य")
    EDUCATED = "EDUCATED", _("शिक्षित")
    UNKNOWN = "UNKNOWN", _("अज्ञात")


class WardWiseEducationalLevel(BaseModel):
    """Ward wise educational level (5.1.2 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    educational_level_type = models.CharField(
        max_length=30,
        choices=EducationalLevelTypeChoice.choices,
        verbose_name=_("शैक्षिक तह प्रकार"),
    )
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत शैक्षिक तह")
        verbose_name_plural = _("वडागत शैक्षिक तह")
        unique_together = ["ward_number", "educational_level_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_educational_level_type_display()}"


# ५.१.५ क्याम्पस तथा प्राविधिक शिक्षालय र अध्ययनरत छात्रछात्राको विवरण


# ५.१.६ विद्यालय वाहिर रहेका तथा विद्यालय छाडेका बालबालिकाहरुको विवरण
# Youth population enums
class YouthAgeGroupChoice(models.TextChoices):
    AGE_5_9 = "AGE_5_9", _("५-९ वर्ष")
    AGE_10_14 = "AGE_10_14", _("१०-१४ वर्ष")
    AGE_15_19 = "AGE_15_19", _("१५-१९ वर्ष")
    AGE_20_24 = "AGE_20_24", _("२०-२४ वर्ष")
    AGE_25 = "AGE_25", _("२५ वर्ष")


class SchoolAttendanceStatusChoice(models.TextChoices):
    ATTENDING = "ATTENDING", _("विद्यालय जाने")
    NOT_ATTENDING = "NOT_ATTENDING", _("विद्यालय नजाने")


class WardWiseYouthSchoolAttendance(BaseModel):
    """Ward wise youth population by school attendance (5.1.6 - विद्यालय वाहिर रहेका तथा विद्यालय छाडेका बालबालिकाहरुको विवरण)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    age_group = models.CharField(
        max_length=15,
        choices=YouthAgeGroupChoice.choices,
        verbose_name=_("उमेर समूह"),
    )
    gender = models.CharField(
        max_length=10, choices=GenderChoice.choices, verbose_name=_("लिंग")
    )
    attendance_status = models.CharField(
        max_length=15,
        choices=SchoolAttendanceStatusChoice.choices,
        verbose_name=_("विद्यालय उपस्थिति अवस्था"),
    )
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत युवा विद्यालय उपस्थिति")
        verbose_name_plural = _("वडागत युवा विद्यालय उपस्थिति")
        unique_together = ["ward_number", "age_group", "gender", "attendance_status"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_age_group_display()} - {self.get_gender_display()} - {self.get_attendance_status_display()}"


# School dropout cause enums


class SchoolDropoutCauseTypeChoice(models.TextChoices):
    LIMITED_SPACE = "LIMITED_SPACE", _("सीमित ठाउँ")
    EXPENSIVE = "EXPENSIVE", _("महँगो")
    FAR = "FAR", _("टाढा")
    HOUSE_HELP = "HOUSE_HELP", _("घरको काम")
    UNWILLING_PARENTS = "UNWILLING_PARENTS", _("अनिच्छुक अभिभावक")
    WANTED_STUDY_COMPLETED = "WANTED_STUDY_COMPLETED", _("अध्ययन पूरा गर्न चाहना")
    MARRIAGE = "MARRIAGE", _("विवाह")
    EMPLOYMENT = "EMPLOYMENT", _("रोजगारी")
    UNKNOWN = "UNKNOWN", _("अज्ञात")
    OTHER = "OTHER", _("अन्य")


class WardWiseSchoolDropout(BaseModel):
    """Ward wise school dropout causes (from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    cause = models.CharField(
        max_length=25,
        choices=SchoolDropoutCauseTypeChoice.choices,
        verbose_name=_("विद्यालय छाड्नुको कारण"),
    )
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत विद्यालय छाड्नुको कारण")
        verbose_name_plural = _("वडागत विद्यालय छाड्नुको कारण")
        unique_together = ["ward_number", "cause"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_cause_display()}"


# ५.१.७ सिकाइ, उपलब्धि तथा उत्तीर्ण दर
# ५.१.८ खुद भर्ना, निरन्तरता तथा टिकाउ दर
# ५.१.९ बाल विकास केन्द्रको विवरण
# ५.१.१० विद्यालय शान्ति क्षेत्र र विद्यालय सुधार योजना विवरण
# ५.१.११ शिक्षक तथा शैक्षिक जनशक्ति विवरण
# ५.१.१२ आधारभूत र माध्यमिक विद्यालयमा पहुँचको अवस्था (प्रमुख वस्तीहरुबाट विद्यालय पुग्न लाग्ने समय)
# ५.१.१३ शैक्षिक संस्था उपलब्ध भौतिक पूर्वाधार तथा सुबिधा
# ५.१.१४ छात्रबृत्ति तथा अन्य लक्षित सुविधा उपलब्धताको अवस्था (छात्रबृत्ति, बालअनुदान, दिवा खाजा)
# ५.१.१५ नमूना तथा इन्टरनेट सुविधा उपलब्ध विद्यालय विवरण
# ५.१.१६ सुधारिएको मापदण्ड (भूकम्प प्रतिरोधी) अनुसार निर्माण भएका तथा रेट्रोफिटिङ्ग गरिएका विद्यालय
# ५.१.१७ स्थानीय सरकारको शिक्षा क्षेत्रमा लगानी
# ५.१.१८ प्राविधिक तथा विशेष सीपयुक्त मानव संसाधन
# ५.१.१९ अपाङ्गता तथा विशेष शिक्षा स्रोतकक्षा र विद्यार्थी विवरण
# ५.१.२० शैक्षिक गुणस्तर सम्बन्धी विवरण
# ५.१.२१ बालमैत्री शिक्षा सम्बन्धी विवरण
# ५.१.२२ विद्यालयको भौतिक अवस्था
# ५.१.२३ स्रोत नक्शा


# ५.२ स्वास्थ्य तथा पोषण
# ५.२.१ स्वास्थ्य संस्था (अस्पताल, प्राथमिक स्वास्थ्य केन्द्र, स्वास्थ्य चौकी र आयुर्वेद केन्द्र) को विवरण
class HealthInstitutionTypeChoice(models.TextChoices):
    HEALTH_POST = "HEALTH_POST", _("स्वास्थ्य चौकी")
    PRIMARY_HEALTH_CENTER = "PRIMARY_HEALTH_CENTER", _("प्राथमिक स्वास्थ्य केन्द्र")
    COMMUNITY_HEALTH_UNIT = "COMMUNITY_HEALTH_UNIT", _("सामुदायिक स्वास्थ्य इकाई")


class HealthInstitution(BaseModel):
    """Health Institution (5.2.1 - स्वास्थ्य संस्था)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    name = models.CharField(max_length=200, verbose_name=_("संस्थाको नाम"))
    institution_type = models.CharField(
        max_length=25,
        choices=HealthInstitutionTypeChoice.choices,
        verbose_name=_("संस्थाको प्रकार"),
    )

    class Meta:
        verbose_name = _("स्वास्थ्य संस्था")
        verbose_name_plural = _("स्वास्थ्य संस्थाहरू")
        unique_together = ["ward_number", "name"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.name}"

    def save(self, *args, **kwargs):
        # Auto-detect institution type from name
        if "चौकी" in self.name:
            self.institution_type = HealthInstitutionTypeChoice.HEALTH_POST
        elif "आ.स्वा.से.के" in self.name:
            self.institution_type = HealthInstitutionTypeChoice.PRIMARY_HEALTH_CENTER
        elif "सा.स्वा.इकाइ" in self.name:
            self.institution_type = HealthInstitutionTypeChoice.COMMUNITY_HEALTH_UNIT
        super().save(*args, **kwargs)


# ५.२.२ स्वास्थ्य संस्थामा उपलब्ध तथा कार्यरत चिकित्सक, स्वास्थ्यकर्मी र अन्य जनशक्ति विवरण
# ५.२.३ प्राथमिक स्वास्थ्य सेवाको पहुँचको अवस्था (प्रमुख बस्तीहरुबाट स्वास्थ्य संस्था पुग्न लाग्ने समय)
# Time to health organization enums
class TimeToHealthOrganizationChoice(models.TextChoices):
    UNDER_15_MIN = "UNDER_15_MIN", _("१५ मिनेट मुनि")
    UNDER_30_MIN = "UNDER_30_MIN", _("३० मिनेट मुनि")
    UNDER_1_HOUR = "UNDER_1_HOUR", _("१ घण्टा मुनि")
    ONE_HOUR_OR_MORE = "1_HOUR_OR_MORE", _("१ घण्टा वा बढी")


class WardWiseTimeToHealthOrganization(BaseModel):
    """Ward wise time to health organization (5.2.3 - प्राथमिक स्वास्थ्य सेवाको पहुँचको अवस्था)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    time_to_health_organization = models.CharField(
        max_length=20,
        choices=TimeToHealthOrganizationChoice.choices,
        verbose_name=_("स्वास्थ्य संस्था पुग्न लाग्ने समय"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत स्वास्थ्य संस्था पहुँच समय")
        verbose_name_plural = _("वडागत स्वास्थ्य संस्था पहुँच समय")
        unique_together = ["ward_number", "time_to_health_organization"]

    def __str__(self):
        return (
            f"वडा {self.ward_number} - {self.get_time_to_health_organization_display()}"
        )


# ५.२.४ उपलब्ध स्वास्थ्य सेवा तथा सुविधाहरु
# ५.२.५ खोप सेवा सम्बन्धी विवरण
# क) खोपको विवरण
class VaccinationIndicatorTypeChoice(models.TextChoices):
    BCG = "BCG", _("बीसीजी")
    MEASLES = "MEASLES", _("दादुरा")
    HEPATITIS_B = "HEPATITIS_B", _("हेपाटाइटिस बी")
    PNEUMONIA = "PNEUMONIA", _("निमोनिया")
    POLIO = "POLIO", _("पोलियो")
    TETANUS = "TETANUS", _("धनुष्टंकार")
    DPT = "DPT", _("डीपीटी")
    JAPANESE_ENCEPHALITIS = "JAPANESE_ENCEPHALITIS", _("जापानी मस्तिष्क ज्वरो")


class WardWiseVaccinationData(BaseModel):
    """Ward wise vaccination data by year (5.2.5 क) खोपको विवरण)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    indicator = models.CharField(
        max_length=25,
        choices=VaccinationIndicatorTypeChoice.choices,
        verbose_name=_("सूचक"),
    )
    year = models.CharField(max_length=20, verbose_name=_("वर्ष"))
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("प्रतिशत"),
    )

    class Meta:
        verbose_name = _("वडागत खोप तथ्यांक")
        verbose_name_plural = _("वडागत खोप तथ्यांक")
        unique_together = ["ward_number", "indicator", "year"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_indicator_display()} - {self.year}"


# ५.२.६ बाल स्वास्थ्य तथा कुपोषणको अवस्था
# ५.२.७ प्रमुख रोग र उपचार सम्बन्धी विवरण
class DiseaseTypeChoice(models.TextChoices):
    FEVER = "FEVER", _("ज्वरो")
    COUGH = "COUGH", _("खोकी")
    ABDOMINAL_PAIN = "ABDOMINAL_PAIN", _("पेट दुखाइ")
    ITCHING = "ITCHING", _("चिलाउने")
    FATIGUE_AND_WEAKNESS = "FATIGUE_AND_WEAKNESS", _("थकान र कमजोरी")
    ARTHRITIS = "ARTHRITIS", _("गठिया")
    CHEST_PAIN = "CHEST_PAIN", _("छाती दुखाइ")
    ORAL_STOMATITIS = "ORAL_STOMATITIS", _("मुखको घाउ")
    DIZZINESS_AND_VERTIGO = "DIZZINESS_AND_VERTIGO", _("चक्कर लाग्ने")
    SHORTNESS_OF_BREATH = "SHORTNESS_OF_BREATH", _("सास फेर्न गाह्रो")


class WardYearWiseCommonDiseases(BaseModel):
    """Ward wise disease data by year (5.2.6 - बाल स्वास्थ्य तथा कुपोषणको अवस्था)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    disease_type = models.CharField(
        max_length=40,
        choices=DiseaseTypeChoice.choices,
        verbose_name=_("रोगको नाम"),
    )
    year = models.CharField(max_length=20, verbose_name=_("वर्ष"))
    case_count = models.PositiveIntegerField(default=0, verbose_name=_("बिरामी संख्या"))

    class Meta:
        verbose_name = _("वडागत रोग तथ्यांक")
        verbose_name_plural = _("वडागत रोग तथ्यांक")
        unique_together = ["ward_number", "disease_type", "year"]

    def __str__(self):
        return (
            f"वडा {self.ward_number} - {self.get_disease_type_display()} - {self.year}"
        )


# ५.२.८ सुरक्षित मातृत्व


class SafeMaternityIndicatorTypeChoice(models.TextChoices):
    FIRST_ANTENATAL_CHECKUP = "FIRST_ANTENATAL_CHECKUP", _("पहिलो गर्भजाँच")
    FOUR_ANTENATAL_CHECKUPS = "FOUR_ANTENATAL_CHECKUPS", _("चार पटक गर्भ जाच गर्ने प्रतिशत")
    INSTITUTIONAL_DELIVERY = "INSTITUTIONAL_DELIVERY", _("संस्थागत प्रशुती संख्या")
    POSTNATAL_CHECKUP_24_HOURS = "POSTNATAL_CHECKUP_24_HOURS", _(
        "२४ घण्टा भित्र सुत्केरी जाँचको प्रतिशत"
    )
    FOUR_POSTNATAL_CHECKUPS = "FOUR_POSTNATAL_CHECKUPS", _("चार पटक सुत्केरी जाँचको प्रतिशत")
    MATERNAL_MORTALITY_RATE = "MATERNAL_MORTALITY_RATE", _("मातृ मृत्युको प्रतिशत")


class SafeMaternityData(BaseModel):
    """Safe maternity data by year (5.2.5 ख) सुरक्षित मातृत्वको अवस्थाको विवरण)"""

    indicator = models.CharField(
        max_length=30,
        choices=SafeMaternityIndicatorTypeChoice.choices,
        verbose_name=_("सूचक"),
    )
    year = models.CharField(max_length=50, verbose_name=_("वर्ष"))
    value = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        verbose_name=_("मान"),
    )

    class Meta:
        verbose_name = _("सुरक्षित मातृत्व तथ्यांक")
        verbose_name_plural = _("सुरक्षित मातृत्व तथ्यांक")
        unique_together = ["indicator", "year"]

    def __str__(self):
        return f"{self.get_indicator_display()} - {self.year}"


# ५.२.९ स्रोत नक्शा


# ५.३ खानेपानी तथा सरसफाई
# ५.३.१ खानेपानी सुविधाको अवस्था
class WardWiseWaterPurification(BaseModel):
    """Ward wise water purification (5.3.1 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    water_purification = models.CharField(
        max_length=20,
        choices=WaterPurificationChoice.choices,
        verbose_name=_("पानी शुद्धिकरण"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत पानी शुद्धिकरण")
        verbose_name_plural = _("वडागत पानी शुद्धिकरण")
        unique_together = ["ward_number", "water_purification"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_water_purification_display()}"


# ५.३.२ खानेपानीको श्रोतको विवरण


class WardWiseDrinkingWaterSource(BaseModel):
    """Ward wise drinking water source (5.3.2 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    drinking_water_source = models.CharField(
        max_length=25,
        choices=DrinkingWaterSourceChoice.choices,
        verbose_name=_("पिउने पानीको स्रोत"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत पिउने पानीको स्रोत")
        verbose_name_plural = _("वडागत पिउने पानीको स्रोत")
        unique_together = ["ward_number", "drinking_water_source"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_drinking_water_source_display()}"


# ५.३.३ शौचालय प्रयोगको अवस्था


class WardWiseToiletType(BaseModel):
    """Ward wise toilet type (5.3.3 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    toilet_type = models.CharField(
        max_length=25,
        choices=ToiletTypeChoice.choices,
        verbose_name=_("शौचालयको प्रकार"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत शौचालयको प्रकार")
        verbose_name_plural = _("वडागत शौचालयको प्रकार")
        unique_together = ["ward_number", "toilet_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_toilet_type_display()}"


# ५.३.४ सार्वजनिक शौचालय
# ५.३.५ फोहोरमैला व्यवस्थापन
class WardWiseSolidWasteManagement(BaseModel):
    """Ward wise solid waste management (5.3.5 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    solid_waste_management = models.CharField(
        max_length=25,
        choices=SolidWasteManagementChoice.choices,
        verbose_name=_("ठोस फोहोर व्यवस्थापन"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत ठोस फोहोर व्यवस्थापन")
        verbose_name_plural = _("वडागत ठोस फोहोर व्यवस्थापन")
        unique_together = ["ward_number", "solid_waste_management"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_solid_waste_management_display()}"


# ५.३.६ ढल व्यवस्थापन
# ५.३.७ स्रोत नक्शा

# ५.४ महिला, बालबालिका तथा सामाजिक समावेशीकरण
# ५.४.१ लिङ्ग अनुसार बाल विवाह (अठार वर्ष मुनिका)


class WardAgeGenderWiseFirstMarriageAge(BaseModel):
    """Ward age gender wise first marriage age (5.4.1 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    first_marriage_age_group = models.CharField(
        max_length=20,
        choices=FirstMarriageAgeGroupChoice.choices,
        verbose_name=_("पहिलो विवाहको उमेर समूह"),
    )
    gender = models.CharField(
        max_length=10, choices=GenderChoice.choices, verbose_name=_("लिंग")
    )
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत उमेर लिंग अनुसार पहिलो विवाहको उमेर")
        verbose_name_plural = _("वडागत उमेर लिंग अनुसार पहिलो विवाहको उमेर")
        unique_together = ["ward_number", "first_marriage_age_group", "gender"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_first_marriage_age_group_display()} - {self.get_gender_display()}"


# ५.४.२ कामदारको रुपमा घर वाहिर रहेका बालबालिका
# ५.४.३ बालक्लव तथा संजालको विवरण
# ५.४.४ घरपरिवार विहीन बालबालिकाको अवस्था
# ५.४.५ अपाङ्गताका आधारमा जनसंख्या


class WardWiseDisabledPopulation(BaseModel):
    """Ward wise disabled population (5.4.5 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    disabled_population = models.PositiveIntegerField(
        default=0, verbose_name=_("अपाङ्गता भएको जनसंख्या")
    )

    class Meta:
        verbose_name = _("वडागत अपाङ्गता भएको जनसंख्या")
        verbose_name_plural = _("वडागत अपाङ्गता भएको जनसंख्या")
        unique_together = ["ward_number"]

    def __str__(self):
        return f"वडा {self.ward_number} - अपाङ्गता: {self.disabled_population}"


# ५.४.१० जेष्ठ नागरिक तथा एकल महिला


class WardWiseOldAgePopulationAndSingleWomen(BaseModel):
    """Ward wise old age population and single women (5.4.10 - from TypeScript schema)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    male_old_age_population = models.PositiveIntegerField(
        default=0, verbose_name=_("पुरुष जेष्ठ नागरिक जनसंख्या")
    )
    female_old_age_population = models.PositiveIntegerField(
        default=0, verbose_name=_("महिला जेष्ठ नागरिक जनसंख्या")
    )
    single_women_population = models.PositiveIntegerField(
        default=0, verbose_name=_("एकल महिला जनसंख्या")
    )

    class Meta:
        verbose_name = _("वडागत जेष्ठ नागरिक र एकल महिला जनसंख्या")
        verbose_name_plural = _("वडागत जेष्ठ नागरिक र एकल महिला जनसंख्या")
        unique_together = ["ward_number"]

    def __str__(self):
        return f"वडा {self.ward_number} - जेष्ठ नागरिक र एकल महिला"

    @property
    def total_old_age_population(self):
        return self.male_old_age_population + self.female_old_age_population


# ५.४.११ अल्पसंख्यक सीमान्तकृत वर्गको विवरण
# ५.४.१२ वार्षिक कार्यक्रमबाट लक्षित कार्यक्रमतर्फ भएको विनियोजन तथा खर्चको अवस्था
# ५.४.१३ स्रोत नक्शा


# Educational Institution Type Choices for 5.1.2
class EducationalInstitutionTypeChoice(models.TextChoices):
    COMMUNITY_SCHOOL = "COMMUNITY_SCHOOL", _("सामुदायिक विद्यालय")
    RELIGIOUS_SCHOOL = "RELIGIOUS_SCHOOL", _("धार्मिक विद्यालय")
    TECHNICAL_SCHOOL = "TECHNICAL_SCHOOL", _("प्राविधिक विद्यालय")
    COMMUNITY_LEARNING_CENTER = "COMMUNITY_LEARNING_CENTER", _("सामुदायिक सिकाई केन्द्र")
    PRIVATE_SCHOOL = "PRIVATE_SCHOOL", _("निजी विद्यालय")
    OTHER = "OTHER", _("अन्य")


# School Level Choices
class SchoolLevelChoice(models.TextChoices):
    PRIMARY = "PRIMARY", _("प्राथमिक")  # प्रा.वि.
    LOWER_SECONDARY = "LOWER_SECONDARY", _("निम्न माध्यमिक")  # आ.वि.
    SECONDARY = "SECONDARY", _("माध्यमिक")  # मा.वि.
    HIGHER_SECONDARY = "HIGHER_SECONDARY", _("उच्च माध्यमिक")
    EARLY_CHILDHOOD = "EARLY_CHILDHOOD", _("बाल विकास केन्द्र")  # बा.वि.के.
    OTHER = "OTHER", _("अन्य")


class WardWiseEducationalInstitution(BaseModel):
    """Ward wise educational institutions and student details (5.1.2)

    This model handles data for community schools and their student enrollment
    across different years and wards.
    """

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    data_year = models.CharField(
        max_length=10,
        verbose_name=_("डेटा वर्ष"),
        help_text=_("Nepali year (e.g., २०७९, २०८०, २०८१)"),
    )
    institution_name = models.CharField(
        max_length=255,
        verbose_name=_("शैक्षिक संस्थाको नाम"),
        help_text=_("Full name of the educational institution"),
    )
    institution_type = models.CharField(
        max_length=50,
        choices=EducationalInstitutionTypeChoice.choices,
        default=EducationalInstitutionTypeChoice.COMMUNITY_SCHOOL,
        verbose_name=_("संस्थाको प्रकार"),
    )
    school_level = models.CharField(
        max_length=50,
        choices=SchoolLevelChoice.choices,
        verbose_name=_("विद्यालयको तह"),
        null=True,
        blank=True,
    )
    male_students = models.PositiveIntegerField(
        default=0,
        verbose_name=_("पुरुष विद्यार्थी संख्या"),
    )
    female_students = models.PositiveIntegerField(
        default=0,
        verbose_name=_("महिला विद्यार्थी संख्या"),
    )
    total_teachers = models.PositiveIntegerField(
        default=0,
        verbose_name=_("कुल शिक्षक संख्या"),
        null=True,
        blank=True,
    )
    is_operational = models.BooleanField(
        default=True,
        verbose_name=_("सञ्चालनमा छ/छैन"),
    )

    class Meta:
        verbose_name = _("वडागत शैक्षिक संस्था र विद्यार्थी विवरण")
        verbose_name_plural = _("वडागत शैक्षिक संस्था र विद्यार्थी विवरण")
        unique_together = ["ward_number", "data_year", "institution_name"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.institution_name} ({self.data_year})"

    @property
    def total_students(self):
        """Calculate total students (male + female)"""
        return self.male_students + self.female_students

    @property
    def gender_ratio(self):
        """Calculate gender ratio (female percentage)"""
        if self.total_students == 0:
            return 0
        return round((self.female_students / self.total_students) * 100, 2)

    def get_school_level_from_name(self):
        """Automatically determine school level from institution name"""
        name = self.institution_name.lower()
        if "मा.वि." in self.institution_name or "माध्यमिक" in name:
            return SchoolLevelChoice.SECONDARY
        elif "प्रा.वि." in self.institution_name or "प्राथमिक" in name:
            return SchoolLevelChoice.PRIMARY
        elif "आ.वि." in self.institution_name:
            return SchoolLevelChoice.LOWER_SECONDARY
        elif "बा.वि.के." in self.institution_name:
            return SchoolLevelChoice.EARLY_CHILDHOOD
        else:
            return SchoolLevelChoice.OTHER

    def save(self, *args, **kwargs):
        """Auto-populate school level if not provided"""
        if not self.school_level:
            self.school_level = self.get_school_level_from_name()
        super().save(*args, **kwargs)


# Teacher Position Types for 5.1.5
class TeacherPositionTypeChoice(models.TextChoices):
    APPROVED_QUOTA = "APPROVED_QUOTA", _("स्वीकृत दरबन्दी")
    RELIEF = "RELIEF", _("राहत")
    FEDERAL_GRANT = "FEDERAL_GRANT", _("संघीय अनुदान")
    RM_GRANT = "RM_GRANT", _("गाउँपालिका अनुदान")
    PRIVATE_SOURCE = "PRIVATE_SOURCE", _("निजी स्रोत")


# Teacher Level Assignment Choices for 5.1.5
class TeacherLevelChoice(models.TextChoices):
    CHILD_DEVELOPMENT = "CHILD_DEVELOPMENT", _("बाल विकास")
    BASIC_1_5 = "BASIC_1_5", _("आधारभूत १-५")
    BASIC_6_8 = "BASIC_6_8", _("आधारभूत ६-८")
    BASIC_9_10 = "BASIC_9_10", _("आधारभूत ९-१०")
    BASIC_11_12 = "BASIC_11_12", _("आधारभूत ११-१२")


class WardWiseTeacherStaffing(BaseModel):
    """Ward wise teacher and educational manpower details (5.1.5)

    This model handles data for teachers and educational staff across different
    schools, levels, and position types.
    """

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    school_name = models.CharField(
        max_length=255,
        verbose_name=_("विद्यालयको नाम"),
    )
    institution_level = models.CharField(
        max_length=20,
        choices=SchoolLevelChoice.choices,
        verbose_name=_("संस्थाको तह"),
    )
    teacher_level = models.CharField(
        max_length=30,
        choices=TeacherLevelChoice.choices,
        verbose_name=_("शिक्षकको तह"),
    )
    position_type = models.CharField(
        max_length=30,
        choices=TeacherPositionTypeChoice.choices,
        verbose_name=_("पदको प्रकार"),
    )
    teacher_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("शिक्षक संख्या"),
    )

    class Meta:
        db_table = "social_ward_wise_teacher_staffing"
        verbose_name = _("वडागत शिक्षक र शैक्षिक जनशक्ति")
        verbose_name_plural = _("वडागत शिक्षक र शैक्षिक जनशक्ति")
        unique_together = [
            "ward_number",
            "school_name",
            "teacher_level",
            "position_type",
        ]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.school_name} - {self.get_teacher_level_display()}"

    @property
    def school_display_name(self):
        """Return shortened school name for display"""
        return self.school_name.replace("लुङ्ग्री-", "").replace("लुग्री-", "")


class WardWiseTeacherSummary(BaseModel):
    """Summary of teacher staffing by level and type for reporting (5.1.5)

    This model aggregates teacher counts for summary reporting and analysis.
    """

    teacher_level = models.CharField(
        max_length=30,
        choices=TeacherLevelChoice.choices,
        verbose_name=_("शिक्षकको तह"),
    )
    position_type = models.CharField(
        max_length=30,
        choices=TeacherPositionTypeChoice.choices,
        verbose_name=_("पदको प्रकार"),
    )
    total_teachers = models.PositiveIntegerField(
        default=0,
        verbose_name=_("कुल शिक्षक"),
    )

    class Meta:
        db_table = "social_ward_wise_teacher_summary"
        verbose_name = _("शिक्षक र शैक्षिक जनशक्ति सारांश")
        verbose_name_plural = _("शिक्षक र शैक्षिक जनशक्ति सारांश")
        unique_together = ["teacher_level", "position_type"]

    def __str__(self):
        return f"{self.get_teacher_level_display()} - {self.get_position_type_display()}: {self.total_teachers}"
