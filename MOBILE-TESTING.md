# 7DS Offline mobile testing

The Hub contains the ARM64 game server and the bootstrap HTTP server. Both listen on the phone's loopback address. Neither Wi-Fi nor an ADB reverse connection is required for gameplay after installation and asset transfer.

1. Open **7DS Offline Hub**.
2. Before creating a new profile, optionally enable **Grant all units to new profiles**.
3. Tap **Start Server**, then **Launch Game**.
4. Keep the server notification active while playing. If Android stops the service, reopen the Hub and start it again.

Packages:

- `dist/7DS-Offline-Hub.apk`
- `dist/7DS-Offline-Client.apk`

The client also needs the preserved game assets in `/sdcard/Android/data/com.netmarble.nanagb/files/bm`. The current USB install includes that transfer. Sharing the two APKs alone does not include the 13 GB asset cache.

Hub package: `com.phoenix.sevends`. Client package: `com.netmarble.nanagb`.

Local profile state is stored privately by the Hub. Reinstalling it with an update preserves that state; uninstalling the Hub removes it. The grant option applies to profile creation and does not reset existing progress.

Development builds reuse the restored desktop request handlers and native serializers. The Android adapter provides the TCP framing, local storage replacement, and UTF-16 encoding. The client retains the working game packet encoding while using the portable TCP transport.

## Permanent summon lineup

Only three native unit banners are active: Meliodas legendary draw (44 festival heroes), Gachiakuta (75 collab heroes), and normal draw (293 remaining heroes). Every character is assigned to one pool, using one base skin per character. Festival/collab draws have no ordinary filler. Normal rarity odds retain R 60%, SR 37%, SSR/UR 3%. Diamonds remain unlimited.

The client APK includes the matching summon and Coin Shop DB and installs it atomically into its own cache before Unity starts. The Hub APK must be updated with it. The other 728 DB tables and existing private profile files are preserved. Detailed pools and exact rates are in `dist/three-banner-pools.json`.

## Testing update: accounts, shop, growth and battle access

The Hub Accounts tab creates, switches and deletes profiles. Switch away from an account before deleting it. Restart the game after switching accounts.

The Server tab's stage diamond multiplier pays that many diamonds per successful story, Fort Solgres or normal Boss Battle clear, including repeats. Zero disables that clear reward; the testing diamond balance remains unlimited.

The Coin Shop includes all 293 normal-pool base units for 30 gold coins each. Festival and collab units are excluded from that added list. The five preserved boss-specific Holy Relic quick-craft tokens (543301-543305) each have a balance of 2,000,000,000. Other growth currencies and materials are replenished to 999,999, including Super Awakening coins and the full-growth token. Max awakening, Super Awakening and reset responses have native packet checks.

The client unlocks content gates and the lobby Battle shortcut without fabricating story completion. Fort Solgres and normal Boss Battle entry/clear handlers are restored. Final Boss, Tower and Demonic Beast battles still need further restoration; an unlocked menu alone does not establish that its battles work. Test Battle shortcut visibility, Fort Solgres and normal Boss Battles in this build.

Unlimited material balances use an enlarged client inventory stack capacity (2,147,483,647 per slot). Without this, the native login inventory builder splits each balance into thousands of ItemData objects and exhausts phone memory. Item IDs, total amounts and the native inventory stack builder remain intact; each seeded item occupies one stack.

Build catalog with `Tools/generate_local_gacha_catalog.py`, regenerate/compile the phone server, then build both APKs. `Tools/build_phone_client.py` packages the new cache automatically. The cache payload is specific to the preserved client version; update the classification and hash when upgrading game data.

## One-step level-90 and LR action fix

The updated Hub handles the native one-step package (10110 -> 14031), classic-hero level-90 token (13505 -> 15500), and LR evolution (10113 -> 14130). One-step settings and exact token IDs are checked against the preserved client configuration. The token upgrades to UR level 90 and six awakening stars, preserving ultimate level, Super Awakening, cosmetics, passive unlocks and team references. Repeating the request does not downgrade heroes above level 90.

LR evolution preserves awakening, Super Awakening and ultimate development, starts the LR at level 1, and uses its own level-100 experience curve. All 32 preserved LR variants, including collabs, pass evolution and subsequent EXP-potion packet tests on the phone's Android runtime. These tests run in an isolated temporary profile and do not modify your game account. Existing Fort Solgres, Boss Battle, Coin Shop, max awakening, Super Awakening and reset contracts also pass. Actual token/LR UI use still needs in-game confirmation.

After updating the Hub, unlock the phone, tap Start Server, and launch the game again. This fix requires only the Hub update; it uses the existing installed client and asset cache.
