# API Documentation Specification

## Overview
The lungri Digital Profile Report API provides comprehensive access to municipality data, report generation, and administrative functions. The API follows RESTful principles and returns JSON responses.

## Base URL
```
Development: http://localhost:8000/api/v1/
Production: https://lungri-report.gov.np/api/v1/
```

## Authentication
```http
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
```

## Core API Endpoints

### 1. Municipality Information
```yaml
GET /api/v1/municipalities/
Description: List all municipalities
Response: Paginated list of municipalities

GET /api/v1/municipalities/{id}/
Description: Get specific municipality details
Parameters:
  - id: Municipality ID
Response: Municipality object with full details

POST /api/v1/municipalities/
Description: Create new municipality (Admin only)
Request Body: Municipality data object

PUT /api/v1/municipalities/{id}/
Description: Update municipality (Admin only)
Request Body: Updated municipality data

DELETE /api/v1/municipalities/{id}/
Description: Delete municipality (Admin only)
```

### 2. Demographics API
```yaml
GET /api/v1/demographics/population/
Description: Get population statistics
Query Parameters:
  - municipality_id: Filter by municipality
  - ward: Filter by ward number
  - age_group: Filter by age group
  - gender: Filter by gender (male/female/other)
Response: Population statistics object

GET /api/v1/demographics/households/
Description: Get household information
Query Parameters:
  - municipality_id: Municipality ID
  - household_type: Type of household
Response: Household statistics

GET /api/v1/demographics/education/
Description: Get education statistics
Query Parameters:
  - municipality_id: Municipality ID
  - education_level: Education level filter
Response: Education statistics

GET /api/v1/demographics/languages/
Description: Get language distribution
Response: Language statistics by population

GET /api/v1/demographics/religions/
Description: Get religious distribution
Response: Religious statistics

GET /api/v1/demographics/castes/
Description: Get caste/ethnicity distribution
Response: Caste and ethnicity statistics
```

### 3. Economics API
```yaml
GET /api/v1/economics/overview/
Description: Get economic overview
Query Parameters:
  - municipality_id: Municipality ID
Response: Economic indicators and statistics

GET /api/v1/economics/agriculture/
Description: Get agriculture and livestock data
Query Parameters:
  - municipality_id: Municipality ID
  - crop_type: Filter by crop type
Response: Agricultural production data

GET /api/v1/economics/industry/
Description: Get industrial data
Query Parameters:
  - municipality_id: Municipality ID
  - industry_type: Filter by industry type
Response: Industrial statistics

GET /api/v1/economics/tourism/
Description: Get tourism data
Response: Tourism sites and visitor statistics

GET /api/v1/economics/employment/
Description: Get employment statistics
Query Parameters:
  - municipality_id: Municipality ID
  - sector: Employment sector
Response: Employment data by sector

GET /api/v1/economics/income/
Description: Get income and expenditure data
Response: Household income statistics
```

### 4. Social Services API
```yaml
GET /api/v1/social/education/schools/
Description: Get educational institutions
Query Parameters:
  - municipality_id: Municipality ID
  - level: School level (primary/secondary/higher)
  - type: School type (public/private)
Response: List of educational institutions

GET /api/v1/social/health/facilities/
Description: Get health facilities
Query Parameters:
  - municipality_id: Municipality ID
  - type: Facility type (hospital/clinic/health_post)
Response: List of health facilities

GET /api/v1/social/water-sanitation/
Description: Get water and sanitation data
Response: Access to water and sanitation facilities

GET /api/v1/social/women-children/
Description: Get women and children welfare data
Response: Statistics on women and children programs

GET /api/v1/social/youth-sports/
Description: Get youth and sports data
Response: Youth programs and sports facilities
```

### 5. Environment API
```yaml
GET /api/v1/environment/forests/
Description: Get forest area data
Query Parameters:
  - municipality_id: Municipality ID
  - forest_type: Type of forest
Response: Forest coverage and management data

GET /api/v1/environment/water-resources/
Description: Get water resources data
Response: Rivers, lakes, and water sources

GET /api/v1/environment/biodiversity/
Description: Get biodiversity data
Response: Flora and fauna information

GET /api/v1/environment/disasters/
Description: Get disaster management data
Response: Disaster risks and preparedness
```

### 6. Infrastructure API
```yaml
GET /api/v1/infrastructure/transportation/
Description: Get transportation infrastructure
Response: Roads, bridges, and transport facilities

GET /api/v1/infrastructure/energy/
Description: Get energy infrastructure
Response: Power sources and distribution

GET /api/v1/infrastructure/communication/
Description: Get communication infrastructure
Response: Telecom and internet connectivity

GET /api/v1/infrastructure/housing/
Description: Get housing and building data
Response: Housing types and construction materials
```

### 7. Governance API
```yaml
GET /api/v1/governance/organization/
Description: Get organizational structure
Response: Administrative hierarchy and positions

GET /api/v1/governance/services/
Description: Get public services data
Response: Available services and delivery mechanisms

GET /api/v1/governance/policies/
Description: Get policies and regulations
Response: Local laws and policies

GET /api/v1/governance/budget/
Description: Get budget information
Query Parameters:
  - fiscal_year: Fiscal year filter
Response: Budget allocation and expenditure
```

### 8. Report Generation API
```yaml
POST /api/v1/reports/generate/
Description: Generate complete report
Request Body:
  {
    "municipality_id": "string",
    "report_type": "full|summary|chapter",
    "chapters": ["demographics", "economics", ...],
    "format": "pdf|html",
    "language": "ne|en"
  }
Response: 
  {
    "report_id": "string",
    "status": "processing|completed|failed",
    "download_url": "string",
    "estimated_completion": "datetime"
  }

GET /api/v1/reports/{report_id}/status/
Description: Check report generation status
Response: Report status and progress

GET /api/v1/reports/{report_id}/download/
Description: Download generated report
Response: PDF file download

GET /api/v1/reports/templates/
Description: Get available report templates
Response: List of report templates

POST /api/v1/reports/preview/
Description: Preview report section
Request Body: Section data
Response: HTML preview
```

## Data Models Examples

### Municipality Model
```json
{
  "id": "string",
  "name": "string",
  "name_nepali": "string",
  "type": "municipality|rural_municipality",
  "province": "string",
  "district": "string",
  "establishment_date": "date",
  "area_sq_km": "decimal",
  "wards_count": "integer",
  "population": "integer",
  "headquarters": "string",
  "website": "url",
  "contact_email": "email",
  "contact_phone": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Population Statistics Model
```json
{
  "municipality_id": "string",
  "total_population": "integer",
  "male_population": "integer",
  "female_population": "integer",
  "other_population": "integer",
  "total_households": "integer",
  "average_household_size": "decimal",
  "literacy_rate": "decimal",
  "age_groups": {
    "0_14": "integer",
    "15_64": "integer",
    "65_plus": "integer"
  },
  "last_updated": "datetime"
}
```

## Error Responses
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object",
    "timestamp": "datetime"
  }
}
```

## Rate Limiting
- **Public Endpoints**: 100 requests per hour
- **Authenticated Users**: 1000 requests per hour
- **Admin Users**: 5000 requests per hour

## Pagination
```json
{
  "count": "integer",
  "next": "url|null",
  "previous": "url|null",
  "results": ["array"]
}
```

## Filtering and Searching
Most list endpoints support:
- `search`: Text search across relevant fields
- `ordering`: Sort by field (use `-` for descending)
- `limit`: Number of results per page
- `offset`: Number of results to skip

Example:
```
GET /api/v1/demographics/population/?search=ward&ordering=-population&limit=10
```
