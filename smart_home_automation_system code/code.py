from abc import ABC, abstractmethod
import json

# Singleton for Smart Home Controller
class SmartHomeController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SmartHomeController, cls).__new__(cls)
        return cls._instance

    def control_device(self, device):
        print(f"Controlling device: {device.get_name()}")


# Device interface
class Device(ABC):
    @abstractmethod
    def get_name(self):
        pass


class Light(Device):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class Thermostat(Device):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class DeviceFactory:
    @staticmethod
    def create_device(device_type, name):
        if device_type == 'light':
            return Light(name)
        elif device_type == 'thermostat':
            return Thermostat(name)
        else:
            raise ValueError("Unknown device type")


# Adapter for third-party devices
class ThirdPartyDevice:
    def connect(self):
        print("Connecting to third-party device")


class ThirdPartyDeviceAdapter:
    def __init__(self, third_party_device):
        self.third_party_device = third_party_device

    def connect(self):
        self.third_party_device.connect()


# Strategy for automation modes
class AutomationStrategy(ABC):
    @abstractmethod
    def execute(self):
        pass


class EnergySavingMode(AutomationStrategy):
    def execute(self):
        print("Activating energy saving mode.")


class SecurityMode(AutomationStrategy):
    def execute(self):
        print("Activating security mode.")


class SmartHome:
    def __init__(self):
        self.strategy = None

    def set_strategy(self, strategy: AutomationStrategy):
        self.strategy = strategy

    def automate(self):
        if self.strategy:
            self.strategy.execute()
        else:
            print("No strategy set.")


# Observer for security alerts
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass


class User(Observer):
    def update(self, message):
        print(f"User notified: {message}")


class SecuritySystem:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

    def security_breach_detected(self):
        self.notify_observers("Security breach detected!")


# Command interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


# Concrete command for unlocking doors
class UnlockDoorCommand(Command):
    def __init__(self, door_lock_proxy):
        self.door_lock_proxy = door_lock_proxy

    def execute(self):
        self.door_lock_proxy.unlock()


class DoorLock:
    def unlock(self):
        print("Door unlocked.")


class DoorLockProxy:
    def __init__(self, door_lock, user_role):
        self.door_lock = door_lock
        self.user_role = user_role

    def unlock(self):
        if self.user_role == 'admin':
            self.door_lock.unlock()
        else:
            print("Access denied: insufficient permissions.")


class SmartHomeSystem:
    def __init__(self):
        self.controller = SmartHomeController()
        self.device_factory = DeviceFactory()
        self.security_system = SecuritySystem()
        self.home = SmartHome()
        self.commands = {}

    def add_device(self, device_type, name):
        device = self.device_factory.create_device(device_type, name)
        print(f"Added device: {device.get_name()}")
        self.controller.control_device(device)

    def set_automation_strategy(self, strategy_type):
        strategies = {
            "energy_saving": EnergySavingMode(),
            "security": SecurityMode()
        }
        if strategy_type in strategies:
            self.home.set_strategy(strategies[strategy_type])
        else:
            print("Unknown strategy")

    def activate_automation(self):
        self.home.automate()

    def detect_security_breach(self):
        self.security_system.security_breach_detected()

    def unlock_door(self, user_role):
        door_lock = DoorLock()
        proxy = DoorLockProxy(door_lock, user_role)
        command = UnlockDoorCommand(proxy)
        command.execute()

    def load_configuration(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            for device in config.get("devices", []):
                self.add_device(device["type"], device["name"])
            print("Configuration loaded.")


# Example usage
if __name__ == "__main__":
    smart_home = SmartHomeSystem()
    
    # Load configuration from a file
    smart_home.load_configuration("config.json")

    # Setting automation strategy
    smart_home.set_automation_strategy("energy_saving")
    smart_home.activate_automation()

    # Detecting a security breach
    user = User()
    smart_home.security_system.add_observer(user)
    smart_home.detect_security_breach()

    # Unlocking the door
    smart_home.unlock_door(user_role='user')  # Access denied
    smart_home.unlock_door(user_role='admin')  # Door unlocked