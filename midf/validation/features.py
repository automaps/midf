import re
from datetime import datetime
from typing import Any, List

from midf.enums import IMDFFeatureType
from midf.imdf_model import (
    IMDFAddress,
    IMDFAmenity,
    IMDFAnchor,
    IMDFBuilding,
    IMDFDetail,
    IMDFFeature,
    IMDFFixture,
    IMDFFootprint,
    IMDFGeofence,
    IMDFKiosk,
    IMDFLevel,
    IMDFManifest,
    IMDFOccupant,
    IMDFOpening,
    IMDFRelationship,
    IMDFSection,
    IMDFUnit,
    IMDFVenue,
)
from .base import BaseValidator, ValidationError, validate_geometry
from .exceptions import (
    AnchorMustHaveGeoreferenceError,
    BuildingMustHaveCategoryError,
    BuildingMustHaveNameError,
    FixtureMustHaveCategoryError,
    FootprintMustHaveBuildingIdsError,
    GeofenceMustHaveCategoryError,
    IMDFValidationError,
    LevelMustHaveOrdinalError,
    LevelMustHaveShortNameError,
    ManifestCreatedDateMustBeValidError,
    ManifestMustHaveCreatedDateError,
    ManifestMustHaveGeneratedByError,
    ManifestMustHaveLanguageError,
    ManifestMustHaveVersionError,
    ManifestVersionMustBeValidError,
    OccupantMustHaveCategoryError,
    OccupantMustHaveNameError,
    OpeningMustHaveCategoryError,
    ReferencedFeatureIDMustBeResolvableError,
    RelationshipMustHaveCategoryError,
    RelationshipMustHaveDirectionError,
    SectionMustHaveNameError,
    UnitMustHaveCategoryError,
    UnitMustHaveLevelIdError,
    VenueMustHaveAddressIdError,
    VenueMustHaveCategoryError,
    VenueMustHaveNameError,
)


class AddressValidator(BaseValidator):

    def validate(self, feature: IMDFFeature) -> List[str]:
        errors = []
        if not isinstance(feature, IMDFAddress):
            raise ValidationError(f"Expected IMDFAddress, got {type(feature)}")

        if not feature.address:
            errors.append(f"Address {feature.id} is missing required field 'address'")
        if not feature.locality:
            errors.append(f"Address {feature.id} is missing required field 'locality'")
        if not feature.country:
            errors.append(f"Address {feature.id} is missing required field 'country'")

        return errors


class AmenityValidator(BaseValidator):

    def validate(self, feature: IMDFAmenity) -> List[str]:
        errors = []
        if not isinstance(feature, IMDFAmenity):
            raise ValidationError(f"Expected IMDFAmenity, got {type(feature)}")

        validate_geometry(feature)
        # errors.extend()

        if not feature.category:
            errors.append(f"Amenity {feature.id} is missing required field 'category'")
        if not feature.unit_ids:
            errors.append(f"Amenity {feature.id} is missing required field 'unit_ids'")

        return errors


class AnchorValidator(BaseValidator):

    def validate(self, feature: IMDFFeature) -> None:
        if not isinstance(feature, IMDFAnchor):
            raise ValidationError(f"Expected IMDFAnchor, got {type(feature)}")

        validate_geometry(feature)

        if False:
            if not feature.georeference:
                raise AnchorMustHaveGeoreferenceError(
                    f"Anchor {feature.id} is missing required field 'georeference'",
                    feature.id,
                )


class DetailValidator(BaseValidator):

    def validate(self, feature: IMDFDetail) -> None:
        if not isinstance(feature, IMDFDetail):
            raise ValidationError(f"Expected IMDFDetail, got {type(feature)}")

        validate_geometry(feature)


class FixtureValidator(BaseValidator):

    def validate(self, feature: IMDFFeature) -> None:
        if not isinstance(feature, IMDFFixture):
            raise ValidationError(f"Expected IMDFFixture, got {type(feature)}")

        validate_geometry(feature)

        if not feature.category:
            raise FixtureMustHaveCategoryError(
                f"Fixture {feature.id} is missing required field 'category'", feature.id
            )


class FootprintValidator(BaseValidator):

    def validate(self, feature: IMDFFootprint) -> None:
        if not isinstance(feature, IMDFFootprint):
            raise ValidationError(f"Expected IMDFFootprint, got {type(feature)}")

        validate_geometry(feature)

        if not feature.building_ids:
            raise FootprintMustHaveBuildingIdsError(
                f"Footprint {feature.id} is missing required field 'building_ids'",
                feature.id,
            )


class GeofenceValidator(BaseValidator):

    def validate(self, feature: IMDFGeofence) -> None:
        if not isinstance(feature, IMDFGeofence):
            raise ValidationError(f"Expected IMDFGeofence, got {type(feature)}")

        validate_geometry(feature)

        if not feature.category:
            raise GeofenceMustHaveCategoryError(
                f"Geofence {feature.id} is missing required field 'category'",
                feature.id,
            )


class KioskValidator(BaseValidator):

    def validate(self, feature: IMDFKiosk) -> None:
        if not isinstance(feature, IMDFKiosk):
            raise ValidationError(f"Expected IMDFKiosk, got {type(feature)}")

        validate_geometry(feature)


class OccupantValidator(BaseValidator):

    def validate(self, feature: IMDFOccupant) -> None:
        if not isinstance(feature, IMDFOccupant):
            raise ValidationError(f"Expected IMDFOccupant, got {type(feature)}")

        if not feature.category:
            raise OccupantMustHaveCategoryError(
                f"Occupant {feature.id} is missing required field 'category'",
                feature.id,
            )
        if not feature.name:
            raise OccupantMustHaveNameError(
                f"Occupant {feature.id} is missing required field 'name'", feature.id
            )


class OpeningValidator(BaseValidator):

    def validate(self, feature: IMDFFeature) -> None:
        if not isinstance(feature, IMDFOpening):
            raise ValidationError(f"Expected IMDFOpening, got {type(feature)}")

        validate_geometry(feature)

        if not feature.category:
            raise OpeningMustHaveCategoryError(
                f"Opening {feature.id} is missing required field 'category'", feature.id
            )


class RelationshipValidator(BaseValidator):

    def validate(self, feature: IMDFFeature) -> None:
        if not isinstance(feature, IMDFRelationship):
            raise ValidationError(f"Expected IMDFRelationship, got {type(feature)}")

        if not feature.category:
            raise RelationshipMustHaveCategoryError(
                f"Relationship {feature.id} is missing required field 'category'",
                feature.id,
            )
        if not feature.direction:
            raise RelationshipMustHaveDirectionError(
                f"Relationship {feature.id} is missing required field 'direction'",
                feature.id,
            )

    def validate_relationships(
        self, imdf_dict: Any  #: Dict[str, List[IMDFFeature]]
    ) -> List[IMDFValidationError]:
        errors = []
        relationships = imdf_dict.get(IMDFFeatureType.relationship, [])

        for relationship in relationships:
            try:
                self.validate(relationship)
            except IMDFValidationError as e:
                errors.append(e)

            if relationship.origin not in imdf_dict:
                errors.append(
                    ReferencedFeatureIDMustBeResolvableError(
                        f"Relationship {relationship.id} has invalid origin {relationship.origin}",
                        relationship.id,
                    )
                )
            if relationship.destination not in imdf_dict:
                errors.append(
                    ReferencedFeatureIDMustBeResolvableError(
                        f"Relationship {relationship.id} has invalid destination {relationship.destination}",
                        relationship.id,
                    )
                )

            if relationship.intermediary:
                for intermediary in relationship.intermediary:
                    if intermediary not in imdf_dict:
                        errors.append(
                            ReferencedFeatureIDMustBeResolvableError(
                                f"Relationship {relationship.id} has invalid intermediary {intermediary}",
                                relationship.id,
                            )
                        )

        return errors


class SectionValidator(BaseValidator):

    def validate(self, feature: IMDFFeature) -> None:
        if not isinstance(feature, IMDFSection):
            raise ValidationError(f"Expected IMDFSection, got {type(feature)}")

        validate_geometry(feature)

        if False:
            if not feature.name:
                raise SectionMustHaveNameError(
                    f"Section {feature.id} is missing required field 'name'", feature.id
                )


class ManifestValidator(BaseValidator):

    def validate(self, manifest: IMDFManifest) -> List[IMDFValidationError]:
        errors = []

        if not manifest.version:
            errors.append(
                ManifestMustHaveVersionError(
                    "Manifest is missing required field 'version'"
                )
            )
        elif not self.is_valid_version(manifest.version):
            errors.append(
                ManifestVersionMustBeValidError(
                    f"Invalid manifest version: {manifest.version}"
                )
            )

        if not manifest.created:
            errors.append(
                ManifestMustHaveCreatedDateError(
                    "Manifest is missing required field 'created'"
                )
            )
        elif not self.is_valid_date_format(manifest.created):
            errors.append(
                ManifestCreatedDateMustBeValidError(
                    f"Invalid created date format: {manifest.created}"
                )
            )

        if not manifest.generated_by:
            errors.append(
                ManifestMustHaveGeneratedByError(
                    "Manifest is missing required field 'generated_by'"
                )
            )

        if not manifest.language:
            errors.append(
                ManifestMustHaveLanguageError(
                    "Manifest is missing required field 'language'"
                )
            )

        return errors

    def is_valid_version(self, version: str) -> bool:
        return re.match(r"^\d+\.\d+\.\d+$", version) is not None

    def is_valid_date_format(self, date_str: str) -> bool:
        try:
            datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            return True
        except ValueError:
            return False


class BuildingValidator(BaseValidator):

    def validate(self, feature: IMDFFeature) -> None:
        if not isinstance(feature, IMDFBuilding):
            raise ValidationError(f"Expected IMDFBuilding, got {type(feature)}")

        validate_geometry(feature)

        if not feature.name:
            raise BuildingMustHaveNameError(
                f"Building {feature.id} is missing required field 'name'", feature.id
            )
        if not feature.category:
            raise BuildingMustHaveCategoryError(
                f"Building {feature.id} is missing required field 'category'",
                feature.id,
            )


class LevelValidator(BaseValidator):

    def validate(self, feature: IMDFFeature) -> None:
        if not isinstance(feature, IMDFLevel):
            raise ValidationError(f"Expected IMDFLevel, got {type(feature)}")

        validate_geometry(feature)

        if feature.ordinal is None:
            raise LevelMustHaveOrdinalError(
                f"Level {feature.id} is missing required field 'ordinal'", feature.id
            )
        if not feature.short_name:
            raise LevelMustHaveShortNameError(
                f"Level {feature.id} is missing required field 'short_name'", feature.id
            )


class UnitValidator(BaseValidator):

    def validate(self, feature: IMDFFeature) -> None:
        if not isinstance(feature, IMDFUnit):
            raise ValidationError(f"Expected IMDFUnit, got {type(feature)}")

        validate_geometry(feature)

        if not feature.category:
            raise UnitMustHaveCategoryError(
                f"Unit {feature.id} is missing required field 'category'", feature.id
            )
        if not feature.level_id:
            raise UnitMustHaveLevelIdError(
                f"Unit {feature.id} is missing required field 'level_id'", feature.id
            )


class VenueValidator(BaseValidator):

    def validate(self, feature: IMDFFeature) -> None:
        if not isinstance(feature, IMDFVenue):
            raise ValidationError(f"Expected IMDFVenue, got {type(feature)}")

        validate_geometry(feature)

        if not feature.name:
            raise VenueMustHaveNameError(
                f"Venue {feature.id} is missing required field 'name'", feature.id
            )
        if not feature.category:
            raise VenueMustHaveCategoryError(
                f"Venue {feature.id} is missing required field 'category'", feature.id
            )
        if not feature.address_id:
            raise VenueMustHaveAddressIdError(
                f"Venue {feature.id} is missing required field 'address_id'", feature.id
            )
