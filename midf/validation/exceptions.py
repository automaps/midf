class IMDFValidationError(Exception):

  def __init__(self, message: str, feature_id: str = None):
    self.message = message
    self.feature_id = feature_id
    super().__init__(self.message)

class ViolationError(IMDFValidationError):
  pass

class InfoError(IMDFValidationError):
  pass

class WarningError(IMDFValidationError):
  pass

# Info errors
class ZeroCountOfUnitQualifiedAddressesError(InfoError):
  pass

# Violation errors
class FeatureIdMustBeStringError(ViolationError):
  pass

class FeatureIdMustBeUniqueError(ViolationError):
  pass

class FeatureIdMustNotBeEmptyError(ViolationError):
  pass

class FeatureMustHaveFeatureTypeError(ViolationError):
  pass

class FeatureMustHaveIdError(ViolationError):
  pass

class FeatureTypeMustBeStringError(ViolationError):
  pass

class FeatureTypeMustNotBeEmptyError(ViolationError):
  pass

class FileMustBeValidGeoJSONError(ViolationError):
  pass

class FileMustContainFeatureCollectionError(ViolationError):
  pass

class ManifestFileMustBePresentError(ViolationError):
  pass

class NameMustBeStringError(ViolationError):
  pass

class ReferencedFeatureIDMustBeResolvableError(ViolationError):
  pass

class VenueCountMustBeExactlyOneError(ViolationError):
  pass

class AddressMustHaveAddressError(ViolationError):
  pass

class AddressMustHaveCountryError(ViolationError):
  pass

class AddressMustHaveLocalityError(ViolationError):
  pass

class AmenityMustHaveCategoryError(ViolationError):
  pass

class AmenityMustHaveUnitIdsError(ViolationError):
  pass

class AnchorMustHaveGeoreferenceError(ViolationError):  # TODO: NOT a rule!
  pass

class FootprintMustHaveBuildingIdsError(Exception):
  pass

class RelationshipMustHaveDirectionError(Exception):
  pass

class SectionMustHaveNameError(Exception):  # TODO: NOT a rule!
  pass

class ManifestMustHaveGeneratedByError(Exception):
  pass

class ManifestMustHaveVersionError(Exception):
  pass

class ManifestMustHaveCreatedDateError(Exception):
  pass

class ManifestMustHaveLanguageError(Exception):
  pass

class BuildingMustHaveNameError(ViolationError):
  pass

class DetailMustHaveCategoryError(ViolationError):
  pass

class FixtureMustHaveCategoryError(ViolationError):
  pass

class FixtureMustHaveLevelIdError(ViolationError):
  pass

class FeatureGeometryTypeInvalidError(Exception):
  ...

class FootprintMustHaveBuildingIdError(ViolationError):
  pass

class GeofenceMustHaveCategoryError(ViolationError):
  pass

class KioskMustHaveCategoryError(ViolationError):
  pass

class KioskMustHaveLevelIdError(ViolationError):
  pass

class LevelMustHaveOrdinalError(ViolationError):
  pass

class LevelMustHaveShortNameError(ViolationError):
  pass

class OccupantMustHaveCategoryError(ViolationError):
  pass

class OccupantMustHaveNameError(ViolationError):
  pass

class OpeningMustHaveCategoryError(ViolationError):
  pass

class RelationshipMustHaveCategoryError(ViolationError):
  pass

class RelationshipMustHaveDestinationError(ViolationError):
  pass

class RelationshipMustHaveOriginError(ViolationError):
  pass

class SectionMustHaveCategoryError(ViolationError):
  pass

class SectionMustHaveLevelIdError(ViolationError):
  pass

class UnitMustHaveCategoryError(ViolationError):
  pass

class UnitMustHaveLevelIdError(ViolationError):
  pass

class VenueMustHaveAddressIdError(ViolationError):
  pass

class VenueMustHaveCategoryError(ViolationError):
  pass

class VenueMustHaveNameError(ViolationError):
  pass

# Warning errors
class AddressHasDissimilarProvinceCodeError(WarningError):
  pass

class AddressMustBeDistinctError(WarningError):
  pass

class AddressShouldHavePostalCodeError(WarningError):
  pass

class AmenityNameShouldBeProvidedError(WarningError):
  pass

class AnchorShouldHaveAddressIdError(WarningError):
  pass

class AnchorShouldHaveUnitIdError(WarningError):
  pass

class BuildingAddressIdShouldBeProvidedError(WarningError):
  pass

class BuildingShouldHaveDisplayPointError(WarningError):
  pass

class DetailShouldHaveLevelIdError(WarningError):
  pass

class FixtureShouldHaveAnchorIdError(WarningError):
  pass

class GeofenceShouldHaveDisplayPointError(WarningError):
  pass

class KioskShouldHaveDisplayPointError(WarningError):
  pass

class LevelShouldHaveAddressIdError(WarningError):
  pass

class LevelShouldHaveBuildingIdsError(WarningError):
  pass

class LevelShouldHaveDisplayPointError(WarningError):
  pass

class OccupantShouldHaveAddressIdError(WarningError):
  pass

class OccupantShouldHaveDisplayPointError(WarningError):
  pass

class OccupantShouldHaveUnitIdsError(WarningError):
  pass

class OpeningShouldHaveDisplayPointError(WarningError):
  pass

class OpeningShouldHaveLevelIdError(WarningError):
  pass

class RelationshipShouldHaveDisplayPointError(WarningError):
  pass

class SectionShouldHaveDisplayPointError(WarningError):
  pass

class UnitShouldHaveDisplayPointError(WarningError):
  pass

class VenueShouldHaveDisplayPointError(WarningError):
  pass

# Additional Violation errors
class GeometryMustBeValidError(ViolationError):
  pass

class GeometryTypeMustBeValidError(ViolationError):
  pass

class PropertiesMustBeValidJSONError(ViolationError):
  pass

class RequiredPropertiesMustBePresentError(ViolationError):
  pass

class PropertyValuesMustBeValidError(ViolationError):
  pass

class CoordinateReferenceSystemMustBeWGS84Error(ViolationError):
  pass

class FeatureCollectionMustContainFeaturesError(ViolationError):
  pass

class FeatureMustHaveGeometryError(ViolationError):
  pass

class FeatureMustHavePropertiesError(ViolationError):
  pass

class AltitudeMustBeValidNumberError(ViolationError):
  pass

class CategoryMustBeValidError(ViolationError):
  pass

class DisplayPointMustBeValidPointError(ViolationError):
  pass

class RestrictionMustBeValidError(ViolationError):
  pass

class AccessibilityMustBeValidError(ViolationError):
  pass

class HoursMustBeValidError(ViolationError):
  pass

class PhoneMustBeValidError(ViolationError):
  pass

class WebsiteMustBeValidURLError(ViolationError):
  pass

class CorrelationIdMustBeValidError(ViolationError):
  pass

class AddressUnitMustBeValidError(ViolationError):
  pass

class PostalCodeMustBeValidError(ViolationError):
  pass

class ProvinceMustBeValidError(ViolationError):
  pass

class RegionMustBeValidError(ViolationError):
  pass

class SubregionMustBeValidError(ViolationError):
  pass

class TimeZoneMustBeValidError(ViolationError):
  pass

class AnchorLatitudeMustBeValidError(ViolationError):
  pass

class AnchorLongitudeMustBeValidError(ViolationError):
  pass

class BuildingHeightMustBeValidError(ViolationError):
  pass

class LevelOrdinalMustBeUniqueError(ViolationError):
  pass

class OutdoorMustBeBooleanError(ViolationError):
  pass

class RelationshipFromMustBeValidError(ViolationError):
  pass

class RelationshipToMustBeValidError(ViolationError):
  pass

class LevelOrdinalMustBeIntegerError(ViolationError):
  pass

class LevelShortNameMustNotBeEmptyError(ViolationError):
  pass

class RelationshipDirectionMustBeValidError(ViolationError):
  pass

class ManifestVersionMustBeValidError(ViolationError):
  pass

class ManifestCreatedDateMustBeValidError(ViolationError):
  pass

class ManifestGeneratedByMustNotBeEmptyError(ViolationError):
  pass

class ManifestLanguageMustBeValidError(ViolationError):
  pass

# Additional Warning errors
class AltitudeReferenceMustBeValidError(WarningError):
  pass

class AnchorPositionMustBeWithinVenueError(WarningError):
  pass

class BuildingHeightShouldBeProvidedError(WarningError):
  pass

class DisplayPointShouldBeProvidedError(WarningError):
  pass

class FeatureShouldHaveNameError(WarningError):
  pass

class LevelOrdinalShouldBeSequentialError(WarningError):
  pass

class OpeningHeightShouldBeProvidedError(WarningError):
  pass

class OpeningWidthShouldBeProvidedError(WarningError):
  pass

class RelationshipShouldHaveOrderError(WarningError):
  pass

class UnitShouldHaveAddressIdError(WarningError):
  pass

class FeatureShouldHaveCorrelationIdError(WarningError):
  pass

class FeatureShouldHaveExternalReferenceError(WarningError):
  pass

# Additional Info errors
class DuplicateFeatureIdWarningError(InfoError):
  pass

class FeatureIdFormatRecommendationError(InfoError):
  pass

class GeometryPrecisionRecommendationError(InfoError):
  pass

class LanguageCodeRecommendationError(InfoError):
  pass

class NameTranslationRecommendationError(InfoError):
  pass

class PropertyNameRecommendationError(InfoError):
  pass

class ReferencedFeatureTypeMismatchWarningError(InfoError):
  pass

class UnusedAddressWarningError(InfoError):
  pass

class UnusedAnchorWarningError(InfoError):
  pass

class UnusedBuildingWarningError(InfoError):
  pass

class UnusedLevelWarningError(InfoError):
  pass

class UnusedUnitWarningError(InfoError):
  pass

class FeatureNameShouldBeTranslatedError(InfoError):
  pass

class FeaturePropertiesShouldUseRecommendedNamesError(InfoError):
  pass

# Add any additional rules that might be in the CSV but not listed here

class BuildingMustHaveCategoryError(ViolationError):
  pass

# ... (add any other new exception classes here)
