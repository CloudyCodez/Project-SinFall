# Project SinFall — 7DS Offline

An experimental Android offline server and patched client for local Grand Cross testing.
The Hub runs the game server on your phone. Gameplay uses loopback networking after setup.

## First tester release

**Start with [7DS-Offline-Hub.apk](https://github.com/CloudyCodez/Project-SinFall/releases/download/v0.1.0-tester.1/7DS-Offline-Hub.apk).**

1. Download and install the Hub on an ARM64 Android 8.0+ phone.
2. Open the Hub and tap **Set up / update game**, then **Download / install client**.
3. Allow the Hub to install apps when Android asks. Return and tap the download button again.
4. Keep setup open during download. Approve Android's game installation prompt.
5. Open the installed game and tap **Download assets and play**. Keep the setup screen open until it finishes.
6. Open the Hub, tap **Start Server**, then **Launch Game**. If the game opened before the server started, restart it from its title screen.

No PC, ADB, root, manual ZIP extraction or access to Android/data is required for this setup path.
Android still requires approval to install the Hub and game. Allow about **24 GB free** before starting;
the client download is about 3.1 GB and assets are about 13.5 GB. Use Wi-Fi for the initial download.
Once setup finishes, assets and local saves remain on the phone for offline use.

The client retains package ID `com.netmarble.nanagb`. Android cannot install it over an official
copy signed by a different key. Back up any existing data before deciding whether to uninstall that copy.
Uninstalling the Hub deletes its private profiles; uninstalling the game deletes its downloaded assets.

## Releases

- [Main tester release](https://github.com/CloudyCodez/Project-SinFall/releases/tag/v0.1.0-tester.1): Hub APK, verified client parts, installation manifest and checksums.
- [Separate asset release](https://github.com/CloudyCodez/Project-SinFall/releases/tag/assets-v0.1.0-tester.1): numbered asset ZIP packs, asset manifest and checksums.

The Hub and game fetch the required files automatically. The numbered client parts are download
segments, not separately installable APKs. The Hub streams them into one Android installation session.
Every completed download is checked with SHA-256. Interrupted files restart; completed parts and
installed asset packs are reused on retry. Keep setup in the foreground; background installation
and automatic download continuation after process termination are not supported in this tester.

## Tester scope

Includes local account management, phone-hosted server startup, Custom/Vanilla controls and the
preserved restoration work. This is an early tester, not a claim that every game system works.
See [mobile testing notes](MOBILE-TESTING.md) and [restoration scope](HUB-EXPANSION.md).
Some older notes describe USB setup and previous builds; the release flow above supersedes that installation procedure.

The new phone-only installer requires fresh-device testing. Build/signature and payload verification
do not establish successful installation or gameplay on every Android version. Report Android version,
device model, which setup step failed, and the exact error. Do not include private save data.

## Development and release preparation

Source includes the Hub, client setup activity, native server adapter, protocol definitions,
restored server handlers and research/build scripts. Signing keys, personal accounts, downloaded
tools, original APKs, extracted game content and generated binaries are excluded from Git.
Game assets are separate release downloads.

The existing game build tools require locally preserved input files; a clean checkout alone cannot
reconstruct the game APK. For this tester, the release builder adds an asset setup activity to the
preserved tested client APK while keeping its existing game DEX and native libraries.

Requirements: Python 3.11+, Java, Android SDK platform 35/build-tools 36.0.0, apktool 3,
local `.keys/7ds-local.jks` and its password file, `dist/7DS-Offline-Client.apk`,
`Research/PhoneClientDecoded/{res,AndroidManifest.xml,apktool.yml}`, `Research/RuntimeConfig`,
`AndroidHub/native/libgcserver.so`, and `PhoneVanillaData/files/bm`.
Use the original private signing key to preserve update compatibility. Never commit the key or password.

```powershell
python Tools/build_tester_release.py --output D:/7DS-Release
python Tools/verify_tester_release.py --output D:/7DS-Release
python Tools/publish_tester_release.py --output D:/7DS-Release
```

Set `SINFALL_JAVA` to the JDK's bin directory, `ANDROID_HOME` to the SDK, and `SINFALL_APKTOOL`
to the apktool JAR if the local defaults do not apply. Publishing requires authenticated `gh`,
an existing pushed `main` branch, and a verified payload. It creates draft releases, uploads files,
and publishes assets before the main tester release.

The native server can be regenerated with `Tools/generate_phone_server.py` and compiled using
`Tools/build_phone_native.py` with the Android NDK. Other legacy scripts retain local research paths.
