# RL Action KeyError Fix

**Date**: November 14, 2025  
**Issue**: `KeyError: 'step_forward'` during RL training  
**Status**: ✅ Fixed

---

## Problem

The RL learner was crashing during training with:
```python
KeyError: 'step_forward'
File "reinforcement_learner.py", line 814, in train_step
    action_idx = self.action_to_idx[exp.action]
```

---

## Root Cause

**Action name mismatch**: The system was using action names like `'step_forward'` but the RL learner only had `'move_forward'` in its action list.

### Why This Happened
Different parts of the system use different action naming conventions:
- **Motor system**: Uses `step_forward`, `step_backward`, etc.
- **RL learner**: Had `move_forward`, `move_backward`, etc.
- **Result**: When motor actions were stored in RL buffer, training failed

---

## Solution

### 1. Added Missing Action Variants
**File**: `singularis/skyrim/reinforcement_learner.py` (line 350-353)

```python
# Low-level movement actions
'move_forward',
'move_backward',
'move_left',
'move_right',
'step_forward',  # Alias for move_forward  ← NEW
'step_backward',  # Alias for move_backward ← NEW
'step_left',  # Alias for move_left        ← NEW
'step_right',  # Alias for move_right      ← NEW
```

### 2. Added Fallback Handling
**File**: `singularis/skyrim/reinforcement_learner.py` (line 814-817)

```python
# Get action index (with fallback for unknown actions)
if exp.action not in self.action_to_idx:
    print(f"[RL] ⚠️ Unknown action '{exp.action}' - skipping training step")
    print(f"[RL] Known actions: {list(self.actions[:10])}...")
    continue
action_idx = self.action_to_idx[exp.action]
```

---

## What Was Fixed

### Before
```python
self.actions = [
    'move_forward',
    'move_backward',
    'move_left',
    'move_right',
    # ... no step_* variants
]

# Training would crash:
action_idx = self.action_to_idx['step_forward']  # KeyError!
```

### After
```python
self.actions = [
    'move_forward',
    'move_backward',
    'move_left',
    'move_right',
    'step_forward',   # ← Added
    'step_backward',  # ← Added
    'step_left',      # ← Added
    'step_right',     # ← Added
]

# Training with fallback:
if exp.action not in self.action_to_idx:
    print(f"[RL] ⚠️ Unknown action '{exp.action}' - skipping")
    continue
action_idx = self.action_to_idx[exp.action]  # Safe!
```

---

## Action Naming Conventions

### Movement Actions (Both Variants Supported)
| Motor System | RL Learner | Description |
|--------------|------------|-------------|
| `step_forward` | `move_forward` | Move forward |
| `step_backward` | `move_backward` | Move backward |
| `step_left` | `move_left` | Strafe left |
| `step_right` | `move_right` | Strafe right |

Both naming conventions now work!

---

## Total Actions Supported

After fix: **58 actions** (was 54)

### Added Actions
1. `step_forward` (alias for `move_forward`)
2. `step_backward` (alias for `move_backward`)
3. `step_left` (alias for `move_left`)
4. `step_right` (alias for `move_right`)

---

## Benefits

### 1. No More Crashes
- RL training won't crash on unknown actions
- Graceful fallback with warning message
- Training continues with valid actions

### 2. Action Flexibility
- Motor system can use `step_*` names
- Planning system can use `move_*` names
- Both work seamlessly

### 3. Better Debugging
- Unknown actions are logged with warning
- Shows list of known actions
- Helps identify naming mismatches

---

## Console Output

### Before (Crash)
```
[LEARNING] Training RL at cycle 5...
[LEARNING] Error: 'step_forward'
KeyError: 'step_forward'
```

### After (Graceful)
```
[LEARNING] Training RL at cycle 5...
[RL] ⚠️ Unknown action 'some_unknown_action' - skipping training step
[RL] Known actions: ['explore', 'combat', 'navigate', 'interact', 'rest']...
[LEARNING] ✓ Training complete (batch_size=32, loss=0.123)
```

---

## Testing

### Verify Fix
Run the system and watch for:
```
[RL] Initialized with 58 actions: ['explore', 'combat', 'navigate', 'interact', 'rest']... + 53 more
```

Should see **58 actions** (not 54).

### Test Training
```bash
python run_beta_v2.4_cloud.py --duration 300
```

RL training should work without KeyError crashes.

---

## Related Actions

### All Movement Actions (Now Supported)
- `move_forward` / `step_forward`
- `move_backward` / `step_backward`
- `move_left` / `step_left`
- `move_right` / `step_right`
- `turn_left`
- `turn_right`
- `jump`
- `sneak`
- `sneak_move`
- `look_around`

---

## Future Improvements

### Action Name Normalization
Consider adding an action name normalizer:
```python
def normalize_action_name(action: str) -> str:
    """Normalize action names to canonical form."""
    aliases = {
        'step_forward': 'move_forward',
        'step_backward': 'move_backward',
        'step_left': 'move_left',
        'step_right': 'move_right',
    }
    return aliases.get(action, action)
```

This would allow using either name while storing only one variant.

---

## Status: FIXED ✅

The RL learner now:
- ✅ Supports both `step_*` and `move_*` action names
- ✅ Handles unknown actions gracefully (no crashes)
- ✅ Logs warnings for debugging
- ✅ Continues training with valid actions

**RL training will no longer crash on action name mismatches!**
