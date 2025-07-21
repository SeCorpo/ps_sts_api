from src.core import BaseModel
from sqlalchemy import Column, Integer, VARCHAR, Enum, Date
from sqlalchemy.orm import relationship

class Person(BaseModel):
    """ Personal information """
    __tablename__ = 'persons'

    person_id = Column("person_id", Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column("email", VARCHAR(length=255), unique=True, nullable=False, index=True)

    first_name = Column("first_name", VARCHAR(64), nullable=False)
    infix = Column("infix", VARCHAR(32), nullable=True)
    last_name = Column("last_name", VARCHAR(64), nullable=False)
    date_of_birth = Column("date_of_birth", Date, nullable=False)
    sex = Column("sex", Enum('m', 'f', 'o'), nullable=False)

    street = Column("street", VARCHAR(64), nullable=True)
    house_number = Column("house_number", VARCHAR(6), nullable=True)
    postal_code = Column("postal_code", VARCHAR(6), nullable=True)
    city = Column("city", VARCHAR(64), nullable=True)
    country = Column("country", VARCHAR(64), nullable=True)

    user = relationship("User", back_populates="person", uselist=False)

    @property
    def fullname(self) -> str:
        if self.infix:
            return f"{self.first_name} {self.infix} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    @property
    def address(self) -> str:
        """ Eikensingel 14, 7213WJ Gorssel """
        parts = []
        if self.street and self.house_number:
            parts.append(f"{self.street} {self.house_number}")
        elif self.street:
            parts.append(self.street)
        if self.postal_code and self.city:
            parts.append(f"{self.postal_code} {self.city}")
        elif self.city:
            parts.append(self.city)
        return ', '.join(parts)