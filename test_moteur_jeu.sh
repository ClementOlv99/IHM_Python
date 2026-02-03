#!/bin/bash
################################################################################
# S.N.A.K.E Game Engine Test Script
#
# This script tests the Moteur_Jeu (Game Engine) and Affichage (Display Agent)
# in isolation by sending a test level directly to the game engine.
#
# Requirements:
#   - Python 3.x with ingescape>=4
#   - Affichage requirements (requests>=2.31.0)
#   - Godot executable in Affichage/src/
#
# Usage:
#   ./test_moteur_jeu.sh
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEVICE="wlan0"  # For local testing
PORT=5670

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         S.N.A.K.E Game Engine Test Suite                  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if script is run from project root
if [ ! -d "Moteur_Jeu" ] || [ ! -d "Affichage" ]; then
    echo -e "${RED}❌ Error: Please run this script from the project root directory${NC}"
    echo "   cd /path/to/S.N.A.K.E"
    exit 1
fi

# Check Python dependencies
echo -e "${YELLOW}📦 Checking dependencies...${NC}"
cd Moteur_Jeu
if ! pip show ingescape > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️ Installing Moteur_Jeu dependencies...${NC}"
    pip install -r requirements.txt --break-system-packages 
fi
cd ..

cd Affichage
if ! pip show requests > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️ Installing Affichage dependencies...${NC}"
    pip install -r requirements.txt --break-system-packages 
fi
cd ..

echo -e "${GREEN}✅ Dependencies OK${NC}"
echo ""

# Create temporary directory for logs
LOG_DIR="test_logs"
mkdir -p "$LOG_DIR"

echo -e "${BLUE}🚀 Starting test sequence...${NC}"
echo ""

# Step 1: Launch Affichage (Display Agent + Godot Renderer) in separate kitty terminal
echo -e "${YELLOW}1️⃣  Launching Affichage (Display Agent) in new terminal...${NC}"

# Check if kitty is available
if ! command -v kitty &> /dev/null; then
    echo -e "${RED}❌ kitty terminal not found. Please install kitty or use default terminal.${NC}"
    echo "   Falling back to background mode..."
    cd Affichage
    python3 src/main.py --device "$DEVICE" --port $PORT --name "Affichage_Test" --verbose > "../$LOG_DIR/affichage.log" 2>&1 &
    AFFICHAGE_PID=$!
    cd ..
else
    # Launch Affichage in kitty terminal with title and keep it open
    kitty --title "🐍 S.N.A.K.E - Affichage & Godot" --hold \
        bash -c "cd Affichage && echo -e '\033[0;36m🎮 S.N.A.K.E Display Agent\033[0m' && echo -e '\033[0;33m📡 Launching Godot renderer...\033[0m' && echo '' && python3 src/main.py --device '$DEVICE' --port $PORT --name 'Affichage_Test' --verbose; echo ''; echo -e '\033[0;31m❌ Affichage stopped\033[0m'; read -p 'Press Enter to close...'" &
    AFFICHAGE_PID=$!
    
    # Also save logs to file by tailing in background
    sleep 1
fi

echo "   PID: $AFFICHAGE_PID"
echo "   Waiting for Godot to start..."
sleep 5  # Give more time for Godot window to appear

# Check if kitty terminal is still running (Affichage inside it)
if ! ps -p $AFFICHAGE_PID > /dev/null; then
    echo -e "${RED}❌ Affichage terminal closed unexpectedly${NC}"
    exit 1
fi
echo -e "${GREEN}   ✅ Affichage running in separate terminal${NC}"
echo ""

# Step 2: Launch Moteur_Jeu (Game Engine) in separate kitty terminal
echo -e "${YELLOW}2️⃣  Launching Moteur_Jeu (Game Engine) in new terminal...${NC}"

if command -v kitty &> /dev/null; then
    # Launch Moteur_Jeu in kitty terminal
    kitty --title "🎮 S.N.A.K.E - Game Engine" --hold \
        bash -c "cd Moteur_Jeu && echo -e '\033[0;36m🐍 S.N.A.K.E Game Engine\033[0m' && echo -e '\033[0;33m⚙️  Starting game logic...\033[0m' && echo '' && python3 src/main.py --device '$DEVICE' --port $PORT --name 'Moteur_Jeu_Test' --verbose; echo ''; echo -e '\033[0;31m❌ Game Engine stopped\033[0m'; read -p 'Press Enter to close...'" &
    MOTEUR_PID=$!
else
    # Fallback to background mode
    cd Moteur_Jeu
    python3 src/main.py --device "$DEVICE" --port $PORT --name "Moteur_Jeu_Test" --verbose > "../$LOG_DIR/moteur_jeu.log" 2>&1 &
    MOTEUR_PID=$!
    cd ..
fi

echo "   PID: $MOTEUR_PID"
echo "   Waiting for agent discovery..."
sleep 2

# Check if Moteur_Jeu is still running
if ! ps -p $MOTEUR_PID > /dev/null; then
    echo -e "${RED}❌ Moteur_Jeu failed to start${NC}"
    kill $AFFICHAGE_PID 2>/dev/null
    exit 1
fi
echo -e "${GREEN}   ✅ Moteur_Jeu running in separate terminal${NC}"
echo ""

# Step 3: Send test level data
echo -e "${YELLOW}3️⃣  Sending test level to game engine...${NC}"

# Create Python test sender script
cat > "$LOG_DIR/send_level.py" << 'EOF'
import ingescape as igs
import json
import time
import sys

# Test level: simple corridor with items
test_level = {
    "layout": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 2, 4, 0, 5, 0, 4, 0, 4, 0, 5, 0, 3, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    "cycle_duration": 0.3
}

print("Starting test sender agent...")
igs.agent_set_name("TestSender")
igs.start_with_device("Loopback Pseudo-Interface 1", 5670)

print("Creating output port...")
igs.output_create("level", igs.DATA_T, None)

print("Waiting for agent discovery...")
time.sleep(2)

print("Sending test level...")
level_json = json.dumps(test_level).encode()
igs.output_set_data("level", level_json)

print("✅ Test level sent successfully!")
print(f"   Layout size: {len(test_level['layout'][0])}x{len(test_level['layout'])}")
print(f"   Items: 3 apples (4), 2 traps (5)")
print(f"   Cycle duration: {test_level['cycle_duration']}s")

# Keep sender alive for a bit
print("\nPress Ctrl+C to stop test sender...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping sender...")

igs.stop()
EOF

python3 "$LOG_DIR/send_level.py" > "$LOG_DIR/sender.log" 2>&1 &
SENDER_PID=$!

echo "   PID: $SENDER_PID"
sleep 3

echo -e "${GREEN}   ✅ Test level sent${NC}"
echo ""

# Step 4: Test direction inputs
echo -e "${YELLOW}4️⃣  Sending test direction inputs...${NC}"

cat > "$LOG_DIR/send_directions.py" << 'EOF'
import ingescape as igs
import time

# Directions: 0=UP, 1=RIGHT, 2=DOWN, 3=LEFT
print("Starting direction test agent...")
igs.agent_set_name("TestDirections")
igs.start_with_device("Loopback Pseudo-Interface 1", 5670)

igs.output_create("direction", igs.INTEGER_T, None)

print("Waiting for discovery...")
time.sleep(2)

# Send movement sequence
directions = [
    (1, "RIGHT - initial direction"),
    (1, "RIGHT - continue"),
    (1, "RIGHT - continue"),
    (2, "DOWN - turn down"),
    (1, "RIGHT - turn right"),
]

for direction, desc in directions:
    print(f"Sending: {desc} ({direction})")
    igs.output_set_int("direction", direction)
    time.sleep(1)

print("✅ Direction test complete")
igs.stop()
EOF

python3 "$LOG_DIR/send_directions.py" > "$LOG_DIR/directions.log" 2>&1 &
DIRECTIONS_PID=$!

echo "   PID: $DIRECTIONS_PID"
echo -e "${GREEN}   ✅ Sending test inputs${NC}"
echo ""

# Summary
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                   Test Suite Running                      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${GREEN}Affichage:${NC}       PID $AFFICHAGE_PID ${CYAN}(kitty terminal)${NC}"
echo -e "  ${GREEN}Moteur_Jeu:${NC}      PID $MOTEUR_PID ${CYAN}(kitty terminal)${NC}"
echo -e "  ${GREEN}Level Sender:${NC}    PID $SENDER_PID"
echo -e "  ${GREEN}Input Sender:${NC}    PID $DIRECTIONS_PID"
echo ""
echo -e "${YELLOW}📊 Monitor logs in: $LOG_DIR/${NC}"
echo ""
echo -e "${CYAN}🖥️  Check the kitty terminal windows:${NC}"
echo "   • Affichage terminal shows Godot launch and HTTP logs"
echo "   • Moteur_Jeu terminal shows game engine debug output"
echo "   • Godot window should appear with the game rendering"
echo ""
echo -e "${GREEN}✨ The Godot window should show:${NC}"
echo "   • A corridor level with walls"
echo "   • Snake starting at entry point (tile marked '2')"
echo "   • 3 apples and 2 trap apples"
echo "   • Snake moving right automatically"
echo ""
echo -e "${BLUE}Press Ctrl+C in THIS terminal to stop all agents${NC}"
echo -e "${YELLOW}(The kitty windows will stay open to review logs)${NC}"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Stopping all agents...${NC}"
    
    # Kill test sender processes first
    kill $DIRECTIONS_PID 2>/dev/null || true
    kill $SENDER_PID 2>/dev/null || true
    
    # Kill main agent processes (this will also terminate their children, including Godot)
    if ps -p $MOTEUR_PID > /dev/null 2>&1; then
        echo "   Stopping Moteur_Jeu..."
        kill $MOTEUR_PID 2>/dev/null || true
    fi
    
    if ps -p $AFFICHAGE_PID > /dev/null 2>&1; then
        echo "   Stopping Affichage (and Godot)..."
        kill $AFFICHAGE_PID 2>/dev/null || true
    fi
    
    # Wait a bit for graceful shutdown
    sleep 2
    
    # Force kill if still running
    kill -9 $DIRECTIONS_PID 2>/dev/null || true
    kill -9 $SENDER_PID 2>/dev/null || true
    kill -9 $MOTEUR_PID 2>/dev/null || true
    kill -9 $AFFICHAGE_PID 2>/dev/null || true
    
    # Also kill any remaining Godot processes
    pkill -f "godot.*project.godot" 2>/dev/null || true
    
    echo ""
    echo -e "${GREEN}✅ All agents stopped${NC}"
    echo -e "${CYAN}💡 The kitty terminal windows are kept open for log review${NC}"
    echo -e "${CYAN}   Close them manually when done${NC}"
    echo -e "${BLUE}📋 Logs also saved in: $LOG_DIR/${NC}"
    exit 0
}

# Set trap for Ctrl+C
trap cleanup INT TERM

# Wait for user interrupt
wait
