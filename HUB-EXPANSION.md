# Hub expansion and server restoration

This is the active implementation scope, not a list of already shipped features.

## Verified recovery point

The installed client completed login inventory initialization and loaded the tavern after the inventory-stack fix. The previous unlimited material balances created millions of native ItemData stack objects and caused Android low-memory kills. The corrected client keeps one stack per seeded storage item. Recovery APKs are in `dist/recovery`.

Inventory access from the start is included in the newer built client at `dist/7DS-Offline-Client.apk` through the verified `Util.IsUnlockItemInventory` gate. That build has not yet replaced the installed recovery build.

## Modes and save safety

- Vanilla: finite balances, earned drops, validated and deducted costs, persistent progression. No unlimited material seed or automatic wardrobe/unit grants.
- Custom: the current unlimited-resource behavior.
- Preserve the existing Custom save. Vanilla requires a separate save namespace; changing modes must not import Custom currency, items, units or progression into a Vanilla grind.
- Server restart and client relogging must reload the selected account/mode. Never label a resource-only toggle as full Vanilla until costs, rewards, currencies and grants consistently obey it.
- Restore mission and Hero's Way tracking and claims, with persisted claim state and no duplicated rewards on relogging.

## Vanilla welcome and summons

- One-time 600-diamond welcome reward delivered through game mail, with delivery and claim flags persisted per account. This is the current interpretation of the requested sign-in bonus; do not repeat it on every login.
- All three banners include native R/SR filler while retaining their intended featured SSR/UR pool.
- Five-star rate: 2.5 times the preserved vanilla baseline for each applicable banner; reduce lower-rarity weight proportionally to keep total probability at 100 percent.
- Client rates and server weights must match exactly. Do not change only the server's rolls.

## Progression and farming priority

Hub priorities selected by the user: progression and farming controls, followed by account backups, server restart/status and reward settings. Include clear descriptions, bounded inputs, saved settings and farming presets. Controls must have actual server effects.

### EZ Farm

Show the toggle only for Vanilla accounts. The server must also enforce that restriction; hiding a button is insufficient.

- Fort Solgres: substantially richer and more plentiful reward drops.
- Gold dungeons: add full/one-step awakening currency and Super Awakening coins.
- EXP dungeons: add verified Perfect Equipment ticket item IDs.
- Awakening book dungeons: distribute boss-specific Holy Relic tokens by dungeon attribute; display the mapping in Hub.
- Distribute other enhancement materials to appropriate areas: awakening/evolution stones, anvils, hammers, engraving resources, LR/true-awakening resources and full-growth tokens as supported by the preserved item catalog.
- Include LR materials in Fort Solgres farming rewards. Custom balances remain unlimited for LR awakening, including collab LRs; verify the actual Legendary Rare awakening transaction.
- Both modes receive collab Holy Relic boxes in inventory. Vanilla gets a finite starter grant; Custom keeps unlimited boxes. Resolve the exact native box IDs and their opening/claim contracts before claiming support.
- Verify exact item IDs, dungeon attributes and native reward serialization before shipping. Do not substitute unrelated event tickets based only on similar icon names.
- EZ Farm should improve finite rewards, not reseed unlimited inventory.
- Disabled EZ Farm uses restored baseline rewards; losses must not grant rewards.

## Presentation

Generated title artwork: `Assets/Branding/7ds-offline-title-v1.png` — Meliodas and Escanor clashing, colored manga illustration, 7DS Offline title. Artwork is generated but not yet wired into the client title asset bundle. Preserve the original bundle and update its integrity manifest when replacing it.

## Required verification before the expanded install

- Fresh Vanilla account: no infinite seed, no leaked Custom save, Inventory available immediately.
- Welcome mail grants exactly 600 diamonds once; reconnect/duplicate claim cannot grant again.
- Finite summon, Coin Shop, development and awakening costs validated before state mutation.
- Earned stage drops persist across server restart and appear correctly in native inventory/reward screens.
- EZ Farm on/off controls real Fort Solgres rewards and does not affect Custom accounts.
- Mission and Hero's Way progress/claims persist without repeated grants.
- Banner probabilities sum to 100 percent and match the rates screen.
- Existing Custom account, working tavern startup and unlimited balances remain intact.
- Install over wireless ADB only after packet tests and build checks; reopen Hub and start the phone server.
