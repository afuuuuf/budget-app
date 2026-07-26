from enum import Enum

class Status(str, Enum):
    CREATED = "Created Successfully"
    DELETED = "Deleted Successfully"
    UPDATED = "Updated Successfully"
    RESTORED = "Restored Successfully"