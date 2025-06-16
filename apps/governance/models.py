"""
Governance models for Lungri Rural Municipality Digital Profile

This module contains models related to organizational structure, human resources,
service delivery, civil organizations, and policies as specified in Chapter 8
of the report structure.
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


# Governance Enums
class PositionTypeChoice(models.TextChoices):
    """Position types in local government"""

    MAYOR = "MAYOR", _("मेयर/अध्यक्ष")
    DEPUTY_MAYOR = "DEPUTY_MAYOR", _("उपमेयर/उपाध्यक्ष")
    WARD_CHAIRPERSON = "WARD_CHAIRPERSON", _("वडा अध्यक्ष")
    WARD_MEMBER = "WARD_MEMBER", _("वडा सदस्य")
    DALIT_WOMAN_MEMBER = "DALIT_WOMAN_MEMBER", _("दलित महिला सदस्य")
    WOMAN_MEMBER = "WOMAN_MEMBER", _("महिला सदस्य")


class EmployeeTypeChoice(models.TextChoices):
    """Employee types"""

    PERMANENT = "PERMANENT", _("स्थायी")
    TEMPORARY = "TEMPORARY", _("अस्थायी")
    CONTRACT = "CONTRACT", _("करार")
    VOLUNTEER = "VOLUNTEER", _("स्वयंसेवक")


class ServiceTypeChoice(models.TextChoices):
    """Service types provided by municipality"""

    BIRTH_REGISTRATION = "BIRTH_REGISTRATION", _("जन्म दर्ता")
    DEATH_REGISTRATION = "DEATH_REGISTRATION", _("मृत्यु दर्ता")
    MARRIAGE_REGISTRATION = "MARRIAGE_REGISTRATION", _("विवाह दर्ता")
    CITIZENSHIP = "CITIZENSHIP", _("नागरिकता")
    RECOMMENDATION = "RECOMMENDATION", _("सिफारिस")
    BUSINESS_REGISTRATION = "BUSINESS_REGISTRATION", _("व्यवसाय दर्ता")
    LAND_REVENUE = "LAND_REVENUE", _("मालपोत")
    TAX_COLLECTION = "TAX_COLLECTION", _("कर संकलन")
    BUILDING_PERMIT = "BUILDING_PERMIT", _("भवन निर्माण अनुमति")
    SOCIAL_SECURITY = "SOCIAL_SECURITY", _("सामाजिक सुरक्षा")


class OrganizationTypeChoice(models.TextChoices):
    """Civil organization types"""

    CBO = "CBO", _("सामुदायिक संस्था")
    NGO = "NGO", _("गैरसरकारी संस्था")
    INGO = "INGO", _("अन्तर्राष्ट्रिय गैरसरकारी संस्था")
    COOPERATIVE = "COOPERATIVE", _("सहकारी संस्था")
    USER_GROUP = "USER_GROUP", _("उपभोक्ता समूह")
    WOMEN_GROUP = "WOMEN_GROUP", _("महिला समूह")
    YOUTH_CLUB = "YOUTH_CLUB", _("युवा क्लब")
    FARMERS_GROUP = "FARMERS_GROUP", _("कृषक समूह")
    MOTHERS_GROUP = "MOTHERS_GROUP", _("आमा समूह")


class PolicyTypeChoice(models.TextChoices):
    """Policy and regulation types"""

    ACT = "ACT", _("ऐन")
    POLICY = "POLICY", _("नीति")
    REGULATION = "REGULATION", _("नियम")
    GUIDELINE = "GUIDELINE", _("निर्देशिका")
    STANDARD = "STANDARD", _("मापदण्ड")
    PROCEDURE = "PROCEDURE", _("कार्यविधि")


# Organizational Structure Models
class ElectedRepresentative(BaseModel):
    """Elected representatives of the municipality"""

    name = models.CharField(max_length=100, verbose_name=_("नाम"))
    name_nepali = models.CharField(
        max_length=100, blank=True, verbose_name=_("नाम (नेपाली)")
    )
    position = models.CharField(
        max_length=30, choices=PositionTypeChoice.choices, verbose_name=_("पद")
    )
    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        null=True,
        blank=True,
        verbose_name=_("वडा नं."),
    )
    political_party = models.CharField(
        max_length=100, blank=True, verbose_name=_("राजनीतिक दल")
    )
    election_year = models.PositiveIntegerField(verbose_name=_("निर्वाचन वर्ष"))
    term_start_date = models.DateField(verbose_name=_("कार्यकाल सुरु मिति"))
    term_end_date = models.DateField(verbose_name=_("कार्यकाल अन्त्य मिति"))
    education_level = models.CharField(
        max_length=50, blank=True, verbose_name=_("शिक्षा स्तर")
    )
    contact_number = models.CharField(
        max_length=20, blank=True, verbose_name=_("सम्पर्क नम्बर")
    )
    email = models.EmailField(blank=True, verbose_name=_("इमेल"))

    class Meta:
        verbose_name = _("निर्वाचित प्रतिनिधि")
        verbose_name_plural = _("निर्वाचित प्रतिनिधिहरू")

    def __str__(self):
        if self.ward_number:
            return (
                f"{self.name} - {self.get_position_display()} - वडा {self.ward_number}"
            )
        return f"{self.name} - {self.get_position_display()}"


class MunicipalityEmployee(BaseModel):
    """Municipality employees and staff"""

    name = models.CharField(max_length=100, verbose_name=_("नाम"))
    name_nepali = models.CharField(
        max_length=100, blank=True, verbose_name=_("नाम (नेपाली)")
    )
    employee_id = models.CharField(
        max_length=20, unique=True, verbose_name=_("कर्मचारी नं.")
    )
    position = models.CharField(max_length=100, verbose_name=_("पद"))
    department = models.CharField(max_length=100, verbose_name=_("विभाग"))
    employee_type = models.CharField(
        max_length=20,
        choices=EmployeeTypeChoice.choices,
        verbose_name=_("कर्मचारी प्रकार"),
    )
    service_level = models.CharField(
        max_length=50, blank=True, verbose_name=_("सेवा स्तर")
    )
    education_level = models.CharField(
        max_length=50, blank=True, verbose_name=_("शिक्षा स्तर")
    )
    joining_date = models.DateField(verbose_name=_("भर्ना मिति"))
    is_active = models.BooleanField(default=True, verbose_name=_("सक्रिय छ"))
    contact_number = models.CharField(
        max_length=20, blank=True, verbose_name=_("सम्पर्क नम्बर")
    )

    class Meta:
        verbose_name = _("नगरपालिका कर्मचारी")
        verbose_name_plural = _("नगरपालिका कर्मचारीहरू")

    def __str__(self):
        return f"{self.name} - {self.position}"


class DepartmentalStructure(BaseModel):
    """Departmental structure and organization"""

    department_name = models.CharField(max_length=100, verbose_name=_("विभागको नाम"))
    department_name_nepali = models.CharField(
        max_length=100, blank=True, verbose_name=_("विभागको नाम (नेपाली)")
    )
    head_position = models.CharField(max_length=100, verbose_name=_("प्रमुखको पद"))
    total_employees = models.PositiveIntegerField(
        default=0, verbose_name=_("कुल कर्मचारी")
    )
    permanent_employees = models.PositiveIntegerField(
        default=0, verbose_name=_("स्थायी कर्मचारी")
    )
    temporary_employees = models.PositiveIntegerField(
        default=0, verbose_name=_("अस्थायी कर्मचारी")
    )
    contract_employees = models.PositiveIntegerField(
        default=0, verbose_name=_("करार कर्मचारी")
    )
    main_functions = models.TextField(blank=True, verbose_name=_("मुख्य कार्यहरू"))
    established_year = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("स्थापना वर्ष")
    )

    class Meta:
        verbose_name = _("विभागीय संरचना")
        verbose_name_plural = _("विभागीय संरचनाहरू")

    def __str__(self):
        return f"{self.department_name}"


# Service Delivery Models
class ServiceDelivery(BaseModel):
    """Services provided by the municipality"""

    service_name = models.CharField(max_length=100, verbose_name=_("सेवाको नाम"))
    service_name_nepali = models.CharField(
        max_length=100, blank=True, verbose_name=_("सेवाको नाम (नेपाली)")
    )
    service_type = models.CharField(
        max_length=30, choices=ServiceTypeChoice.choices, verbose_name=_("सेवाको प्रकार")
    )
    responsible_department = models.ForeignKey(
        DepartmentalStructure, on_delete=models.CASCADE, verbose_name=_("जिम्मेवार विभाग")
    )
    service_fee_npr = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00, verbose_name=_("सेवा शुल्क (रुपैयाँ)")
    )
    processing_time_days = models.PositiveIntegerField(
        default=1, verbose_name=_("प्रक्रिया समय (दिन)")
    )
    required_documents = models.TextField(blank=True, verbose_name=_("आवश्यक कागजातहरू"))
    service_procedure = models.TextField(blank=True, verbose_name=_("सेवा प्रक्रिया"))
    is_online_available = models.BooleanField(
        default=False, verbose_name=_("अनलाइन उपलब्ध छ")
    )
    monthly_service_count = models.PositiveIntegerField(
        default=0, verbose_name=_("मासिक सेवा संख्या")
    )

    class Meta:
        verbose_name = _("सेवा प्रवाह")
        verbose_name_plural = _("सेवा प्रवाहहरू")

    def __str__(self):
        return f"{self.service_name}"


class ServiceFeedback(BaseModel):
    """Citizen feedback on services"""

    service = models.ForeignKey(
        ServiceDelivery, on_delete=models.CASCADE, verbose_name=_("सेवा")
    )
    feedback_date = models.DateField(verbose_name=_("प्रतिक्रिया मिति"))
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("मूल्याङ्कन (१-५)"),
    )
    feedback_text = models.TextField(blank=True, verbose_name=_("प्रतिक्रिया"))
    citizen_ward = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        null=True,
        blank=True,
        verbose_name=_("नागरिकको वडा"),
    )
    is_complaint = models.BooleanField(default=False, verbose_name=_("गुनासो हो"))
    is_resolved = models.BooleanField(default=False, verbose_name=_("समाधान भयो"))

    class Meta:
        verbose_name = _("सेवा प्रतिक्रिया")
        verbose_name_plural = _("सेवा प्रतिक्रियाहरू")

    def __str__(self):
        return f"{self.service.service_name} - {self.rating}/5"


# Civil Organizations Models
class CivilOrganization(BaseModel):
    """Civil society organizations and NGOs"""

    name = models.CharField(max_length=200, verbose_name=_("संस्थाको नाम"))
    name_nepali = models.CharField(
        max_length=200, blank=True, verbose_name=_("संस्थाको नाम (नेपाली)")
    )
    organization_type = models.CharField(
        max_length=20,
        choices=OrganizationTypeChoice.choices,
        verbose_name=_("संस्थाको प्रकार"),
    )
    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        null=True,
        blank=True,
        verbose_name=_("वडा नं."),
    )
    registration_number = models.CharField(
        max_length=50, blank=True, verbose_name=_("दर्ता नम्बर")
    )
    registration_date = models.DateField(
        null=True, blank=True, verbose_name=_("दर्ता मिति")
    )
    total_members = models.PositiveIntegerField(default=0, verbose_name=_("कुल सदस्य"))
    male_members = models.PositiveIntegerField(default=0, verbose_name=_("पुरुष सदस्य"))
    female_members = models.PositiveIntegerField(
        default=0, verbose_name=_("महिला सदस्य")
    )
    working_areas = models.TextField(blank=True, verbose_name=_("कार्य क्षेत्रहरू"))
    annual_budget_npr = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("वार्षिक बजेट (रुपैयाँ)"),
    )
    contact_person = models.CharField(
        max_length=100, blank=True, verbose_name=_("सम्पर्क व्यक्ति")
    )
    contact_number = models.CharField(
        max_length=20, blank=True, verbose_name=_("सम्पर्क नम्बर")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("सक्रिय छ"))

    class Meta:
        verbose_name = _("नागरिक संगठन")
        verbose_name_plural = _("नागरिक संगठनहरू")

    def __str__(self):
        if self.ward_number:
            return f"{self.name} - वडा {self.ward_number}"
        return f"{self.name}"


class CommunityGroup(BaseModel):
    """Community-based groups and committees"""

    name = models.CharField(max_length=200, verbose_name=_("समूहको नाम"))
    name_nepali = models.CharField(
        max_length=200, blank=True, verbose_name=_("समूहको नाम (नेपाली)")
    )
    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    group_type = models.CharField(
        max_length=30,
        choices=[
            ("SAVINGS_GROUP", _("बचत समूह")),
            ("WATER_USER", _("पानी उपभोक्ता समूह")),
            ("FOREST_USER", _("वन उपभोक्ता समूह")),
            ("MOTHERS_GROUP", _("आमा समूह")),
            ("FARMERS_GROUP", _("कृषक समूह")),
            ("TOLE_COMMITTEE", _("टोल समिति")),
            ("SCHOOL_COMMITTEE", _("विद्यालय समिति")),
            ("HEALTH_COMMITTEE", _("स्वास्थ्य समिति")),
            ("MEDIATION_COMMITTEE", _("मेलमिलाप समिति")),
        ],
        verbose_name=_("समूहको प्रकार"),
    )
    formation_date = models.DateField(null=True, blank=True, verbose_name=_("गठन मिति"))
    total_members = models.PositiveIntegerField(default=0, verbose_name=_("कुल सदस्य"))
    male_members = models.PositiveIntegerField(default=0, verbose_name=_("पुरुष सदस्य"))
    female_members = models.PositiveIntegerField(
        default=0, verbose_name=_("महिला सदस्य")
    )
    chairperson_name = models.CharField(
        max_length=100, blank=True, verbose_name=_("अध्यक्षको नाम")
    )
    secretary_name = models.CharField(
        max_length=100, blank=True, verbose_name=_("सचिवको नाम")
    )
    main_activities = models.TextField(blank=True, verbose_name=_("मुख्य गतिविधिहरू"))
    is_active = models.BooleanField(default=True, verbose_name=_("सक्रिय छ"))

    class Meta:
        verbose_name = _("सामुदायिक समूह")
        verbose_name_plural = _("सामुदायिक समूहहरू")

    def __str__(self):
        return f"{self.name} - वडा {self.ward_number}"


# Financial Management Models
class AnnualBudget(BaseModel):
    """Annual budget and expenditure"""

    fiscal_year = models.CharField(max_length=10, verbose_name=_("आर्थिक वर्ष"))
    total_budget_npr = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name=_("कुल बजेट (रुपैयाँ)")
    )
    internal_revenue_npr = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        verbose_name=_("आन्तरिक आय (रुपैयाँ)"),
    )
    federal_grant_npr = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        verbose_name=_("संघीय अनुदान (रुपैयाँ)"),
    )
    provincial_grant_npr = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        verbose_name=_("प्रदेश अनुदान (रुपैयाँ)"),
    )
    capital_expenditure_npr = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        verbose_name=_("पूँजीगत खर्च (रुपैयाँ)"),
    )
    current_expenditure_npr = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00, verbose_name=_("चालु खर्च (रुपैयाँ)")
    )
    development_expenditure_npr = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        verbose_name=_("विकास खर्च (रुपैयाँ)"),
    )
    budget_utilization_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("बजेट उपयोग प्रतिशत"),
    )

    class Meta:
        verbose_name = _("वार्षिक बजेट")
        verbose_name_plural = _("वार्षिक बजेटहरू")
        unique_together = ["fiscal_year"]

    def __str__(self):
        return f"बजेट {self.fiscal_year}"


class MunicipalAsset(BaseModel):
    """Municipality assets and properties"""

    asset_name = models.CharField(max_length=200, verbose_name=_("सम्पत्तिको नाम"))
    asset_name_nepali = models.CharField(
        max_length=200, blank=True, verbose_name=_("सम्पत्तिको नाम (नेपाली)")
    )
    asset_type = models.CharField(
        max_length=30,
        choices=[
            ("LAND", _("जग्गा")),
            ("BUILDING", _("भवन")),
            ("VEHICLE", _("सवारी साधन")),
            ("EQUIPMENT", _("उपकरण")),
            ("MACHINERY", _("मेसिन")),
            ("FURNITURE", _("फर्निचर")),
            ("INFRASTRUCTURE", _("पूर्वाधार")),
        ],
        verbose_name=_("सम्पत्तिको प्रकार"),
    )
    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        null=True,
        blank=True,
        verbose_name=_("वडा नं."),
    )
    acquisition_date = models.DateField(
        null=True, blank=True, verbose_name=_("प्राप्ति मिति")
    )
    acquisition_value_npr = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("प्राप्ति मूल्य (रुपैयाँ)"),
    )
    current_value_npr = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("हालको मूल्य (रुपैयाँ)"),
    )
    condition = models.CharField(
        max_length=20,
        choices=[
            ("EXCELLENT", _("उत्कृष्ट")),
            ("GOOD", _("राम्रो")),
            ("FAIR", _("मध्यम")),
            ("POOR", _("खराब")),
            ("DAMAGED", _("बिग्रिएको")),
        ],
        default="GOOD",
        verbose_name=_("अवस्था"),
    )
    is_functional = models.BooleanField(
        default=True, verbose_name=_("काम गर्ने अवस्थामा छ")
    )

    class Meta:
        verbose_name = _("नगरपालिका सम्पत्ति")
        verbose_name_plural = _("नगरपालिका सम्पत्तिहरू")

    def __str__(self):
        return f"{self.asset_name}"


# Policies and Regulations Models
class PolicyRegulation(BaseModel):
    """Policies, acts, and regulations"""

    title = models.CharField(max_length=200, verbose_name=_("शीर्षक"))
    title_nepali = models.CharField(
        max_length=200, blank=True, verbose_name=_("शीर्षक (नेपाली)")
    )
    policy_type = models.CharField(
        max_length=20, choices=PolicyTypeChoice.choices, verbose_name=_("प्रकार")
    )
    approval_date = models.DateField(verbose_name=_("स्वीकृति मिति"))
    effective_date = models.DateField(null=True, blank=True, verbose_name=_("लागु मिति"))
    approval_authority = models.CharField(
        max_length=100, verbose_name=_("स्वीकृति निकाय")
    )
    objectives = models.TextField(blank=True, verbose_name=_("उद्देश्यहरू"))
    key_provisions = models.TextField(blank=True, verbose_name=_("मुख्य व्यवस्थाहरू"))
    is_active = models.BooleanField(default=True, verbose_name=_("लागु छ"))
    amendment_count = models.PositiveIntegerField(
        default=0, verbose_name=_("संशोधन संख्या")
    )
    last_amendment_date = models.DateField(
        null=True, blank=True, verbose_name=_("अन्तिम संशोधन मिति")
    )

    class Meta:
        verbose_name = _("नीति नियम")
        verbose_name_plural = _("नीति नियमहरू")

    def __str__(self):
        return f"{self.title}"


class ProjectProgram(BaseModel):
    """Major projects and programs"""

    name = models.CharField(max_length=200, verbose_name=_("आयोजनाको नाम"))
    name_nepali = models.CharField(
        max_length=200, blank=True, verbose_name=_("आयोजनाको नाम (नेपाली)")
    )
    program_type = models.CharField(
        max_length=30,
        choices=[
            ("INFRASTRUCTURE", _("पूर्वाधार")),
            ("SOCIAL", _("सामाजिक")),
            ("ECONOMIC", _("आर्थिक")),
            ("ENVIRONMENT", _("वातावरणीय")),
            ("GOVERNANCE", _("सुशासन")),
            ("DISASTER_RISK_REDUCTION", _("विपद् जोखिम न्यूनीकरण")),
            ("CAPACITY_BUILDING", _("क्षमता विकास")),
        ],
        verbose_name=_("आयोजनाको प्रकार"),
    )
    implementing_ward = models.CharField(
        max_length=50, blank=True, verbose_name=_("कार्यान्वयन वडा")
    )
    start_date = models.DateField(verbose_name=_("सुरु मिति"))
    end_date = models.DateField(null=True, blank=True, verbose_name=_("समाप्ति मिति"))
    total_budget_npr = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name=_("कुल बजेट (रुपैयाँ)")
    )
    expenditure_npr = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00, verbose_name=_("खर्च (रुपैयाँ)")
    )
    funding_source = models.CharField(
        max_length=100, blank=True, verbose_name=_("बजेटको स्रोत")
    )
    implementing_agency = models.CharField(
        max_length=100, blank=True, verbose_name=_("कार्यान्वयन निकाय")
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("PLANNING", _("योजना")),
            ("ONGOING", _("जारी")),
            ("COMPLETED", _("सम्पन्न")),
            ("SUSPENDED", _("रोकिएको")),
            ("CANCELLED", _("रद्द")),
        ],
        default="PLANNING",
        verbose_name=_("स्थिति"),
    )
    beneficiaries = models.PositiveIntegerField(
        default=0, verbose_name=_("लाभान्वित जनसंख्या")
    )
    objectives = models.TextField(blank=True, verbose_name=_("उद्देश्यहरू"))
    achievements = models.TextField(blank=True, verbose_name=_("उपलब्धिहरू"))

    class Meta:
        verbose_name = _("आयोजना कार्यक्रम")
        verbose_name_plural = _("आयोजना कार्यक्रमहरू")

    def __str__(self):
        return f"{self.name}"

    @property
    def budget_utilization_percentage(self):
        if self.total_budget_npr > 0:
            return round((self.expenditure_npr / self.total_budget_npr) * 100, 2)
        return 0
