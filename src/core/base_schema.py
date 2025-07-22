from pydantic import BaseModel, model_validator, ConfigDict
from typing import Any

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def strip_strings(cls, values: dict[str, Any]):
        """ Strip whitespace from all string fields and convert empty strings to None """
        for k, v in values.items():
            if isinstance(v, str):
                v = v.strip()
                values[k] = v if v else None
        return values

    @classmethod
    def from_orm(cls, orm_obj):
        """ Convert from an ORM object to a schema instance """
        return cls.model_validate(orm_obj)

    def to_model(self, model_class):
        """Instantiate a SQLAlchemy model from this schema"""
        return model_class(**self.model_dump(exclude_unset=True))