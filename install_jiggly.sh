#!/bin/bash

# Create directory for the service
mkdir -p ~/.local/bin/jiggly_muse

# Copy files to installation directory
cp JigglyMuse.py ~/.local/bin/jiggly_muse/
cp requirements.txt ~/.local/bin/jiggly_muse/

# Install requirements
pip3 install -r requirements.txt

# Create systemd user service directory if it doesn't exist
mkdir -p ~/.config/systemd/user/

# Create systemd service file
cat > ~/.config/systemd/user/jigglymuse.service << EOL
[Unit]
Description=JigglyMuse Mouse Movement Service
After=graphical-session.target

[Service]
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/$USER/.Xauthority
ExecStart=/usr/bin/python3 /home/$USER/.local/bin/jiggly_muse/JigglyMuse.py
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
EOL

# Enable and start the service
systemctl --user daemon-reload
systemctl --user enable jigglymuse
systemctl --user start jigglymuse

echo "JigglyMuse installed and started! Check status with: systemctl --user status jigglymuse"
