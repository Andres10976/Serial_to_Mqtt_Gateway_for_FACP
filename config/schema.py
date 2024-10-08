from pydantic import BaseModel

class ThingsboardConfig(BaseModel):
    device_token: str
    host: str
    port: int

class SerialConfig(BaseModel):
    puerto: str

class RelayConfig(BaseModel):
    pin: int
    high_time: int
    low_time: int
    
class RelayMonitorConfig(BaseModel):
    alarm_pin: int
    trouble_pin: int
    publish_interval: int
    alarm_active_high: bool
    trouble_active_high: bool

class ConfigSchema(BaseModel):
    thingsboard: ThingsboardConfig
    serial: SerialConfig
    relay: RelayConfig
    relay_monitor: RelayMonitorConfig
    id_modelo_panel: int