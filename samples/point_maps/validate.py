"""# Example features to validate
features_list = [Feature(a.id, a.__dict__, a.geometry if hasattr(a, 'geometry') else None) for a in
                 imdf_dict.values() if
                 isinstance(a, IMDFFeature)]

# Run validation on example features
validate_all_features(features_list)"""
