#!/usr/bin/env bash
# -------------------------------------------------------------------
#  make_profile_skeleton.sh
#
#  Creates a blank .md file for every leaf item in the
#  “Digital Profile Report” outline, translated to English
#  slugs and organised into:
#     introduction/  demographics/  economics/
#     environment/   infrastructure/  governance/
#
#  Usage
#     chmod +x make_profile_skeleton.sh
#     ./make_profile_skeleton.sh
#
#  Re‑running is safe: existing files are left untouched.
# -------------------------------------------------------------------
set -euo pipefail

create() {
  local dir="$1" slug="$2"
  mkdir -p "$dir"
  local file="$dir/$slug.md"
  [[ -e "$file" ]] || {
    printf '# %s\n\n<!-- auto‑generated stub -->\n' "${slug//-/ }" > "$file"
    echo "✅  $file"
  }
}

# -------------------------------------------------------------------
#  Every line below is:   folder|file‑slug   (NO SPACES around “|”)
# -------------------------------------------------------------------
while IFS='|' read -r folder slug; do
  [[ -z "$folder" || -z "$slug" ]] && continue
  create "$folder" "$slug"
done <<'END_OF_LIST'
# ------------------ 1 • INTRODUCTION --------------------------------
introduction|background
introduction|objectives
introduction|legal-and-policy-basis
introduction|preparation-stages
introduction|stage-framework-tools-methods
introduction|stage-workshop
introduction|stage-enumerator-selection-deployment
introduction|stage-data-collection
introduction|stage-data-processing-analysis-source-map
introduction|stage-draft-report-preparation
introduction|stage-feedback-collection
introduction|stage-final-report-preparation
introduction|scope-of-situation-analysis
# ------------------ 2 • MUNICIPAL PROFILE (DEMOGRAPHICS) ------------
demographics|geographic-location
demographics|historical-background-and-naming
demographics|political-situation
demographics|topography
demographics|natural-resources
demographics|cultural-excellence
demographics|development-potentials
demographics|household-production
demographics|human-development-index
# ------------------ 3 • POPULATION ----------------------------------
demographics|settlement-and-household
demographics|population-distribution
demographics|age-and-sex-population
demographics|mother-tongue-population
demographics|religion-population
demographics|caste-ethnicity-population
demographics|household-head
demographics|occupation-population
demographics|economically-active-population
demographics|disability-population
demographics|migration
demographics|vital-events
demographics|social-security-beneficiaries
demographics|institutional-population
demographics|source-map-population
# ------------------ 4 • ECONOMY -------------------------------------
economics|skilled-human-resources
economics|main-occupation
economics|average-income
economics|average-expenditure-and-savings
economics|poverty-classification
economics|food-security-status
economics|housing-structure
economics|poverty-rate
economics|import-export-status
economics|industrial-raw-material-production
economics|unemployment
economics|foreign-employment
economics|landless
economics|source-map-economic
economics|current-land-use
economics|land-ownership
economics|land-type
economics|arable-land
economics|barren-land
economics|source-map-land
economics|public-ponds-fish-farming
economics|irrigation-facility-availability
economics|irrigation-sources
economics|agricultural-production
economics|livestock-production
economics|crop-diseases-pests
economics|fruit-vegetable-diseases-pests
economics|livestock-diseases-pests
economics|commercial-agricultural-farms
economics|modern-livestock-farms
economics|agri-livestock-human-resources
economics|agri-livestock-groups
economics|collection-and-cooling-centers
economics|agri-markets-fairs
economics|source-map-agriculture
economics|tourist-sites
economics|hotels-resorts-restaurants
economics|tourism-services-facilities
economics|religious-historical-tourist-sites
economics|hotels-resorts-homestay
economics|source-map-tourism
economics|industrial-development
economics|production-service-industries
economics|mills-and-processing
economics|trade-and-business
economics|minerals-and-mines
economics|local-markets-trade-centers
economics|banks-and-financial-institutions
economics|cooperatives
economics|source-map-industry
# ------------------ 5 • SOCIAL STATUS (DEMOGRAPHICS) ----------------
demographics|literacy-5-and-15-plus
demographics|educational-status-5-plus
demographics|schools-students-by-level
demographics|students-enrolled-by-level
demographics|campuses-technical-institutes
demographics|out-of-school-children
demographics|learning-achievement-pass-rate
demographics|gross-enrolment-retention-survival-rate
demographics|ecd-centers
demographics|schools-peace-zone-improvement-plan
demographics|teachers-and-education-workforce
demographics|access-to-basic-and-secondary-schools
demographics|educational-infrastructure-and-facilities
demographics|scholarships-and-targeted-facilities
demographics|model-schools-internet-facilities
demographics|earthquake-resistant-and-retrofitted-schools
demographics|local-government-investment-education
demographics|technical-and-specialized-human-resources
demographics|disability-special-education-resource-classes
demographics|educational-quality
demographics|child-friendly-education
demographics|physical-condition-of-schools
demographics|source-map-education
demographics|health-institutions
demographics|health-workforce
demographics|access-to-primary-health-services
demographics|health-services-facilities
demographics|immunization-safe-motherhood
demographics|child-health-malnutrition
demographics|major-diseases-treatment
demographics|safe-motherhood
demographics|source-map-health
demographics|drinking-water-facilities
demographics|drinking-water-sources
demographics|toilet-use
demographics|public-toilets
demographics|solid-waste-management
demographics|sewage-management
demographics|source-map-water-sanitation
demographics|child-marriage-by-sex
demographics|working-children-outside-home
demographics|child-clubs-networks
demographics|orphaned-children
demographics|disability-population
demographics|elderly-and-single-women
demographics|minority-marginalized-groups
demographics|budget-allocation-expenditure-targeted-programs
demographics|source-map-inclusion
demographics|playgrounds-parks-picnic-sites
demographics|professional-athletes
demographics|youth-clubs
demographics|youth-creativity-entrepreneurship
demographics|source-map-youth
demographics|religious-historical-sites
demographics|public-places-pati-pauwa-chautara
demographics|local-festivals-fairs
demographics|special-education-resource-class-students
demographics|religious-site-details
demographics|local-festivals-fairs-details
demographics|source-map-culture
demographics|peace-and-security-status
# ------------------ 6 • ENVIRONMENT ---------------------------------
environment|forest-area-types
environment|forest-management
environment|plantation-open-space
environment|forest-products
environment|herbal-production-collection-export
environment|forest-products-export
environment|source-map-forests
environment|watershed-sub-watershed-status
environment|water-spring-details
environment|rivers-streams
environment|lakes-ponds-wetlands
environment|water-resources-and-use
environment|structured-sources-land-structures
environment|source-map-water-resources
environment|fauna-by-habitat
environment|important-flora
environment|protected-areas
environment|source-map-biodiversity
environment|parks-and-gardens-details
environment|vulnerable-households
environment|human-physical-losses
environment|disaster-risk-timing
environment|damaged-public-infrastructure
environment|disaster-preparedness
environment|emergency-transport
environment|open-space-details
environment|source-map-disaster
# ------------------ 7 • INFRASTRUCTURE ------------------------------
infrastructure|road-network-status
infrastructure|on-going-roads
infrastructure|transport-services-routes
infrastructure|vehicles-within-municipality
infrastructure|suspension-bridges
infrastructure|travel-time-to-center
infrastructure|bus-parks-stops
infrastructure|source-map-transport
infrastructure|cooking-fuel-households
infrastructure|lighting-fuel-households
infrastructure|electricity-generation
infrastructure|households-with-electricity
infrastructure|alternative-energy-households
infrastructure|source-map-energy
infrastructure|postal-and-press
infrastructure|telecommunication
infrastructure|radio-stations
infrastructure|access-to-modern-facilities
infrastructure|source-map-communication
infrastructure|surface-drainage-status
infrastructure|roofing-type-households
infrastructure|government-buildings
infrastructure|distance-office-to-ward-centers
infrastructure|slaughterhouses
infrastructure|cremation-sites
infrastructure|source-map-housing
# ------------------ 8 • GOVERNANCE ----------------------------------
governance|municipal-organizational-structure
governance|subject-branches-human-resources
governance|federal-provincial-offices
governance|revenue-expenditure-last-five-years
governance|municipal-immovable-assets
governance|available-services-types
governance|service-process-and-feedback
governance|citizen-awareness-centers-platforms-tol-development
governance|traditional-community-based-institutions
governance|thematic-groups-institutions
governance|community-mediation-committee
governance|ngos-ingo-budget
governance|source-map-institutions
governance|municipal-laws-policies-guidelines-standards
governance|major-projects-last-three-years
governance|major-programs-projects
governance|municipal-employees
governance|special-protected-autonomous-areas
governance|source-map-governance
END_OF_LIST
