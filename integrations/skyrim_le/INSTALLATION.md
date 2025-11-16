# Skyrim LE Bridge - Installation Guide

Connect Singularis AGI to Skyrim Legendary Edition.

---

## Prerequisites

1. **Skyrim Legendary Edition** installed
2. **SKSE 1.7.3** (NOT SKSE64)
   - Download: http://skse.silverlock.org/
   - Install: Extract to Skyrim folder, run `skse_loader.exe`
3. **Python packages** (in your `.venv-dml310`):
   ```powershell
   pip install mss vgamepad
   ```

---

## Step 1: Install SKSE Script

### Option A: Using Creation Kit (Recommended)

1. **Copy script source**:
   ```
   integrations/skyrim_le/SingularisExporter.psc
   → Skyrim/Data/Scripts/Source/SingularisExporter.psc
   ```

2. **Open Creation Kit**:
   - File → Data → Load `Skyrim.esm`

3. **Create new quest**:
   - Object Window → Character → Quest
   - Right-click → New
   - ID: `SingularisExporterQuest`
   - Priority: 80
   - Check "Start Game Enabled"
   - Check "Run Once"

4. **Attach script**:
   - Quest → Scripts tab
   - Add Script: `SingularisExporter`
   - Properties:
     - UpdateInterval: 0.5
     - MaxNPCs: 10
     - ExportPath: "Data/SKSE/Plugins/singularis_state.json"

5. **Compile**:
   - Gameplay → Compile Papyrus Scripts
   - Select `SingularisExporter.psc`
   - Compile

6. **Save plugin**:
   - File → Save
   - Name: `SingularisExporter.esp`

7. **Enable in launcher**:
   - Skyrim Launcher → Data Files
   - Check `SingularisExporter.esp`

### Option B: Manual Script Compilation

If you don't have Creation Kit:

1. **Install Papyrus Compiler**:
   - Comes with SKSE
   - Located: `Skyrim/Papyrus Compiler/`

2. **Compile script**:
   ```powershell
   cd "C:\Program Files (x86)\Steam\steamapps\common\Skyrim\Papyrus Compiler"
   
   PapyrusCompiler.exe ^
     "SingularisExporter.psc" ^
     -import="C:\Program Files (x86)\Steam\steamapps\common\Skyrim\Data\Scripts\Source" ^
     -output="C:\Program Files (x86)\Steam\steamapps\common\Skyrim\Data\Scripts"
   ```

3. **Create quest manually** (requires Creation Kit or xEdit)

---

## Step 2: Create Export Directory

```powershell
# Create SKSE plugins folder
mkdir "C:\Program Files (x86)\Steam\steamapps\common\Skyrim\Data\SKSE\Plugins"
```

---

## Step 3: Test SKSE Export

1. **Launch Skyrim via SKSE**:
   ```
   Skyrim/skse_loader.exe
   ```

2. **Load a save game**

3. **Check export file**:
   ```
   Skyrim/Data/SKSE/Plugins/singularis_state.json
   ```

   Should contain:
   ```json
   {
     "timestamp": 1700000000.0,
     "player": {
       "id": "player",
       "pos": [1234.5, 5678.9, 100.0],
       "health": 0.85,
       "in_combat": false,
       ...
     },
     "npcs": [...]
   }
   ```

4. **Verify updates**:
   - File should update every 0.5 seconds
   - Watch timestamp change

---

## Step 4: Configure Bridge in Python

Edit `config_local.py`:

```python
# Skyrim LE Bridge
SKYRIM_LE_ENABLED = True
SKYRIM_LE_STATE_FILE = "C:/Program Files (x86)/Steam/steamapps/common/Skyrim/Data/SKSE/Plugins/singularis_state.json"
SKYRIM_LE_SCREENSHOT_REGION = None  # Full screen, or (x, y, width, height)
```

---

## Step 5: Test Bridge

```python
from singularis.skyrim.skyrim_le_bridge import SkyrimLEBridge

# Initialize
bridge = SkyrimLEBridge()

# Test screenshot
screenshot = bridge.capture_screenshot()
print(f"Screenshot: {screenshot.size if screenshot else 'Failed'}")

# Test game state
state = bridge.read_game_state()
print(f"Game state: {state['player']['health'] if state else 'Failed'}")

# Test controller (with game running!)
from singularis.skyrim.actions import Action, ActionType
action = Action(ActionType.MOVE_FORWARD, duration=1.0)
bridge.execute_action(action)
```

---

## Step 6: Run with Real Game

Update `run_local_agi.py` to use bridge instead of mock data:

```python
from singularis.skyrim.skyrim_le_bridge import SkyrimLEBridge

# Initialize bridge
bridge = SkyrimLEBridge()

# In cycle():
screenshot = bridge.capture_screenshot()
game_snapshot = bridge.read_game_state()

# After decision:
if best_action:
    success = bridge.execute_action(best_action)
```

---

## Troubleshooting

### SKSE script not running

- **Check SKSE version**: Must be 1.7.3 for LE (not SKSE64)
- **Check quest enabled**: In Creation Kit, quest must be "Start Game Enabled"
- **Check script compiled**: `Data/Scripts/SingularisExporter.pex` should exist
- **Check SKSE log**: `My Documents/My Games/Skyrim/SKSE/skse.log`

### Export file not created

- **Check permissions**: SKSE needs write access to `Data/SKSE/Plugins/`
- **Run as admin**: Try running `skse_loader.exe` as administrator
- **Check path**: Verify `ExportPath` property in script

### vgamepad not working

- **Install driver**: vgamepad needs ViGEmBus driver
  - Download: https://github.com/ViGEm/ViGEmBus/releases
  - Install: `ViGEmBus_Setup_x64.exe`
- **Restart**: Restart PC after driver install
- **Check device**: Device Manager → Xbox 360 Controller should appear when script runs

### Screenshot capture fails

- **Install mss**: `pip install mss`
- **Check permissions**: Some games block screen capture
- **Windowed mode**: Try running Skyrim in windowed mode
- **Region**: Specify exact window region if full screen fails

### Controller input not working in game

- **Enable controller**: Skyrim Settings → Controls → Enable Gamepad
- **Disable Steam Input**: Steam → Skyrim → Properties → Controller → Disable Steam Input
- **Test manually**: Use vgamepad test script to verify controller works

---

## Performance Tips

### Reduce SKSE export frequency

In script properties:
```
UpdateInterval = 1.0  ; Update every 1 second instead of 0.5
```

### Limit NPC export

In script properties:
```
MaxNPCs = 5  ; Export only 5 nearest NPCs
```

### Reduce screenshot resolution

In bridge init:
```python
bridge = SkyrimLEBridge(
    screenshot_region=(0, 0, 640, 480)  # Lower resolution
)
```

---

## Next Steps

1. ✅ Install SKSE + script
2. ✅ Verify JSON export working
3. ✅ Test bridge in Python
4. ⏳ Integrate into `run_local_agi.py`
5. ⏳ Watch Lydia play Skyrim! 🎮✨

---

## Files Created

```
integrations/skyrim_le/
├── SingularisExporter.psc       # Papyrus script for SKSE
├── INSTALLATION.md              # This file
└── README.md                    # Overview

singularis/skyrim/
└── skyrim_le_bridge.py          # Python bridge module
```

---

## Support

If you encounter issues:

1. Check SKSE log: `My Documents/My Games/Skyrim/SKSE/skse.log`
2. Check Papyrus log: `My Documents/My Games/Skyrim/Logs/Script/Papyrus.0.log`
3. Test each component separately (SKSE → screenshot → controller)
4. Verify all prerequisites installed

**You're about to see Lydia play Skyrim LE with personality!** 🎮✨
