from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import MetaData

# Define naming convention for MySQL constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Create metadata with naming convention
metadata = MetaData(naming_convention=convention)

@as_declarative(metadata=metadata)
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    # Add MySQL-specific table arguments
    __table_args__ = {
        'mysql_engine': 'InnoDB',  # Use InnoDB engine for transactions
        'mysql_charset': 'utf8mb4',  # Use utf8mb4 for full Unicode support
        'mysql_collate': 'utf8mb4_unicode_ci'  # Case-insensitive collation
    } 