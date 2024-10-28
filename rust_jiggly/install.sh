#!/bin/bash

# Build the release version
cd rust_jiggly
cargo build --release

# Create directory for the service
mkdir -p ~/.local/bin/jiggly_muse_rust

# Copy binary to installation directory
cp target/release/jiggly_muse ~/.local/bin/jiggly_muse_rust/

# Create systemd service file
cat > ~/.config/systemd/user/jigglymuse-rust.service << EOL
[Unit]
Description=Rust JigglyMuse Mouse Movement Service
After=graphical-session.target

[Service]
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/$USER/.Xauthority
ExecStart=/home/$USER/.local/bin/jiggly_muse_rust/jiggly_muse
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
EOL

# Enable and start the service
systemctl --user daemon-reload
systemctl --user enable jigglymuse-rust
systemctl --user start jigglymuse-rust

echo "Rust JigglyMuse installed and started! Check status with: systemctl --user status jigglymuse-rust"
