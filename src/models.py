from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Table, Column, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


db = SQLAlchemy()

favorites_characters = Table(
    "favorites_characters",
    db.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("character_id", Integer, ForeignKey("character.id"), primary_key=True)
)

favorites_locations = Table(
    "favorites_locations",
    db.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("location_id", Integer, ForeignKey("location.id"), primary_key=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    favorites_characters:Mapped[list["Character"]]=relationship(
        "Character",
        secondary = favorites_characters,
        back_populates= "favorite_by_user"
    )

    favorites_locations:Mapped[list["Location"]]=relationship(
        "Location",
        secondary = favorites_locations,
        back_populates= "favorite_by_user"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    favorite_by_user:Mapped[list["User"]]=relationship(
        "User",
        secondary = favorites_characters,
        back_populates= "favorites_characters"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    favorite_by_user:Mapped[list["User"]]=relationship(
        "User",
        secondary = favorites_locations,
        back_populates= "favorites_locations"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
