from typing import Collection, Dict, List

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFManifest
from .exceptions import (
    FeatureGeometryTypeInvalidError,
    GeometryMustBeValidError,
    IMDFValidationError,
    InfoError,
    ViolationError,
    WarningError,
)
from .features import (
    AddressValidator,
    AmenityValidator,
    AnchorValidator,
    BuildingValidator,
    DetailValidator,
    FixtureValidator,
    FootprintValidator,
    GeofenceValidator,
    KioskValidator,
    LevelValidator,
    ManifestValidator,
    OccupantValidator,
    OpeningValidator,
    RelationshipValidator,
    SectionValidator,
    UnitValidator,
    VenueValidator,
)


def validate_geometric_containment(
    imdf_dict: dict[str, Collection[IMDFFeature]],
) -> None:
    levels = imdf_dict.get(IMDFFeatureType.level, [])
    units = imdf_dict.get(IMDFFeatureType.unit, [])
    amenities = imdf_dict.get(IMDFFeatureType.amenity, [])
    openings = imdf_dict.get(IMDFFeatureType.opening, [])

    # Check geometry validity
    for feature_type, features in [
        (IMDFFeatureType.level, levels),
        (IMDFFeatureType.unit, units),
        (IMDFFeatureType.amenity, amenities),
        (IMDFFeatureType.opening, openings),
    ]:
        for feature in features:
            if not feature.geometry.is_valid:
                raise GeometryMustBeValidError(
                    f"{feature_type.capitalize()} {feature.id} has an invalid geometry",
                    feature.id,
                )

    # Check if units are contained within levels
    for unit in units:
        if not unit.geometry.is_valid:
            continue
        contained = False
        for level in levels:
            if not level.geometry.is_valid:
                continue
            if level.geometry.contains(unit.geometry):
                contained = True
                break
        if not contained:
            raise FeatureGeometryTypeInvalidError(
                f"Unit {unit.id} is not contained within any level", unit.id
            )

    # Add more geometric containment checks as needed


class IMDFValidator:

    def __init__(self):
        self.validators = {
            IMDFFeatureType.address: AddressValidator(),
            IMDFFeatureType.amenity: AmenityValidator(),
            IMDFFeatureType.anchor: AnchorValidator(),
            IMDFFeatureType.building: BuildingValidator(),
            IMDFFeatureType.detail: DetailValidator(),
            IMDFFeatureType.fixture: FixtureValidator(),
            IMDFFeatureType.footprint: FootprintValidator(),
            IMDFFeatureType.geofence: GeofenceValidator(),
            IMDFFeatureType.kiosk: KioskValidator(),
            IMDFFeatureType.level: LevelValidator(),
            IMDFFeatureType.occupant: OccupantValidator(),
            IMDFFeatureType.opening: OpeningValidator(),
            IMDFFeatureType.relationship: RelationshipValidator(),
            IMDFFeatureType.section: SectionValidator(),
            IMDFFeatureType.unit: UnitValidator(),
            IMDFFeatureType.venue: VenueValidator(),
        }
        self.manifest_validator = ManifestValidator()

    def validate_dataset(
        self, imdf_dict: Dict[str, Collection[IMDFFeature]], manifest: IMDFManifest
    ) -> Dict[str, List[IMDFValidationError]]:
        errors = {"violations": [], "warnings": [], "info": []}

        # Validate manifest
        try:
            self.manifest_validator.validate(manifest)
        except IMDFValidationError as e:
            self._categorize_error(errors, e)

        # Validate features
        for feature_type, features in imdf_dict.items():
            if feature_type in self.validators:
                validator = self.validators[feature_type]
                for feature in features:
                    try:
                        validator.validate(feature)
                    except IMDFValidationError as e:
                        self._categorize_error(errors, e)

        # Validate relationships
        relationship_validator = self.validators[IMDFFeatureType.relationship]
        try:
            relationship_validator.validate_relationships(imdf_dict)
        except IMDFValidationError as e:
            self._categorize_error(errors, e)

        # Validate geometric containment
        try:
            validate_geometric_containment(imdf_dict)
        except IMDFValidationError as e:
            self._categorize_error(errors, e)

        return errors

    def _categorize_error(
        self, errors: Dict[str, List[IMDFValidationError]], error: IMDFValidationError
    ):
        if isinstance(error, ViolationError):
            errors["violations"].append(error)
        elif isinstance(error, WarningError):
            errors["warnings"].append(error)
        elif isinstance(error, InfoError):
            errors["info"].append(error)
