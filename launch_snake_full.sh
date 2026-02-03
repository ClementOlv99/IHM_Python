#!/bin/bash
################################################################################
# S.N.A.K.E Distributed System Launcher
#
# Launches all required agents for the S.N.A.K.E game:
#   - Superviseur (game orchestrator)
#   - Generateur_Manuel (level generator)
#   - Generateur_Elements (item spawner)
#   - Createur_Niveau (level assembler)
#   - Detecteur_Input_Snake (keyboard input)
#   - Moteur_Jeu (game engine) ← YOUR FOCUS
#   - Affichage (display agent + Godot renderer) ← YOUR FOCUS
#   - Whiteboard (optional UI)
#
# Usage:
#   ./launch_snake_full.sh [device_name]
#
# Examples:
#   ./launch_snake_full.sh                    # Use loopback (local only)
#   ./launch_snake_full.sh en0                # Use network device en0
#   ./launch_snake_full.sh wlan0              # Use WiFi device
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
DEVICE="wlan0"
PORT=5670
LOG_DIR="snake_logs"

# Agent list (order doesn't matter due to autodiscovery)
declare -A AGENTS=(
    ["Superviseur"]="Superviseur"
    ["Generateur_Manuel"]="Generateur_Manuel"
    ["Generateur_Elements"]="Generateur_Elements"
    ["Createur_Niveau"]="Createur_Niveau"
    ["Detecteur_Input_Snake"]="Detecteur_Input_Snake"
    ["Moteur_Jeu"]="Moteur_Jeu"
    ["Affichage"]="Affichage"
)

# PID tracking
declare -A PIDS

echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║      ███████╗   ███╗   ██╗   █████╗   ██╗  ██╗  ███████╗    ║
║      ██╔════╝   ████╗  ██║  ██╔══██╗  ██║ ██╔╝  ██╔════╝    ║
║      ███████╗   ██╔██╗ ██║  ███████║  █████╔╝   █████╗      ║
║      ╚════██║   ██║╚██╗██║  ██╔══██║  ██╔═██╗   ██╔══╝      ║
║      ███████║   ██║ ╚████║  ██║  ██║  ██║  ██╗  ███████╗    ║
║      ╚══════╝   ╚═╝  ╚═══╝  ╚═╝  ╚═╝  ╚═╝  ╚═╝  ╚══════╝    ║
║                                                               ║
║            Distributed Snake Game System                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${BLUE}🎮 S.N.A.K.E Distributed System Launcher${NC}"
echo ""
echo -e "📡 Network device: ${GREEN}$DEVICE${NC}"
echo -e "🔌 Discovery port:  ${GREEN}$PORT${NC}"
echo -e "📁 Log directory:   ${GREEN}$LOG_DIR${NC}"
echo ""

# Check if running from project root
if [ ! -d "Moteur_Jeu" ] || [ ! -d "Affichage" ]; then
    echo -e "${RED}❌ Error: Run from project root directory${NC}"
    exit 1
fi

# Create log directory
mkdir -p "$LOG_DIR"
echo "" > "$LOG_DIR/launch.log"

# Install dependencies
echo -e "${YELLOW}📦 Checking dependencies...${NC}"
for agent in "${!AGENTS[@]}"; do
    if [ -f "${AGENTS[$agent]}/requirements.txt" ]; then
        cd "${AGENTS[$agent]}"
        pip install -q -r requirements.txt --break-system-packages 2>&1 | grep -v "already satisfied" || true
        cd ..
    fi
done
echo -e "${GREEN}✅ Dependencies ready${NC}"
echo ""

# Launch agents
echo -e "${BLUE}🚀 Launching agents...${NC}"
echo ""

for agent in "${!AGENTS[@]}"; do
    folder="${AGENTS[$agent]}"
    
    echo -ne "${YELLOW}Starting ${agent}...${NC}"
    
    cd "$folder"
    python3 src/main.py \
        --device "$DEVICE" \
        --port $PORT \
        --name "$agent" \
        --verbose \
        > "../$LOG_DIR/${agent}.log" 2>&1 &
    
    PID=$!
    PIDS[$agent]=$PID
    cd ..
    
    # Verify agent started
    sleep 0.5
    if ps -p $PID > /dev/null; then
        echo -e "\r${GREEN}✅ ${agent} started (PID: $PID)${NC}"
    else
        echo -e "\r${RED}❌ ${agent} failed to start${NC}"
        echo -e "   Check log: $LOG_DIR/${agent}.log"
    fi
    
    # Stagger launches to allow autodiscovery
    sleep 1
done

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              All Agents Running                           ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Display agent status
echo -e "${CYAN}📊 Agent Status:${NC}"
for agent in "${!PIDS[@]}"; do
    echo -e "   ${GREEN}●${NC} $agent (PID: ${PIDS[$agent]})"
done
echo ""

echo -e "${CYAN}🎮 Game Controls:${NC}"
echo "   • Arrow keys: Move snake"
echo "   • Space: Pause/Resume"
echo "   • ESC: Quit"
echo ""

echo -e "${CYAN}🖥️  Monitor:${NC}"
echo "   • Godot window should appear showing the game"
echo "   • Logs available in: $LOG_DIR/"
echo "   • Watch logs: tail -f $LOG_DIR/Moteur_Jeu.log"
echo ""

# Step: Send initial configuration to Superviseur to start the game
echo -e "${YELLOW}🚀 Starting game by sending configuration to Superviseur...${NC}"

# Create Python script to trigger Superviseur
cat > "$LOG_DIR/trigger_game.py" << 'EOF'
#!/usr/bin/env python3
import ingescape as igs
import time
import signal

# Signal handler
interrupted = False
def signal_handler(sig, frame):
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)

# Connect to Ingescape network
igs.agent_set_name("GameTrigger")
igs.output_create("config", igs.INTEGER_T, None)

# Start agent
igs.start_with_device("DEVICE_PLACEHOLDER", 5670)

# Wait for network connection
print("Waiting for Superviseur...")
time.sleep(3)

# Send initial config (1 = normal progression)
print("Sending initial configuration to Superviseur...")
igs.output_set_int("config", 1)

print("✅ Game started! Configuration sent to Superviseur.")
print("The level generation pipeline should now activate.")

# Keep alive briefly to ensure message is sent
time.sleep(2)

igs.stop()
EOF

# Replace DEVICE_PLACEHOLDER with actual device
sed -i "s/DEVICE_PLACEHOLDER/$DEVICE/" "$LOG_DIR/trigger_game.py"

# Run trigger script
python3 "$LOG_DIR/trigger_game.py" >> "$LOG_DIR/trigger.log" 2>&1 &
TRIGGER_PID=$!

# Wait for trigger to complete
sleep 5

echo -e "${GREEN}✅ Game initialization complete${NC}"
echo ""

echo -e "${YELLOW}⚠️  Press Ctrl+C to stop all agents${NC}"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down all agents...${NC}"
    
    # Kill all agents
    for agent in "${!PIDS[@]}"; do
        PID=${PIDS[$agent]}
        if ps -p $PID > /dev/null 2>&1; then
            echo -e "   Stopping $agent (PID: $PID)..."
            kill $PID 2>/dev/null || true
        fi
    done
    
    # Wait for graceful shutdown
    sleep 2
    
    # Force kill any remaining
    for agent in "${!PIDS[@]}"; do
        PID=${PIDS[$agent]}
        if ps -p $PID > /dev/null 2>&1; then
            echo -e "   Force stopping $agent..."
            kill -9 $PID 2>/dev/null || true
        fi
    done
    
    echo ""
    echo -e "${GREEN}✅ All agents stopped${NC}"
    echo -e "${BLUE}📋 Session logs: $LOG_DIR/${NC}"
    echo ""
    exit 0
}

# Set trap for Ctrl+C
trap cleanup INT TERM

# Monitor agents
echo -e "${CYAN}🔍 Monitoring agents (checking every 5s)...${NC}"
echo ""

while true; do
    # Check if any agent crashed
    for agent in "${!PIDS[@]}"; do
        PID=${PIDS[$agent]}
        if ! ps -p $PID > /dev/null 2>&1; then
            echo -e "${RED}❌ Agent $agent (PID: $PID) has stopped!${NC}"
            echo -e "   Check log: $LOG_DIR/${agent}.log"
            # Don't exit, let user decide
        fi
    done
    
    sleep 5
done
