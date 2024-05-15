from datetime import datetime

from sqlalchemy import String, Text, Boolean, BIGINT
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class File(Base):
    __tablename__ = "files"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    extension: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(Text)
    md5sum: Mapped[str] = mapped_column(String(255))
    clean: Mapped[bool] = mapped_column(Boolean)
    duplicated_md5: Mapped[bool] = mapped_column(Boolean, default=False)
    size: Mapped[int] = mapped_column(BIGINT)
    created: Mapped[int]
    modified: Mapped[int]

    def __repr__(self) -> str:
        return f"path={self.path!r} md5: {self.md5sum}"


class Image(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    extension: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(Text)
    md5sum: Mapped[str] = mapped_column(String(255))
    clean: Mapped[bool] = mapped_column(Boolean)
    duplicated_md5: Mapped[bool] = mapped_column(Boolean, default=False)
    size: Mapped[int] = mapped_column(BIGINT)
    created: Mapped[int]
    modified: Mapped[int]


