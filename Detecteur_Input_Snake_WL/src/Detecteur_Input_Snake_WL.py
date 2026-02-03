#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Detecteur_Input_Snake_WL (Wayland-compatible version)
#
#  Created by Ingenuity i/o on 2026/02/03
#
#  Copyright © 2025 Ingenuity i/o. All rights reserved.
#
import ingescape as igs
from evdev import InputDevice, categorize, ecodes, list_devices
import select
import sys

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Detecteur_Input_Snake_WL(metaclass=Singleton):
    def __init__(self):
        # outputs
        self._DirectionO = None
        
        # Find keyboard device
        self.keyboard_device = None
        self._find_keyboard_device()
    
    def _find_keyboard_device(self):
        """
        Find the first keyboard input device.
        Looks for devices with KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT capabilities.
        """
        devices = [InputDevice(path) for path in list_devices()]
        
        for device in devices:
            # Check if device has arrow key capabilities
            capabilities = device.capabilities()
            if ecodes.EV_KEY in capabilities:
                keys = capabilities[ecodes.EV_KEY]
                # Check for arrow keys
                if (ecodes.KEY_UP in keys and 
                    ecodes.KEY_DOWN in keys and 
                    ecodes.KEY_LEFT in keys and 
                    ecodes.KEY_RIGHT in keys):
                    self.keyboard_device = device
                    igs.info(f"Using keyboard device: {device.name} ({device.path})")
                    break
        
        if self.keyboard_device is None:
            igs.error("No suitable keyboard device found!")
            igs.error("Available devices:")
            for device in devices:
                igs.error(f"  - {device.name} ({device.path})")
            igs.error("\nYou may need to:")
            igs.error("  1. Run this agent with sudo (or add user to 'input' group)")
            igs.error("  2. Check /dev/input/event* permissions")
            sys.exit(1)

    # outputs
    @property
    def DirectionO(self):
        return self._DirectionO

    @DirectionO.setter
    def DirectionO(self, value):
        self._DirectionO = value
        if self._DirectionO is not None:
            igs.output_set_int("direction", self._DirectionO)
    
    def dir(self):
        """
        Wait for an arrow key press and return the corresponding direction.
        
        Direction mapping (matches original):
        - UP: 1
        - RIGHT: 2
        - DOWN: 3
        - LEFT: 4
        
        Returns:
            int: Direction value (1-4) or None if interrupted
        """
        if self.keyboard_device is None:
            igs.error("No keyboard device available")
            return None
        
        try:
            # Wait for keyboard events
            while True:
                # Use select to check for events (allows for interruption)
                r, w, x = select.select([self.keyboard_device], [], [], 0.1)
                
                if r:
                    for event in self.keyboard_device.read():
                        # Only process key down events (not key release)
                        if event.type == ecodes.EV_KEY:
                            key_event = categorize(event)
                            
                            # Check for key press (not release or hold)
                            if key_event.keystate == key_event.key_down:
                                # Map arrow keys to directions
                                if event.code == ecodes.KEY_UP:
                                    return 1
                                elif event.code == ecodes.KEY_RIGHT:
                                    return 2
                                elif event.code == ecodes.KEY_DOWN:
                                    return 3
                                elif event.code == ecodes.KEY_LEFT:
                                    return 4
        
        except (IOError, OSError) as e:
            igs.error(f"Error reading keyboard device: {e}")
            return None
        except KeyboardInterrupt:
            # Allow graceful shutdown
            return None


