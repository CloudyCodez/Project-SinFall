# Grand Cross local testing in LDPlayer

Run `Tools/Launch-GrandCross-LDPlayer-Local.ps1` and leave its Frida session open. The launcher uses emulator-5554, starts the local game and content services when needed, restores ADB reverse ports, and installs the tested r21 native library. The current LD installation and decoded asset cache are prerequisites; this is not yet a standalone distributable APK.

The Cloud local account has completed tutorial flags and a two-billion-diamond testing wallet. Hero summon responses keep the wallet unchanged. Login restores the same balance, so it cannot be exhausted through local draws.

Hero banners use the preserved 2.113.1 client tables, with event banners reopened locally. The main hero banner (group 120) uses a uniform pool of all 412 preserved hero IDs; other groups use corresponding DB_gamble_group weights. Pulled skins are saved in `Server/local-test-account-skins.txt` and restored on server restart. This is a single local test account.

Verified on October 6, 2026: local login, main-menu access, Draw artwork, an eleven-hero summon through the original animation and results screen, and an unchanged two-billion-diamond balance. Screenshots are in `Research/gc-wallet.png` and `Research/gc-result.png`.

Also verified: opening story stage 100102, team setup, cutscene playback, and player/enemy combat turns. Native hero enhancement works; the user's Meliodas level-up is persisted in `Server/local-test-development.txt`. Passive ownership is saved in `Server/local-test-passives.txt`.

Cosmetics are automatically owned on each login: 5,916 matching client database entries (2,203 outfits, 1,858 weapons, 1,855 hairstyles). The native protocol's message limit is raised to 1 MiB because this wardrobe exceeds its default 64 KiB. Equipped groups are persisted in `Server/local-test-cosmetics.txt`. Generation is repeatable with `Tools/build_cosmetic_catalog.py`; the catalog uses original client IDs and resource groups. Story costume check (10101) and Closet shop info (10669) now have local responses.

This does not establish full game restoration. Story completion rewards, awakening,  other development actions, item/artifact draws, banner mileage rewards, duplicate-coin conversion, and live-service systems still require native verification or further implementation. The game/Hub mobile APK packaging remains unfinished.

October 6 restoration batch: the user confirmed outfit, weapon, and hairstyle equip/save works. Added normal hero evolution (10089), ultimate upgrade (10090), limit break (10096), 414 unlimited hero coin item types, persistent full team slots/associations, and quest start/progress/clear (10801-10803) using the preserved story chain. These new paths need user testing in LDPlayer. Evolution migrates passive/development state and team references, removes the previous skin, and persists the replacement. Level-up experience caps now include the saved limit-break count. Quest progress and clear state persist in `Server/local-test-quests.txt`; teams persist in `Server/local-test-teams.txt`.

`Tools/check_restoration_contracts.py` verifies 8 response layouts against native readers, story-chain IDs, inventory uniqueness, and preserved account files. It does not substitute for native menu/action testing. Quest reward item grants, region/basepoint reputation rewards, bulk development, super awakening, equipment development, and reconnect remain unfinished.
