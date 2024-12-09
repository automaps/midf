"""# Example features to validate
features_list = [Feature(a.id, a.__dict__, a.geometry if hasattr(a, 'geometry') else None) for a in
                 imdf_dict.values() if
                 isinstance(a, IMDFFeature)]

# Run validation on example features
validate_all_features(features_list)"""

from midf.loading import MANIFEST_KEY, load_imdf
from midf.validation.validator import IMDFValidator

# Load your IMDF data
imdf_dict = load_imdf("path/to/your/imdf/data")
manifest = imdf_dict.pop(MANIFEST_KEY)[0]

# Create validator and validate
imdf_validator = IMDFValidator()
errors = imdf_validator.validate_dataset(imdf_dict, manifest)

# Print errors
if errors["violations"] or errors["warnings"] or errors["info"]:
    print("Validation errors found:")
    for category in ["violations", "warnings", "info"]:
        if errors[category]:
            print(f"\n{category.capitalize()}:")
            for error in errors[category]:
                print(f"- {error}")
else:
    print("IMDF dataset is valid.")
