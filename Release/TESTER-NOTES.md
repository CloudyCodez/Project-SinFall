# Project SinFall — first Android tester

Download **7DS-Offline-Hub.apk** below to begin. The Hub downloads and verifies the game client;
the game's setup screen downloads and installs the separately hosted assets.

1. Install/open the Hub → **Set up / update game** → **Download / install client**.
2. Enable installation from the Hub when Android asks, return, and tap the button again.
3. Approve the client installation. Open the game → **Download assets and play**.
4. After assets finish, start the Hub server and launch the game.

ARM64 Android 8.0+; allow about 24 GB free before setup. Keep download screens open.
Android installation approval is required. No PC, root, ADB or manual asset copying is needed.
The game shares the official client's package name, so a differently signed installed copy can block installation.

Assets: [separate asset release](https://github.com/CloudyCodez/Project-SinFall/releases/tag/assets-v0.1.0-tester.1).
Do not manually install `.partNNN` files; the Hub combines them into one verified install session.

This is an experimental tester. The new installer needs fresh-device validation; there was no
Android device connected during release preparation. Some restored systems remain incomplete.
See the repository's testing notes for known restoration limits.

Retries reuse verified client parts and completed asset packs. A partial download restarts its current file.
Hub profiles are private to the Hub; uninstalling it removes those profiles.
