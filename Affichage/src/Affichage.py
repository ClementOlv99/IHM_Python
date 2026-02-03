#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Affichage - Display Agent & Godot Bridge
#
#  Created by Ingenuity i/o on 2026/01/30
#
#  Copyright © 2025 Ingenuity i/o. All rights reserved.
#
import ingescape as igs
import subprocess
import requests
import json
import time
import socket
from pathlib import Path


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Affichage(metaclass=Singleton):
    """
    Display agent that bridges Ingescape and Godot renderer.
    
    Responsibilities:
        1. Launch Godot executable on startup
        2. Receive display data from Moteur_Jeu
        3. Forward data to Godot HTTP server (localhost:5671)
    
    Receives:
        - DisplayI: JSON bytes (game state from engine)
    """
    
    def __init__(self):
        # Ingescape inputs
        self.DisplayI = None
        
        # Godot process management
        self.godot_process = None
        self.godot_url = "http://localhost:5671/game_data"
        self.godot_ready = False
        self.godot_log_file = None  # Track log file handle for cleanup
        
        # Launch Godot renderer on initialization
        self.launch_godot()
    
    def launch_godot(self):
        """
        Launch the Godot renderer executable in background.
        The Godot project will start an HTTP server on port 5671.
        """
        try:
            # Paths relative to Affichage.py location
            script_dir = Path(__file__).parent
            godot_executable = script_dir / "godot"
            project_file = script_dir / "project.godot"
            
            # Verify files exist
            if not godot_executable.exists():
                igs.error(f"Godot executable not found: {godot_executable}")
                return
            
            if not project_file.exists():
                igs.error(f"Godot project not found: {project_file}")
                return
            
            # Make executable if not already
            godot_executable.chmod(0o755)
            
            # Create logs directory if it doesn't exist
            log_dir = script_dir.parent / "test_logs"
            log_dir.mkdir(exist_ok=True)
            godot_log = log_dir / "godot.log"
            
            igs.info(f"Launching Godot renderer: {godot_executable}")
            igs.info(f"Project path: {script_dir}")
            igs.info(f"Godot logs: {godot_log}")
            
            # Open log file for Godot output
            godot_log_file = open(godot_log, 'w')
            self.godot_log_file = godot_log_file  # Store for cleanup
            
            # Launch Godot with verbose output
            # Output goes to both terminal and log file
            self.godot_process = subprocess.Popen(
                [
                    str(godot_executable),
                    "--path", str(script_dir),
                    "--verbose"  # Enable Godot's verbose output
                ],
                stdout=godot_log_file,
                stderr=subprocess.STDOUT,  # Merge stderr into stdout
                cwd=str(script_dir)
            )
            
            igs.info("Godot renderer launched - waiting for HTTP server...")
            igs.info(f"Monitor Godot output: tail -f {godot_log}")
            
            # Wait for Godot HTTP server port to be open (max 10 seconds)
            for attempt in range(20):
                time.sleep(0.5)
                try:
                    # Check if port 5671 is open (more reliable than HTTP request)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex(('localhost', 5671))
                    sock.close()
                    
                    if result == 0:
                        self.godot_ready = True
                        igs.info("✅ Godot HTTP server port 5671 is open!")
                        break
                except Exception as e:
                    igs.debug(f"Port check attempt {attempt}: {e}")
                    continue
            
            if not self.godot_ready:
                igs.warn("Godot HTTP server port not open after 10 seconds")
                igs.warn(f"Check Godot logs: {godot_log}")
            
        except Exception as e:
            igs.error(f"Failed to launch Godot: {e}")
            import traceback
            igs.error(traceback.format_exc())
    
    def forward_display_data(self, data_bytes):
        """
        Forward display data to Godot HTTP server.
        
        Args:
            data_bytes (bytes): JSON-encoded game state
        """
        if not data_bytes:
            return
        
        try:
            # Decode JSON data
            data_dict = json.loads(data_bytes.decode())
            
            # Send POST request to Godot server
            response = requests.post(
                self.godot_url,
                json=data_dict,
                timeout=1
            )
            
            if response.status_code == 200:
                # Success - no need to log every frame
                pass
            else:
                igs.warn(f"Godot server returned status {response.status_code}")
            
        except requests.exceptions.ConnectionError:
            if not self.godot_ready:
                # Still starting up, wait
                self.godot_ready = False
                igs.debug("Godot server not ready yet")
            else:
                igs.warn("Lost connection to Godot server")
        
        except requests.exceptions.Timeout:
            igs.warn("Timeout sending data to Godot")
        
        except json.JSONDecodeError as e:
            igs.error(f"Invalid JSON data received: {e}")
        
        except Exception as e:
            igs.error(f"Error forwarding data to Godot: {e}")
    
    def cleanup(self):
        """
        Terminate Godot process on shutdown.
        Called before agent stops.
        """
        if self.godot_process:
            igs.info("Shutting down Godot renderer...")
            self.godot_process.terminate()
            
            # Wait for process to end (max 5 seconds)
            try:
                self.godot_process.wait(timeout=5)
                igs.info("Godot renderer stopped")
            except subprocess.TimeoutExpired:
                igs.warn("Godot did not stop gracefully, forcing...")
                self.godot_process.kill()
                self.godot_process.wait()
        
        # Close Godot log file if open
        if self.godot_log_file:
            try:
                self.godot_log_file.close()
                igs.info("Godot log file closed")
            except Exception as e:
                igs.warn(f"Error closing Godot log file: {e}")




