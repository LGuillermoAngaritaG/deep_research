from pydantic import BaseModel, Field

class Section(BaseModel):
    title: str = Field(description="The title/subtitle of the section")
    content: str = Field(description="The content of the section, that answers the title of the section")
    references: str = Field(description="The references of the section, that are used to answer the title of the section")

class documentationOutput(BaseModel):
    sections: list[Section] = Field(description="The sections of the report, that are used to answer the outline")