# Detecteur_Input_Snake_WL - Wayland-Compatible Keyboard Input Agent

Wayland-compatible version of the Snake keyboard input detector using `evdev` for direct keyboard event capture.

## Features

- **Wayland Support**: Uses evdev to read keyboard events directly from `/dev/input/event*` devices
- **Arrow Key Detection**: Captures UP, DOWN, LEFT, RIGHT arrow keys
- **Direction Output**: Sends direction integers (1=UP, 2=RIGHT, 3=DOWN, 4=LEFT) to game engine

## Requirements

```bash
pip install -r requirements.txt
```

### Permissions

This agent requires access to `/dev/input/event*` devices. You have two options:

**Option 1: Add user to input group (recommended)**
```bash
sudo usermod -a -G input $USER
# Log out and log back in for changes to take effect
```

**Option 2: Run with sudo (not recommended for production)**
```bash
sudo python3 src/main.py --device wlan0 --verbose
```

### Verify Permissions

Check your input device permissions:
```bash
ls -l /dev/input/event*
# Should show: crw-rw---- 1 root input ...
```

Test evdev access:
```bash
python3 -c "from evdev import list_devices; print(list_devices())"
```

## Usage

### Basic Usage

```bash
python3 src/main.py --device wlan0 --port 5670 --verbose
```

### Command-Line Options

- `--device <name>` : Network device for Ingescape autodiscovery (required if multiple NICs)
- `--port <num>` : Autodiscovery port (default: 5670)
- `--name <name>` : Published agent name (default: Detecteur_Input_Snake_WL)
- `--verbose` : Enable console logging
- `--help` : Show help message

## How It Works

1. **Device Detection**: Scans `/dev/input/event*` for keyboard devices with arrow key capabilities
2. **Event Monitoring**: Uses `select()` to monitor keyboard events with 0.1s timeout (non-blocking)
3. **Direction Mapping**: Converts arrow key presses to direction integers:
   - UP → 1
   - RIGHT → 2
   - DOWN → 3
   - LEFT → 4
4. **Ingescape Output**: Publishes direction via `direction` output (INTEGER type)

## Differences from Original

| Feature | Original (pynput) | Wayland (evdev) |
|---------|------------------|----------------|
| Wayland Support | ❌ No | ✅ Yes |
| Permissions | User-level | Requires input group or root |
| Event Source | X11/system API | `/dev/input/event*` |
| Blocking | Blocking listener | Non-blocking select() |

## Troubleshooting

### "No suitable keyboard device found"

**Problem**: Agent cannot find keyboard in `/dev/input/`

**Solution**: 
1. List available devices: `ls /dev/input/event*`
2. Check capabilities: `evtest` (install with `sudo apt install evtest`)
3. Verify arrow keys present in device capabilities

### "Permission denied" on `/dev/input/eventX`

**Problem**: User lacks permission to read input devices

**Solution**:
```bash
sudo usermod -a -G input $USER
# Log out and log back in
groups  # Verify 'input' group appears
```

### Agent doesn't receive arrow keys

**Problem**: Wrong keyboard device selected

**Solution**: 
1. Use `evtest` to identify correct device:
   ```bash
   sudo evtest  # Shows all devices
   # Press arrow keys to see which device responds
   ```
2. Modify `_find_keyboard_device()` to match your device name if needed

## Testing

Test the agent standalone:

```bash
# In separate terminal, monitor Ingescape logs
tail -f ~/Documents/Ingescape/logs/Detecteur_Input_Snake_WL.log

# Run agent
python3 src/main.py --device wlan0 --verbose

# Press arrow keys - you should see direction outputs logged
```

## Integration with S.N.A.K.E

Replace `Detecteur_Input_Snake` in launch script:

```bash
# In launch_snake_full.sh, change:
["Detecteur_Input_Snake"]="Detecteur_Input_Snake"

# To:
["Detecteur_Input_Snake_WL"]="Detecteur_Input_Snake_WL"
```

Ensure I/O mappings in `S.N.A.K.E.igssystem` connect `Detecteur_Input_Snake_WL.direction` → `Moteur_Jeu.direction`.



