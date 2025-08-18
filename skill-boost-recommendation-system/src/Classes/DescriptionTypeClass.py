from enum import Enum

class DescType(str, Enum):
    """
    Enumeration for describing different descriptor types.

    This Enum class is used to differentiate between various types of descriptors
    in a system that might handle different data or user profiles.

    Attributes:
        User (str): Represents a descriptor related to user entities.
        Data (str): Represents a descriptor related to data entities.
    """

    User = "User"  # Indicates a descriptor that pertains to user-related information.
    Data = "Data"  # Indicates a descriptor that pertains to data-related information.
