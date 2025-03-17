# Copyright 2024 Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from typing import Optional, List

from sqlalchemy import (
    String,
    Computed,
    Date,
    LargeBinary,
    Integer,
    Numeric,
    ForeignKey,
    JSON,
    Boolean,
    DateTime,
    BigInteger,
    ARRAY,
    ForeignKeyConstraint,
    Sequence,
    TextClause,
    Index,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# Most models in this sample use a client-side generated UUID as primary key.
# This allows inserts to use Batch DML, as the primary key value does not need
# to be returned from Spanner using a THEN RETURN clause.
#
# The Venue model uses a standard auto-generated integer primary key. This uses
# an IDENTITY column in Spanner. IDENTITY columns use a backing bit-reversed
# sequence to generate unique values that are safe to use for primary keys.
#
# The TicketSale model uses a bit-reversed sequence for primary key generation.
# This is achieved by creating a bit-reversed sequence and assigning the id
# column of the model a server_default value that gets the next value from that
# sequence.


class Singer(Base):
    __tablename__ = "singers"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    last_name: Mapped[str] = mapped_column(String(200), nullable=False)
    full_name: Mapped[str] = mapped_column(
        String, Computed("COALESCE(first_name || ' ', '') || last_name")
    )
    birthdate: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    picture: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    albums: Mapped[List["Album"]] = relationship(
        back_populates="singer", cascade="all, delete-orphan"
    )
    concerts: Mapped[List["Concert"]] = relationship(
        back_populates="singer", cascade="all, delete-orphan"
    )


class Album(Base):
    __tablename__ = "albums"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    release_date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    singer_id: Mapped[str] = mapped_column(ForeignKey("singers.id"))
    singer: Mapped["Singer"] = relationship(back_populates="albums")
    tracks: Mapped[List["Track"]] = relationship(
        back_populates="album",
        primaryjoin="Album.id == foreign(Track.id)",
        order_by="Track.track_number",
    )


class Track(Base):
    __tablename__ = "tracks"
    # This interleaves the table `tracks` in its parent `albums`.
    __table_args__ = {
        "spanner_interleave_in": "albums",
        "spanner_interleave_on_delete_cascade": True,
    }
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    track_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    duration: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    recorded_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime,
        nullable=True,
        # TODO: Enable this once 'func.now()' is mapped to CURRENT_TIMESTAMP
        # server_default=func.now(),
        server_default=TextClause("CURRENT_TIMESTAMP"),
    )
    album: Mapped["Album"] = relationship(
        back_populates="tracks",
        foreign_keys=[id],
        primaryjoin="Track.id == Album.id",
        remote_side="Album.id",
    )


# SQLAlchemy does not know what 'spanner_interleave_in' means, so we need to
# explicitly tell SQLAlchemy that `tracks` depends on `albums`, and that
# `albums` therefore must be created before `tracks`.
Track.__table__.add_is_dependent_on(Album.__table__)


class Venue(Base):
    __tablename__ = "venues"
    __table_args__ = (Index("venues_code_unique", "code", unique=True),)
    # Venue uses a standard auto-generated primary key.
    # This translates to an IDENTITY column in Spanner.
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(JSON, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    concerts: Mapped[List["Concert"]] = relationship(
        back_populates="venue", cascade="all, delete-orphan"
    )


class Concert(Base):
    __tablename__ = "concerts"
    venue_code: Mapped[str] = mapped_column(
        String(10), ForeignKey("venues.code"), primary_key=True
    )
    start_time: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, primary_key=True, nullable=False
    )
    singer_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("singers.id"), primary_key=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    singer: Mapped["Singer"] = relationship(back_populates="concerts")
    venue: Mapped["Venue"] = relationship(back_populates="concerts")
    ticket_sales: Mapped[List["TicketSale"]] = relationship(back_populates="concert")


class TicketSale(Base):
    __tablename__ = "ticket_sales"
    __table_args__ = (
        ForeignKeyConstraint(
            ["venue_code", "start_time", "singer_id"],
            ["concerts.venue_code", "concerts.start_time", "concerts.singer_id"],
        ),
    )
    id: Mapped[int] = mapped_column(
        BigInteger,
        Sequence("ticket_sale_id"),
        server_default=TextClause("GET_NEXT_SEQUENCE_VALUE(SEQUENCE ticket_sale_id)"),
        primary_key=True,
    )
    customer_name: Mapped[str] = mapped_column(String(200), nullable=False)
    seats: Mapped[list[str]] = mapped_column(ARRAY(String(20)), nullable=False)
    concert: Mapped["Concert"] = relationship(back_populates="ticket_sales")
    venue_code: Mapped[str] = mapped_column(String(10), ForeignKey("venues.code"))
    start_time: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, nullable=False
    )
    singer_id: Mapped[str] = mapped_column(String(36), ForeignKey("singers.id"))
