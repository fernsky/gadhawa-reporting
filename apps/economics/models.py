"""
Economics models for Lungri Rural Municipality Digital Profile

This module contains models related to agriculture, livestock, employment, income,
cooperatives, and economic activities as specified in the SQL schema files.
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


# Common enums from Demographics app
class GenderChoice(models.TextChoices):
    MALE = "MALE", _("पुरुष")
    FEMALE = "FEMALE", _("महिला")
    OTHER = "OTHER", _("अन्य")


# Food Crop Enums (based on municipality-wide-food-crops.ts)
class FoodCropChoice(models.TextChoices):
    PADDY = "PADDY", _("धान")
    CORN = "CORN", _("मकै")
    WHEAT = "WHEAT", _("गहुँ")
    MILLET = "MILLET", _("कोदो")
    BARLEY = "BARLEY", _("जौ")
    PHAPAR = "PHAPAR", _("फापर")
    JUNELO = "JUNELO", _("जुनेलो")
    KAGUNO = "KAGUNO", _("कागुनो")
    OTHER = "OTHER", _("अन्य")


# Pulse Enums (based on municipality-wide-pulses.ts)
class PulseChoice(models.TextChoices):
    LENTIL = "LENTIL", _("मसुरो")
    CHICKPEA = "CHICKPEA", _("चना")
    PEA = "PEA", _("केराउ")
    PIGEON_PEA = "PIGEON_PEA", _("रहर")
    BLACK_GRAM = "BLACK_GRAM", _("मास")
    SOYABEAN = "SOYABEAN", _("भटमास")
    SNAKE_BEAN = "SNAKE_BEAN", _("बोडी")
    BEAN = "BEAN", _("सिमी")
    HORSE_GRAM = "HORSE_GRAM", _("गहत")
    OTHER = "OTHER", _("अन्य")
    NONE = "NONE", _("छैन")


# Oil Seed Enums (based on municipality-wide-oil-seeds.ts)
class OilSeedChoice(models.TextChoices):
    MUSTARD = "MUSTARD", _("तोरी/सरसोँ")
    FLAX = "FLAX", _("तिसी")
    SUNFLOWER = "SUNFLOWER", _("सूर्यमुखी")
    OTHER = "OTHER", _("अन्य")
    NONE = "NONE", _("छैन")


# Spice Enums (based on municipality-wide-spices.ts)
class SpiceChoice(models.TextChoices):
    GARLIC = "GARLIC", _("लसुन")
    TURMERIC = "TURMERIC", _("बेसार")
    CHILI_PEPPER = "CHILI_PEPPER", _("खुर्सानी")
    GINGER = "GINGER", _("अदुवा")
    CORIANDER = "CORIANDER", _("धनिया")
    SICHUAN_PEPPER = "SICHUAN_PEPPER", _("टिमुर")
    BLACK_PEPPER = "BLACK_PEPPER", _("मरिच")
    CINNAMOMUM_TAMALA = "CINNAMOMUM_TAMALA", _("तेजपात")
    CUMIN = "CUMIN", _("जीरा")
    FENUGREEK = "FENUGREEK", _("मेथी")
    OTHER = "OTHER", _("अन्य")
    NONE = "NONE", _("छैन")


# Vegetable Enums (based on municipality-wide-vegetables.ts)
class VegetableChoice(models.TextChoices):
    POTATO = "POTATO", _("आलु")
    CAULIFLOWER = "CAULIFLOWER", _("काउली")
    CABBAGE = "CABBAGE", _("बन्दाकोपी")
    TOMATO = "TOMATO", _("गोलभेडा")
    RADISH = "RADISH", _("मुला")
    CARROT = "CARROT", _("गाजर")
    TURNIP = "TURNIP", _("सल्गम")
    CAPSICUM = "CAPSICUM", _("भेडेखुर्सानी")
    OKRA = "OKRA", _("भिन्डी")
    BRINJAL = "BRINJAL", _("भन्टा")
    ONION = "ONION", _("प्याज")
    STRING_BEAN = "STRING_BEAN", _("सिमी")
    RED_KIDNEY_BEAN = "RED_KIDNEY_BEAN", _("राजमा")
    CUCUMBER = "CUCUMBER", _("काकरो")
    PUMPKIN = "PUMPKIN", _("फर्सी")
    BITTER_GOURD = "BITTER_GOURD", _("करेला")
    LUFFA = "LUFFA", _("घिरौला")
    SNAKE_GOURD = "SNAKE_GOURD", _("चिचिण्डो")
    CALABASH = "CALABASH", _("लौका")
    BALSAM_APPLE = "BALSAM_APPLE", _("तिते करेला")
    MUSHROOM = "MUSHROOM", _("च्याउ")
    SQUICE = "SQUICE", _("इस्कुस")
    MUSTARD_GREENS = "MUSTARD_GREENS", _("रायो साग")
    GARDEN_CRESS = "GARDEN_CRESS", _("चमसुर")
    SPINACH = "SPINACH", _("पालुङ्गो")
    COLOCASIA = "COLOCASIA", _("तारो")
    YAM = "YAM", _("बन तारो")
    OTHER = "OTHER", _("अन्य")
    NONE = "NONE", _("छैन")


# Fruit Enums (based on municipality-wide-fruits.ts)
class FruitChoice(models.TextChoices):
    MANGO = "MANGO", _("आँप")
    JACKFRUIT = "JACKFRUIT", _("रुख कटहर")
    LITCHI = "LITCHI", _("लीची")
    BANANA = "BANANA", _("केरा")
    LEMON = "LEMON", _("कागती")
    ORANGE = "ORANGE", _("सुन्तला")
    NIBUWA = "NIBUWA", _("निबुवा")
    SWEET_ORANGE = "SWEET_ORANGE", _("मिठो सुन्तला")
    SWEET_LEMON = "SWEET_LEMON", _("मिठो कागती")
    JYAMIR = "JYAMIR", _("ज्यामिर")
    POMELO = "POMELO", _("भोगटे")
    PINEAPPLE = "PINEAPPLE", _("भुइंकटहर")
    PAPAYA = "PAPAYA", _("मेवा")
    AVOCADO = "AVOCADO", _("घिउ")
    KIWI = "KIWI", _("किवी")
    GUAVA = "GUAVA", _("अम्बा")
    PLUM = "PLUM", _("आलुबुखारा")
    PEACH = "PEACH", _("आरु")
    PEAR = "PEAR", _("नाशपाती")
    POMEGRANATE = "POMEGRANATE", _("दाडिम")
    WALNUT = "WALNUT", _("ओखर")
    JAPANESE_PERSIMMON = "JAPANESE_PERSIMMON", _("हरियो खुर्पानी")
    HOG_PLUM = "HOG_PLUM", _("लापसी")
    NONE = "NONE", _("छैन")


# Irrigation Source Enums (based on municipality-wide-irrigation-source.ts)
class IrrigationSourceChoice(models.TextChoices):
    LAKE_OR_RESERVOIR = "LAKE_OR_RESERVOIR", _("ताल वा जलाशय")
    IRRIGATION_CANAL = "IRRIGATION_CANAL", _("सिंचाई नहर")
    RAINWATER_COLLECTION = "RAINWATER_COLLECTION", _("वर्षाको पानी संकलन")
    ELECTRIC_LIFT_IRRIGATION = "ELECTRIC_LIFT_IRRIGATION", _("विद्युतीय लिफ्ट सिंचाई")
    CANAL = "CANAL", _("नहर")
    PUMPING_SET = "PUMPING_SET", _("पम्पिङ सेट")
    UNDERGROUND_IRRIGATION = "UNDERGROUND_IRRIGATION", _("भूमिगत सिंचाई")
    OTHER = "OTHER", _("अन्य")


# Animal Product Enums (based on municipality-wide-animal-products.ts)
class AnimalProductChoice(models.TextChoices):
    MILK = "MILK", _("दूध")
    MILK_PRODUCT = "MILK_PRODUCT", _("दुग्ध उत्पादन")
    EGG = "EGG", _("अण्डा")
    MEAT = "MEAT", _("मासु")
    OTHER = "OTHER", _("अन्य")


# Measurement Unit Enums (based on municipality-wide-animal-products.ts)
class MeasurementUnitChoice(models.TextChoices):
    TON = "TON", _("टन")
    KG = "KG", _("केजी")
    COUNT = "COUNT", _("संख्या")
    LITER = "LITER", _("लिटर")
    OTHER = "OTHER", _("अन्य")


# Business Type Enums (based on municipality-wide-commercial-agricultural-animal-husbandry-farmers-group.ts)
class BusinessTypeChoice(models.TextChoices):
    VEGETABLE_FARMING = "VEGETABLE_FARMING", _("तरकारी खेती")
    GOAT_FARMING = "GOAT_FARMING", _("बाख्रा पालन")
    POULTRY_FARMING = "POULTRY_FARMING", _("कुखुरा पालन")
    FISH_FARMING = "FISH_FARMING", _("माछा पालन")
    CATTLE_FARMING = "CATTLE_FARMING", _("गाई पालन")
    ANIMAL_HUSBANDRY = "ANIMAL_HUSBANDRY", _("पशुपालन")
    LIVESTOCK_POULTRY = "LIVESTOCK_POULTRY", _("पशुपन्छी पालन")
    BEEKEEPING = "BEEKEEPING", _("मौरी पालन")
    FRUIT_FARMING = "FRUIT_FARMING", _("फलफूल खेती")
    MUSHROOM_FARMING = "MUSHROOM_FARMING", _("च्याउ खेती")
    PIG_FARMING = "PIG_FARMING", _("सुंगुर पालन")
    NURSERY = "NURSERY", _("नर्सरी")
    DAIRY_FARMING = "DAIRY_FARMING", _("दुग्ध उत्पादन")
    MIXED_FARMING = "MIXED_FARMING", _("मिश्रित खेती")
    AGRICULTURE = "AGRICULTURE", _("कृषि")
    ORGANIC_FARMING = "ORGANIC_FARMING", _("जैविक खेती")
    OTHER = "OTHER", _("अन्य")


# Crop Type for diseases (based on municipality-wide-crop-diseases.ts)
class CropTypeChoice(models.TextChoices):
    RICE = "RICE", _("धान")
    WHEAT = "WHEAT", _("गहुँ")
    CORN = "CORN", _("मकै")
    VEGETABLES = "VEGETABLES", _("तरकारी")
    FRUITS = "FRUITS", _("फलफूल")
    OTHER = "OTHER", _("अन्य")


# Vegetable/Fruit for diseases (based on municipality-wide-vegetables-and-fruits-diseases.ts)
class VegetableFruitDiseaseChoice(models.TextChoices):
    TOMATO = "TOMATO", _("गोलभेडा")
    CAULIFLOWER = "CAULIFLOWER", _("काउली")
    CABBAGE = "CABBAGE", _("बन्दाकोपी")
    POTATO = "POTATO", _("आलु")
    MUSTARD = "MUSTARD", _("तोरी")
    OTHER = "OTHER", _("अन्य")


# Economically Active Age Groups (based on ward-age-gender-wise-economically-active-population.ts)
class EconomicallyActiveAgeGroupChoice(models.TextChoices):
    AGE_0_TO_14 = "AGE_0_TO_14", _("०-१४ वर्ष")
    AGE_15_TO_59 = "AGE_15_TO_59", _("१५-५९ वर्ष")
    AGE_60_PLUS = "AGE_60_PLUS", _("६० वर्षभन्दा माथि")


# Time Spent on Household Chores (based on ward-time-wise-household-chores.ts)
class TimeSpentChoice(models.TextChoices):
    LESS_THAN_1_HOUR = "LESS_THAN_1_HOUR", _("१ घण्टाभन्दा कम")
    HOURS_1_TO_3 = "HOURS_1_TO_3", _("१-३ घण्टा")
    HOURS_4_TO_6 = "HOURS_4_TO_6", _("४-६ घण्टा")
    HOURS_7_TO_9 = "HOURS_7_TO_9", _("७-९ घण्टा")
    HOURS_10_TO_12 = "HOURS_10_TO_12", _("१०-१२ घण्टा")
    MORE_THAN_12_HOURS = "MORE_THAN_12_HOURS", _("१२ घण्टाभन्दा बढी")


# Months Sustained by Annual Income (based on ward-wise-annual-income-sustenance.ts)
class MonthsSustainedChoice(models.TextChoices):
    UPTO_THREE_MONTHS = "UPTO_THREE_MONTHS", _("३ महिना सम्म")
    THREE_TO_SIX_MONTHS = "THREE_TO_SIX_MONTHS", _("३ देखि ६ महिना")
    SIX_TO_NINE_MONTHS = "SIX_TO_NINE_MONTHS", _("६ देखि ९ महिना")
    TWELVE_MONTHS = "TWELVE_MONTHS", _("१२ महिना")


# Financial Account Types (based on ward-wise-financial-accounts.ts)
class FinancialAccountTypeChoice(models.TextChoices):
    BANK = "BANK", _("बैंक")
    FINANCE = "FINANCE", _("वित्त")
    MICRO_FINANCE = "MICRO_FINANCE", _("साना वित्त")
    COOPERATIVE = "COOPERATIVE", _("सहकारी")
    NONE = "NONE", _("छैन")


# House Ownership Types (based on ward-wise-house-ownership.ts)
class HouseOwnershipTypeChoice(models.TextChoices):
    PRIVATE = "PRIVATE", _("निजी")
    RENT = "RENT", _("भाडा")
    INSTITUTIONAL = "INSTITUTIONAL", _("संस्थागत")
    OTHER = "OTHER", _("अन्य")


# Household Base Types (based on ward-wise-household-base.ts)
class HouseholdBaseTypeChoice(models.TextChoices):
    CONCRETE_PILLAR = "CONCRETE_PILLAR", _("कंक्रिट स्तम्भ")
    CEMENT_JOINED = "CEMENT_JOINED", _("सिमेन्ट जोडिएको")
    MUD_JOINED = "MUD_JOINED", _("माटो जोडिएको")
    WOOD_POLE = "WOOD_POLE", _("काठको खाम्बा")
    OTHER = "OTHER", _("अन्य")


# Income Source Types (based on ward-wise-household-income-source.ts)
class IncomeSourceTypeChoice(models.TextChoices):
    JOB = "JOB", _("जागिर")
    AGRICULTURE = "AGRICULTURE", _("कृषि")
    BUSINESS = "BUSINESS", _("व्यापार")
    INDUSTRY = "INDUSTRY", _("उद्योग")
    FOREIGN_EMPLOYMENT = "FOREIGN_EMPLOYMENT", _("वैदेशिक रोजगार")
    LABOUR = "LABOUR", _("श्रम")
    OTHER = "OTHER", _("अन्य")


# Outer Wall Types (based on ward-wise-household-outer-wall.ts)
class OuterWallTypeChoice(models.TextChoices):
    CEMENT_JOINED = "CEMENT_JOINED", _("सिमेन्ट जोडिएको")
    UNBAKED_BRICK = "UNBAKED_BRICK", _("काच्ची इँट")
    MUD_JOINED = "MUD_JOINED", _("माटो जोडिएको")
    TIN = "TIN", _("पाता")
    BAMBOO = "BAMBOO", _("बाँस")
    WOOD = "WOOD", _("काठ")
    PREFAB = "PREFAB", _("प्रिफ्याब")
    OTHER = "OTHER", _("अन्य")


# Land Ownership Types (based on ward-wise-land-ownership.ts)
class LandOwnershipTypeChoice(models.TextChoices):
    PRIVATE = "PRIVATE", _("निजी")
    GUTHI = "GUTHI", _("गुठी")
    PUBLIC_EILANI = "PUBLIC_EILANI", _("सार्वजनिक ऐलानी")
    VILLAGE_BLOCK = "VILLAGE_BLOCK", _("गाउँ ब्लक")
    OTHER = "OTHER", _("अन्य")


# Loan Use Types (based on ward-wise-households-loan-use.ts)
class LoanUseTypeChoice(models.TextChoices):
    AGRICULTURE = "AGRICULTURE", _("कृषि")
    BUSINESS = "BUSINESS", _("व्यापार")
    HOUSEHOLD_EXPENSES = "HOUSEHOLD_EXPENSES", _("घरेलु खर्च")
    FOREIGN_EMPLOYMENT = "FOREIGN_EMPLOYMENT", _("वैदेशिक रोजगार")
    EDUCATION = "EDUCATION", _("शिक्षा")
    HEALTH_TREATMENT = "HEALTH_TREATMENT", _("स्वास्थ्य उपचार")
    HOME_CONSTRUCTION = "HOME_CONSTRUCTION", _("घर निर्माण")
    VEHICLE_PURCHASE = "VEHICLE_PURCHASE", _("सवारीसाधन खरिद")
    CEREMONY = "CEREMONY", _("समारोह")
    OTHER = "OTHER", _("अन्य")


# Major Skills (based on ward-wise-major-skills.ts)
class SkillTypeChoice(models.TextChoices):
    TEACHING_RELATED = "TEACHING_RELATED", _("शिक्षण सम्बन्धी")
    PHOTOGRAPHY_RELATED = "PHOTOGRAPHY_RELATED", _("फोटोग्राफी सम्बन्धी")
    HANDICRAFT_RELATED = "HANDICRAFT_RELATED", _("हस्तकला सम्बन्धी")
    MUSIC_DRAMA_RELATED = "MUSIC_DRAMA_RELATED", _("संगीत नाटक सम्बन्धी")
    STONEWORK_WOODWORK = "STONEWORK_WOODWORK", _("ढुंगा काठको काम")
    CARPENTERY_RELATED = "CARPENTERY_RELATED", _("सिकर्मी सम्बन्धी")
    PLUMBING = "PLUMBING", _("प्लम्बिंग")
    HUMAN_HEALTH_RELATED = "HUMAN_HEALTH_RELATED", _("मानव स्वास्थ्य सम्बन्धी")
    ANIMAL_HEALTH_RELATED = "ANIMAL_HEALTH_RELATED", _("पशु स्वास्थ्य सम्बन्धी")
    ELECTRICITY_INSTALLMENT_RELATED = "ELECTRICITY_INSTALLMENT_RELATED", _(
        "बिजुली जडान सम्बन्धी"
    )
    HOTEL_RESTAURANT_RELATED = "HOTEL_RESTAURANT_RELATED", _("होटल रेष्टुरेन्ट सम्बन्धी")
    AGRICULTURE_RELATED = "AGRICULTURE_RELATED", _("कृषि सम्बन्धी")
    PRINTING_RELATED = "PRINTING_RELATED", _("छपाई सम्बन्धी")
    DRIVING_RELATED = "DRIVING_RELATED", _("ड्राइभिंग सम्बन्धी")
    MECHANICS_RELATED = "MECHANICS_RELATED", _("मेकानिक्स सम्बन्धी")
    FURNITURE_RELATED = "FURNITURE_RELATED", _("फर्निचर सम्बन्धी")
    SHOEMAKING_RELATED = "SHOEMAKING_RELATED", _("जुत्ता बनाउने सम्बन्धी")
    SEWING_RELATED = "SEWING_RELATED", _("सिलाई सम्बन्धी")
    JWELLERY_MAKING_RELATED = "JWELLERY_MAKING_RELATED", _("गहना बनाउने सम्बन्धी")
    BEUATICIAN_RELATED = "BEUATICIAN_RELATED", _("सौन्दर्य सम्बन्धी")
    SELF_PROTECTION_RELATED = "SELF_PROTECTION_RELATED", _("आत्मरक्षा सम्बन्धी")
    LAND_SURVEY_RELATED = "LAND_SURVEY_RELATED", _("जमिन सर्वेक्षण सम्बन्धी")
    COMPUTER_SCIENCE_RELATED = "COMPUTER_SCIENCE_RELATED", _("कम्प्युटर विज्ञान सम्बन्धी")
    ENGINEERING_DESIGN_RELATED = "ENGINEERING_DESIGN_RELATED", _(
        "इन्जिनियरिङ डिजाइन सम्बन्धी"
    )
    RADIO_TELEVISION_ELECTRICAL_REPAIR = "RADIO_TELEVISION_ELECTRICAL_REPAIR", _(
        "रेडियो टेलिभिजन विद्युतीय मर्मत"
    )
    LITERARY_CREATION_RELATED = "LITERARY_CREATION_RELATED", _("साहित्यिक सृजना सम्बन्धी")
    OTHER = "OTHER", _("अन्य")
    NONE = "NONE", _("छैन")


# Remittance Amount Groups (based on ward-wise-remittance.ts)
class RemittanceAmountGroupChoice(models.TextChoices):
    RS_0_TO_49999 = "RS_0_TO_49999", _("० देखि ४९,९९९ रुपैयाँ")
    RS_50000_TO_99999 = "RS_50000_TO_99999", _("५०,००० देखि ९९,९९९ रुपैयाँ")
    RS_100000_TO_149999 = "RS_100000_TO_149999", _("१,००,००० देखि १,४९,९९९ रुपैयाँ")
    RS_150000_TO_199999 = "RS_150000_TO_199999", _("१,५०,००० देखि १,९९,९९९ रुपैयाँ")
    RS_200000_TO_249999 = "RS_200000_TO_249999", _("२,००,००० देखि २,४९,९९९ रुपैयाँ")
    RS_250000_TO_299999 = "RS_250000_TO_299999", _("२,५०,००० देखि २,९९,९९९ रुपैयाँ")
    RS_300000_TO_349999 = "RS_300000_TO_349999", _("३,००,००० देखि ३,४९,९९९ रुपैयाँ")
    RS_350000_TO_399999 = "RS_350000_TO_399999", _("३,५०,००० देखि ३,९९,९९९ रुपैयाँ")
    RS_400000_TO_449999 = "RS_400000_TO_449999", _("४,००,००० देखि ४,४९,९९९ रुपैयाँ")
    RS_450000_TO_499999 = "RS_450000_TO_499999", _("४,५०,००० देखि ४,९९,९९९ रुपैयाँ")
    RS_500000_PLUS = "RS_500000_PLUS", _("५,००,००० रुपैयाँभन्दा माथि")


# Remittance Expense Types (based on ward-wise-remittance-expenses.ts)
class RemittanceExpenseTypeChoice(models.TextChoices):
    EDUCATION = "education", _("शिक्षा")
    HEALTH = "health", _("स्वास्थ्य")
    HOUSEHOLD_USE = "household_use", _("घरेलु प्रयोग")
    FESTIVALS = "festivals", _("चाडपर्व")
    LOAN_PAYMENT = "loan_payment", _("ऋण भुक्तानी")
    LOANED_OTHERS = "loaned_others", _("अरुलाई ऋण")
    SAVING = "saving", _("बचत")
    HOUSE_CONSTRUCTION = "house_construction", _("घर निर्माण")
    LAND_OWNERSHIP = "land_ownership", _("जमिन स्वामित्व")
    JWELLERY_PURCHASE = "jwellery_purchase", _("गहना खरिद")
    GOODS_PURCHASE = "goods_purchase", _("सामान खरिद")
    BUSINESS_INVESTMENT = "business_investment", _("व्यापारिक लगानी")
    OTHER = "other", _("अन्य")
    UNKNOWN = "unknown", _("थाहा छैन")


# Time to Financial Organization (based on ward-wise-time-to-financial-organization.ts)
class TimeToFinancialOrganizationChoice(models.TextChoices):
    UNDER_15_MIN = "UNDER_15_MIN", _("१५ मिनेट भन्दा कम")
    UNDER_30_MIN = "UNDER_30_MIN", _("१५-३० मिनेट")
    UNDER_1_HOUR = "UNDER_1_HOUR", _("३०-६० मिनेट")
    ONE_HOUR_OR_MORE = "1_HOUR_OR_MORE", _("१ घण्टा वा बढी")
    LABOR = "LABOR", _("श्रमिक")
    WOMEN = "WOMEN", _("महिला")
    YOUTH = "YOUTH", _("युवा")


class SkillTypeChoice(models.TextChoices):
    AGRICULTURE_RELATED = "AGRICULTURE_RELATED", _("कृषि सम्बन्धी")
    LIVESTOCK_RELATED = "LIVESTOCK_RELATED", _("पशुपालन सम्बन्धी")
    CONSTRUCTION_RELATED = "CONSTRUCTION_RELATED", _("निर्माण सम्बन्धी")
    HANDICRAFT_RELATED = "HANDICRAFT_RELATED", _("हस्तकला सम्बन्धी")
    MECHANICAL_RELATED = "MECHANICAL_RELATED", _("मेकानिकल सम्बन्धी")
    ELECTRICAL_RELATED = "ELECTRICAL_RELATED", _("विद्युत सम्बन्धी")
    PLUMBING_RELATED = "PLUMBING_RELATED", _("प्लम्बिङ सम्बन्धी")
    TAILORING_RELATED = "TAILORING_RELATED", _("सिलाई सम्बन्धी")
    BEAUTY_PARLOR = "BEAUTY_PARLOR", _("सौन्दर्य पार्लर")
    DRIVING_RELATED = "DRIVING_RELATED", _("चालक सम्बन्धी")
    COMPUTER_RELATED = "COMPUTER_RELATED", _("कम्प्युटर सम्बन्धी")
    HEALTH_RELATED = "HEALTH_RELATED", _("स्वास्थ्य सम्बन्धी")
    TEACHING_RELATED = "TEACHING_RELATED", _("शिक्षण सम्बन्धी")
    OTHER = "OTHER", _("अन्य")


class LoanPurposeChoice(models.TextChoices):
    AGRICULTURE = "AGRICULTURE", _("कृषि कार्य")
    LIVESTOCK = "LIVESTOCK", _("पशुपालन")
    BUSINESS = "BUSINESS", _("व्यापार व्यवसाय")
    EDUCATION = "EDUCATION", _("शिक्षा")
    HEALTH = "HEALTH", _("स्वास्थ्य उपचार")
    HOUSE_CONSTRUCTION = "HOUSE_CONSTRUCTION", _("घर निर्माण")
    LAND_PURCHASE = "LAND_PURCHASE", _("जग्गा खरिद")
    MARRIAGE = "MARRIAGE", _("विवाह")
    FOREIGN_EMPLOYMENT = "FOREIGN_EMPLOYMENT", _("वैदेशिक रोजगारी")
    CONSUMPTION = "CONSUMPTION", _("उपभोग")
    OTHER = "OTHER", _("अन्य")


class HouseholdChoreTimeChoice(models.TextChoices):
    LESS_THAN_2_HOURS = "LESS_THAN_2_HOURS", _("२ घण्टाभन्दा कम")
    BETWEEN_2_4_HOURS = "BETWEEN_2_4_HOURS", _("२-४ घण्टा")
    BETWEEN_4_6_HOURS = "BETWEEN_4_6_HOURS", _("४-६ घण्टा")
    BETWEEN_6_8_HOURS = "BETWEEN_6_8_HOURS", _("६-८ घण्टा")
    MORE_THAN_8_HOURS = "MORE_THAN_8_HOURS", _("८ घण्टाभन्दा बढी")


class IncomeSourceChoice(models.TextChoices):
    AGRICULTURE = "AGRICULTURE", _("कृषि")
    LIVESTOCK = "LIVESTOCK", _("पशुपालन")
    WAGE_LABOR = "WAGE_LABOR", _("ज्याला मजदुरी")
    SALARIED_JOB = "SALARIED_JOB", _("तलबी जागिर")
    BUSINESS = "BUSINESS", _("व्यापार व्यवसाय")
    FOREIGN_REMITTANCE = "FOREIGN_REMITTANCE", _("वैदेशिक रेमिटेन्स")
    PENSION = "PENSION", _("निवृत्तिभरण")
    SOCIAL_SECURITY = "SOCIAL_SECURITY", _("सामाजिक सुरक्षा भत्ता")
    RENT = "RENT", _("भाडा")
    INTEREST = "INTEREST", _("ब्याज")
    OTHER = "OTHER", _("अन्य")


class AnnualIncomeSustenanceChoice(models.TextChoices):
    SUFFICIENT = "SUFFICIENT", _("पर्याप्त")
    INSUFFICIENT = "INSUFFICIENT", _("अपर्याप्त")
    BARELY_SUFFICIENT = "BARELY_SUFFICIENT", _("मुश्किल चल्छ")


class LandPossessionTypeChoice(models.TextChoices):
    OWNED = "OWNED", _("आफ्नै")
    RENTED = "RENTED", _("भाडामा लिएको")
    SHARECROPPING = "SHARECROPPING", _("अधिया/तेहिया")
    GOVERNMENT = "GOVERNMENT", _("सरकारी")
    COMMUNITY = "COMMUNITY", _("सामुदायिक")
    OTHER = "OTHER", _("अन्य")


class HouseOwnershipChoice(models.TextChoices):
    OWNED = "OWNED", _("आफ्नै")
    RENTED = "RENTED", _("भाडामा")
    FREE = "FREE", _("निःशुल्क")
    GOVERNMENT = "GOVERNMENT", _("सरकारी")
    INSTITUTIONAL = "INSTITUTIONAL", _("संस्थागत")


class TimeToFinancialOrgChoice(models.TextChoices):
    UNDER_30_MIN = "UNDER_30_MIN", _("३० मिनेटभन्दा कम")
    BETWEEN_30MIN_1HR = "BETWEEN_30MIN_1HR", _("३० मिनेट - १ घण्टा")
    BETWEEN_1_2_HOURS = "BETWEEN_1_2_HOURS", _("१-२ घण्टा")
    BETWEEN_2_3_HOURS = "BETWEEN_2_3_HOURS", _("२-३ घण्टा")
    MORE_THAN_3_HOURS = "MORE_THAN_3_HOURS", _("३ घण्टाभन्दा बढी")


class FinancialAccountTypeChoice(models.TextChoices):
    BANK_ACCOUNT = "BANK_ACCOUNT", _("बैंक खाता")
    COOPERATIVE_ACCOUNT = "COOPERATIVE_ACCOUNT", _("सहकारी खाता")
    MICROFINANCE_ACCOUNT = "MICROFINANCE_ACCOUNT", _("लघुवित्त खाता")
    MOBILE_BANKING = "MOBILE_BANKING", _("मोबाइल बैंकिङ")
    DIGITAL_WALLET = "DIGITAL_WALLET", _("डिजिटल वालेट")
    NO_ACCOUNT = "NO_ACCOUNT", _("कुनै खाता छैन")


# =============================================================================
# MUNICIPALITY-WIDE MODELS
# =============================================================================
# ४.१ प्रमुख आर्थिक विवरण

# ४.१.१ प्राविधिक, सीपयुक्त तथा विशेष दक्षता भएका मानव संशाधनको विवरण


class WardWiseMajorSkills(BaseModel):
    """Ward wise major skills"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    skill_type = models.CharField(
        max_length=40, choices=SkillTypeChoice.choices, verbose_name=_("सीपको प्रकार")
    )
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत प्रमुख सीप")
        verbose_name_plural = _("वडागत प्रमुख सीप")
        unique_together = ["ward_number", "skill_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_skill_type_display()}"


# ४.१.३ औसत आम्दानी विवरण


class WardWiseHouseholdIncomeSource(BaseModel):
    """Ward wise household income source"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    income_source = models.CharField(
        max_length=20,
        choices=IncomeSourceTypeChoice.choices,
        verbose_name=_("आम्दानीको स्रोत"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत घरपरिवारको आम्दानीको स्रोत")
        verbose_name_plural = _("वडागत घरपरिवारको आम्दानीको स्रोत")
        unique_together = ["ward_number", "income_source"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_income_source_display()}"


# ४.१.४ औसत खर्च तथा बचत विवरण


class WardWiseFinancialAccounts(BaseModel):
    """Ward wise financial accounts"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    financial_account_type = models.CharField(
        max_length=20,
        choices=FinancialAccountTypeChoice.choices,
        verbose_name=_("वित्तीय खाताको प्रकार"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत वित्तीय खाता")
        verbose_name_plural = _("वडागत वित्तीय खाता")
        unique_together = ["ward_number", "financial_account_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_financial_account_type_display()}"


# ४.१.५ विपन्नता स्तरीकरण विवरण


# ४.१.६ खाद्यान्न सुरक्षाको अवस्था
# क) वार्षिक कृषि उत्पादनले परिवार चलाउन पुग्नेको विवरण


class WardWiseAnnualAgriculturalSustenance(BaseModel):
    """Ward wise annual agricultural sustenance"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    months_sustained = models.CharField(
        max_length=25,
        choices=MonthsSustainedChoice.choices,
        verbose_name=_("चल्ने महिना"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत वार्षिक कृषि उत्पादनको निर्वाह")
        verbose_name_plural = _("वडागत वार्षिक कृषि उत्पादनको निर्वाह")
        unique_together = ["ward_number", "months_sustained"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_months_sustained_display()}"


# ४.१.७ आवास संरचना विवरण
# क) घरको स्वामित्वको आधारमा घरधुरीको विवरण
class WardWiseHouseOwnership(BaseModel):
    """Ward wise house ownership"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    ownership_type = models.CharField(
        max_length=20,
        choices=HouseOwnershipTypeChoice.choices,
        verbose_name=_("स्वामित्वको प्रकार"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत घर स्वामित्व")
        verbose_name_plural = _("वडागत घर स्वामित्व")
        unique_together = ["ward_number", "ownership_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_ownership_type_display()}"


# ख) जगको आधारमा घरधुरीको विवरण


class WardWiseHouseholdBase(BaseModel):
    """Ward wise household base"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    base_type = models.CharField(
        max_length=20,
        choices=HouseholdBaseTypeChoice.choices,
        verbose_name=_("घरको जगको प्रकार"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत घरको जग")
        verbose_name_plural = _("वडागत घरको जग")
        unique_together = ["ward_number", "base_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_base_type_display()}"


# ग) बाहिरी गारोको आधारमा घरधुरीको विवरण


class WardWiseHouseholdOuterWall(BaseModel):
    """Ward wise household outer wall"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    wall_type = models.CharField(
        max_length=20,
        choices=OuterWallTypeChoice.choices,
        verbose_name=_("बाहिरी भित्ताको प्रकार"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत घरको बाहिरी भित्ता")
        verbose_name_plural = _("वडागत घरको बाहिरी भित्ता")
        unique_together = ["ward_number", "wall_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_wall_type_display()}"


# ४.१.८ गरिबीको दर (गरिबीको रेखामुखी रहेको जनसंख्या)
# ४.१.९ आयात र निर्यातको अवस्था
# ४.१.१० औद्योगिक कच्चा पदार्थ उत्पादनको अवस्था (काठ, खोटो, जडिबुटी, लोक्ता, अल्लो, चुनढुङ्गा, मार्वल, स्लेट आदि)
# ४.१.११ बेरोजगार सम्बन्धी विवरण

# ४.१.१२ वैदेशिक रोजगारीमा गएकाहरुको विवरण


class WardWiseForeignEmploymentCountries(BaseModel):
    """Ward wise foreign employment countries"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    country = models.CharField(max_length=100, verbose_name=_("देश"))
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत वैदेशिक रोजगार देश")
        verbose_name_plural = _("वडागत वैदेशिक रोजगार देश")
        unique_together = ["ward_number", "country"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.country}"


class WardWiseRemittance(BaseModel):
    """Ward wise remittance"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    amount_group = models.CharField(
        max_length=25,
        choices=RemittanceAmountGroupChoice.choices,
        verbose_name=_("रकम समूह"),
    )
    sending_population = models.PositiveIntegerField(
        default=0, verbose_name=_("पठाउने जनसंख्या")
    )

    class Meta:
        verbose_name = _("वडागत रेमिटेन्स")
        verbose_name_plural = _("वडागत रेमिटेन्स")
        unique_together = ["ward_number", "amount_group"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_amount_group_display()}"


# ४.१.१३ सुकुम्बासी सम्बन्धी विवरण
# ४.१.१४ स्रोत नक्शा

# ४.२ भू–उपयोग तथा स्वामित्व


class WardWiseHouseholdLandPossessions(BaseModel):
    """Ward wise household land possessions"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत घरपरिवारको जमिनको स्वामित्व")
        verbose_name_plural = _("वडागत घरपरिवारको जमिनको स्वामित्व")
        unique_together = ["ward_number"]

    def __str__(self):
        return f"वडा {self.ward_number} - जमिन स्वामित्व"


# ४.२.१ वर्तमान भू–उपयोग
# ४.२.२ भू–स्वामित्व
# ४.२.३ जग्गाको किसिम
# ४.२.४ खेतीयोग्य जमिन सम्बन्धी विवरण
# ४.२.५ बाँझो जमिन सम्बन्धी विवरण
# ४.२.६ स्रोत नक्शा

# ४.३ कृषि तथा पशु विकास
# ४.३.१ सार्वजनिक पोखरी तथा माछापालन सम्बन्धी विवरण
# ४.३.२ सिंचाइ सुविधाको उपलब्धता विवरण


class WardWiseIrrigatedArea(BaseModel):
    """Ward wise irrigated area"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    irrigated_area_hectares = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name=_("सिंचित क्षेत्रफल (हेक्टर)"),
    )
    unirrigated_area_hectares = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name=_("असिंचित क्षेत्रफल (हेक्टर)"),
    )

    class Meta:
        verbose_name = _("वडागत सिंचित क्षेत्रफल")
        verbose_name_plural = _("वडागत सिंचित क्षेत्रफल")
        unique_together = ["ward_number"]

    def __str__(self):
        return f"वडा {self.ward_number} - सिंचित: {self.irrigated_area_hectares} हेक्टर"


# ४.३.३ सिंचाइको स्रोत सम्बन्धी विवरण


class MunicipalityWideIrrigationSource(BaseModel):
    """Municipality wide irrigation source"""

    irrigation_source = models.CharField(
        max_length=30,
        choices=IrrigationSourceChoice.choices,
        verbose_name=_("सिंचाइको स्रोत"),
    )
    coverage_in_hectares = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("क्षेत्रफल (हेक्टर)")
    )

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी सिंचाइ स्रोत")
        verbose_name_plural = _("गाउँपालिका व्यापी सिंचाइ स्रोत")
        unique_together = ["irrigation_source"]

    def __str__(self):
        return (
            f"{self.get_irrigation_source_display()} - {self.coverage_in_hectares} हेक्टर"
        )


# ४.३.४ कृषि उत्पादन सम्बन्धी विवरण


class MunicipalityWideFoodCrops(BaseModel):
    """Municipality wide food crops"""

    food_crop = models.CharField(
        max_length=20, choices=FoodCropChoice.choices, verbose_name=_("खाद्यान्न बाली")
    )
    production_in_tonnes = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("उत्पादन (टन)")
    )
    sales_in_tonnes = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("बिक्री (टन)")
    )
    revenue_in_rs = models.DecimalField(
        max_digits=14, decimal_places=2, default=0.00, verbose_name=_("आम्दानी (रु.)")
    )

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी खाद्यान्न बाली")
        verbose_name_plural = _("गाउँपालिका व्यापी खाद्यान्न बाली")
        unique_together = ["food_crop"]

    def __str__(self):
        return f"{self.get_food_crop_display()} - {self.production_in_tonnes} टन"


class MunicipalityWideFruits(BaseModel):
    """Municipality wide fruits"""

    fruit_type = models.CharField(
        max_length=25, choices=FruitChoice.choices, verbose_name=_("फलफूलको प्रकार")
    )
    production_in_tonnes = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("उत्पादन (टन)")
    )
    sales_in_tonnes = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("बिक्री (टन)")
    )
    revenue_in_rs = models.DecimalField(
        max_digits=14, decimal_places=2, default=0.00, verbose_name=_("आम्दानी (रु.)")
    )

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी फलफूल")
        verbose_name_plural = _("गाउँपालिका व्यापी फलफूल")
        unique_together = ["fruit_type"]

    def __str__(self):
        return f"{self.get_fruit_type_display()} - {self.production_in_tonnes} टन"


class MunicipalityWideOilSeeds(BaseModel):
    """Municipality wide oil seeds"""

    oil_seed = models.CharField(
        max_length=20, choices=OilSeedChoice.choices, verbose_name=_("तेलहन बाली")
    )
    production_in_tonnes = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("उत्पादन (टन)")
    )
    sales_in_tonnes = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("बिक्री (टन)")
    )
    revenue_in_rs = models.DecimalField(
        max_digits=14, decimal_places=2, default=0.00, verbose_name=_("आम्दानी (रु.)")
    )

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी तेलहन बाली")
        verbose_name_plural = _("गाउँपालिका व्यापी तेलहन बाली")
        unique_together = ["oil_seed"]

    def __str__(self):
        return f"{self.get_oil_seed_display()} - {self.production_in_tonnes} टन"


class MunicipalityWidePulses(BaseModel):
    """Municipality wide pulses"""

    pulse = models.CharField(
        max_length=20, choices=PulseChoice.choices, verbose_name=_("दलहन बाली")
    )
    production_in_tonnes = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("उत्पादन (टन)")
    )
    sales_in_tonnes = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("बिक्री (टन)")
    )
    revenue_in_rs = models.DecimalField(
        max_digits=14, decimal_places=2, default=0.00, verbose_name=_("आम्दानी (रु.)")
    )

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी दलहन बाली")
        verbose_name_plural = _("गाउँपालिका व्यापी दलहन बाली")
        unique_together = ["pulse"]

    def __str__(self):
        return f"{self.get_pulse_display()} - {self.production_in_tonnes} टन"


class MunicipalityWideSpices(BaseModel):
    """Municipality wide spices"""

    spice_type = models.CharField(
        max_length=25, choices=SpiceChoice.choices, verbose_name=_("मसलाको प्रकार")
    )
    production_in_tonnes = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("उत्पादन (टन)")
    )
    sales_in_tonnes = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("बिक्री (टन)")
    )
    revenue_in_rs = models.DecimalField(
        max_digits=14, decimal_places=2, default=0.00, verbose_name=_("आम्दानी (रु.)")
    )

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी मसला")
        verbose_name_plural = _("गाउँपालिका व्यापी मसला")
        unique_together = ["spice_type"]

    def __str__(self):
        return f"{self.get_spice_type_display()} - {self.production_in_tonnes} टन"


class MunicipalityWideVegetables(BaseModel):
    """Municipality wide vegetables"""

    vegetable_type = models.CharField(
        max_length=25, choices=VegetableChoice.choices, verbose_name=_("तरकारीको प्रकार")
    )
    production_in_tonnes = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("उत्पादन (टन)")
    )
    sales_in_tonnes = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("बिक्री (टन)")
    )
    revenue_in_rs = models.DecimalField(
        max_digits=14, decimal_places=2, default=0.00, verbose_name=_("आम्दानी (रु.)")
    )

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी तरकारी")
        verbose_name_plural = _("गाउँपालिका व्यापी तरकारी")
        unique_together = ["vegetable_type"]

    def __str__(self):
        return f"{self.get_vegetable_type_display()} - {self.production_in_tonnes} टन"


# ४.३.५ पशुपन्छीजन्य उत्पादन सम्बन्धी विवरण


class MunicipalityWideAnimalProducts(BaseModel):
    """Municipality wide animal products"""

    animal_product_type = models.CharField(
        max_length=20,
        choices=AnimalProductChoice.choices,
        verbose_name=_("पशु उत्पादनको प्रकार"),
    )
    measurement_unit = models.CharField(
        max_length=10,
        choices=MeasurementUnitChoice.choices,
        verbose_name=_("मापदण्डको एकाइ"),
    )
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("मात्रा")
    )
    value_in_rs = models.DecimalField(
        max_digits=14, decimal_places=2, default=0.00, verbose_name=_("मूल्य (रु.)")
    )

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी पशु उत्पादन")
        verbose_name_plural = _("गाउँपालिका व्यापी पशु उत्पादन")
        unique_together = ["animal_product_type", "measurement_unit"]

    def __str__(self):
        return f"{self.get_animal_product_type_display()} - {self.quantity} {self.get_measurement_unit_display()}"


# ४.३.६ खाद्यान्न बालीमा लाग्ने रोग तथा कीरा


class MunicipalityWideCropDiseases(BaseModel):
    """Municipality wide crop diseases"""

    crop = models.CharField(
        max_length=20, choices=CropTypeChoice.choices, verbose_name=_("बाली")
    )
    major_pests = models.TextField(verbose_name=_("प्रमुख शत्रु जीव"))
    major_diseases = models.TextField(verbose_name=_("प्रमुख रोग"))

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी बालीको रोग")
        verbose_name_plural = _("गाउँपालिका व्यापी बालीको रोग")
        unique_together = ["crop"]

    def __str__(self):
        return f"{self.get_crop_display()} - रोग र कीरा"


# ४.३.७ फलफूल तथा तरकारीमा लाग्ने रोग तथा कीरा


class MunicipalityWideVegetablesAndFruitsDiseases(BaseModel):
    """Municipality wide vegetables and fruits diseases"""

    crop = models.CharField(
        max_length=20,
        choices=VegetableFruitDiseaseChoice.choices,
        verbose_name=_("बाली"),
    )
    major_pests = models.TextField(verbose_name=_("प्रमुख शत्रु जीव"))
    major_diseases = models.TextField(verbose_name=_("प्रमुख रोग"))

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी तरकारी र फलफूलको रोग")
        verbose_name_plural = _("गाउँपालिका व्यापी तरकारी र फलफूलको रोग")
        unique_together = ["crop"]

    def __str__(self):
        return f"{self.get_crop_display()} - रोग र कीरा"


# ४.३.८ पशुपन्छिमा लाग्ने रोग तथा कीरा


class MunicipalityWideAnimalDiseases(BaseModel):
    """Municipality wide animal diseases"""

    animal_type = models.CharField(max_length=100, verbose_name=_("पशु प्रकार"))
    major_diseases = models.TextField(verbose_name=_("प्रमुख रोगहरू"))
    major_pests = models.TextField(verbose_name=_("प्रमुख परजीवीहरू"))
    preventive_measures = models.TextField(
        verbose_name=_("रोकथामका उपायहरू"), blank=True, null=True
    )

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी पशु रोग")
        verbose_name_plural = _("गाउँपालिका व्यापी पशु रोगहरू")
        unique_together = ["animal_type"]

    def __str__(self):
        return f"{self.animal_type} - रोग र परजीवी"


# ४.३.९ व्यवसायिक कृषि फर्म सम्बन्धी विवरण


class MunicipalityWideCommercialAgriculturalAnimalHusbandryFarmersGroup(BaseModel):
    """Municipality wide commercial agricultural animal husbandry farmers group"""

    name = models.CharField(max_length=255, verbose_name=_("नाम"))
    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    type = models.CharField(
        max_length=30,
        choices=BusinessTypeChoice.choices,
        verbose_name=_("व्यापारको प्रकार"),
    )

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी व्यापारिक कृषि पशुपालन किसान समूह")
        verbose_name_plural = _("गाउँपालिका व्यापी व्यापारिक कृषि पशुपालन किसान समूह")

    def __str__(self):
        return f"{self.name} - {self.get_type_display()}"


class MunicipalityWideAgricultureRelatedFarmersGroup(BaseModel):
    """Municipality wide agriculture related farmers group"""

    name = models.CharField(max_length=255, verbose_name=_("नाम"))
    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी कृषि सम्बन्धी किसान समूह")
        verbose_name_plural = _("गाउँपालिका व्यापी कृषि सम्बन्धी किसान समूह")

    def __str__(self):
        return f"{self.name} - वडा {self.ward_number}"


# ४.३.१० आधुनिक (व्यवसायिक) पशुपालन (फार्म) सम्बन्धी विवरण
# ४.३.११ कृषि तथा पशु सेवासँग सम्बन्धित मानव संशाधन
# Position enums for agricultural experts
class AgriculturalPositionChoice(models.TextChoices):
    OFFICER_SIXTH = "OFFICER_SIXTH", _("अधिकृत छैटौ (शाखा प्रमुख)")
    TECHNICAL_ASSISTANT_FIFTH = "TECHNICAL_ASSISTANT_FIFTH", _("प्रा.स (सहायक पाँचौ)")
    TECHNICAL_ASSISTANT_FOURTH = "TECHNICAL_ASSISTANT_FOURTH", _(
        "ना.प्रा.स (सहायक चौथो)"
    )
    TECHNICAL_ASSISTANT_PROVINCE_FOURTH = "TECHNICAL_ASSISTANT_PROVINCE_FOURTH", _(
        "ना.प्रा.स (प्रदेश) (सहायक चौथो)"
    )


class MunicipalityWideAgriculturalExperts(BaseModel):
    """Municipality wide agricultural experts"""

    name = models.CharField(max_length=100, verbose_name=_("कर्मचारीको नाम"))
    position = models.CharField(
        max_length=40, choices=AgriculturalPositionChoice.choices, verbose_name=_("पद")
    )
    contact_number = models.CharField(max_length=20, verbose_name=_("सम्पर्क न."))

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी कृषि विज्ञ")
        verbose_name_plural = _("गाउँपालिका व्यापी कृषि विज्ञ")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.get_position_display()}"


# ४.३.१२ कृषि तथा पशुपालनसँग सम्बन्धित समूह तथा सामुदायिक संस्थाको विवरण
# ४.३.१३ संकलन केन्द्र तथा चिस्यान केन्द्र
# ४.३.१४ कृषि बजार तथा हाटबजार सम्बन्धी विवरण
# ४.३.१५ स्रोत नक्शा


# ४.४ पर्यटन विकास
# ४.४.१ पर्यटकीय स्थलहरुको विवरण
class TouristicSite(BaseModel):
    """Tourist attraction sites in the municipality"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    name = models.CharField(max_length=255, verbose_name=_("नाम"))

    class SignificanceTypeChoice(models.TextChoices):
        TOURISTIC_RELIGIOUS = "TOURISTIC_RELIGIOUS", _("पर्यटकीय तथा धार्मिक")
        TOURISTIC_RELIGIOUS_SCENIC = "TOURISTIC_RELIGIOUS_SCENIC", _(
            "पर्यटकीय तथा धार्मिक, दृश्यावलोकन"
        )
        TOURISTIC = "TOURISTIC", _("पर्यटकीय")
        RELIGIOUS = "RELIGIOUS", _("धार्मिक")
        SCENIC = "SCENIC", _("दृश्यावलोकन")
        OTHER = "OTHER", _("अन्य")

    significance_type = models.CharField(
        max_length=30,
        choices=SignificanceTypeChoice.choices,
        verbose_name=_("महत्त्व प्रकार"),
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("विवरण"))

    class Meta:
        verbose_name = _("पर्यटकीय स्थल")
        verbose_name_plural = _("पर्यटकीय स्थलहरू")
        ordering = ["ward_number", "name"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.name}"


# ४.४.२ होटल, रिसोर्ट तथा रेष्टुरेन्ट सम्बन्धी विवरण
# ४.४.३ उपलब्ध पर्यटकीय सेवा तथा सुविधा सम्बन्धी विवरण
# ४.४.४ धार्मिक, ऐतिहासिक तथा पर्यटकीय स्थल सम्बन्धी विवरण
# ४.४.५ होटेल, रिसोर्ट तथा होमस्टे सम्बन्धी विवरण
# ४.४.६ स्रोत नक्शा

# ४.५ उद्योग, व्यापार तथा वैंकिङ्ग
# ४.५.१ औद्योगिक विकास (लघु, घरेलु, साना, मझौला, ठूला उद्योग, सरकारी, पब्लिक, निजी र सहकारी)
# ४.५.२ उत्पादन तथा सेवामूलक उद्योग सम्बन्धी विवरण
# ४.५.३ घट्ट, मिल तथा संकलन र प्रशोधन सम्बन्धी विवरण
# ४.५.४ व्यापार र व्यवसाय सम्बन्धी विवरण (किराना, थोक, मासु, तरकारी र फलफूल आदि)
# ४.५.५ खनिज तथा खानी सम्बन्धी विवरण
# ४.५.६ स्थानीय बजार तथा व्यापारिक केन्द्रको विवरण


# ४.५.८ सहकारी सम्बन्धी विवरण
class CooperativeTypeChoice(models.TextChoices):
    AGRICULTURE = "AGRICULTURE", _("कृषि")
    MULTIPURPOSE = "MULTIPURPOSE", _("बहुउद्देश्यीय")
    WOMEN = "WOMEN", _("महिला")
    SOCIAL_ENTREPRENEURSHIP = "SOCIAL_ENTREPRENEURSHIP", _("सामाजिक उद्यमी")
    OTHER = "OTHER", _("अन्य")


class MunicipalityWideCooperatives(BaseModel):
    """Municipality wide cooperatives information"""

    name = models.CharField(max_length=255, verbose_name=_("नाम"))
    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
        null=True,
        blank=True,
    )
    cooperative_type = models.CharField(
        max_length=30,
        choices=CooperativeTypeChoice.choices,
        verbose_name=_("सहकारी प्रकार"),
        default=CooperativeTypeChoice.AGRICULTURE,
    )
    address = models.CharField(max_length=255, verbose_name=_("ठेगाना"), blank=True)

    class Meta:
        verbose_name = _("गाउँपालिका व्यापी सहकारी")
        verbose_name_plural = _("गाउँपालिका व्यापी सहकारीहरू")
        ordering = ["ward_number", "name"]

    def __str__(self):
        ward_str = f"वडा {self.ward_number}" if self.ward_number else "अन्य"
        return f"{self.name} - {ward_str}"


# ४.५.९ स्रोत नक्शा


# =============================================================================
# WARD-WISE MODELS
# =============================================================================


class WardAgeGenderWiseEconomicallyActivePopulation(BaseModel):
    """Ward age gender wise economically active population"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    age_group = models.CharField(
        max_length=20,
        choices=EconomicallyActiveAgeGroupChoice.choices,
        verbose_name=_("उमेर समूह"),
    )
    gender = models.CharField(
        max_length=10, choices=GenderChoice.choices, verbose_name=_("लिंग")
    )
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत उमेर लिंग अनुसार आर्थिक रूपमा सक्रिय जनसंख्या")
        verbose_name_plural = _("वडागत उमेर लिंग अनुसार आर्थिक रूपमा सक्रिय जनसंख्या")
        unique_together = ["ward_number", "age_group", "gender"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_age_group_display()} - {self.get_gender_display()}"


class WardTimeWiseHouseholdChores(BaseModel):
    """Ward time wise household chores"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    time_spent = models.CharField(
        max_length=20, choices=TimeSpentChoice.choices, verbose_name=_("समय व्यतीत")
    )
    population = models.PositiveIntegerField(default=0, verbose_name=_("जनसंख्या"))

    class Meta:
        verbose_name = _("वडागत समय अनुसार घरेलु काम")
        verbose_name_plural = _("वडागत समय अनुसार घरेलु काम")
        unique_together = ["ward_number", "time_spent"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_time_spent_display()}"


class WardWiseHouseholdsInAgriculture(BaseModel):
    """Ward wise households in agriculture"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    involved_in_agriculture = models.PositiveIntegerField(
        default=0, verbose_name=_("कृषिमा संलग्न घरपरिवार")
    )
    non_involved_in_agriculture = models.PositiveIntegerField(
        default=0, verbose_name=_("कृषिमा संलग्न नभएका घरपरिवार")
    )

    class Meta:
        verbose_name = _("वडागत कृषिमा संलग्न घरपरिवार")
        verbose_name_plural = _("वडागत कृषिमा संलग्न घरपरिवार")
        unique_together = ["ward_number"]

    def __str__(self):
        return f"वडा {self.ward_number} - कृषि संलग्नता"


class WardWiseHouseholdsLoanUse(BaseModel):
    """Ward wise households loan use"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    loan_use = models.CharField(
        max_length=25, choices=LoanUseTypeChoice.choices, verbose_name=_("ऋणको प्रयोग")
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत घरपरिवारको ऋणको प्रयोग")
        verbose_name_plural = _("वडागत घरपरिवारको ऋणको प्रयोग")
        unique_together = ["ward_number", "loan_use"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_loan_use_display()}"


class WardWiseHouseholdsOnLoan(BaseModel):
    """Ward wise households on loan"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत ऋणमा रहेका घरपरिवार")
        verbose_name_plural = _("वडागत ऋणमा रहेका घरपरिवार")
        unique_together = ["ward_number"]

    def __str__(self):
        return f"वडा {self.ward_number} - ऋणमा रहेका घरपरिवार"


class WardWiseLandOwnership(BaseModel):
    """Ward wise land ownership"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    land_ownership_type = models.CharField(
        max_length=20,
        choices=LandOwnershipTypeChoice.choices,
        verbose_name=_("जमिन स्वामित्वको प्रकार"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत जमिन स्वामित्व")
        verbose_name_plural = _("वडागत जमिन स्वामित्व")
        unique_together = ["ward_number", "land_ownership_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_land_ownership_type_display()}"


class WardWiseRemittanceExpenses(BaseModel):
    """Ward wise remittance expenses"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    remittance_expense = models.CharField(
        max_length=25,
        choices=RemittanceExpenseTypeChoice.choices,
        verbose_name=_("रेमिटेन्स खर्च"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत रेमिटेन्स खर्च")
        verbose_name_plural = _("वडागत रेमिटेन्स खर्च")
        unique_together = ["ward_number", "remittance_expense"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_remittance_expense_display()}"


class WardWiseTrainedPopulation(BaseModel):
    """Ward wise trained population"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    trained_population = models.PositiveIntegerField(
        default=0, verbose_name=_("तालिम प्राप्त जनसंख्या")
    )

    class Meta:
        verbose_name = _("वडागत तालिम प्राप्त जनसंख्या")
        verbose_name_plural = _("वडागत तालिम प्राप्त जनसंख्या")
        unique_together = ["ward_number"]

    def __str__(self):
        return f"वडा {self.ward_number} - तालिम प्राप्त: {self.trained_population}"


class WardWiseTimeToFinancialOrganization(BaseModel):
    """Ward wise time to financial organization (4.5.7 - बैंक तथा वित्तीय संस्था सम्बन्धी विवरण)"""

    ward_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name=_("वडा नं."),
    )
    time_to_financial_organization_type = models.CharField(
        max_length=20,
        choices=TimeToFinancialOrganizationChoice.choices,
        verbose_name=_("वित्तीय संस्थासम्म पुग्ने समय"),
    )
    households = models.PositiveIntegerField(default=0, verbose_name=_("घरपरिवार"))

    class Meta:
        verbose_name = _("वडागत वित्तीय संस्थासम्म पुग्ने समय")
        verbose_name_plural = _("वडागत वित्तीय संस्थासम्म पुग्ने समय")
        unique_together = ["ward_number", "time_to_financial_organization_type"]

    def __str__(self):
        return f"वडा {self.ward_number} - {self.get_time_to_financial_organization_type_display()}"
