"""
Skyrim LE Bridge - Game Integration

Connects the local AGI to Skyrim Legendary Edition:
1. Screenshot capture (mss)
2. Game state reading (SKSE JSON export)
3. Controller input (vgamepad)

Requirements:
- SKSE 1.7.3 for Skyrim LE
- Papyrus script or SKSE plugin exporting game state to JSON
- vgamepad for virtual Xbox controller
- mss for screen capture
"""

import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
from PIL import Image
import numpy as np
from loguru import logger

try:
    import mss
except ImportError:
    logger.warning("[SkyrimLE] mss not installed - screenshot capture disabled")
    mss = None

try:
    import vgamepad as vg
except ImportError:
    logger.warning("[SkyrimLE] vgamepad not installed - controller input disabled")
    vg = None

from .actions import ActionType, Action


class SkyrimLEBridge:
    """
    Bridge between Singularis AGI and Skyrim Legendary Edition.
    
    Handles:
    - Screenshot capture from game window
    - Game state reading from SKSE JSON export
    - Controller input via virtual Xbox 360 gamepad
    """
    
    def __init__(
        self,
        state_file: Optional[Path] = None,
        screenshot_region: Optional[tuple] = None
    ):
        """
        Initialize Skyrim LE bridge.
        
        Args:
            state_file: Path to SKSE JSON export file
                       Default: Skyrim/Data/SKSE/Plugins/singularis_state.json
            screenshot_region: (x, y, width, height) or None for full screen
        """
        # SKSE state file
        if state_file is None:
            # Try common Skyrim LE install locations
            steam_path = Path("C:/Program Files (x86)/Steam/steamapps/common/Skyrim")
            if steam_path.exists():
                state_file = steam_path / "Data/SKSE/Plugins/singularis_state.json"
            else:
                state_file = Path("singularis_state.json")  # Fallback to local
        
        self.state_file = Path(state_file)
        self.screenshot_region = screenshot_region
        
        # Virtual gamepad
        if vg is not None:
            self.gamepad = vg.VX360Gamepad()
            logger.info("[SkyrimLE] Virtual Xbox 360 gamepad initialized")
        else:
            self.gamepad = None
            logger.warning("[SkyrimLE] vgamepad not available - controller input disabled")
        
        # Screenshot capture
        if mss is not None:
            self.screen_capture = mss.mss()
            logger.info("[SkyrimLE] Screen capture initialized")
        else:
            self.screen_capture = None
            logger.warning("[SkyrimLE] mss not available - screenshot capture disabled")
        
        logger.info(f"[SkyrimLE] Bridge initialized")
        logger.info(f"  State file: {self.state_file}")
        logger.info(f"  Screenshot region: {self.screenshot_region or 'Full screen'}")
    
    def capture_screenshot(self) -> Optional[Image.Image]:
        """
        Capture screenshot from Skyrim window.
        
        Returns:
            PIL Image or None if capture failed
        """
        if self.screen_capture is None:
            logger.warning("[SkyrimLE] Screenshot capture not available")
            return None
        
        try:
            if self.screenshot_region:
                # Capture specific region
                x, y, w, h = self.screenshot_region
                monitor = {"top": y, "left": x, "width": w, "height": h}
            else:
                # Capture primary monitor
                monitor = self.screen_capture.monitors[1]
            
            screenshot = self.screen_capture.grab(monitor)
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            
            return img
        
        except Exception as e:
            logger.error(f"[SkyrimLE] Screenshot capture failed: {e}")
            return None
    
    def read_game_state(self) -> Optional[Dict[str, Any]]:
        """
        Read game state from SKSE JSON export.
        
        Returns:
            Game state dict or None if read failed
        """
        if not self.state_file.exists():
            logger.warning(f"[SkyrimLE] State file not found: {self.state_file}")
            return None
        
        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)
            
            return state
        
        except json.JSONDecodeError as e:
            logger.error(f"[SkyrimLE] Failed to parse state JSON: {e}")
            return None
        except Exception as e:
            logger.error(f"[SkyrimLE] Failed to read state file: {e}")
            return None
    
    def execute_action(self, action: Action) -> bool:
        """
        Execute action via virtual gamepad.
        
        Args:
            action: Action to execute
        
        Returns:
            True if executed successfully
        """
        if self.gamepad is None:
            logger.warning("[SkyrimLE] Gamepad not available")
            return False
        
        try:
            action_type = action.action_type
            duration = action.duration
            intensity = getattr(action, 'intensity', 1.0)
            
            # Movement actions
            if action_type == ActionType.MOVE_FORWARD:
                self._move_forward(duration, intensity)
            elif action_type == ActionType.MOVE_BACKWARD:
                self._move_backward(duration, intensity)
            elif action_type == ActionType.MOVE_LEFT:
                self._strafe_left(duration, intensity)
            elif action_type == ActionType.MOVE_RIGHT:
                self._strafe_right(duration, intensity)
            
            # Combat actions
            elif action_type == ActionType.ATTACK:
                self._attack(duration)
            elif action_type == ActionType.BLOCK:
                self._block(duration)
            elif action_type == ActionType.POWER_ATTACK:
                self._power_attack(duration)
            
            # Stealth
            elif action_type == ActionType.SNEAK:
                self._toggle_sneak()
            
            # Interaction
            elif action_type == ActionType.ACTIVATE:
                self._activate()
            
            # Wait
            elif action_type == ActionType.WAIT:
                time.sleep(duration)
            
            else:
                logger.warning(f"[SkyrimLE] Unknown action type: {action_type}")
                return False
            
            logger.debug(f"[SkyrimLE] Executed: {action_type}")
            return True
        
        except Exception as e:
            logger.error(f"[SkyrimLE] Action execution failed: {e}")
            return False
    
    # ========================================
    # Controller Input Methods
    # ========================================
    
    def _move_forward(self, duration: float, intensity: float = 1.0):
        """Move forward."""
        self.gamepad.left_joystick_float(x_value_float=0.0, y_value_float=intensity)
        self.gamepad.update()
        time.sleep(duration)
        self.gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
        self.gamepad.update()
    
    def _move_backward(self, duration: float, intensity: float = 1.0):
        """Move backward."""
        self.gamepad.left_joystick_float(x_value_float=0.0, y_value_float=-intensity)
        self.gamepad.update()
        time.sleep(duration)
        self.gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
        self.gamepad.update()
    
    def _strafe_left(self, duration: float, intensity: float = 1.0):
        """Strafe left."""
        self.gamepad.left_joystick_float(x_value_float=-intensity, y_value_float=0.0)
        self.gamepad.update()
        time.sleep(duration)
        self.gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
        self.gamepad.update()
    
    def _strafe_right(self, duration: float, intensity: float = 1.0):
        """Strafe right."""
        self.gamepad.left_joystick_float(x_value_float=intensity, y_value_float=0.0)
        self.gamepad.update()
        time.sleep(duration)
        self.gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
        self.gamepad.update()
    
    def _attack(self, duration: float):
        """Attack (right trigger)."""
        self.gamepad.right_trigger_float(value_float=1.0)
        self.gamepad.update()
        time.sleep(duration)
        self.gamepad.right_trigger_float(value_float=0.0)
        self.gamepad.update()
    
    def _block(self, duration: float):
        """Block (left trigger)."""
        self.gamepad.left_trigger_float(value_float=1.0)
        self.gamepad.update()
        time.sleep(duration)
        self.gamepad.left_trigger_float(value_float=0.0)
        self.gamepad.update()
    
    def _power_attack(self, duration: float):
        """Power attack (hold right trigger + forward)."""
        self.gamepad.left_joystick_float(x_value_float=0.0, y_value_float=1.0)
        self.gamepad.right_trigger_float(value_float=1.0)
        self.gamepad.update()
        time.sleep(duration)
        self.gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
        self.gamepad.right_trigger_float(value_float=0.0)
        self.gamepad.update()
    
    def _toggle_sneak(self):
        """Toggle sneak (left stick click)."""
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
        self.gamepad.update()
    
    def _activate(self):
        """Activate/interact (A button)."""
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.update()
    
    def cleanup(self):
        """Cleanup resources."""
        if self.screen_capture is not None:
            self.screen_capture.close()
        
        if self.gamepad is not None:
            # Reset gamepad to neutral
            self.gamepad.reset()
            self.gamepad.update()
        
        logger.info("[SkyrimLE] Bridge cleaned up")


# ========================================
# Helper Functions
# ========================================

def create_mock_screenshot(width: int = 224, height: int = 224) -> Image.Image:
    """
    Create mock screenshot for testing without game running.
    
    Args:
        width: Image width
        height: Image height
    
    Returns:
        Random noise image
    """
    img_array = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    return Image.fromarray(img_array)


def create_mock_game_state(
    health: float = 1.0,
    in_combat: bool = False,
    num_enemies: int = 0
) -> Dict[str, Any]:
    """
    Create mock game state for testing without SKSE export.
    
    Args:
        health: Player health (0-1)
        in_combat: Whether in combat
        num_enemies: Number of nearby enemies
    
    Returns:
        Mock game state dict
    """
    return {
        "timestamp": time.time(),
        "player": {
            "id": "player",
            "pos": [0.0, 0.0, 0.0],
            "facing_yaw": 0.0,
            "health": health,
            "stamina": 0.8,
            "magicka": 0.6,
            "sneaking": False,
            "in_combat": in_combat
        },
        "npcs": [
            {
                "id": f"enemy_{i}",
                "pos": [float(10 + i * 5), 0.0, 0.0],
                "health": 0.8,
                "is_enemy": True,
                "is_alive": True,
                "distance_to_player": 10.0 + i * 5,
                "has_line_of_sight_to_player": True,
                "awareness_level": 0.7
            }
            for i in range(num_enemies)
        ]
    }
