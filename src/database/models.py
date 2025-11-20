"""Data models for components."""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ComponentSpecs:
    """Component specifications."""
    # Required fields (no defaults) - must come first
    voltage_min: float
    voltage_max: float
    current_max: float
    package: str
    interfaces: List[str]
    pin_count: int
    # Optional fields (with defaults) - must come after required fields
    voltage_out: Optional[float] = None
    flash_memory_mb: Optional[float] = None
    ram_mb: Optional[float] = None
    temperature_range: Optional[List[float]] = None
    humidity_range: Optional[List[float]] = None
    pressure_range: Optional[List[float]] = None
    capacitance_nf: Optional[float] = None
    capacitance_uf: Optional[float] = None
    resistance_ohm: Optional[float] = None
    tolerance_percent: Optional[float] = None
    power_watts: Optional[float] = None
    frequency_mhz: Optional[float] = None
    gain_dbi: Optional[float] = None
    range_cm: Optional[List[float]] = None
    resolution: Optional[str] = None
    accel_range: Optional[str] = None
    gyro_range: Optional[str] = None
    capacity_mb: Optional[float] = None
    capacity_kb: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ComponentSpecs":
        """Create ComponentSpecs from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


@dataclass
class ComponentPricing:
    """Component pricing information."""
    price_usd: float
    currency: str = "USD"
    stock_status: str = "in_stock"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ComponentPricing":
        """Create ComponentPricing from dictionary."""
        return cls(**data)


@dataclass
class Component:
    """Component data model."""
    mpn: str
    manufacturer: str
    category: str
    description: str
    specs: ComponentSpecs
    pricing: ComponentPricing
    datasheet_url: str
    compatibility: Dict[str, Any]
    alternatives: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Component":
        """Create Component from dictionary."""
        return cls(
            mpn=data["mpn"],
            manufacturer=data["manufacturer"],
            category=data["category"],
            description=data["description"],
            specs=ComponentSpecs.from_dict(data["specs"]),
            pricing=ComponentPricing.from_dict(data["pricing"]),
            datasheet_url=data.get("datasheet_url", ""),
            compatibility=data.get("compatibility", {}),
            alternatives=data.get("alternatives", [])
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert Component to dictionary."""
        return {
            "mpn": self.mpn,
            "manufacturer": self.manufacturer,
            "category": self.category,
            "description": self.description,
            "specs": {
                "voltage_min": self.specs.voltage_min,
                "voltage_max": self.specs.voltage_max,
                "voltage_out": self.specs.voltage_out,
                "current_max": self.specs.current_max,
                "package": self.specs.package,
                "interfaces": self.specs.interfaces,
                "pin_count": self.specs.pin_count,
                "flash_memory_mb": self.specs.flash_memory_mb,
                "ram_mb": self.specs.ram_mb,
            },
            "pricing": {
                "price_usd": self.pricing.price_usd,
                "currency": self.pricing.currency,
                "stock_status": self.pricing.stock_status,
            },
            "datasheet_url": self.datasheet_url,
            "compatibility": self.compatibility,
            "alternatives": self.alternatives,
        }

