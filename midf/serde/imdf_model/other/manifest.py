from pydantic import BaseModel


class IMDFManifest(BaseModel):
    version: str
    created: str
    generated_by: str
    language: str
