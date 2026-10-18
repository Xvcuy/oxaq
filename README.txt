OXAQ Server 1.0 (Linux edition)
===============================
Build:  ./build.sh   (Debian/Ubuntu, sudo, internet, ~20-40 min)  ->  OXAQ-Server-1.0.iso
Run:    VirtualBox/QEMU/USB. In VirtualBox enable Audio (for the boot sound) and a NAT network (internet).

Boot: dots -> big OXAQOS + your real boot-sound mp3 -> fade out -> console with header "OXAQ Server 1.0".
Included: Python 3 + pip + venv, Node.js + npm, mineflayer, git, curl, tmux, NetworkManager (DHCP; Wi-Fi: nmtui).
Commands: devkit | newbot NAME [host] [port] | oxaq-install-ai (Ollama, optional)
Notes: NOT test-built (my sandbox has no internet). Boot logs are hidden with "quiet"; the splash runs when tty1 logs in.
The fade uses setvtrgb, works only on the real Linux console (tty1), not over SSH.
