# Controller Menu Opening Issue - Troubleshooting

**Problem**: AGI thinks it's in inventory menu but visually still in game world

---

## 🔍 **Root Cause Analysis**

### **Session Evidence**
From `skyrim_agi_20251113_164246_4c8433b0.md`:

```
State says: "Scene: inventory"
Visual analysis says: "dark, atmospheric sky with swirling clouds", "crosshair in center"
Visual similarity: 0.995 (STUCK)
```

**Diagnosis**: The `OPEN_INVENTORY` action is being called, but the START button press isn't actually opening the menu in Skyrim.

---

## 🎮 **Possible Causes**

### **1. vgamepad Not Recognized by Skyrim**
**Issue**: Windows might not recognize the virtual Xbox controller  
**Solution**: Install ViGEmBus driver

```powershell
# Check if vgamepad is working
pip show vgamepad

# Install ViGEmBus (required for vgamepad)
# Download from: https://github.com/ViGEm/ViGEmBus/releases
```

### **2. Skyrim Not in Focus**
**Issue**: Controller input only works when game window has focus  
**Solution**: Ensure Skyrim is the active window

### **3. Controller Not Enabled in Skyrim**
**Issue**: Skyrim might have controller support disabled  
**Solution**: 
- Check Skyrim settings → Controls → Enable Gamepad
- Restart Skyrim after connecting virtual controller

### **4. Timing Issue**
**Issue**: Button press happens too fast for Skyrim to register  
**Solution**: Added 0.5s delay after START button press

---

## ✅ **Fixes Applied**

### **1. Added Debug Logging**

```python
# In controller_bindings.py
async def open_menu(ctrl, duration=0.0):
    print("[CONTROLLER] Opening menu with START button...")
    await ctrl.tap_button(XboxButton.START)
    await asyncio.sleep(0.5)  # Wait for menu to open
    print("[CONTROLLER] Menu should be open now")
```

### **2. Added Button Press Logging**

```python
# In controller.py
async def tap_button(self, button: XboxButton, duration: float = 0.1):
    if not self.dry_run:
        print(f"[VGAMEPAD] Tapping {button.value} button")
    self.press_button(button)
    await asyncio.sleep(duration)
    self.release_button(button)
```

---

## 🔧 **Verification Steps**

### **1. Check vgamepad Installation**
```bash
python -c "import vgamepad; print('vgamepad OK')"
```

### **2. Check Controller Initialization**
Look for this in console output:
```
OK Virtual Xbox 360 controller initialized
```

### **3. Check Button Presses**
Look for these in console output:
```
[CONTROLLER] Opening menu with START button...
[VGAMEPAD] Tapping START button
[CONTROLLER] Menu should be open now
```

### **4. Test in Skyrim**
1. Start Skyrim
2. Enable controller in settings
3. Run AGI
4. Watch for START button press
5. Verify menu actually opens

---

## 🚨 **If Menu Still Doesn't Open**

### **Option A: Use Keyboard Fallback**

```python
# In actions.py - add keyboard fallback for menu
if self.controller is not None:
    result = await self.controller.execute_action("menu")
    if not result:
        # Fallback to keyboard
        pyautogui.press('tab')
```

### **Option B: Force Keyboard Mode**

```python
# In skyrim_agi.py config
use_controller = False  # Force keyboard/mouse mode
```

### **Option C: Hybrid Mode**

```python
# Use controller for movement/camera, keyboard for menus
if action_type in [ActionType.OPEN_INVENTORY, ActionType.OPEN_MAP]:
    # Use keyboard
    pyautogui.press('tab')
else:
    # Use controller
    await self.controller.execute_action(action)
```

---

## 📊 **Expected Console Output**

### **Working Controller**
```
[CONTROLLER] Opening menu with START button...
[VGAMEPAD] Tapping START button
[CONTROLLER] Menu should be open now
[PERCEPTION] Scene detected: menu
[VISUAL] Menu interface visible
```

### **Broken Controller**
```
[CONTROLLER] Opening menu with START button...
[VGAMEPAD] Tapping START button
[CONTROLLER] Menu should be open now
[PERCEPTION] Scene detected: inventory  # ❌ Wrong!
[VISUAL] Dark sky, crosshair visible    # ❌ Still in game!
Visual similarity: 0.995 (STUCK)        # ❌ Nothing changed!
```

---

## 🎯 **Recommended Actions**

### **Immediate**
1. ✅ Check console for `[VGAMEPAD]` messages
2. ✅ Verify ViGEmBus driver installed
3. ✅ Enable controller in Skyrim settings
4. ✅ Test with manual controller input

### **Short-term**
1. Add keyboard fallback for critical actions
2. Implement hybrid controller/keyboard mode
3. Add visual verification after menu actions

### **Long-term**
1. Implement scene detection to verify menu opened
2. Add retry logic if action fails
3. Create controller health check system

---

## 📝 **Files Modified**

1. **`singularis/skyrim/controller_bindings.py`**
   - Added debug logging to `open_menu()`
   - Added 0.5s delay after START press

2. **`singularis/skyrim/controller.py`**
   - Added debug logging to `tap_button()`

---

## ✅ **Next Steps**

1. Run AGI and check console for `[VGAMEPAD]` messages
2. If no messages appear → vgamepad not initialized
3. If messages appear but menu doesn't open → Skyrim not recognizing controller
4. If menu opens but AGI doesn't detect it → scene detection issue

---

**Status**: Debugging tools added, awaiting next session test 🔍
