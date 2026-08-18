# Implementation Plan: New Custom Items & GPU Downloader UI

The user requested that we DO NOT overwrite existing items, but instead create entirely NEW items for the PC Access, Skip Mt. Moon, and GPU Spawning functionalities. Furthermore, the GPU Spawner should feature a "Search/List" UI that shows all GPUs in the game, allowing the player to select which one to spawn in battle.

## Proposed Changes

### 1. Revert Existing Item Changes
- Revert modifications made to `ITEM_VS_SEEKER`, `ITEM_FAME_CHECKER`, `ITEM_TEACHY_TV`, `ITEM_TRI_PASS`, and `ITEM_RAINBOW_PASS` in `src/data/items.json` (and the generated headers).

### 2. Create 3 New Key Items
We will add 3 brand new items to the game's database (`src/data/items.json`), complete with their own IDs, descriptions, and properties:
- **`ITEM_PC_ACCESS`**: Key Item. When used in the overworld, opens the PC Storage System.
- **`ITEM_SKIP_MT_MOON`**: Key Item. When used in the overworld, warps the player to Route 4.
- **`ITEM_RIG_DOWNLOADER`**: Key Item. When used in battle, opens a UI to select a GPU to download.

### 3. Build the GPU Downloader UI
Since building a full text-search UI from scratch in GBA C is extremely complex, we need a robust approach for the "Search" functionality.

**Option A (Scrollable List Menu - Recommended)**:
We create a custom fullscreen scrolling List Menu that displays all 386 GPUs in the game alphabetically. The player can quickly scroll through the list and press A to select the GPU they want.

**Option B (Text Input Search)**:
We invoke the game's built-in "Naming Screen" (normally used to name Pokémon). The player types the name of the GPU (e.g., "RTX 4090"). We then compare the typed text against all GPU names in the game and spawn the match. (If they typo, it fails).

**Option C (Pokédex Integration)**:
We temporarily open the Pokédex UI. The player navigates the Pokédex, selects a GPU, and we intercept that selection to spawn the GPU.

## User Review Required
> [!IMPORTANT]
> **Which UI approach do you prefer for the GPU Search?**
> Option A (Scrollable List Menu) is the most standard and user-friendly for a ROM hack. Is Option A acceptable, or do you strictly want a Naming Screen (Option B) where you type the name?

## Open Questions
- Should the `ITEM_RIG_DOWNLOADER` be usable ONLY in battle, or also in the overworld (to maybe spawn them directly into your party instead of battle)?

## Verification Plan
1. Compile the ROM and verify the 3 new items are obtainable via our cheat function.
2. Verify `ITEM_PC_ACCESS` opens the PC and safely returns.
3. Verify `ITEM_SKIP_MT_MOON` warps without glitching.
4. Verify `ITEM_RIG_DOWNLOADER` safely suspends the battle, opens the custom UI, returns to battle, and spawns the correct GPU.
