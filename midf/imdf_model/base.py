from pydantic import BaseModel, ConfigDict

__all__ = ["IMDFFeature", "IMDFFeatureReference"]


class IMDFFeature(BaseModel):
    model_config = ConfigDict(
        # extra="allow,"
        arbitrary_types_allowed=True
    )

    id: str  # ae095f89-49f8-4189-b5dd-9c6d62de3203


class IMDFFeatureReference(IMDFFeature):
    feature_type: str  # building
