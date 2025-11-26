from datetime import date
from typing import Optional, Literal
from src.core import BaseModel
from sqlalchemy import Integer, Enum, Date, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.models import User


class Person(BaseModel):
    """ Personal information """
    __tablename__ = 'persons'

    person_id: Mapped[int] = mapped_column("person_id", Integer, primary_key=True, autoincrement=True, nullable=False)
    email: Mapped[str] = mapped_column("email", String(255), unique=True, nullable=False, index=True)

    first_name: Mapped[str] = mapped_column("first_name", String(64), nullable=False)
    infix: Mapped[Optional[str]] = mapped_column("infix", String(32), nullable=True)
    last_name: Mapped[str] = mapped_column("last_name", String(64), nullable=False)
    date_of_birth: Mapped[date] = mapped_column("date_of_birth", Date, nullable=False)
    sex: Mapped[Literal['m', 'f', 'o']] = mapped_column("sex",Enum('m', 'f', 'o', name="sex_enum"), nullable=False)

    street: Mapped[Optional[str]] = mapped_column("street", String(64), nullable=True)
    house_number: Mapped[Optional[str]] = mapped_column("house_number", String(6), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column("postal_code", String(6), nullable=True)
    city: Mapped[Optional[str]] = mapped_column("city", String(64), nullable=True)
    country: Mapped[Optional[str]] = mapped_column("country", String(64), nullable=True)

    user: Mapped[Optional["User"]] = relationship("User", back_populates="person", uselist=False)

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