from dataclasses import dataclass, field


@dataclass
class DepartureJson:
    from_scheduled_time: str
    from_estimated_time: str
    platform: str
    length: str
    to_crs: str = field(default="???")
    to_name: str = field(default="???")
    to_scheduled_time: str = field(default="???")
    to_estimated_time: str = field(default="???")
