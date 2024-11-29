from enum import Enum

class ReservationStatus(Enum):
    WAITING = "WAITING"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"