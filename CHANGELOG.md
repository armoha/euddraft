# Changelog

## [0.11.0.1] - 2026.09.09
### Added
- Support custom `sectorSize` (`[main] sectorSize: 3~15`) in freeze-protected maps; the sector size is threaded into the in-game key calculation
- Support the fake empty `staredit\scenario.chk` (added by sector-size `SaveMap`) in freeze: decoy entries are preserved as obfuscation while the real chk block (locale 0x409) is selected for protection and placed where the in-game key search resolves it first

### Bugfix
- Fix freezeMpq glob selecting `.lib` import library instead of `.pyd` on Windows
- Fix `CallerProxy.Evaluate` i32 overflow with eudplib 0.81.0
- Fix MPQ crypt routines using 64-bit `unsigned long` on LP64 platforms, which corrupted hash-table decryption and failed freeze with `(keyfile) not found`

## [0.11.0.0] - 2026.09.07
### Changed
- Updated Python 3.13.5 → 3.14t (free-threaded build)

### Added
- Added GitHub Actions CI/CD for cross-platform release builds (Windows, macOS, Linux)
- Cross-platform `libepScriptLib` — now builds and ships for Linux, macOS, and Windows
- Added build documentation

### Improved
- Updated eudplib 0.81.0
- epScript `co_linetable` rewriting in Rust
- Merge consecutive constant DoActions in epScript parser
- Trim hot-path dispatch overhead in payload/const encoding
- Optimize `_memcpy`, `f_memcmp`, `f_randomize`, `EUDLoopPlayerUnit` loop branch conditions
- Lazy-load the epScript library
- Vendor stormlib-rs instead of submodule — no nested submodules needed
- freezeMpq is now a no-GIL module
- Improved `mkdist.py` to explicitly copy freezeMpq for incremental builds

### Bugfix
- Fix temporary values dropped while borrowed
- Prevent panic by overflow with `i32::MIN`/`i64::MIN`
- Fix incorrect tranwire for Goliath (was Wraith)
- Fix `train_unit_command` typo
- Replace deprecated `locale.getdefaultlocale()`

## [0.10.2.5] - 2025.08.04
### Bugfix
- Fixed a bug where repeated calls to `f_dbstr_addstr` caused the return value to increase unexpectedly.
- Fixed iterating `EUDVArray`.
  * Allow `EUDSetContinuePoint()` for iterating `EUDVArray`.
  * Type casting array items when iterating EUDVArray.
- Allow `@property` for `EUDStruct`.
  * For non-existing fields, `AttributeError` will be raised instead of `KeyError`.

### Improved
- Updated Python 3.11 -> 3.13.5
- Better duplicated switch cases error message.
- `EUDStruct.field = value;` type casts `value` for non-`ConstType` as well.

## [0.10.2.3] - 2025.04.26
### Bugfix
- Fixed `CUnit.cgive(newOwner)` not supported EUD error when `newOwner` has no unit.
- Fixed compile error on writing `CSprite` members.
- Fixed compile error on `CUnit.reset_buildq(bq1=0xE4)` for `CUnit` constant.
- Fixed not supported EUD error when there're multiple `EUDLoopNewCUnit`.
- Fixed `CUnit/CSprite` member comparison to use ptr instead of epd.

### Improved
- Remove randomizing the order of some built-in triggers/actions
- Reduce trigger in `CUnit.reset_buildq(bq1=0xE4)`

## [0.10.2.2] - 2025.03.18
### Bugfix
- epTrace: fixed invalid epmap file (Contributed by Xenon : https://cafe.naver.com/edac/134776)

### Improved
- Fixed missing header file error with GCC (Contributed by @zuhanit : https://github.com/armoha/euddraft/issues/158)

## [0.10.2.1] - 2025.02.03
### Bugfix
- Fix bug where `EUDLoopNewCUnit` would miss a unit (armoha/euddraft#132)
- Fixed error line print functions decreasing Unit limit when CCMU
- Fix `CUnit.cast(epd, ptr=ptr)` error

### Improved
- Update Python 3.12.8, update eudplib 0.80.0

## [0.10.1.6] - 2024.12.28
### Bugfix
- Fix `CUnit.reset_buildq()` to initialise `secondaryOrder`
- Fix `CUnit.flingyID` (word) and `Weapon.flingy` (dword) data size (reported by @Chromowolf)
- [epScript] Fixed bug where `EUDFuncPtr` could not be called when it was a function parameter (reported by Skywindragoon)
- [epScript] Fix bug where setting the current upgrade level does not work and modifies temporary variables instead (reported by @GGrush-SCMapper)
- Fixed a bug where `CUnit.cast` and `CSprite.cast` would create a trigger to copy variable (reported by @GGrush-SCMapper)
  * Fixed bug where `static var` with type `CUnit` or `CSprite` was initialised every time
- Fix `+= value;` compilation error in `CUnit` and `CSprite`
- Fixed bug where using ptr when assigning to `CUnitMember` or `CSpriteMember` didn't work (reported by @GGrush-SCMapper)

### Improved
- Added lazy evaluation of `EnumMember` values

## [0.10.1.5] - 2024.10.11
### Changed
- Renamed `CUnit.set_noclip`/`clear_noclip` (report by 고래밥은맛있어)

### Added
- `StringBuffer` can be used as argument for format printing function (reported by Yuuki-Asuna)

### Bugfix
- epScript: allow 0 as initial value for typed local variables
- Fix bug that caused QuickDebug map to be broken in euddraft 0.10.1.0-4 (reported by 블라인드)
- Fix compilation error in member comparison condition of variable scdata instance (reported by furina)

### Improved
- In cp read function, combine action of adding non-zero cpoffset to function call trigger

## [0.10.1.4] - 2024.10.09
### Bugfix
- Fixed bug where some triggers wouldn't execute after 4,294,967,295 game ticks (2,087 days in Fastest game), or after setting 0x57F23C to -1 (reported by snoqqqq)

### Improved
- Improve error message for format print functions when placeholders are more than arguments (reported by Yuuki-Asuna)

## [0.10.1.3] - 2024.10.05
### Changed
- Remove unused issueError parameter in Encode functions
- `scdata.flags.Flag = X;` only takes `true`, `false`, `1`, `0` or `EUDVariable`

### Added
- Add literal type hints for basic triggers, scdata and `EUDLoopPlayer`
  * Support autocomplete for `"string"` parameters in Python development environment
- scdata: add `ButtonSetMember`, change `CUnit.currentButtonSet` to ButtonSet type

### Bugfix
- Fixed `TrgUnit.rank` from word to byte
- Fixed compilation error in `EUDJump(variable)` (reported by 공나물)
- Fixed build error with input map missing `(listfile)` (reported by 귀여미)

### Improved
- Remove '[Warning]' text in front of type errors
- Add simple MPQ protection

## [0.10.1.1] - 2024.10.02
### Bugfix
- Fixed compilation error when turning off [freeze] protection

### Improved
- Update Korean localization

## [0.10.1.0] - 2024.09.30
### Changed
- Rewrite `mpqapi` in Rust, change usage of `MPQ` class:
```py
# Instantiate MPQs
mpq = MPQ.open(MPQpath)  # Open an MPQ
mpq = MPQ.create(create_path, sector_size=3, file_count=1024)  # create MPQ
# *advanced* Create an MPQ with the same content with a new sector_size
mpq = MPQ.clone_with_sector_size(MPQpath, create_path, sector_size)

# Read the MPQ internal file
file_content: bytes = mpq.extract_file(filepath)  # extract file from MPQ
# Get file names from (listfile)
filenames: list[str] = mpq.get_file_names_from_listfile()

# Add files to MPQ
mpq.add_file(name_to_use_in_MPQ, path_of_file_to_be_added, replace_existing=True)

# get/change the maximum number of files limit
maximum_number_of_files: int = mpq.get_max_file_count()
mpq.set_max_file_count(new_file_count_limit)

mpq.compact()  # defragment / compress MPQ
```
- Changed `MPQAddFile` to also accept the path of file to be added:
  * `MPQAddFile(name_to_use_in_MPQ, file_path_or_file_content)`
  Because `StormLib` requires a file system path, it is more advantageous to enter a file path. Entering the file contents as in the old usage creates a temporary file and passes the temporary file location to `StormLib`, with the overhead of copying the file contents.

### Bugfix
- epScript: `var globalVariable = constant_initial_value;` created an empty trigger scope, causing a `RecursionError` when there are at least 327 of these global variables (reported by snoqqqq)
- Fix autoupdate to not leave old files behind

### Improved
- Replace setuptools with maturin in eudplib packaging, make it easy to build eudplib
- Optimized `CUnit.check_buildq`
- Optimized `LoadMap`
- Optimized number of eudplib initialisation triggers

## [0.10.0.2] - 2024.09.26
### Bugfix
- Fixed bug in fixed line print functions; `StringBuffer.printfAt`, `DisplayTextAt`, etc. (reported by 고래밥은맛있어, 맛있는건못참아)
- scdata: Fix compilation error in 2 byte member `+=` (reported by 텔)
- Fix compilation error in `f_epdread_cp` function (reported by 맛있는건못참아)
- Fix compilation error when assigning 0 to `CUnit` variable (reported by @Chromowolf)
- Fix `f_rand` returned 0 (reported by @Chromowolf)

### Improved
- Add stack trace to warning messages (reported by 콤)
- Optimized the number of triggers in `EUDByteReader.readbyte()`, `f_raise_CCMU()`, `f_getcurpl()`

## [0.10.0.1] - 2024.09.23
### Bugfix
- [MSQC] Fix mouse button event compilation error (reported by 텔)
- Bugfix: `DisplayTextAt`, `DisplayTextAllAt` compilation error fixed (reported by @dr-zzt)
- Fixed bug with Korean translation text not showing up

### Improved
- Optimize `f_rand()` function and fix to not change CurrentPlayer
- Added error message for invalid arguments when creating `EUDVariable`, `EUDXVariable`, `EUDVArray`

## [0.10.0.0] - 2024.09.22
### Changed
- `EUDArray` now uses EPD by default
  * For backward compatibility with existing code, `EPD(EPD of ConstExpr)` returns EPD as is (with warning message)
  * Added `ptrEUDArray` and `errorReapplyEPD` flags to `[main]`
  ```ini
  [main]
  ptrEUDArray : True
  errorReapplyEPD : True
  :: If the `ptrEUDArray` flag is turned on, EUDArray will use the ptr address as before
  :: If the `errorReapplyEPD` flag is turned on, applying the EPD function to a constant EPD value will result in an error
  ```
  * If the `ptrEUDArray` flag is on, EPD is not calculated when array is only used in passing to or from function boundaries. When array element is accessed, EPD calculation trigger is added at array declaration on demand.
- epScript: Added type variable feature.
  * Reference types (`EUDArray`, `EUDVArray`, epScript `object` (=`EUDStruct`), `EUDStructArray`, `CUnit`, `CSprite`) can only be assigned to the same type. Operations such as `+=,` `-=,` `*=,` `/=` are not supported because they can change to invalid addresses.
  * Value types (such as `LocalLocale`, `TrgUnit`, `Weapon`, `UnitOrder`, `Flingy`, `Sprite`, `Image`, `TrgPlayer`, `Upgrade`, `Tech`, etc.) supports assigment and other operations like `+=`, `-=`, ...
```js
// Syntax
var name: Type = initialValue;
static var name: Type = initialValue;
var name1: type1, name2: type2, name3: type3 = initial1, initial2, initial3;

// Example
function onPluginStart() {
    // Link hatchery to larvae
    var hatchery: CUnit = 0;
    foreach(unit : EUDLoopPlayerCUnit()) {
        if (unit.unitType == "Zerg Hatchery") {
            hatchery = unit;
        }
    }
    foreach(unit : EUDLoopPlayerCUnit()) {
        if (unit.unitType == "Zerg Larva") {
            larva.connectedUnit = hatchery;
        }
    }
}
```
- epScript: Relative Path Import Bug Fixes and Behavior Changes
  * Fixed a bug that caused modules to be duplicated every time a relative path import was made.
  * If a path can be imported with an absolute path, it will be replaced with an absolute path import.
  * Consider making the path accessible with `sys.path.insert(1, path)` when a parent folder prevents importing, or consider adding `__init__.py` when importing between files inside a folder to be recognized as a Python package.
- Changed behavior of epScript `object` (=`EUDMethod` of `EUDStruct`) to not duplicate triggers for each static instance they call
- Change cast behavior: don't copy the value, just use it as is and apply the type.
- Simplified `EUDVariable` constructor: `EUDVariable` now only accepts an initial value as a constructor.
  * For advanced initialization options, use `EUDXVariable(epd, modifier, initial value, (optional) bitmask 0xFFFFFFFF by default)`.
- Fix `f_getuserplayerid()` and `EUDLoopPlayer` to return `TrgPlayer` type
- Change `DBString` memory layout
- `Db` initialized with `"string"` will raise error if string has a null byte in the middle
- `DBString` will raise error with a \0 null byte in the middle
- `objFieldN` flag won't change the maximum number of objects (=32768)

### Added
- `EUDVArray` supports epScript `foreach` loop
```js
const varr = EUDVArray(10)(py_range(10));
foreach(x : varr) {
    printAll("{}", x);
    if (x >= 5) break;
}
// prints: 0, 1, 2, 3, 4, 5
```
- scdata: Added current upgrade/tech level read/write
  * Optimized to cache epd and subp for upgrade/tech and player, so that if they are unchanged or only change them with `+= 1`, epd and subp are not recalculated, and instead reuse the previously calculated results. (See Improved section)
```js
// Upgrade[TrgPlayer] = New_Upgrade_Level;
const infantryWeapon = Upgrade("Terran Infantry Weapon");
foreach(player : EUDLoopPlayer()) {
   infantryWeapon[player] = 1;
}

// const upgrade_level = Upgrade[TrgPlayer];
printAll("current Terran Infantry Weapon level for P1: {}", infantryWeapon[player]);

// Tech[TrgPlayer] = new Tech level;
var spiderMines: Tech = "Spider Mines";
spiderMines[P1] = 1;

// const hasResearched = Tech[TrgPlayer]; // return 1 if tech is non-zero
once (Tech("Stim Pack")[P1]) {
    printAll("Red researched stim pack.");
}
```
- scdata: Added `TrgUnit` members:
  * `TrgUnit.unitBoundsLT`
  * `TrgUnit.unitBoundsRB`
  * `TrgUnit.unitBoundsL`
  * `TrgUnit.unitBoundsT`
  * `TrgUnit.unitBoundsR`
  * `TrgUnit.unitBoundsB`
- Added `UnitGroup.length` (suggested by 쥬뱅)
- `EUDLightBool` can be initialized with `True` (suggested by @Chromowolf)
- Added `suppressWarnings` flag on `[main]` (suggested by Ultraviolet)
  * This suppresses every warnings in Python
  * EUD Editor 2 has longstanding issue of not distinguishing warning and error. You can workaround this issue with `suppressWarnings` flag.
- Added simple obfuscation to constant strings for print functions

### Bugfix
- Fixed `<`, `>` for `EUDVariable` (reported by 고래밥은맛있어)
- epScript: fixed incorrect line number on error (reported by @Chromowolf)
- (https://github.com/armoha/eudplib/pull/28) fixed infinite loop in `EUDLoopRange(start, end)` when `start == end` (contributed by 고래밥은맛있어)
- Fixed constant CUnit instance e.g. `CUnit(EPD(0x59CCA8))`
- Fixed `EUDStruct.cast` could return `None` when subclass overrides `__init__` without `_from` parameter
- Fixed bug where Python warning messages were not printed
- Fixed bugs with `CUnit(constant)`, `CSprite.from_ptr (constant)`

### Improved
- Improved epd and cp read functions to share their triggers
- Performance improvements for `EUDVArray`, `PVariable`, `f_repmovsd_epd`, etc.
- Fixed `$L` and `setloc_epd` to also warn of location name misspellings
- Added compilation error when string count exceeds 65535
- Improved `ConstExpr` division compile error message
- scdata: Improved error message for `UnsupportedMember`
- scdata: added caching to improve performance with ArrayMember
  * When accessing a non-4-byte member, if the variable is unchanged, it will reuse the previously calculated result instead of recalculating epd, subp.
  * `scdataInstance += 1;` is specialized to update all cache values, so cache invalidation and recalculation does not occur.
```js
var unit: TrgUnit = dwrand() % 228;
// (1)
unit.maxShield = 10000;
unit.elevation = 1;

unit = dwrand() % 228;
// (2)
unit.maxHp = 10000 * 256;
// (3)
unit.hasShield = false;

/*
ArrayMember of the scdata instance wrapping EUDVariable will cache derived values for members whose stride is not 4 bytes.
All non-4-byte-stride member accesses will perform a cache check condition and update derived values if the value has changed.

Because unit uses 1-byte (elevation, hasShield) and 2-byte (maxShield) members, the  cache check condition detects a value change at (1), and every derived values are updated; unit / 4, unit % 4, unit / 2 and 2*(unit % 2).
(member usages affect globally to every usages, even retroactively)
`var unit` is unchanged between unit.maxShield and unit.elevation, so unit.elevation does not run update for derived values.

`unit`'s value has changed at (2) ,but unit.maxHp is a 4-byte member, so it does not run perform a cache check condition.
unit.hasShield access at (3) will perform a cache check condition and may update derived values.
*/

// The cache is associated with the wrapped variable, not the scdata instance.
// If cast interprets the same variable as multiple types, the bitmask range can be extended by the largest type.
var v = 23;  // 0x17
const p = TrgPlayer.cast(v);
P12.cummulativeMineral = 9999;
// TrgPlayer's bitmask is 0xF
// If that's all we've written, we'll print out the cumulative gas for P8 (playerID=7)
printAll("{}", p.cumulativeGas);  

// If we cast variable v to a TrgUnit, and access a non-4-byte-stride member,
// the bitmask of variable v is expanded from 0xF (TrgPlayer) to 0xFF (TrgUnit) globally:
const u = TrgUnit.cast(v);  
printAll(u.gasCost, 200);

// This acts globally, so,
// The above printAll("{}", p.cumulativeGas); will print 9999,
// which is P24's cumulative gas = P12's cumulative minerals.
```
- Miscellaneous bug fixes and improvements

## [0.9.11.2] - 2024.09.07
### Changed
- [MSQC] local condition allows not only `EUDVariable`, `EUDXVariable`, `EUDLightVariable`, `EUDLightBool` but *any object* registered by `EUDRegisterObjectToNamespace` (suggested by 고래밥은맛있어)

### Bugfix
- Bugfix: `CUnit`/`CSprite.from_ptr(ptr)` returns old value when ptr is 0 (reported by @dr-zzt)
- Fixed bug with CUnit/CSprite not caching ptr/epd

### Improved
- Change `f_getuserplayerid` and `EUDLoopPlayer` to return `TrgPlayer`.
  * Considering that in the future `f_getuserplayerid` will return a subclass of `TrgPlayer` and provide local/desync offsets as members
- eudplib 0.77.9 update
- Updated Korean translation files

## [0.9.11.1] - 2024.09.04
### Changed
- Update known features in scdata (contributed by DarkenedFantasies)
  * CSprite.flags.Flag4 (0x10) -> `CSprite.flags.IsSubunit`: sorts sprite elevation higher, so that subunits always appear above base unit
  * CSprite.unknown0x12 -> `CSprite.grpWidth`
  * CSprite.unknown0x13 -> `CSprite.grpHeight`
  * CUnit/TrgUnit.movementFlags.Unknown -> `CUnit/TrgUnit.movementFlags.BrakeOnPathStep`: unit decelerates when reaching the end of current path segment
  * CUnit.ghostNukeMissile -> `CUnit.ghostNukeDot`: [points to CThingy of nuclear dot](https://github.com/BoomerangAide/GPTP/blob/ce321f0fa83174aee741b91f1b2eaec30300773e/GPTP/hooks/orders/spells/nuke_orders.cpp#L204-L222)
  * TrgUnit.AIFlags -> `TrgUnit.dontBecomeGuard`
  * Tech.requirementOffset -> `Tech.researchRequirementOffset`, `Tech.techUseRequirementOffset`

### Added
- Added multi-dimensional object array, added bound check for object array (suggested by 고래밥은맛있어)
```js
// epScript example)
object Point { var x, y; };

function onPluginStart() {
    // static allocation of objects
    const point2x3 = (Point * 3 * 2)();
    foreach(i : py_range(2)) {
        point2x3[i] = (Point * 3)();
        foreach(j : py_range(3)) {
            point2x3[i][j] = Point()
        }
    }

    point2x3[2];  // index out of bound error
    point2x3[0][3];  // index out of bound error
}
```
- Added scdata members
  * `TrgPlayer.unitColor`: byte
  * `TrgPlayer.minimapColor`: byte
  * `TrgPlayer.remainingGamePause`: byte
  * `TrgPlayer.missionObjectives`: TrgString
  * `TrgPlayer.unitScore`: dword
  * `TrgPlayer.buildingScore`: dword
  * `TrgPlayer.killScore`: dword
  * `TrgPlayer.razingScore`: dword
  * `TrgPlayer.customScore`: dword
- Added scdata flag members
  * `CUnit.pathingFlags`
    - `CUnit.pathingFlags.HasCollision` (0x01)
    - `CUnit.pathingFlags.IsStacked` (0x02)
    - `CUnit.pathingFlags.Decollide` (0x04)
  * `TrgUnit.groupFlags`
    - `TrgUnit.groupFlags.Zerg` (0x01)
    - `TrgUnit.groupFlags.Terran` (0x02)
    - `TrgUnit.groupFlags.Protoss` (0x04)
    - `TrgUnit.groupFlags.Men` (0x08)
    - `TrgUnit.groupFlags.Building` (0x10)
    - `TrgUnit.groupFlags.Factory` (0x20)
    - `TrgUnit.groupFlags.Independent` (0x40)
    - `TrgUnit.groupFlags.Neutral` (0x80)
  * `TrgUnit.movementFlags`: Same as `CUnit.movementFlags`.
    - `TrgUnit.movementFlags.OrderedAtLeastOnce` (0x01)
    - `TrgUnit.movementFlags.Accelerating` (0x02)
    - `TrgUnit.movementFlags.Braking` (0x04)
    - `TrgUnit.movementFlags.StartingAttack` (0x08)
    - `TrgUnit.movementFlags.Moving` (0x10)
    - `TrgUnit.movementFlags.Lifted` (0x20)
    - `TrgUnit.movementFlags.Unknown` (0x40)
    - `TrgUnit.movementFlags.AlwaysZero` (0x80)
    - `TrgUnit.movementFlags.HoverUnit` (0xC1)
  * `TrgUnit.baseProperty`
    - `TrgUnit.baseProperty.Building` (0x00000001)
    - `TrgUnit.baseProperty.Addon` (0x00000002)
    - `TrgUnit.baseProperty.Flyer` (0x00000004)
    - `TrgUnit.baseProperty.Worker` (0x00000008)
    - `TrgUnit.baseProperty.Subunit` (0x00000010)
    - `TrgUnit.baseProperty.FlyingBuilding` (0x00000020)
    - `TrgUnit.baseProperty.Hero` (0x00000040)
    - `TrgUnit.baseProperty.RegeneratesHp` (0x00000080)
    - `TrgUnit.baseProperty.AnimatedIdle` (0x00000100)
    - `TrgUnit.baseProperty.Cloakable` (0x00000200)
    - `TrgUnit.baseProperty.TwoUnitsInOneEgg` (0x00000400)
    - `TrgUnit.baseProperty.SingleEntity` (0x00000800): prevent multiple selections, checked for all Powerups units.
    - `TrgUnit.baseProperty.ResourceDepot` (0x00001000): Where to return resources
    - `TrgUnit.baseProperty.ResourceContainer` (0x00002000)
    - `TrgUnit.baseProperty.Robotic` (0x00004000)
    - `TrgUnit.baseProperty.Detector` (0x00008000)
    - `TrgUnit.baseProperty.Organic` (0x00010000)
    - `TrgUnit.baseProperty.RequiresCreep` (0x00020000)
    - `TrgUnit.baseProperty.Unused` (0x00040000)
    - `TrgUnit.baseProperty.RequiresPsi` (0x00080000)
    - `TrgUnit.baseProperty.Burrowable` (0x00100000)
    - `TrgUnit.baseProperty.Spellcaster` (0x00200000)
    - `TrgUnit.baseProperty.PermanentCloak` (0x00400000)
    - `TrgUnit.baseProperty.PickupItem` (0x00800000): Checked for units that can be held like powerups
    - `TrgUnit.baseProperty.IgnoresSupplyCheck` (0x01000000)
    - `TrgUnit.baseProperty.MediumOverlay` (0x02000000): related to spell effect overlay size
    - `TrgUnit.baseProperty.LargeOverlay` (0x04000000)
    - `TrgUnit.baseProperty.AutoAttackAndMove` (0x08000000)
    - `TrgUnit.baseProperty.CanAttack` (0x10000000)
    - `TrgUnit.baseProperty.Invincible` (0x20000000)
    - `TrgUnit.baseProperty.Mechanical` (0x40000000)
    - `TrgUnit.baseProperty.ProducesUnits` (0x80000000)
  * `TrgUnit.availabilityFlags`
    - `TrgUnit.availabilityFlags.NonNeutral` (0x001)
    - `TrgUnit.availabilityFlags.UnitListing` (0x002): be able to be created with CreateUnit action
    - `TrgUnit.availabilityFlags.MissionBriefing` (0x004)
    - `TrgUnit.availabilityFlags.PlayerSettings` (0x008)
    - `TrgUnit.availabilityFlags.AllRaces` (0x010)
    - `TrgUnit.availabilityFlags.SetDoodadState` (0x020)
    - `TrgUnit.availabilityFlags.NonLocationTriggers` (0x040)
    - `TrgUnit.availabilityFlags.UnitHeroSettings` (0x080)
    - `TrgUnit.availabilityFlags.LocationTriggers` (0x100)
    - `TrgUnit.availabilityFlags.BroodWarOnly` (0x200)
  * `Weapon.targetFlags`
    - `Weapon.targetFlags.Air` (0x001)
    - `Weapon.targetFlags.Ground` (0x002)
    - `Weapon.targetFlags.Mechanical` (0x004)
    - `Weapon.targetFlags.Organic` (0x008)
    - `Weapon.targetFlags.NonBuilding` (0x010)
    - `Weapon.targetFlags.NonRobotic` (0x020)
    - `Weapon.targetFlags.Terrain` (0x040)
    - `Weapon.targetFlags.OrganicOrMechanical` (0x080)
    - `Weapon.targetFlags.PlayerOwned` (0x100): Can target only your own units, like a defiler's consume
- Added scdata enum members
  * `CUnit.resourceType` = "None", "Gas", "Ore", "GasOrOre", "PowerUp"
    What the worker is carrying
  * `TrgUnit.nameString` = "string"
  * `TrgUnit.rank` = "Rank name" [see link for a list of ranks](https://github.com/armoha/eudplib/blob/main/eudplib/core/rawtrigger/strdict/stattxt.py#L1689-L1934)
  * `TrgUnit.readySound/whatSoundStart/whatSoundEnd/pissedSoundStart/pissedSoundEnd/yesSoundStart/yesSoundEnd` = [sfxdata.dat StarCraft sound effects file path](https://github.com/armoha/eudplib/blob/966b1649868d87f7c887a390ab4efa8bd4c22ba6/eudplib/core/rawtrigger/strdict/sfxdata.py#L3-L1145) (case insensitive, both '/' and '\\' are allowed as separators)
  * `TrgUnit.sizeType` = "Independent", "Small", "Medium", "Large"
  * `TrgUnit.rightClickAction` = "NoCommand_AutoAttack", "NormalMove_NormalAttack", "NormalMove_NoAttack", "NoMove_NormalAttack", "Harvest", "HarvestAndRepair", "Nothing"
  * `Flingy.movementControl` = "FlingyDat", "PartiallyMobile_Weapon", "IscriptBin"
  * `Weapon.damageType` = "Independent", "Explosive", "Concussive", "Normal", "IgnoreArmor"
  * `Weapon.explosionType` = "None", "NormalHit", "SplashRadial", "SplashEnemy", "Lockdown", "NuclearMissile", "Parasite", "Broodlings", "EmpShockwave", "Irradiate", "Ensnare", "Plague", "StasisField", "DarkSwarm", "Consume", "YamatoGun", "Restoration", "DisruptionWeb", "CorrosiveAcid", "MindControl", "Feedback", "OpticalFlare", "Maelstrom", "Unknown_Crash", "SplashAir"
  * `Weapon.behavior` = "Fly_DoNotFollowTarget", "Fly_FollowTarget", "AppearOnTargetUnit", "PersistOnTargetSite", "AppearOnTargetSite", "AppearOnAttacker", "AttackAndSelfDestruct", "Bounce", "AttackNearbyArea", "GoToMaxRange"
  * `Tech/Upgrade.race` = "Zerg", "Terran", "Protoss", "All"
  * `Image.drawingFunction` = "Normal", "NormalNoHallucination", "NonVisionCloaking", "NonVisionCloaked", "NonVisionDecloaking", "VisionCloaking", "VisionCloaked", "VisionDecloaking", "EMPShockwave", "UseRemapping", "Shadow", "HpBar", "WarpTexture", "SelectionCircle", "PlayerColorOverride", "HideGFX_ShowSizeRect", "Hallucination", "WarpFlash"
  * `UnitOrder.animation` = "Init", "Death", "GndAttkInit", "AirAttkInit", "Unused1", "GndAttkRpt", "AirAttkRpt", "CastSpell", "GndAttkToIdle", "AirAttkToIdle", "Unused2", "Walking", "WalkingToIdle", "SpecialState1", "SpecialState2", "AlmostBuilt", "Built", "Landing", "LiftOff", "IsWorking", "WorkingToIdle", "WarpIn", "Unused3", "StarEditInit", "Disable", "Burrow", "UnBurrow", "Enable", "NoAnimation"
- offsetmap: add `ArrayEnumMember`
- offsetmap: add an optional `stride` argument to the constructor of `ArrayMember`
  * Example 1) Define `TrgUnit.constructionGraphic` as `constructionGraphic = ArrayMember(0x6610B0, MemberKind.IMAGE, stride=4)` because it is of type `Image` but the stride is 4 bytes.
  * Example 2) `TrgPlayer.unitColor` is 1 byte in size, but the gap is 8 bytes, so we define it as `unitColor = ArrayMember(0x581D76, MemberKind.BYTE, stride=8)`.

### Bugfix
- Fix `{:c}`, `{:n}` (`PColor`, `PName`) compilation error (reported by spin137)
- Fix compilation error in `DisplayTextAll`, `DisplayTextAllAt` functions (reported by @dr-zzt)
- Fix size, offset errors in scdata (reported by DarkenedFantasies)
  * `CUnit.gatherQueueCount`: size -> bool
  * `CUnit.isUnderStorm`: size -> bool
  * `CUnit.resourceBelongsToAI`: size -> bool
  * `TrgUnit.constructionGraphic`: size -> dword
  * `Weapon.targetFlags`: size -> word
  * `Weapon.maxRange`: offset -> 0x657470
  * `Weapon.cooldown`: offset -> 0x656FB8
  * `Upgrade.mineralCostBase`: offset -> 0x655740

### Improved
- Improved error message for invalid input when creating `CUnit`, `CSprite`
- scdata uses more specific types (reported by DarkenedFantasies)
  * `TrgUnit.constructionGraphic`: Image
  * `TrgUnit.armorUpgrade`: Upgrade
  * `TrgUnit.portrait`: Portrait
  * `TrgUnit.nameString`: TrgString
  * `Weapon.label`: StatText
  * `Weapon.icon`: icon
  * `Weapon.upgrade`: Upgrade
  * `Weapon.targetErrorMessage`: StatText
  * `Upgrade.label`: StatText
  * `Upgrade.icon`: icon
  * `UnitOrder.icon`: Icon
  * `UnitOrder.weapon`: Weapon
  * `UnitOrder.techUsed`: Tech
  * `UnitOrder.obscuredOrder`: UnitOrder

## [0.9.11.0] - 2024.09.01
### Changed
- Fixed `EUDJump` not using trigger if trigger address to jump to is constant
- Added unreachable `EUDJump` compilation error
- Added warnings to unreachable `break`, `continue`
- epScript: Change `"string"` to be usable as an expression
- Change `CUnit.cast(other)` and `CSprite.cast(other)` to use variable as reference instead of copying it when target is a variable

### Added
- Added easy StarCraft data modification (scdata) to existing types (contributed by @dr-zzt)
```js
// Example of scdata function
function example(unit: TrgUnit) {
    unit.armor += 1;  // Increase unit armor by 1
    unit.groundWeapon.damage += 1;  // increase the damage of the unit's ground weapon by 1

    unit.groundWeapon = Weapon("Gauss Rifle");  // change the unit's ground weapon to a Gauss Rifle

    P1.ore += 1;  // increase P1 mineral by 1
    if (P1.ore >= 100) {
        printAll("Red has collected at least 100 minerals");
    }
}
```
  * Detailed explanation to be written by @dr-zzt
- epScript: Add forward declaration syntax for object (suggested by 하늘바라군 and 0xFF)
```js
object Food;
object Animal {
    function eat_food(food: Food) {} // possible
};
object Meat extends Food {}; // This is not possible
```
- `CUnit.from_next()`
- Add keyword argument `ignore_subunit` to `CUnit.cgive(player)` (default = `false`)
- epScript: Change encoding syntax (`$U`, `$L`, etc) to allow all expressions in addition to strings.

### Bugfix
- Bugfix: `Array[i] = i;` bug fixed (reported by HeukSulTang, Xenon)
- Fixed a bug where `CUnit.cgive(player)` was not working properly.
- Bugfix: `CUnit.set_hallucination()` and `CUnit.clear_hallucination()` modify the status flag `IsNormal`, causing units to move around ignoring terrain
- Fix 'int' object has no attribute 'Evaluate' error in ExprProxy wrapping int
- epScript: Fix `object` `extends` to accept expressions including `a.b` in place of superclass (report by 0xFF)
- epScript: Fixed bug where writing return type in function forward declaration syntax would result in an error (reported by 0xFF)
- Fixed an error when putting variables in functions that run for all players, such as `DisplayTextAll` and `PlayWAVAll` (reported by furina)
- Fixed typos in some `Portrait` entries (reported by @dr-zzt)
- Fixed bug where rvalue variable optimizations were not applied
- Fix `TriggerScopeError` exception to be thrown early when triggers are declared in invalid positions.
  * Fixed bug resulting in invalid triggers regardless of exception handling
- Fixed `Forward not initialized` compile error when declaring `EUDByteReader`, `EUDByteWriter` and not using `.readbyte` or `.writebyte` method

### Improved
- Enum/flag members such as `CUnit.movementFlags` and `CUnit.statusFlags` can now be used as values.
- Typos in access to members of `CUnit`, `CSprite`, flag members, etc. now raise errors (use `__slots__`)
- Improved location functions `f_setloc`, `f_addloc`, and `f_dilateloc`; no longer generate actions for coordinate arguments with 0 (suggested by 콤)
- Built-in read functions share overlapping triggers to save the number of triggers
- Replaced terminal color library `colorama` with `rich`
- Improved EDS/EDD duplicate settings error message
- Improved performance to minimize trigger usage when using variables as arguments in conditions/actions
- Improved `EUDByteReader`, `EUDByteWriter` performance
- Optimized `EUDJump` to create 2 triggers -> 1 trigger when trigger address to jump to is a variable
- Add `__divmod__` to `ExprProxy`

## [0.9.10.12] - 2024.01.25
### Changed
- `CUnit.cgive(player)` will change sprite color

### Bugfix
- [epScript] Fixed to not prepend `f_` for non-ascii named function definition
- Forbid using `unit.remove()` inside of `unit.dying` block of `UnitGroup.cploop`
- Fixed `CUnit.cgive(player)` to properly unlink unit
- Fixed `CUnit.cgive(player)` to change minimap color of subunit

### Improved
- Updated eudplib 0.76.15, cx_Freeze 6.15.13
- Faster `EUDVarBuffer.WritePayload` (contributed by @phu54321 : https://github.com/armoha/eudplib/commit/29ed0ef5a50bc78d375b9d09aba27598c83268c9)
  * Reduced compile time by 4.2%
- [epScript] Rewrite linetable calculating code in Rust (https://github.com/armoha/eudplib/pull/25)
  * Reduced compile time by 5.7%
  * Total 9.66% faster compile time

## [0.9.10.11] - 2023.12.29
### Bugfix
- Fixed build error with [main] debug option (reported by 스타맵돌이)

### Improved
- Update eudplib to 0.76.14
- Reduced compile times in eudplib frontend by 20% (contributed by @phu54321 : https://github.com/armoha/eudplib/pull/24)
- Improved `GetObjectAddr` in Writing phase
- Reduced compile times by about 10%

## [0.9.10.10] - 2023.12.27
### Changed
- `ConstExpr` and `EUDObject` use `__new__` instead of `__init__`
  * For migration of subclasses, see https://stackoverflow.com/questions/28236516/python-subclassing-a-class-with-custom-new
- Removed `currentAction` keyword argument for `RawTrigger`

### Added
- Add `CUnit.set_collision()`

  Clear `NoCollide` and `IsGathering` status flags. Reverse of `CUnit.remove_collision()`.
- Prints elapsed build time for `.edd`

### Improved
- Update eudplib to 0.76.13
- Rewrote `RlocInt`, `ConstExpr`, `EUDObject` and `RawTrigger.WritePayload` in Rust (https://github.com/armoha/eudplib/pull/22)
- Reduced build time by 30% (Total 60% compared to euddraft 0.9.10.6 or older)

## [0.9.10.9] - 2023.12.23
### Bugfix
- Fixed settbl2 didn't work with custom stat_txt.tbl (reported by neonoew)

## [0.9.10.7] - 2023.12.19
### Changed
- The offset and rlocmode of ConstExpr and RlocInt_C are changed from unsigned to signed
- ConstExpr operations are changed to only return ConstExpr (not int)
  * Try write `int(ConstExpr)` for type conversion

### Added
- Add `CUnit.remove()` (Thanks to DarkenedFantasies)

  Remove unit without death effect.

### Improved
- Improved build time by about 40% (armoha/eudplib#21)
  * Massively improved Allocating Phase: Rewrote StackObjects and AllocObject in Rust
  * Improved Writing Phase: Rewrote ConstructPayload in Rust
  * Exclude slow Condition/Action parameter validity checks
- Update Korean localization

## [0.9.10.6] - 2023.12.15
### Added
- [epScript] Allow "string literal" in index/subscript syntax

### Bugfix
- Fixed 'TypeError: Value after * must be an iterable, not EUDVariable' in f_setcurpl2cpcache (reported by WestICE)

## [0.9.10.5] - 2023.12.15
### Bugfix
- Fix bugs in bitwise left/right shift operations (<<, >>) when right-handed-side value >= 32
  * Fix freeze on game start in maps using EUD Editor 2 TriggerEditor (reported by @iDoodler-DS)
  * Fix bug in `f_bitlshift(a, b)` executing too many triggers when rhs is var >= 32
  * Fix bug in `f_bitrshift(a, b)` returning incorrect value when rhs is var >= 32

## [0.9.10.4] - 2023.12.13
### Added
- [epScript] py_module won't prepend f_ on function name

```js
// epScript drawing circle example
import py_math;

function circle() {
    foreach (k : py_range(10)) {
        MoveLocation("effect", "Terran Ghost", P1, "Anywhere");
        // no need to use py_eval anymore!
        const x = py_int(math.cos(k * math.pi / 5) * 30);
        const y = py_int(math.sin(k * math.pi / 5) * 30);
        addloc("effect", x, y);
        CreateUnit(1, "Scanner Sweep", "effect", P1);
    }
    RemoveUnit("Scanner Sweep", P1);
}
```

## [0.9.10.3] - 2023.12.13
### Bugfix
- SoundLooper.py : Fixed build error in `SoundLooper.initialize()`
- [dataDumper] : Fixed build error in custom stat_txt.tbl map
- Fixed build error in `copy.copy(Condition or Action)`
- Fixed build error in `CUnit.setloc(location)`
- Revert name change of `ExprProxy.getValue()`
- Revert name change of `_AddStatText(bytes)`, `_addedFiles`
- Revert EUDFunc and EUDFuncPtr related changes of 0.9.10.2
  * Optimize EUD function return : remove intermediate variable and use return assign trigger
  * Optimize `f_getcurpl()` to not pass through variable trigger

### Improved
- Better error message for invalid type of EUDArray initial values
- Fixed `unProxy(object)` to raise error for cycle reference to prevent cycle loop

## [0.9.10.2] - 2023.12.11
### Changed
- Updated Python from 3.10.10 to 3.11.6
- [epScript] Removed `class` and `subobject` syntax. Merge them into `object` (+`extends`)
- `GetMapStringAddr(string)` is now constant function
  * `GetMapStringAddr(string_constant)` returns string address as constant expression (ConstExpr)
- `ExprProxy` forbids inplace operators by default
- Integrate `_Unique` with const types (`TrgPlayer`, `TrgUnit` etc.)
- Change `StringBuffer` to `EUDStruct`

### Bugfix
- [freeze] Fixed bug with non-compressed encrypted OGG file (Contributed by @phu54321)
- [epScript] Fixed StopIteration error following any compile error in Python 3.11
- soundlooper.py : Fixed array access out of bound
- [MSQC] Fixed mouse location to work close to right/lower border (Reported by Staminize)
- Fixed typos in Sprite, Image, Iscript etc. (Reported by @Dr-zzt)
- Fixed the number of members of inherited epScript object/EUDStruct could exceed objFieldN (Reported by Astro)
  * Fixed to check object member validity when defining class (was checked on instantiation)
- Fixed `UnitGroup.cploop` to restore CurrentPlayer at the end
- Fixed `EUDLoopNewCUnit` to restore CurrentPlayer at the end
- Fixed compile error in `CUnit.reset_buildq()`
- Fixed cycle loop when copy.copy(x) on Condition and Action
- Fixed `Disabled(Condition or Action)` to return input Condition/Action instead of None

### Added
- [dataDumper] Autodetect stat_txt.tbl encoding
  * TBL functions like `f_settbl` will use detected encoding by default
- Added condition `CUnit.are_buildq_empty()`
- Added condition `CUnit.check_buildq(unit)`
- Added compile-time value range check for `CUnit` members
- [epScript] string literal is allowed in comparison expression and assignment statement
- Added `LocalLocale`
  * Detect user's StarCraft language settings on game start

    ```py
    "enUS",  # [1] English
    "frFR",  # [2] Français
    "itIT",  # [3] Italiano
    "deDE",  # [4] Deutsch
    "esES",  # [5] Español - España
    "esMX",  # [6] Español - Latino
    "ptBR",  # [7] Português
    "zhCN",  # [8] 简体中文
    "zhTW",  # [9] 繁體中文
    "jaJP",  # [10] 日本語
    "koUS",  # [11] 한국어 (음역)
    "koKR",  # [12] 한국어 (완역)
    "plPL",  # [13] Polski
    "ruRU",  # [14] Русский
    ```
  * 0 = (unknown), 1~14 = locale values
  * How to use
    - LocalLocale == "koUS" : Compare if local user uses 한국어 (음역)
    - LocalLocale != "enUS" : Compare if local user does not use English
    - LocalLocale << "zhCN" : Assign 简体中文 value (8) to the variable which stores language value (Does not modify user's language setting with EUD)
  * Limitations
    - Can't detect language setting for free-to-play users
    - Can't disambiguage 한국어 음역(koUS) and 완역(koKR). Currently both are detected as 음역(koUS).
- Added `QueueGameCommand_AddSelect(unitCount, ptrArray)` function
- Added `QueueGameCommand_RemoveSelect(unitCount, ptrArray)` function

### Improved
- Fixed freeze vulnerability (Reported by @phu54321)
- Optimize `CUnit.cgive(player)` and `CUnit.set_color(player)`
- Optimize EUD function return : remove intermediate variable and use return assign trigger
- Optimize `f_getcurpl()` to not pass through variable trigger
- Removed `StringBuffer` initialization trigger, which no longer needed due to `GetMapStringAddr` update
- Optimize `QueueGameCommand_Select(unitCount, ptrArray)` by removing intermediate buffer

## [0.9.9.9] - 2023.06.13
### Changed
- Changed `atan2_256(y, x)` and `lengthdir_256(length, angle256)` to obey coordinate system that StarCraft uses
  * No need to convert from SC system to mathematical system
- `$T`, `EncodeString`, `GetStringIndex` use UTF-8
- Downgrade python version, from 3.11.1 to 3.10.10
  * Fixed `StopIteration` verbose error message

### Bugfix
- Fixed 32 bit wireframe bugs for siege tank, zealot etc.
- Fixed `cunitread_cp` function with 0-valued source (reported by paols)
- Fixed bug for `cunit.cgive(player);` during `EUDLoopPlayerCUnit(player)` (reported by GGrush)
- Fixed `UnitGroup.add(variable);` modifying variable (reported by GGrush)
- Fixed relative import duplicating module instances
- Fixed error message for epScript-generated python file showing different line number and content
- Fixed `CUnit.statusFlags` for not raising error on attribute typos (Fixes armoha/euddraft#113)
- Fixed bug in return-typed lambda function  with no parameter type generating untyped function
- Fixed `NonSeqCompute` with `None` modifier
- Fixed bug to let eps-server retrieve CUnit member informations

### Added
- [epScript] Added keywords `class`, `extends`
  * You can inherit between `object` (=`EUDStruct`)
- Allow jumping statements while looping `EUDQueue` and `EUDDeque`
  * Can use `break;`, `continue;` and `EUDSetContinuePoint();` within `foreach(element : queue) {}` loop
- Allow `object.constTypedMember = constValue;`, like `instance.player = P1;`
- Added 3 signed division functions
  * return constants for constant arguments
  * `const quotient, remainder = div_towards_zero(a, b);`

    Calculates the quotient and remainder of (a ÷ b), rounding the quotient towards zero.

    Calculate signed division, unlike unsigned division `div(a, b)`.
    Consistent with C-like languages including JavaScript.
  * `const quotient, remainder = div_floor(a, b);`

    Calculates the quotient and remainder of (a ÷ b), rounding the quotient towards negative infinity.

    Calculate signed division, unlike unsigned division `div(a, b)`.
    Consistent with mathematical modulo.
  * `const quotient, remainder = div_euclid(a, b);`

    Calculates the quotient and remainder of Euclidean division of a by b.

    Calculate signed division, unlike unsigned division `div(a, b)`.
    This computes the quotient such that `a = quotient * b + remainder`, and `0 <= r < abs(b)`.

    In other words, the result is a ÷ b rounded to the quotient such that `a >= quotient * b`.
    If `a > 0`, this is equal to round towards zero; if `a < 0`, this is equal to round towards +/- infinity (away from zero).
- Added in-place negation and abs for `VariableBase` (`EUDVariable` and `EUDLightVariable`)
  * `var.ineg();` : negate variable in-place (same as `x = -x;`)
  * `var.iabs();` : self-assign absolute value in-place (same as `x = (x & (1 << 31) == 0) ? x : -x;`)
  * `DoActions(var.ineg(action=true));` : action alternative
  * `DoActions(var.iabs(action=true));`

### Improved
- Reduced the number of trigger execution for `EPD`
- Rvalue optimization for `EPD`
- Reduced division and remainder triggers
- Added bound checks for constant subscript on `EUDArray` and `EUDVArray(size)` types
- Reduced constant multiplication triggers for overflowing high bits
- Duplicated object field name is now compile error
- Added support on `UnitOrder` for order names EUD Editor uses
- Better error for non-existing unit name and consttypes
- Fixed some error messages to print `repr` representation
- Updated eudplib 0.75.0, cx_Freeze 6.15.1, pybind 2.10.4

## [0.9.9.7] - 2023.01.29
### Bugfix
- Fixed `ImportError: Module use of python310.dll conflicts with this version of Python.`
- Fixed `TypeError: Population must be a sequence.  For dicts or sets, use sorted(d).`

### Improved
- Updated to Python 3.11.1
  * eudplib now supports both Python 3.10 and 3.11
- **epScript:** local `var v = rvalue_variable;` won't additionally copy
  * Fixed some corner cases to wrongly elide copy or miss opportunity
- `SetVariables(rvalue_variable, value)`now raises compile error
- Updated Korean localization
- Forcing stdin, stdout, stderr of euddraft to always use UTF-8
- Updated eudplib 0.74.9, cx_Freeze 6.14.2

## [0.9.9.5] - 2023.01.24
### Bugfix
- Fixed CUnit.posY bug (reported by 할루)
- Fixed CSprite(integer)

### Added
- Added `CUnit.cgive(player)`

### Improved
- `CUnit`, `CSprite`: copy variable on initialization, deleted `__slots__`
- Updated eudplib 0.74.5

## [0.9.9.4] - 2023.01.19
### Changed
- Changed `EPDOffsetMap` from function to abstract class, changed `EPDCUnitMap` to alias of `CUnit`
- Changed `_EUDStructArray` from dynamic class to static class

### Bugfix
- [dataDumper] always run firstmost, regardless of the order of plugins (reported by iDoodler)
  * Fixed ChangeStarText and settblf not working in onPluginStart of EUD Editor 2 TriggerEditor
- Fixed `f_badd_epd` calling `f_bwrite_epd` when value is variable (reported by wdcqc)
- Fixed compile error for `RunAIScript("4-character code")` (reported by wdcqc)
- Fixed `EUDDeque.appendleft` corrupting `foreach` deque iterator triggers

### Added
- Added `Is64bitWireframe()` local (desync) condition
  * evaluated to True on 64 bit StarCraft, False on 32 bit StarCraft.
  * Output map becomes custom wireframe UMS map: causing wireframe bug side-effects for Siege Tank, High Templar, Zealot etc.
- Added proxy classes `CUnit`, `CSprite`
  * You can create a `CUnit` instance with 4 methods
  * `CUnit(epd)`: epd-only CUnit constructor (typed parameter and CUnit.cast only accept epd)
  * `CUnit(epd, ptr=ptr)`: ptr and epd constructor
  * `CUnit.from_read(epd)`: read CUnit value from epd address to construct CUnit instance
  * `CUnit.from_ptr(ptr)`: calculate EPD with triggers by subtraction and division to construct CUnit instance
  * List of members: https://github.com/armoha/eudplib/blob/master/eudplib/offsetmap/cunit.py#L84-L371
- Added `EUDLoopCUnit`, `EUDLoopNewCUnit`, `EUDLoopPlayerCUnit`
- Added `offsetmap` module
  * `offsetmap.EPDOffsetMap`
  * `offsetmap.MemberKind`
  * `offsetmap.BaseMember`
  * `offsetmap.Member`
  * `offsetmap.CUnitMember`
  * `offsetmap.CSpriteMember`
  * `offsetmap.EnumMember`
  * `offsetmap.Flag`

## [0.9.9.3] - 2023.01.14
### Bugfix
- Fixed compile error for EUD Editor 3 BGM Player and Open source Song guessing games

## [0.9.9.2] - 2023.01.12
### Changed
- Removed dependencies: Cython, numpy, matplotlib, pywin32, cffi, idna
  * Cython's typing support is not mature yet, causing various errors so it's removed. The slow compilation will be solved by introducing mypyc.
  * While removing Cython, numpy is also removed since it is closely linked to Cython.
  * Unlike Python-based game engines such as Ren'Py, euddraft is a compiler that creates EUD maps with plug-ins written in eps/py, and Starcraft acts as a game engine. What Starcraft executes is only a trigger. numpy and matplotlib can help create trigger, but they can't be used directly in Starcraft, which is confusing for beginners who aren't awared of this details. When cx_Freeze is updated in the future and Python 3.11 is introduced, numpy's compilation time savings are also expected to be minimal. Using numpy and matplotlib to generate eps/py code can also be achived by external code generation like how EUD Editor does, so they're removed.
  * pywin32, cffi, idna have been unused in euddraft for a long time, so they're removed.

### Bugfix
- [MSQC] Fixed not working bug
- Fixed error `NotImplementedError: You should not call an overloaded function.` (reported by 택하이)

### Improved
- Added dependency openpyxl: can read/write excel file
- [epScript] Allow relative import to load global variables and functions (reported by Low Signal)
- [epScript] armoha/euddraft#66: Raise compile error when trying to overwrite Python keyword (reported by Low Signal)
- Improve error message when modifier is variable in SetVariables, SeqCompute, EUDVariable.SetModifier (reported by Low Signal)

## [0.9.9.1] - 2023.01.09
### Bugfix
- [epScript] Fixed compile error in single global variable and global const array declarations

## [0.9.9.0] - 2023.01.09
### Changed
- Raise compile error or warning when unexpected constant is used as condition, like `if (Db(4))`
  * 'Condition is always true` warning for castable proxy classes: EUDArray, EUDVArray, EUDStruct (object in epScript) etc
  * Compile error for the other ConstExpr
  * Integers like -1, 0, 1 behaves same as before, converts 0 into `Never()`, non-zero integers into `Always()` condition.
- Changed name `TrgTBL` -> `StatText`
- Chaged `VariableBase` and `EUDObject` to abstract class

### Bugfix
- [epScript] Don't wrap global consants with ExprProxy unless there's forward-declared function call.
  * No need to write `globalConst.getValue()` in most cases.
- [MSQC] Use Move order instead of right click
  * The player can't deliberately controls QCUnit by group hotkey selection and right clicking.
- [draw.py] Fixed infinite compile bug in `Point x, y = Shape[index]` (reported by Avlos)
- [epScript] Fixed bug in relative path import (reported by 유즈맵조아조아)
  * Fixed compile error for Artanis song guessing game open source, exists in euddraft 0.9.8.3~0.9.8.13
- Fixed compile error in `EPDCUnitMap.set_color(player)` (reported by 할루)
- Fixed compile error `TypeError: EncodePlayer() got an unexpected keyword argument 'issueError'` (reported by HuntRabbit)
  * Fixed compile error with [BetterBrain] plugin
- Removed ambiguous string warning added in euddraft 0.9.8.13, rollbacked previous behavior and improved error message (reported by nn2)
- Fixed unsupported EUD error in `f_dwpatch_epd`

### Improved
- [epScript] Don't add initialization trigger for global variables when their initial values are constants
- Fixed CreateUnitWithProperties with HP 100% to create unit with MaxHP > 167772 full-health
- UnitProperty reuses UnitProperty of equal result: ex) cloaked=None and cloaked=False share same properties
- Optimize EUD loops (EUDInfLoop, EUDLoopN, EUDLoopRange, EUDWhile) to execute 1 less trigger for every iterations (reported by 콤)
- Arithmetic of ConstExpr yields integer offset when rlocmode becomes 0
- Added and improved eudplib error messages
- Update euddraft Korean localization
- Updated eudplib 0.73.16

### Added
- [epScript] Can write function call syntax on outermost scope
  * Raises TriggerScopeError when you added trigger by writing Trigger action or calling EUD function.
  : `"Must put Trigger into onPluginStart, beforeTriggerExec or afterTriggerExec"`
  * Useful for eudplib functions like `EUDOnStart`, `InitialWireframe`, `MPQAddFile`, `EUDRegisterObjectToNamespace`\
  or calling python library functions in epScript.
- Revised and added type hints
- Added `TriggerScopeError`: subclass of `EPError`. Raised when trigger was written at unusable scope
- Added function `b2utf8(bytes) -> str`: decode bytes to UTF-8 string

## [0.9.8.13] - 2023.01.01
### Bugfix
- Fixed various bugs

### Improved
- Added more type hints
- Type checked eudplib with mypy
- Updated eudplib 0.73.1

## [0.9.8.12] - 2022.12.31
### Bugfix
- Fixed `a[index] /= (power of 2 constant)` compile error for `EUDVArray`, `PVariable` (reported by gongnamu)
- Fixed `EUDLoopNewUnit` missed iterating preplaced units under certain circumstances (reported by Oneiro)

### Improved
- Added type hints for some eudplib functions: localize, maprw, trigger, trigtrg, utils
  * Work in progress: core, ctrlstru, epscript, eudlib
- Updated eudplib 0.72.6

## [0.9.8.11] - 2022.12.30
### Changed
- `$T`, `EncodeString`, `GetStringIndex` rollbacked to use CP949 encoding for new string.

### Bugfix
- `[chatEvent]` When hash collisions, fall-back to string comparison (reported by LLAS)

### Improved
- `[chatEvent]` Added simple encryption for chat patterns
- Added typing for eudlib/utilf
- Updated eudplib 0.72.5

## [0.9.8.10] - 2022.12.25
### Bugfix
- Allow `EUDOnStart` to be used everywhere in your code
- Fixed `println`, `printAt`, `simpleprint` didn't work (armoha/euddraft#28)
  * No longer need to put `GetGlobalStringBuffer()` in `onPluginStart`
- Allow `SetWireframes` without using `InitialWireframe`
- **[epScript]** Allow `py_len()` for global constants
  * Allow `len()` for `ExprProxy`

### Improved
- Updated eudplib 0.72.3, pybind11 v2.10.2
- Optimize size of `StringBuffer` initialization triggers

## [0.9.8.9] - 2022.12.20
### Changed
- `$T`, `EncodeString`, `GetStringIndex` uses UTF-8 encoding for new string.

### Bugfix
- Fixed coordinates in null tiles warning
- Fixed `InitialWireframe` bug when Marine was not editted. (reported by Oneiro)

### Improved
- eudplib supports Python 3.11
- `[chatEvent]` Support global eud namespace
  ```ini
  :: edd/eds example
  [chatEvent]
  __addr__: addr
  __patternAddr__: patternAddr
  __ptrAddr__: ptrAddr
  __lenAddr__: lenAddr
  sell : 2
  sellghost : 3
  sellhydra : 4
  selldragoon : 5
  ^'ore .*.*$: 1
  ^'gas .*.*$: 2
  [test.eps]
  ```
  ```js
  // Example epScript code (test.eps)
  var addr, patternAddr, ptrAddr, lenAddr;
  function onPluginStart() {
      EUDRegisterObjectToNamespace("addr", addr);
      EUDRegisterObjectToNamespace("patternAddr", patternAddr);
      EUDRegisterObjectToNamespace("ptrAddr", ptrAddr);
      EUDRegisterObjectToNamespace("lenAddr", lenAddr);
  }
  function chat();
  function beforeTriggerExec() {
      chat();
  }
  function chat() {
      if (addr < 1) return;
      setcurpl(getuserplayerid());
      if (addr >= 2) {
          println("\x07Chat Detected \x04(id: {})", addr);
          return;
      }
      if (patternAddr) {
          println("\x07Pattern Detected \x04(id: {})", patternAddr);
          return;
      }
      DisplayText("\x05Chat not belong to [chatEvent] settings");
  }
  ```
- Add duplicated entries warning for `EUDRegisterObjectToNamespace`
- Add assertion messages for `InitialWireframe` and `EUDOnStart`

## [0.9.8.7] - 2022.12.14
### Bugfix
- `[chatEvent]` Fixed wrong pattern length (reported by Yuuki-Asuna)
- `[unlimiter]` Fixed compile error (reported by 파냥이)

## [0.9.8.6] - 2022.12.13
### Bugfix
- Fixed `EPDCUnitMap.isBlind` type from `bool` to `u8` (reported by Skywindragoon)
- `EPDCUnitMap.is_dying()` was not working with `[unlimiter]` plugin, and now it raises compile error
  * CSprite is always 0 for units spawned after running `[unlimiter]`, and looking into just CUnit, we can't tell whether it is already dead or dying. To distinguish between dead and dying with `[unlimiter]`, we need to store that unit is in usage, on additional memory space using `EUDLoopNewUnit` etc. It involves non-trivial cost so we'd rather explicitly state current status and leave this matter to end users.

### Added
- Added `IsUnlimiterOn()`: useful for library writers
- Added `InitialWireframe` class/namespace\
  Supports both 32 bit and 64 bit StarCraft.
  * `InitialWireframe.wireframes(unit, wireframe)`
    - Set initial TranWire.grp, GrpWire.grp, Wirefram.grp of unit.
    - Must called at outermost scope!
  * `InitialWireframe.tranwire(unit, wireframe)`
  * `InitialWireframe.grpwire(unit, wireframe)`
  * `InitialWireframe.wirefram(unit, wireframe)`
- Added `SetWireframes(unit, wireframe)`, `SetTranWire(unit, wireframe)`, `SetGrpWire(unit, wireframe)`, `SetWirefram(unit, wireframe)`
  * Edit wireframe at runtime. Supports both 32 bit and 64 bit StarCraft.
  * Only works when `InitialWireframe` is used!

## [0.9.8.5] - 2022.12.06
### Bugfix
- Fixed typo in `Trigger(preserved=False)` and `DoActions(preserved=False)` (reported by 콤)

### Improved
- Print null tile coordinates for 00.0000 warning
- Optimized `f_atan2(y, x)` and `f_lengthdir(length, angle)`

### Added
- Added `f_atan2_256(y, x)` and `f_lengthdir_256(length, angle)`

## [0.9.8.4] - 2022.11.29
### Changed
- `EUDLoopNewUnit` no longer modify **CUnit +0xA5** `uniquenessIdentifier`
- Multiple `EUDLoopNewUnit` now check whether unit is newly created independently (reported by PR프로덕션)
  * Previous behavior: Only first executed `EUDLoopNewUnit` can iterate new units since previous trigger frame. Following `EUDLoopNewUnit` only iterates newly created units between loops.
- Can call `cunit.remove();` multiple times in `UnitGroup.cploop`

### Bugfix
- Allow `selftype` for non-const method call
- Fixed armoha/euddraft#34 : non-const `EUDTypedMethod` call raises `EPError: Different number of variables(n) from type declarations(n-1)`

### Improved
- Optimize `f_playerexist(player)`
- Optimize read functions for empty case
  * **Example)** Local (desync) unit selection
  ```js
  const localSelect = EPD(0x6284B8);
  for(var mySelect = localSelect; mySelect < localSelect + 12; mySelect++) {
    // Much faster and cleaner when mySelect is *not* empty
    const ptr, epd = cunitepdread_epd(mySelect);
    if (epd == 0) break;

    // .. than this, which substitutes mySelect on condition
    if (MemoryEPD(mySelect, Exactly, 0)) break;
    const ptr, epd = cunitepdread_epd(mySelect);
  }
  ```
- `switch`: Omit masked range check if bitmask == 0

## [0.9.8.3] - 2022.11.03
### Changed
- `EPDOffsetMap` rollbacked to accept a tuple of *(name, offset, type)* pairs
- Added and changed types `EPDOffsetMap` takes
  * Available type: bool, 1, 2, 4, "CUnit", "CSprite", "Position", "PositionX", "PositionY", `Flingy`, `TrgPlayer`, `TrgUnit`, `UnitOrder`, `Upgrade`, `Tech`

### Improved
- Updated eudplib 0.71.7, cx_Freeze 6.13.1, pybind11
- Optimize epScript object (EUDStruct) in-place operations and comparisons
- Optimize EPDCUnitMap edit/comparison
- `f_bitlshift(a, b)` calculates `a << b` on compile time when both are constants

### Bugfix
- [epScript] Fixed armoha/euddraft#73 : Modifying python collections resulted in shadowing var
- Fixed `dwread(constexpr)` to calculate EPD on compile time (reported by Cocoa)
- Fixed bug in `EUDDeque.append(value)` when tail warps around
- Fixed trailing-whitespace typos in `Image`
- `UnitGroup`: `.dying` block checks *hp == 0*, instead of *hp < 0.5*
- Fixed missing optimization (reported by @Chromowolf)

### Added
- Added `matplotlib` library
- Added `EUDQueue.clear()`, `EUDDeque.clear()`
- Added `f_wadd_epd(epd, subp, value)`, `f_wsubtract_epd(epd, subp, value)`, `f_badd_epd(epd, subp, value)`, `f_bsubtract_epd(epd, subp, value)`
  * Only 0, 1, 2 are allowed in *subp* for `f_wadd_epd` and `f_wsubtract_epd`
- Added types `Weapon`, `Flingy`, `Sprite`, `Upgrade`, `Tech`, `UnitOrder`, `Icon`, `Portrait`
- Added functions `EncodeWeapon`, `EncodeFlingy`, `EncodeSprite`, `EncodeUpgrade`, `EncodeTech`, `EncodeUnitOrder`, `EncodeIcon`, `EncodePortrait`
- Added `f_(set/add/dilate)loc(loc, x, y, action=true)`

## [0.9.8.2] - 2022.10.24
- Updated eudplib 0.71.2
- Fix bug in `pow(a, b)` function (contributed by @Chromowolf )
- [epScript] Fix bug with global variable and `%` operator (reported by @Chromowolf )
- [epScript] Fixed armoha/euddraft#56 : Assigning constant to another module's variable 'rebinds' variable to constant
  * No longer need to workaround with `SetVariables`

## [0.9.8.1] - 2022.10.21
- Updated eudplib 0.71.1
- Fixed bug breaking preserved TRIG triggers
- Fixed compile error when `import numpy` (reported by PyroManiac)
- Added `EUDDeque(length)()`\
  `EUDDeque` is a double-ended queue with fixed-size buffer. It supports efficient insertions and removals from both ends.\
  Once a deque is full, when new items are added, a corresponding number of items are discarded from the opposite end.
  * `.length` : current length
  * `.append(x)` : Add x to the right side of the deque.
  * `.pop()` : Remove and return an element from the right side of the deque.
  * `.appendleft(x)` : Add x to the left side of the deque.
  * `.popleft()` : Remove and return an element from the left side of the deque
  * `.empty()` : Condition evaluated to True when deque is empty
  * Also supports `foreach` iteration. Iterating over `EUDDeque` goes left to right.
    ```js
    // dq3 is deque with length 3
    const dq3 = EUDDeque(3)();
    const ret = EUDCreateVariables(6);

    // Nothing happen if you loop empty deque
    foreach(v : dq3) { ret[0] += v; }

    // Add 1 and 2 to the right
    dq3.append(1);  // dq3 : (1)
    dq3.append(2);  // dq3 : (1, 2)
    foreach(v : dq3) { ret[1] += v; }  // 3 = 1 + 2

    // Add 3 and 4 to the right
    dq3.append(3);  // dq3 : (1, 2, 3)
    dq3.append(4);  // dq3 : (2, 3, 4)
    foreach(v : dq3) { ret[2] += v; }  // 9 = 2 + 3 + 4

    // Add 5 to the right
    dq3.append(5);  // dq3 : (3, 4, 5)
    foreach(v : dq3) { ret[3] += v; }  // 12 = 3 + 4 + 5

    // Remove and return 3 from the left
    const three = dq3.popleft();  // dq3 : (4, 5)
    foreach(v : dq3) { ret[4] += v; }  // 9 = 4 + 5

    // Add 6 and 7 to the right
    dq3.append(6);  // dq3 : (4, 5, 6)
    dq3.append(7);  // dq3 : (5, 6, 7)
    foreach(v : dq3) { ret[5] += v; }  // 18 = 5 + 6 + 7
    ```
  * `EUDDeque` behaves like Python `collections.deque(maxlen=length)`.
- [epScript] armoha/euddraft#86 : Allow trailing comma after function arguments
- [epScript] armoha/euddraft#87 : Allow binary number representation
  * `0b1 == 1`, `0b10 == 2`, `0b11 == 3`
- Fixed bug `EUDQueue.empty()` was always `true`
- Fixed compile error when only one of `EUDQueue.append(x)` and `EUDQueue.popleft()` is used

## [0.9.7.12] - 2022.10.19
- Updated eudplib 0.70.18
- Fixed error iterating globals raises `TypeError: iter() returned non-iterator of type 'list'` (reported by 줸님)
- `UnitGroup`: `unit.dying` block checks currentHP too (Prevent 0-hp zombie unit)
- `getattr(EPDCUnitMap, attrName)` correctly raises `AttributeError`
- `EUDLoopUnit2`: rollback to use `0x0C CSprite` to detect unit death when there's no plugin whose name has `unlimiter`

## [0.9.7.10] - 2022.10.18
- Updated eudplib 0.70.12
- Fixed bug causing unsupported EUD error in `PVariable[var] -= value;` (reported by @westreed )
- Fixed compile error for `PVariable` with `<<=`, `>>=`, `^=`
- Fixed bug in `var <<= var;`not storing output to variable

## [0.9.7.9] - 2022.10.17
- Added `numpy` library
- Updated to Python 3.10.8
- Updated eudplib 0.70.9
- [epScript] Fixed bugs in in-place item comparisons and writes, and migrate to epScript side (reported by 34464 and others)
  * Fixed bugs in comparison operator precedence
  * Fixed bug in `>`, `<`, `&=`
- Fixed armoha/euddraft#82 : wrongly replace `Disabled(PreserveTrigger())` to `preserved=True` trigger flag (reported by @Chromowolf )
- Fixed some triggers did not running repeatedly (reported by ehwl)
- Fixed `var << number` compile error (reported by GGrush)
- Fixed bug in `EUDNot`
- Fixed `*=`, `/=`, `<<=`, `>>=` wrongly convert Lvalue `var` into Rvalue
- Fixed armoha/euddraft#65 : better error message for `if (Action)`

## [0.9.7.3] - 2022.10.09
- Optimize in-place item comparisons and writes for `EUDArray` and `EUDVArray` (https://github.com/armoha/eudplib/commit/3a1287507cda4d9988b96e983a22b9d7c61c170c)
  * Implemented various `EUDVArray` operation optimizations.
- Add missing operator `%` for `ItemProxy` (reported by 34464)
- [epScript] bugfix in helper.py (reported by 34464)
- Fix bug in `ItemProxy` with `EUDVariable` methods (reported by 택하이)
- Fix bug in `ItemProxy` with `EUDSwitch` statement (reported by 34464, Cocoa)

## [0.9.7.0] - 2022.10.08
- Fix error on `EncodeAIScript` (armoha/eudplib#15, contributed by @joshow)
- Add documentations for classic triggers (armoha/eudplib#17, contributed by @zuhanit)
- Fix error on `EPDCUnitMap.isBlind()` (reported by wdcqc)
- Optimize in-place item comparisons and writes for `EUDArray` and `EUDVArray` (armoha/eudplib#18)
  * still work-in-progress for `EUDVArray[const] -= var` and `EUDVArray[var] &= value` etc.
- Better error message for `EUDLoopPlayer(ptype, force, race)`
- Update eudplib 0.70.0

## [0.9.6.1] - 2022.07.03
- epScript update
- Fixed `PVariable` cast bug, parameter type bug
- Improved `PVariable` performance more
- Added read-only property `epd` on `UnitGroup.cploop`\
  You can get `epd` with `const epd = unit.epd;` (runs 4 triggers)
- epScript: separate stubCodes\
  Separate helper functions e.g. `_CGFW` to separate file\
  Prevent user from overwriting internal helper function by mistake
- `EUDLoopUnit2` optimization
  Runs 5 triggers -> 3 triggers per each alive unit
  (was equal to `UnitGroup` iteration but now faster)
- `switch` statement binary search performance optimization
- fixed bug on `EPDCUnitMap`: `unit.is_dying`
- Encode functions like `EncodeLocation` fixed to try both UTF-8 and CP949
- eudplib 0.69.9 update

## [0.9.6.0] - 2022.06.02
- Added `f_pow(a, b)`
  Calculates `a^b` (base `a`, and exponent or power `b`)
- Optimized `EUDLoopUnit2`
  Runs 9 Triggers -> 5 Triggers for every alive units (was slower than looping `UnitGroup` but now has same performance)
- `PVariable` now accepts `TrgPlayer` for index subscript: `pvar[P1] += 1;`
- Fixed bug in `soundlooper`
- `EncodeUnit` will try `UTF-8` and then `CP949` for unit name encoding
- epScript: Fixed `AddCurrentPlayer` not working
- Updated eudplib 0.69.8

## [0.9.5.9] - 2022.05.22
- Fixed `epdswitch` bug not restoring CurrentPlayer
- Bugfix in switch
- switch statement will use simple comparisons, jump table or binary search according to cases' distribution
- Add `UnitGroup`
    ```js
    // epScript example

    // UnitGroup Declaration
    const zerglings = UnitGroup(1000);
    // max capacity = 1000

    // Register Unit
    zerglings.add(epd);

    // Loop UnitGroup
    foreach(unit : zerglings.cploop) {
        // Run Triggers on **any** zerglings (alive or dead)
        foreach(dead : unit.dying) {
            // Run Triggers on dead zerglings
        }  // <- dead zergling will be removed at end of *dying* block
        // Run Triggers on alive zerglings
    }

    // example usage
    function afterTriggerExec() {
        const zerglings = UnitGroup(1000);
        foreach(ptr, epd : EUDLoopNewUnit()) {
            const cunit = EPDCUnitMap(epd);
            if (cunit.unitId = $U("Zerg Zergling")) {
                zerglings.add(epd);
            }
        }
        foreach(unit : zerglings.cploop) {
            foreach(dead : unit.dying) {
                // spawn Infested Terran when zergling dies
                dead.move_cp(0x4C / 4);  // Owner
                const owner = bread_cp(0, 0);
                dead.move_cp(0x28 / 4);  // Unit Position
                const x, y = posread_cp(0);

                setloc("loc", x, y);
                CreateUnit(1, "Infested Terran", "loc", owner);
            }
        }

        // user can also remove unit from group with user-defined conditions.
        // error will be return if `unit.remove()` is never called.
        // Currently, it is also an error if `unit.remove()` is called twice or more times...
        foreach(unit : zerglings.cploop) {
            // remove zergling from its group when it burrows
            unit.move_cp(0xDC / 4);  //  Burrowed = 0x00000010
            if (DeathsX(CurrentPlayer, AtLeast, 1, 0, 0x10)) {
                // kill zergling when it burrows
                unit.move_cp(0x4C / 4);
                bwrite_cp(0, 1, 0);  // set order to Die
                unit.remove();
            }
        }
    }
    ```
- Add `EUDQueue`
  ```js
  const queue = EUDQueue(20)();  // maximum size
  queue.append(1);
  queue.append(4);
  queue.append(2);
  if (!queue.empty()) {
      const a = queue.popleft();
      const b = queue.popleft();
      const c = queue.popleft();
      simpleprint(a, b, c);  // 1, 4, 2
  }
  ```

## [0.9.5.8] - 2022.05.16
- Fixed bug in `getcurpl()`
- Allow constant for switch variable
- Added bitmask in switch statement (default: `0xFFFFFFFF`)
- Added `EPDSwitch`
  ```js
  var x = 1 + 256;
  switch (x, 255) {
    // 256 in x is ignored, since switch mask is 255
    case 0:
      // Don't run
      break;
    case 1:
      // Run!
      break;
  }

  const unitId = epd + 0x64/4;
  epdswitch (unitId, 255) {  // you can put constant epd in epdswitch too
    // switch branching by unit kind
    case $U("Terran Marine"):
      // Run when unitType is marine
      break;
    case $U("Terran Ghost"):
      // Run when unitType is ghost
      break;
  }
  ```
- Fixed bug in switch with no case, or switch with case 0

### Changed
- ```ini
  :: Removed unit name string force re-encoding feature.
  :: UTF-8 string map no longer needs to write `decodeUnitName : UTF-8` option.

  :: Now CP949 string map *must* add below option to be able to concatenate unit name to string.
  [main]
  decodeUnitName : CP949
  :: This is mandatory when you want to display unit name by StringBuffer or customText,
  :: and when you're using outdated version of SCMDraft2 or not using locale 65001 (UTF-8).
  ```
- Applied `/MT` option for `libepScriptLib.dll`: distribution includes vcruntime.
- Updated `pybind11`

### Improved
- Optimized `EUDSwitch`\
  : Only search XOR bits of all cases. No longer use binary search.\
  Internally use 0 condition 0 action jump table triggers.
- Improved trigger conditon/action error message
  ```py
  DoActions(CreateUnit(1, "Artanis", P8, "Anywhere"))
  # EPError: [Warning] "P8" is not location
  ```
- Optimized `StringBuffer.print/printAll`, `DisplayTextAll`
- Updated Korean translation

### Added
- Added all user actions (including observers)\
  : `DisplayTextAll(text)`, `PlayWAVAll(soundpath)`,
  `MinimapPingAll(location)`, `CenterViewAll(location)`,
  `SetMissionObjectivesAll(text)`, `TalkingPortraitAll(unit, time)`
- Added simple mask write functions\
  : `maskwrite_epd(epd, value, mask)`, `maskwrite_cp(cpoffset, value, mask)`
- Added CUnit and CSprite read functions
  - `f_epdcunitread_epd`, `f_epdcunitread_cp`\
    : read epd of CUnit.
  - `f_spriteread_epd`, `f_spriteread_cp`\
    : read ptr of CSprite.
  - `f_spriteepdread_epd`, `f_spriteepdread_cp`
    : read ptr, epd pair of CSprite.
  - `f_epdspriteread_epd`, `f_epdspriteread_cp`
    : read epd of CSprite.
- More `EPDOffsetMap`, `EPDCUnitMap` functionalities
  - `"cunit"` type returns `ptr, epd` pair.
  - `"sprite"` type returns `epd`.
  - `buildQueue` indexing changed from 1 to 5.
  - Added methods on `EPDCUnitMap`
    ```js
    cunit.setloc(location);
    cunit.set_color(player);
    if (cunit.check_status_flag(value)) ...
    if (cunit.check_status_flag(value, mask)) ...
    cunit.reset_buildq();
    cunit.reset_buildq(Q1=0xE4);
    cunit.die();
    cunit.set_status_flag(value);
    cunit.set_status_flag(value, mask);
    cunit.clear_status_flag(mask);
    cunit.remove_collision();
    cunit.set_invincible();
    cunit.clear_invincible();
    cunit.set_gathering();
    cunit.clear_gathering();
    cunit.set_speed_upgrade();
    cunit.clear_speed_upgrade();
    cunit.set_hallucination();
    cunit.clear_hallucination();
    cunit.power();
    cunit.unpower();
    cunit.set_air();
    cunit.set_ground();
    cunit.set_noclip();
    cunit.clear_noclip();
    if (cunit.is_dying()) ...
    if (cunit.is_completed()) ...
    if (cunit.is_hallucination()) ...
    if (cunit.is_in_building()) ...
    if (cunit.is_in_transport()) ...
    if (cunit.is_burrowed()) ...
    ```
  - Added more members on `EPDCUnitMap`\
    : [See hyperlink for details, (type, size, offset) of each entries](https://github.com/armoha/eudplib/blob/b94a3ff0fe2a90d189f92b9b24e33fa700efa583/eudplib/eudlib/epdoffsetmap.py#L132-L327)

## [0.9.5.4] - 2022.05.05
- Add keyword argument `dest`, `nextptr` for `EUDVArray`
- Add `ConstExpr` checking for `nextptr` of `RawTrigger`
- Allow `None` for argument of `nonConstActions` for `SeqCompute` to reuse some parts of variable trigger
- Allow layout stacking on `EUDVarBuffer`
- Fix bug when there're few custom variables
  occurs on CtrigAsm maps which load few eudplib function

## [0.9.5.3] - 2022.04.17
- (Hotfix!) Fixed bug in custom variable buffer
- Added function `ShufflePayload(mode)` (default: `True`)\
  Similar to `CompressPayload(mode)`, turn on or off shuffling objects after Collecting phase.
- Added `[main]` config option `shufflePayload : True`
- Updated eudplib 0.69.3

## [0.9.5.2] - 2022.04.14
- (armoha/euddraft#55) Better config error message (by @zuhanit)
![better config error message](https://user-images.githubusercontent.com/36349353/163330102-91b83907-4d6d-4484-a787-22231d1d62ca.png)
- (armoha/eudplib#5) Speed up compile time: better EUDVariable trigger-generating (about -20% for `test_unittest`)
- Added keyword argument `nextptr` for `EUDVArray`, `EUDVariable`, `EUDXVariable`
- (armoha/euddraft#37) Fixed bug in `[main] objFieldN : x` (solved
- Added keyword argument `currentAction` for `RawTrigger`
- Updated eudplib 0.69.2

## [0.9.5.1] - 2022.03.29
- `[chatEvent]` Fix bug in cache invalidation (bd87ea16261092c3ec14b400700ca4562c2c21b5)
- Optimize temporary variables in arithmetics (https://github.com/armoha/eudplib/pull/4):
  ```js
  // ① Now use 1 variable. Still does addition 5 times...
  // Previously this code created temporary variables on every additions
  dwread_epd(0) + 1 + 2 + 3 + 4 + 5;  // 10T25A -> 5T5A (Reduced 5 Triggers 20 SetDeaths)
  // ② Faster methods. Previously these codes created 1 temporary variable too, now gone!
  dwread_epd(0) + (1 + 2 + 3 + 4 + 5);  // 2T5A -> 1T1A
  1 + 2 + 3 + 4 + 5 + dwread_epd(0);    // Both reduced 1 Trigger 4 SetDeaths
  ```
- Add `EUDVariable.IsRValue()`
- Allow `>`, `<` for `EUDLightVariable`
- `[MSQC]` allow EUDLightBool as conditional by @Chromowolf (#52)

## [0.9.5.0] - 2022.03.26
### Changed
- 64 bit release
- Updated `Python 3.10.2`, `cx_Freeze 6.10`, `pybind11`
- Updated `StormLib`, `eudplib 0.69.1`
- Add bitmask `0xFFFFFFFF` for all `EUDVariable`
- `[chatEvent]` Removed `__encoding__` option. Ignore it when provided.

### Improved
- Optimize basic arithmetics of `EUDVariable` using EUD bitmask\
Design: https://blog.naver.com/kein0011/222649764825 \
Implementation: https://cafe.naver.com/edac/110286
- `epScript`: local `var` won't additionally copy RValue
  ```js
  // now run same amount of triggers on both cases
  const a = dwread_epd(0);
  var b = dwread_epd(0);
  ```

### Bugfix
- (#51) Fixed aliasing bug in initializing multiple local variables
- Fixed `UnicodeEncodeError` in EUD Editor 3 .eds compile\
example: `[chatEvent]` writing japanese song title: https://cafe.naver.com/edac/109969
- `[MSQC]` Fixed bug in `xy, src1, src2 : dst1, dst2` syntax: https://cafe.naver.com/edac/109844
- `[MSQC]` Fixed displaying names of mouse locations

### Added
- `[chatEvent]` Add SipHash feature\
Chat messages to detect are no longer stored as plaintext on map file.\
instead, hashes are stored and compared to player chat messages: https://cafe.naver.com/edac/110699
- Add optional parameter subp for `f_strlen_epd(epd, subp=0)`
- Add in-place operations for all variable types (`EUDLightVariable`, `EUDVariable`, ...): `&=`, `|=`, `^=`, `<<=`, `>>=`

## [0.9.4.8] - 2022.01.09
- Add `Image`, `Iscript` types and `EncodeImage`, `EncodeIscript` functions.
```js
// Change image Scanner Hit sprite uses
function ScannerImage(image: Image) {
    wwrite(0x666458, image);
}
function afterTriggerExec() {
    ScannerImage("Hallucination Hit");
}
```
- fadeOut text effects now paint last color in front of text when **(1) effect is finished** and **(2)** last color is one of **overwriting colors**.
   (Overwriting colors = 0: null, 5: gray, 0x14: invisible)
  * No need to call `TextFX_Remove(tag)` after fadeOut done when last color is 0 or 0x14.

## [0.9.4.7] - 2022.01.02
- eudplib 0.67.3
- (Hotfix!) Fixed bugs in MRGN protection

## [0.9.4.6] - 2021.12.28
- Add Location section protection
- Specialize `EUDByteWriter.writebyte(constexpr)` perf
- Improve `var * var` perf
- Update `pybind11`
- More `EPDCUnitMap` members: `originX`, `originY`, `secondaryOrderX`, `secondaryOrderY`, `rallyX`, `rallyY`
    (Still, `EPDCUnitMap.getpos("member")` is recommended.)

## [0.9.4.5] - 2021.12.23
- Fixed `freezeMpq.pyd` fail to load
- Updated `StormLib`
- `MPQ.Extract(fname)` extracts UTF-8 filename
- ~~Better `orphan condition` error message~~ (Reverted due to impact on compile time...)
- Better eudplib functions performance
  * All EPD read functions: Reduced 1 Trigger, 3 SetDeaths. Parameter directly edits `CurrentPlayer (0x6509B0)`, without intermediate variable.
  (`dwread_epd`, `cunitread_epd`, `maskread_epd`, `bread_epd`, `posread_epd`, ...)
  * `cunitread_epd`: Reduced 2 Triggers, 5 SetDeaths. Bitmask changes to `0x3FFFF0`. Moved `0x400008` to initial values.
  * `setloc_epd(loc, epd)`: Reduced 5 Triggers, 13 SetDeaths. Internally uses `posread_cp`. Retunred `x, y` directly edit location modifying actions.

## [0.9.4.4] - 2021.12.09
- `SCArchive` related change

## [0.9.4.3] - 2021.11.24
- Fixed `IsPName(player, "nickname")` condition didn't check end of name whose length is `4n+1`.

## [0.9.4.2] - 2021.11.21
- fix bug invoking freeze protection with non-ASCII filename in non-Korean OS

## [0.9.4.1] - 2021.11.17
- bugfix: `StringBuffer.DisplayAt`, `printAt` printed on wrong line when `line` was `EUDVariable`.

## [0.9.4.0] - 2021.11.16
- Optimized random functions, `DisplayTextAt`, `StringBuffer.DisplayAt`, `f_repmovsd_epd`
- Added `f_printAll`, `f_printAllAt`, `FixedText`
  - **f_printAll(format_string, \*args)**\
    Print text for all players.
  - **f_printAllAt(line, format_string, \*args)**\
    Print text for all players on line.
  - **FixedText( *(optional)action(s)_to_execute_at_end* )**\
    Store textptr at start of `FixedText`, restore textptr back when `FixedText` ends.\
    Useful for printing (multiple) texts and preserving existing chat messages without `f_gettextptr` call.
    ```py
    # Example: DisplayTextAt with f_gettextptr
    @EUDTypedFunc([None, TrgString])
    def DisplayTextAt(line, text):
        display_text = DisplayText(0)
        textptr = f_gettextptr()
        VProc([line, text], [
            line.QueueAddTo(EPD(0x640B58)),
            text.SetDest(EPD(display_text) + 1),
        ])
        RawTrigger(
            conditions=Memory(0x640B58, AtLeast, 11),
            actions=SetMemory(0x640B58, Subtract, 11),
        )
        DoActions(display_text, SetMemory(0x640B58, SetTo, textptr))

    # Example: DisplayTextAt with FixedText
    @EUDTypedFunc([None, TrgString])
    def DisplayTextAt(line, text):
        display_text = DisplayText(0)
        with FixedText(display_text):
            VProc([line, text], [
                line.QueueAddTo(EPD(0x640B58)),
                text.SetDest(EPD(display_text) + 1),
            ])
            RawTrigger(
                conditions=Memory(0x640B58, c.AtLeast, 11),
                actions=SetMemory(0x640B58, c.Subtract, 11),
            )
    ```
- Update Cython version
- Added specifying initial destination and modifier for `EUDVariable` and `EUDXVariable`\
  `EUDVariable(dest, modifier, value)`\
  `EUDXVariable(dest, modifier, value, bitmask)`
- Added `EUDFullFunc`
    ```py
    # Example: DisplayTextAt with EUDFullFunc
    # initially set parameter `line` to add on textptr
    # initially set parameter `text` to modify DisplayText action
    _display_text = DisplayText(0)
    @EUDFullFunc(
        [
            # inital destination, modifier, value, bitmask for parameter `line`
            (EPD(0x640B58), Add, 0, None),
            # inital destination, modifier, value, bitmask for parameter `text`
            (EPD(_display_text) + 1, SetTo, 0, None)
        ],
        [None, TrgString],
    )
    def DisplayTextAt(line, text):
        with FixedText(_display_text):
            VProc([line, text], [])
            RawTrigger(
                conditions=c.Memory(0x640B58, AtLeast, 11),
                actions=c.SetMemory(0x640B58, Subtract, 11),
            )

    # Example: Optimizing f_repmovsd_epd with EUDFullFunc
    _cpmoda = Forward()
    @EUDFullFunc(
        # initially set `dstepdp` to add on _cpmoda
        # initially set `srcepdp` to modify CurrentPlayer
        [(_cpmoda, Add, 0, None), (EPD(0x6509B0), SetTo, 0, None)],
        [None, None, None],
    )
    def f_repmovsd_epd(dstepdp, srcepdp, copydwn):
        global _cpmoda

        VProc([dstepdp, srcepdp], c.SetMemoryEPD(_cpmoda, SetTo, -1))

        if EUDWhileNot()(copydwn == 0):
            cpmod = f_dwread_cp(0)
            _cpmoda << EPD(cpmod.getDestAddr())

            VProc(
                cpmod,
                [
                    cpmod.AddDest(1),
                    c.SetMemory(0x6509B0, Add, 1),
                    copydwn.SubtractNumber(1),
                ],
            )

        EUDEndWhile()

        f_setcurpl2cpcache()
    ```

## [0.9.3.9] - 2021.11.15
- Allow `<<=` and `>>=` for `EUDVariable`
  * Allow `const << var`, `const >> var`
- Allow comparison between `ConstExpr`s (`baseobj` and `rlocmode` should be equal.)
  ```py
  from eudplib import *

  array = EUDArray(4)
  a, b = array + 4, array + 8
  if a < b:  # True
      pass
  ```

## [0.9.3.8] - 2021.10.30
- Fixed SetPName
- Added `f_eprintAll(format_string, *args)`
  * Print on error line for all players.

## [0.9.3.6] - 2021.09.10
- eudplib 0.66.3
- **[epScript]** Added relative path import. Closes #39.
    Example)
    ```js
    /* c.py
     * folder
     * ├ b.eps
     * └ inner
     *　└ a.eps
     * src
     * └ main.eps (plugin [main.eps])
     ***/

    // import `c.py` in `src/main.eps`
    import ..c;
    // import `folder/b.eps` in `src/main.eps`
    import ..folder.b;
    // import `folder/inner/a.eps` in `src/main.eps`
    import ..folder.inner.a;

    // import `folder/inner/a.eps in `folder/b.eps`
    import .inner.a;

    // import `folder/b.eps` in `folder/inner/a.eps`
    import ..b;
    // import `c.py` in `folder/inner/a.eps`
    import ...c;
    ```
- Fixed `StringBuffer.fadeIn`/`fadeOut` didn't erase previous texteffect on screen when tag is not specified.
- Changed `StringBuffer.fadeIn`/`fadeOut` with `line=10` or `line=-1` to push existing messages up instead of overwrite.
- Added `StringBuffer.tagprint(format_string, *args, line, tag)`  \
    print function with tag. You can erase the message on screen with `TextFX_Remove(tag)`.

## [0.9.3.4] - 2021.08.31
- Added `once` conditional. (`EUDExecuteOnce()(conditions)` in eudplib)
    ```js
    once (condition1 && condition2) {
        onceStatements;
    }

    static var k = 0;
    const function_with_side_effect = function (x) {
        k++;
        return x;
    };
    for(var i = 0; i < 10; i++) {
        once (function_with_side_effect(true)) {
            simpleprint("function_with_side_effect is called exactly once.");
        }
    }
    simpleprint("k ==", k);  // k == 1
    ```
- `once` with no condition costs from 2 triggers to 1 trigger.
- Updated `pybind11`.

## [0.9.3.3] - 2021.08.25
- eudplib 0.66.0
   * (beta) Optimize `if` statement and `&&` for constant condition with no side effect. (`EUDSCAnd`)
   * Added `Condition.Negate()`, `EUDLightBool()`
- `[MSQC]` : Fixed bug when string limit is exceeded
- Better error message for duplicated plugin config
    * ```
      :: Error message example)
      [chatEvent]
      SOUL LADY : 20200721
      SOUL LADY : 13

      :: Duplicate key SOUL LADY in [chatEvent]
      :: [Line 120] SOUL LADY : 20200721
      :: [Line 121] SOUL LADY : 13
      ```
- Upgrade to Python 3.8.10, cx_Freeze 6.8b3

## [0.9.2.0] - 2021.04.15
- Updated `StormLib.dll` to latest unicode build.
- eudplib 0.65.1
  * `$T`, `EncodeString` use `utf-8` when string can't be encoded with `cp949`.
- `[cammove]` Fixed off-by-one location errors: Fixes #30
- Removed `QueueGameCommand_LeaveGame` (no-op)

## [0.9.1.5] - 2021.03.31
- `[MSQC]` Fixed val/xy didn't set return value for 0. (#5)
- Fixed `{:s}` in formatted print for malaligned constant string. (#26)

## [0.9.1.4] - 2021.03.17
- `f_settbl`: Added encoding parameter (default: "CP949")
`f_settbl(tbl, offset, *args, encoding="cp949")`
`f_settblf(tbl, offset, format_string, *args, encoding="cp949")`
`encoding` specifies which encoding `str` arguments will use.
When `encoding` is "utf-8", `f_settbl` or `f_settblf` appends "\u2009\0" at end of tbl string, to ensure SC:R to always interpret as unicode entry.
(Partial edit functions `f_settbl2`, `f_settblf2` do **not** add any null terminator or thin space character.)
It is user's responsibility to use same encoding in other types of arguments; `bytes`, `Db` etc.

## [0.9.1.3] - 2021.03.07
- No more compile error when `(Set)Memory(X)` address is not aligned by 4. (Truncated to close address)
- Fix typos in `TrgTBL`
- Fixed `EUDLoopUnit2` not worked with **[unlimiter]**
- Added `objFieldN` option to specify max field number of epScript `object` (`EUDStruct`)
```
[main]
...
objFieldN: 16
```

## [0.9.0.9] - 2021.01.28
- More map protection
- Added missing entries of `EPDCUnitMap`
- Added option to specify encoding to decode unit name string
```cs
[main]
...
decodeUnitName : utf-8
```

## [0.9.0.8] - 2020.12.11
- Fix bug when handling negative filesize in mpq fails to compile.
```py
    File "C:\Py\lib\ctypes_init_.py", line 62, in create_string_buffer
    ValueError: Array length must be >= 0, not -1
```

## [0.9.0.7] - 2020.12.09
- Fixed compile error when last string does not have null terminator.

## [0.9.0.6] - 2020.11.21
- Updated `cx_Freeze`
- Fix `IsPName(player, nickname)`
- (`Set`)`Memory`(`X`) now raises error for unaligned memory address.
- *[chatEvent]* fixed bug using unaligned address to bypass duplicate address checking.

## [0.9.0.4] - 2020.10.08
- Added `IsPName(player, name)`
  * player: player to check their name, should be `Player1` ~ `Player8` or `CurrentPlayer`.
  * name: nickname to check if equals, should be `"string"` or `Db` type.

## [0.9.0.3] - 2020.09.30
* Fix bug (0000.00) null terrain tile wasn't actually replaced with (0000.01) null tile.

## [0.9.0.2] - 2020.09.23
- **[chatEvent]** Fixed `ptrAddr` not being set when chat is detected. Added initialization of `lenAddr` and `ptrAddr` to 0
- Replace (0000.00) null terrain with (0000.01) tile if present in the map, and warn

## [0.9.0.1] - 2020.09.09
- Fixed `ctypes/create_string_buffer` error

## [0.9.0.0] - 2020.08.08
- Initialize payload at compile time
  * Remove `CreateVector/PayloadRelocator` ( see: https://cafe.naver.com/edac/88753 )

- Unify `Encode~/Get~Index` functions. Remove `TrgLocationIndex`
  * Both functions now start from 1. Subtract 20 from code using `0x58DC60`. (see: https://cafe.naver.com/edac/83158 )
  * No need to worry about when to add 1 to locations anymore.
  ```js
  $L("Anywhere")  // = 64
  ```
- Add keyword-only argument `sectorSize` to `SaveMap`
  * Value: 3~15. Regular editors use 3 and WarCraft 3 optimizer uses 7.
  * `euddraft` uses **15** for testing.
  * Think of it as the base MPQ compression unit. Higher values reduce map size.
  * When `sectorSize` is set, only files in (listfile) are copied to the output map.
    ```cs
    [main]
    sectorSize: 3  # Write like this, under [main]
    ```
    - Setting is ignored for maps using **freeze** or **SCDB**.

### Bugfix
- Fix bug where inlined triggers with `Disable`-checked `PreserveTrigger` actions still repeat
- Fix **[MSQC]** error when input map uses `STRx` section

### Other
- Change MPQ compression algorithm
- Set TBL start address to a multiple of 4
- Improve file path readability in `eudplib` internal error messages
- Update `StormLib`
- Fix missing `"Switch 256"`
- Fix `f_settblf2` typo
- Fix tempcustomText rwcommon error in EUD Editor 2
- Add `MPQCheckFile(filename)`: function to check whether the given filename already exists in MPQ
- Convert `StringBuffer.print("text with size 32 or larger")` to `DisplayText`
- Remove `OpenSSL`, `mpaq` features, update freeze
- Remove unused values/flags from `UNIT`, `UNIx`, `UPGx`, `TECx`
- Make it a compile error to use SCDB and freeze together (08.03)

## [0.8.9.9] - 2019.12.09
Update **eudplib 0.61**

### Bugfix

- Fix bug where **StringBuffer** string addresses are not multiples of 4
- Fix bug where `DisplayTextAt` does not compile

### Added

- Add multilingual support for **eudplib** messages

    - Load system locale by default. Can be set with the `LANG` environment variable.
    - On Windows `cmd`, set English with `setx LANG en`.
- Localize eudplib error messages and print all warnings/errors to stderr
- Change all string addresses to multiples of 4
- Add `EUDByteStream`

  Both `.readbyte()` and `.writebyte(b)` are available, and\
  Current position can be passed to another `EUDByteReader`/`Writer`/`Stream` with `.copyto(byterw)`.
- Add `ep_warn`, `EPWarning`, `ep_eprint`
- Optimize `CPByteWriter`, `f_strnstr` performance

### Changed

- Deprecation warning for `_safe` read functions

  `f_dwepdread_epd_safe`, `f_dwread_epd_safe`, `f_epdread_epd_safe` will be removed in **eudplib 0.63**.


## [0.8.9.8] - 2019.12.05

### Changed

- Roll back `StringBuffer`

  Change `soundlooper` to write strings per player instead of per sound file.


## [0.8.9.7] - 2019.11.23

### Bugfix

- Fix bug where `"Protoss Unused type   1"` was coded as Assimilator.
- Fix `StringBuffer.fadeInf`, `.fadeOutf` not returning whether text effects finished. (Thanks to Yuuki-Asuna for reporting.)

### Added

- Update to Python 3.8, cx_Freeze 6.1.
- Optimize `*=`, `//=`, `%=` to return directly into lhs.


## [0.8.9.6] - 2019.11.13

### Added

- Skip inlining for incompressible triggers.

    Thanks to Yuuki-Asuna for helping determine the trigger size cutoff.


## [0.8.9.5] - 2019.11.12

### Added

- Add TRIG trigger sharing.

    Repeating triggers without `Wait` or `Transmission` actions are inserted only once and shared by all trigger players. Only applied when inlining rate is 1.\
    Even if trigger players 2-8 are checked, only one trigger is inserted and linked by modifying `nextptr`.

    - Size reduction example for a 4005-trigger map (TrigEditPlus 160k lines)

        ```
        basemap: 2.17MB
        Without sharing: 3.01MB (freeze: 3.23MB)
        Trigger sharing: 1.76MB (freeze: 2.09MB)
        ```

### Bugfix

- Fix bug where printing 11 lines of text with `StringBuffer` to multiple players overwrote content.

### Changed

- **Set default inlining rate to 1.**

    Apply `PRT_SetInliningRate(1)` by default. This should reduce size in most cases. **If triggers behave strangely after the patch and turning it off with `PRT_SetInliningRate(0)` fixes it, please report it!** There may be other actions besides `Wait` that must not be shared.

- Remove `Always` conditions, `Comment`, `PreserveTrigger` actions from TRIG triggers.

    Use the trigger's `preserved` flag instead of the `PreserveTrigger` action.


## [0.8.9.4] - 2019.11.04

### Added

- Allow `PRT_SetInliningRate(1)` full-trigger inlining for [freeze] and inline_eudplib maps.

### Bugfix

- Fix bug where `f_wwrite` with subp 3 only wrote the front byte.


## [0.8.9.3] - 2019.11.04

### Bugfix

- [freeze] hotfix.
- Fix bug where inlined triggers always had size 2408 bytes.

### Added

- Add experimental full-trigger inlining.

    Enabled with `PRT_SetInliningRate(1)`. Moves all triggers to strings. Reduces size when the proportion of single-trigger-player triggers is high.


## [0.8.9.2] - 2019.11.02

### Bugfix

- **Fix [freeze] protection bug**

    - Up to [0.8.9.0], triggers using CP trick in input maps sometimes failed to execute. [0.8.9.1] had a chance of the bug even without CP trick due to a mistake during optimization/obfuscation.


## [0.8.9.1] - 2019.10.29

### Added

- Make `DoActions` accept variable arguments.

  Can be used as `DoActions(action1, action2, action3, ...)` without a list.
- Optimize EUD function returns.
  - Move all function-return-related actions to the call trigger. Now functions with return values use only one trigger per call. Fewer actions are executed.
  - Add `ret=[variable list]` keyword argument to EUD function calls.
    ```python
    v << f_bitxor(v, key)  # Return value is stored in a temp variable and reassigned to v.
    f_bitxor(v, key, ret=v)  # Return value is assigned directly to v.
    ```
- Add `EncodeTBL("string")` function to convert `stat_txt.tbl` strings to their IDs.
  - Use `$B("string")` in **epScript**.
  - `f_settbl`, `f_settbl2`, `GetTBLAddr` now also accept strings as arguments.
  - See [TBL string list].
- Remove `VProc` action count limit. Return a list of triggers when there are 2 or more triggers.
- Add `EUDXTypedFunc(bitmasks, argtypes, rettypes)`, EUDXVariable`.getMaskAddr()`.
- Harden `[freeze]` against vulnerabilities. Prevent unFreeze.
  - Make eudplib code private and take down pip since an automatic freeze unprotector was released.

### Changed

- **freeze protector is applied by default.** To disable, add the following to .eds, .edd:
    ```
    [freeze]
    freeze: 0
    ```
- Optimize bitwise operations.
    - `AND, OR, NAND, NOR` are no longer EUD functions. Compute with a single trigger.

### Bugfix

- Fix bug where function name was missing from error message when the number of return values was inconsistent;
```EPError: Numbers of returned value should be constant. (From function caller)```
- Fix argument error in method StringBuffer`.insertf(index, format_string, *args)`.


## [0.8.9.0] - 2019.10.19

This is a major update focused on new features.

### Changed

- Fix `f_simpleprint` to print to all players.
- Optimize `EUDByteReader`/`Writer`. Remove `EUDByteStream`.

    Calling EUDByteReader`.writebyte()` or EUDByteWriter`.readbyte()` now raises `AttributeError`. EUDByteStream seemed unused so it was removed; it will be restored if anyone uses it.

### Added

- Add function `f_parse(dst, radix=10)`:
  * `dst`: string address.
  * `radix`: 0 or 2-36, (default: base 10).

    Return the integer value converted from the string in the given base (default: base 10) along with the digit count. Return `0, 0` if it cannot be converted to a number. Negative numbers are supported, and leading whitespace is ignored. If `radix` is 0, read as binary if starting with `0b` or `0B`, octal if starting with `0o` or `0O`, and hex if starting with `0x` or `0X`.
  * Example patterns recognized as numbers (regex)

    - Binary: `\s*[+-]?(0[bB])?[01]+`
    - Decimal:` \s*[+-]?\d+`
    - Hex: `\s*[+-]?(0[xX])?[\da-fA-F]+`
  * Exception handling: parsing number 0 returns `0, 1`. Non-numbers return `0, 0`. Initially considered making something like EUDGetErrno, but switched to returning digit count as it seemed better.
  * Overflow protection: if absolute value exceeds 0x7FFFFFFF, return `±0x7FFFFFFF, digit count`.

    Digit count may be 1 larger for non-decimal bases. (If the quotient of 0x7FFFFFFF ÷ radix just before overflow is below, but digit count equals that of 0x7FFFFFFF, it is 1 larger. Otherwise it is the same.)

- Add format string support: no more readability loss from `"",` or `epd2s` when combining strings.
    ```javascript
    // Player title example
    SetPNamef(cp, "{:t} \x07Level: \x04{} {:c}{:n}", title, level, cp, cp);
    // Old way
    SetPName(cp, epd2s(title), " \x07Level: \x04", level, " ", PColor(cp), PName(cp));
    ```
    #### Supported format types
    - `c` : color of the given player number (=PColor)
    - `n` : name of the given player number (=PName)
    - `s` : string address to append (=ptr2s)
    - `t` : EPD address of string to append (=epd2s)
    - `x` or `X`: print value in hex (hptr)

    Later, `{:02}` will pad single digits with a leading 0 to two digits. (For decimal points, min:sec, hour:min:sec output, etc.)
  * Supported function list
    - Functions `SetPNamef(player, format_string, *args)`, `f_eprintf(format_string, *args)`
    - Methods StringBuffer`.printf(format_string, *args)`, `printfAt(line, format_string, *args)`, `insertf`, `appendf(format_string, *args)`, `fadeInf`, `fadeOutf(format_string, *args, color=(tuple), wait=1, reset=True, line=-1, tag=hashable)`
    - Functions `f_settblf`, `f_settblf2(tblID, offset, format_string, *args)`
    - Functions `f_sprintf(dst, format_string, *args)`, `f_sprintf_cp(format_string, *args)`: format-output versions of f_dbstr_print, f_cpstr_print.

- Add condition `IsUserCP()`:

    Condition comparing whether CurrentPlayer matches the user. It is a non-shared condition. Can also be used in RawTrigger. Like the old eudplib _f_initextstr, it writes the `f_getuserplayerid()` value to the value address at game start.

### Improved

- Improve performance when `f_dbstr_print` has 2 or more arguments.
- Optimize `EUDExecuteOnce`.
- Reduce init triggers from 500 to 427.
- Add `EUDLightVariable` feature:
  - Like EUDVariable, putting eudlv in a condition becomes eudlv`.AtLeast(1)`. Can be used as dst for SeqCompute, etc.


## [0.8.8.1] - 2019.10.10

### Added

- Add `epd2s` support to `f_dbstr_print`. (Fix `PColor`, `ct.color` related errors)
- Add EPDOffsetMap`.getdwepd(name)`.

  Returns `f_dwepdread_epd(offset)`.
- Optimize `SeqCompute` and EUD function calls: https://cafe.naver.com/edac/82207
- Optimize location functions (`f_setloc`, `f_addloc`, `f_dilateloc`) when the location is constant and the coordinates are variables.


## [0.8.7.9] - 2019.10.02

### Bugfix

- Fix values shifting after `EUDContinue` in `EUDLoopUnit2`.
- [chatEvent] Raise an error on duplicate `__Addr__`, `__lenAddr__`, `__ptrAddr__`, `__patternAddr__`.

### Changed

- Change the default to *-1* when no value is passed in [MSQC] `val` and `xy` syntax.

  Previously a 0 initial value was indistinguishable from a passed 0, so this was changed.
- Always use `STRx` as the string section. (Size 2GB, 65535 entries)
- Change `EUDLoopUnit2` to skip when the current order is [0]Die with [unlimiter], and when CSprite is 0 on maps not using it.

### Added

- Add `EPDCUnitMap`: https://cafe.naver.com/edac/82244
- Add [MSQC] `val` syntax. Print a hint text on how to turn it off when using `QCDebug`.
    ```
    additionalCondition ; val, src : dst
    ```
  - `src`: Unshared address or `EUDVariable` to pass.
  - `dst`: Shared unit (death value), `EUDArray`, or `PVariable`.
  - Passable value range
    - On 256x256 maps: 0~16,777,215
    - On 64x64 maps: 0~1,048,575
  - Use `val` instead of `xy` when passing unshared non-coordinate values (not locations or screen coordinates).

- `soundlooper`: Sound playback now works. (Thanks to 아티아 for testing.)

    - Accept up to 1000 sounds (0~999)
    - Accept varied sound file names: sound1.ogg, sound02.ogg, sound003.ogg, sound4.ogg
- Add function `GetGlobalStringBuffer()`. DBString`.Display()` now outputs to the global string buffer.
- Add EUD function `DisplayTextAt(line, TrgString)`.
  - `line`: 0~10, first line = 0, 11th line = 10.
  - Not an action. When no text composition is needed, this is faster than StringBuffer`.printAt`. String space is plentiful anyway... It combines chat and `DisplayText` viewing into a single function.
- Optimize `f_cp949_to_utf8_cpy(dst, src)` and return `dst`.


## [0.8.7.8] - 2019.09.25

### Changed

- (Temporary) `StringBuffer` now uses chat output. (It edits the screen directly like `SetPName`.)
    - StringBuffer`.Play()` (sound playback) does not work. Use this until the next patch.


## [0.8.7.7] - 2019.09.25

### Bugfix

- Fix [MSQC] encoding errors from console messages in other language environments.

### Added

- Add `CRGB` (player color) section support.
- Add `STRx` section support.

    Used when the input map is a Remastered-only map with a STRx section.
    Added in anticipation of STRx (65536 strings, 2GB total) support in the next SCMDraft2 release.

#### Notice on string modification

The SC:R 1.23.1.6623 patch blocked string content modification, so `StringBuffer`, `customText`, and `soundlooper` are currently broken; this cannot be fixed in eudplib/euddraft and needs a further patch. Chat output that edits already-displayed DisplayText still works, so use that for urgent cases. (`eprintln`, `customText.chatprint`, etc.)


## [0.8.7.6] - 2019.09.21

### Changed

- Revert the `f_settbl` change from [0.8.7.5]. (Fixes breakage from the function change in existing code)
- Add `f_settbl2(tblID, offset, *args)` for editing TBL sections. It does not append *\0*.

### Improved

- Keep the hash table size unchanged when it is already large enough for the added files.
- Show the corresponding Windows error when growing the hash table or inserting files fails.
- Slightly improve `f_dbstr_adddw` performance.
- Slightly improve loop performance (`EUDLoopList`, `EUDLoopUnit`, `EUDLoopNewUnit`, `EUDLoopUnit2`, `EUDLoopPlayerUnit`, `EUDLoopSprite`)


## [0.8.7.5] 2019.09.20

eudplib 0.59.1 is released on PyPI. Update with `pip install eudplib -U`.

### Changed

- `f_settbl(tblID, offset, *contents)` no longer writes the trailing string null (\0). (Reported by 갈대)

### Added

- Grow the hash / block table sizes to fit the number of added files. (Suggested by 아티아)

### Improved

- Optimize freeze: about 500 fewer objects on an empty map.


## [0.8.7.4] - 2019.09.12

### Bugfix

- Fix auto-update errors with no internet connection.
- Fix forced edd recompilation (R key) running repeatedly.


## [0.8.7.3] - 2019.09.02

### Bugfix

- Fix errors applying freeze protection by drag-dropping a map file onto euddraft.exe
- Fix `UnboundLocalError` in `f_strnstr`. (Thanks to 34464 for reporting.)
- Fix location function errors.
- Fix `PColor` errors.
- Fix errors using CurrentPlayer in the `SetKills` action.
- Fix **[epScript]** `SetKills` action not adding DoActions.

### Changed

- Change `PColor(player)` to detect the current player color and convert to a similar text color.

  Previously it only worked on maps using the default player colors (red~yellow); now it works on any map (based on the 256-color jungle palette researched by 혼돈과 무질서). <05> is not used.
- Change `str`, `int`, `bytes` argument behavior in string output functions from `CPString` -> `epd2s`.

  CPString was added over reports that customText lags, but the lag looks mostly due to unfamiliar EUD Editor 2 TriggerEditor usage and Classic triggers, so switch to `epd2s(EPD(Db(...)))`. It costs about 32x performance but saves about 10x map size; will revert if problematic.
- Passing a Db argument to string output functions now outputs as `epd2s(EPD(...))`.

### Added

- Add method StringBuffer`.printAt(line, *args)`.
- Allow `f_setloc`, `f_addloc`, `f_dilateloc` to take left/top/right/bottom coordinates:
    - `f_setloc("loc", x, y)` : Set to a point location at (x, y, x, y).
    - `f_setloc("loc", left, top, right, bottom)` : Set the location to (left, top, right, bottom)
    - `f_addloc("loc", x, y)` : Move the location by x, y.
    - `f_addloc("loc", left, top, right, bottom)` : Add (left, top, right, bottom) to the location coordinates.
    - `f_dilateloc("loc", x, y)` : Expand the location by x horizontally and y vertically.
    - `f_dilateloc("loc", left, top, right, bottom)` : Add (-left, -top, right, bottom) to the location coordinates.
- Overlap MRGN PRT and ORT triggers: size reduced 4816 -> 3244 bytes.
- Improve `_f_mul` (variable×variable multiply) performance
  - SetDeaths executed for 100×variable reduced 62 -> 41.
- Use only one trigger when all `f_setloc`, `f_addloc`, `f_dilateloc` arguments are constants.

#### To. 맛빙

- Add [freeze] prompt option.
    ```
    [freeze]
    prompt: 1
    ```
    Generates a normal scx, then applies MPQ protection after pausing and pressing any key.


## [0.8.7.2] - 2019.06.11

### Bugfix

- Fix f_raise_CCMU lowering the unit limit when executed in a Cannot state.

  Previously it was only known to lower the unit limit *when 0x628438 was modified without restoring the original value*, but *modifying 0x628438 in a Cannot state* also lowers the unit limit after the Cannot state is lifted. In a Cannot state 0x628438 is 0, yet SetMemory(0x628438, SetTo, 0) still lowers the unit limit. Never touch 0x628438 via actions in a Cannot state.

### Changed

- No more C++ build tools needed for `pip install eudplib`. (eudplib 0.59.0)
  - Password-based basemap unprotection was added in euddraft 0.8.4.8. It is only usable from eudplib and blocked in euddraft due to errors, and the new bsdiff4 dependency started requiring C++ build tools for eudplib installs. Since most users use euddraft and install eudplib only for text-editor autocompletion, it was moved to a separate branch in the distribution.


## [0.8.7.1] - 2019.06.08

### Bugfix

- Fix [MSQC] xy syntax erroring when src is an address.

### Added

- Add plugin [chatEvent].

  The old [채팅인식4] was made before EUDX and did not work well, so this was rebuilt with EUDX. eds/edd syntax is the same as [채팅인식4].
  - [chatEvent] eds/edd syntax
    ```
    [chatEvent]
    <chatTextToRecognize>: <number >= 2>
    @GG: 10
    └ When a user chats "@GG", address __addr__ is set to 10.
    　When __addr__ is not specified, 0x58D900 is used.
    　When a user chats but the text matches no eds/edd entry, address __addr__ is set to 1.
    ```

  - `^시작.*중간.*끝$: 숫자`
  - `^맛빙.*.*$: 1`

    When a user chats starting with "맛빙~", address `__patternAddr__` is set to 1.
  - `^.*.*팧$: 2`

    When a user chats ending with "~팧", address `__patternAddr__` is set to 2.
  - `^.*알타.*$: 3`

    When a user chats containing "~알타~", address `__patternAddr__` is set to 3. When `__ptrAddr__` is specified, `__ptrAddr__` is set to the chat start address. When `__lenAddr__` is specified, `__lenAddr__` is set to the chat length (in bytes).

  - EUD variables will also be usable as `__addr__`, `__ptrAddr__`, `__patternAddr__`, `__lenAddr__` in the next version.


## [0.8.7.0] - 2019.06.06

### Bugfix

- Fix [MSQC] `QCUnit`, `QCLoc`, `QCPlayer` not changing from default values
- Fix `EUDFunc`, `EUDMethod` to use `inspect.getfullargspec` instead of inspect.getargspec

### Added
- Add `f_setcurpl2cpcache()`.  ** Advanced **

  Sets CurrentPlayer (the value at offset 0x6509B0) as eudplib's CurrentPlayer cache. Use it to restore the original CurrentPlayer after using CP tricks. Note: changing 0x6509B0 and restoring it with `f_setcurpl2cpcache` with other CP-trick functions in between causes CP cache misses and performance loss. (Functions internally using CP tricks: ptr/epd read/write functions; `dwread_epd`, `wread`, `bwrite`, etc., `EUDByteStream`, `f_readgen_epd`, `f_strlen_epd`, `f_strlen`) Only use in simple functions that call no other functions mid-trick; in cases like f_cpstr_print where other functions run in the middle of CP tricks, it costs performance.

  Usage: https://github.com/armoha/eudplib/commit/18fd56c0775373d4da7041974c763975142f2c63

### Improved

- Replace `f_repmovsd_epd` with a simpler, faster version
- Apply `FlattenList` to `VProc`
- Save shared `EUDByteStream` count


## [0.8.6.9] - 2019.05.24

eudplib is also updated to 0.58.9.

### Bugfix

- Fix units placed at 100% energy appearing with default mana (50) in game.
(Thanks to 나도모름 for reporting)

### Added

- Add new methods to `EUDVariable`. ** Advanced **
    * EUDVariable`.getDestAddr()`
      - Address of the EPD address in the EUD variable's SetDeaths action.
      - Similar purpose to EUDVariable.getValueAddr(), the address of the value.
    * EUDVariable`.SetDest(epd)`
    * EUDVariable`.AddDest(epd)`
    * EUDVariable`.SubtractDest(epd)`: An action used in `VProc`, like EUDVariable`.QueueAssignTo(epd)`.

        When copying one variable's value to multiple addresses, using `QueueAssignTo` every time sets the variable with SetTo each time, so use `QueueAssignTo` only for the first copy and then just change the address to save one action each.
* Optimize `f_setcurpl(player)` when `player` is a variable.
  - Actions executed: 15 → 10
* Optimize CP-trick functions. (At least 22 fewer actions executed)
  - ptr/epd read/write functions, `EUDByteStream`, `f_readgen_epd`, `f_strlen_epd`, `f_strlen`.
* Remove unnecessary value copies in `f_dwrand`, `f_rand`
* Other optimizations including eudplib/trigger/filler.py.
- Remove duplicate dll files, move to lib folder.


## [0.8.6.8] - 2019.05.06

### Changed

- Delete location and switch name strings from the outmap.
- Delete location string-number info from the output map.
  - To save string capacity + slightly hinder unprotected-map editing. Not deleted when used as unit names, map titles/descriptions, or force names.
  - Note they will be deleted when locations/switches share a string with sounds/comments/DisplayText, etc.


## [0.8.6.7] - 2019.05.06

### Bugfix

- Fix all strings being encoded as `utf-8`


## [0.8.6.6] - 2019.05.06

### Bugfix

- Fix text effects showing in the default color. (Thanks to 아티아 for reporting)

### Added

- Improve `f_randomize` performance and change to `EUDFunc`.
- `VProc` now also accepts an iterable of EUDVariables as the first argument.
  - Sets nextptr in the order VProc -> variable1 -> variable2 -> variable3 -> ... -> next trigger.

### Changed

- Output maps are now saved as StarCraft: Remastered scx. (Not playable on 1.16)
- `u2b` now encodes text not encodable in cp949 as utf-8.
  - Characters not encodable in cp949, like Simplified Chinese, now use utf-8 encoding, fixing DisplayText errors. Changed for EUD Editor users in China.
- Strings used as unit names are now utf-8 encoded.
  - Unit names are now easier to use in string compositions. To use unit names in stat_txt.tbl compositions, convert back to cp949.
- **[epScript]** Actions now become triggers only when followed by a semicolon.
  - DoActions, RawTrigger, and Trigger can now be used in eps without py_eval.


## [0.8.6.5] - 2019.04.17

### Added

- Add **[epScript]** `list(...)`, `VArray(...)` syntax.
  - `VArray(initialValues)` : Create an `EUDVArray` with the given initial values.
  - `list(elements)` : Create a Python list.
    ```javascript
    var a, b, c, d;
    const vlist = list(a, b, c, d);
    const varray = VArray(1, 2, 3, 4);
    function afterTriggerExec() {
        foreach(i, v : py_enumerate(vlist)) {
            const e = VArray(a, b, c, d);
            e[v] = varray[i];
        }
    }
    ```
#### Note: array initialization in epScript
```javascript
// In-game initialization: initializes each time the code runs (at game start for global scope).
// Values decided in-game, like function return values, can also be used.
const a = [getuserplayerid(), 0, 0];
const b = VArray(GetTBLAddr(1), GetTBLAddr(2), GetTBLAddr(3));

// Compile-time initialization: initializes when inserted into the map. Only constant expressions allowed.
const a = EUDArray(list(1, 2, 3, 4));
const b = EUDVArray(4)(list(EPD(a), EPD(a)+1, EPD(a)+2, EPD(a)+3));
```


## [0.8.6.4] - 2019.04.15

### Bugfix

- Fix bug reading `PVariable[i]` with a constant index. (Thanks to 아스나 for reporting.)


## [0.8.6.3] - 2019.04.15

### Changed

- Improve `EUDVArray` performance
    * 3x+ faster reads via `EUDVArray[EUDVariable]`.
    * Use one trigger when both `EUDVArray` and index are constant in reads/writes.
- Change behavior when the index exceeds the `EUDVArray` length

    * When the index is an EUD variable, upper bits are ignored.
    Example) If the `EUDVArray` size is 5, 6, 7, or 8, only bits 4, 2, 1 of the index are read.

        ```javascript
        const a = EUDVArray(8)();
        var i8, i9 = 8, 9;
        a[i8];  // a[0]
        a[i9];  // a[1]
        ```

    * Exceeding the array size is undefined behavior and may change at any time! Do not use it!

    * Constant indices are caught at compile time with `ep_assert "EUDVArray index out of bounds"`.

- PVariable now supports type casting.


## [0.8.6.2] - 2019.04.10

### Bugfix

- Fix compile errors when dividing by 1. (Thanks to 아스나 for reporting)


## [0.8.6.1] - 2019.04.08

### Bugfix

- Fix `f_wwrite_epd(epd, subp, w)` and `f_wwrite(ptr, w)` writing 0 when the address is constant and w is an EUD variable. (Thanks to Photon for reporting.)
    - EUD Editor 2 TriggerEditor edits 2-byte data like weapon damage (both Set/Add) with wwrite instead of EUDX, so this bug since [0.8.4.6] caused constant-address SetDatfile/AddDatfile damage upgrades to set damage to 0 and other unintended behavior; please update.

### Changed

- Fewer triggers when multiplying/dividing by -1, 0, 1. Use `f_bitlshift` when multiplying by 2, 4, 8, ... , 128
- Optimize `f_dwbreak`, `f_dwbreak2`


## [0.8.6.0] - 2019.04.04

### Changed

- Change StringBuffer`.fadeIn/fadeOut` usage, add `line` argument
- StringBuffer`.fadeIn/fadeOut` returns *-1* on CurrentPlayer mismatch.
- Add newline (\n) support to `TextFX_FadeIn/FadeOut`

#### Simplified the text effect syntax, which was overly complex.
* `line`:
  * *0~10* pins output to lines 1~11 from the top
  * *-1~-11* prints on lines 1~11 from the bottom on first output, then stays at the previous position once shown (scrolling text like chat/DisplayText)
    ```javascript
    // epScrit example
    const s = StringBuffer(1023);

    function texteffect() {
        const tecolor = 4, 2, 0x1E, 5, 0;

        const t = s.fadeIn("\x13\x04The world was created from \x19a single light\x04.
    \n \n\x13\x04The light split the void in two, making heaven and earth,
    \n\x13\x04and named it \x19Artia World\x04 after himself.",
            line=6, color=tecolor, wait=2, tag=py_str("FAH")
        );
        if(t >= 1) return;

        var wait;
        wait += 1;
        if(wait <= 99) return;

        wait = 0;
        TextFX_SetTimer("FAH", SetTo, 0);
        TextFX_Remove("FAH");
    }


    function afterTriggerExec() {
        foreach(h : EUDLoopPlayer()) {
            setcurpl(h);
            texteffect();
        }
    }
    ```


## [0.8.5.8] - 2019.04.03

### Bugfix

- Fix text effects treating tabs and newlines like color codes (found by 아티아)
  - Fix `colors` overwriting tab/newline characters: `<09>` tabs and `<0A>`, `<0C>` newlines should have been exempted like `<12>`, `<13>` alignment codes, but were handled like color codes.
  - Note that using `\n` in TextFX still prevents removing the next line with `TextFX_Remove`, and writing line by line lets each line run its text effect independently, so writing one line at a time is recommended.


## [0.8.5.7] - 2019.04.03

### Bugfix

- Fix error when putting an Object into a trigger field (reported by 디펜더)
- Fix GetTBLAddr error


## [0.8.5.5] - 2019.04.02

### Bugfix

- Fix bug from a bad f_constdiv fix: a remainder calculation error left the remainder equal to the dividend, causing various bugs.

### Added

- Optimize variable×constant multiplication.
- Add `encoding` keyword argument to `f_dbstr_print` and `f_cpstr_print` (default: *"UTF-8"*)
- Add `f_settbl(tblID, offset, *contents)`


## [0.8.5.2] - 2019.04.02

### Bugfix

- Fix tpatcher bug (thanks to 아티아 for quick feedback)

### Changed

- `f_dbstr_print` and `DBString` now use *UTF-8* encoding by default.

### Added

- Optimize `f_dwrand` (17 fewer triggers)
- Optimize using variables in word and byte condition/action fields
  - Unit/resource/score types, (condition) switches, (action) flags, and alliance types now run 3 triggers instead of 37; other bytes require multiplication so run 12 triggers.
  - Conditions: switch state, comparison type, condition type, flags
  - Actions: unit count, switch state, action type, modifier, order
- Add EUDLoopPlayer: iterate only in-game players from P1–P8 matching the conditions.
  - Player types (Human, Computer, Neutral, Rescueable), forces (0–3), and races (ZTP, user-selectable, etc.) can be used as conditions. Like EUDPlayerLoop, defeated or empty slots are skipped.
  - Unlike EUDPlayerLoop, it does not change CurrentPlayer.
    ```javascript
    // epScript example

    foreach(h : EUDLoopPlayer()) {
        // +1 minerals for all in-game human players
        SetResources(h, Add, 1, Ore);
    }

    foreach(f1 : EUDLoopPlayer("Human", Force1)) {
        // +1 gas for in-game Force1 human players
        SetResources(f1, Add, 1, Gas);
    }
    ```

    ```python
    # eudplib example

    for u in EUDLoopPlayer("Human", None, "User selectable"):
        # +1 minerals for all human players with race set to User selectable
        DoActions(SetResources(u, Add, 1, Ore))

    for z in EUDLoopPlayer(None, Force2, "Zerg"):
        # +1 gas for Force2 Zerg players
        # (Does not include players who picked Zerg in the lobby as User selectable.)
        DoActions(SetResources(z, Add, 1, Gas))
    ```


## [0.8.5.1] - 2019.04.01

### Bugfix

- Fix `SetPName` initialization trigger bug.


## [0.8.5.0] - 2019.04.01

### Bugfix

- Fix `SetPName` reading one byte less of chat content (thanks to 아티아 for reporting.)
- Fix `SetPName` nickname comparison bug.
- Fix `no attribute` error when using `EUDArray` and `PVariable` in [MSQC]

### Added

- Allow location names as the first argument of location functions (`f_setloc`, `f_addloc`, `f_dilateloc`, `f_getlocTL`, `f_setloc_epd`).
- Add `EOS` keyword argument to `f_cpstr_print`.(Default=*True*)
    - With `EOS=False`, the string terminator is not written.


## [0.8.4.9] - 2019.04.01

### Bugfix

- Fix SetPName also modifying players whose nicknames contain another player's nickname (thanks to 아티아 for reporting.)

### Added

- Now `Db` can also be created from a string.
  - `Db("string")` is the same as `Db(u2utf8("string\0"))`.
- Optimize assigning variables to word/byte condition/action fields
  - Using variables in Unit and Modifier fields was over 32x slower than in dword fields like Player and Location; word and byte performance improved to about 50% and 75%. There is still room for improvement, so tpatcher.py will be rewritten in the next update.
- Add `SQC` library.
  - See the [SQC 사용법] link for usage. Fix mouse location not working on 96 and 192 sized maps.
- Rename plugin [MurakamiShiinaQC] ▶ [MSQC] and add features.
  - Rename `QCSafety` ▶ `QCDebug`
  - Add built-in unshared detection for keyboard, mouse clicks, etc:
    * `KeyDown(Q)`: recognized once the moment the Q key is pressed. Works only once even when held down.
    * `KeyUp(W)`: recognized once the moment the held W key is released.
    * `KeyPress(E)`: recognized continuously while the E key is held down.
    Writing just the key like Q ; W ; E as before applies as KeyDown.

    - `MouseDown(L)`  recognized once the moment the left mouse button is clicked.
    - `MouseUp(R)`       recognized once the moment the held right click is released.
    - `MosePress(M)`    recognized continuously while the middle (wheel) mouse button is held down.

  - `NotTyping`: true when there is no chat input box. Does not work while chatting.
  - Now `EUDArray`, `PVariable`, and `EUDVariable` can also be used in [MSQC]. Variables/arrays for use in [MSQC] must be registered in advance with `EUDRegisterObjectToNamespace("a", a)`.
    * `EUDVariable`: can only be used in conditions.
    * `EUDArray`, `PVariable`: can only be used in return values.
  - #### [MSQC] eds/edd writing example
    ```
    [MSQC]
    NotTyping ; KeyDown(A) : EUDArray, 1
    ∴ When not chatting and the A key is pressed ▶ add 1 to EUDArray[player].
    ```
- Add `soundlooper` library
  - Usage is the same, but changed to use StringBuffer and EUDX actions instead of customText and `eudx.py`. See the [soundlooper 사용법] article.
- Re-add `[bgmplayer]` plugin
: It was removed because it has fewer features than my soundlooper or EUDEditor2's BGMPlayer so nobody seemed to use it, but it is re-added as there seems to be demand. Like soundlooper and EUDEditor2's BGMPlayer, the bgmplayer plugin also uses system time (0x51CE8C) so it is not affected by lag/speed changes. It plays a single background music track.
  - #### [bgmplayer] Usage
    ```
    [bgmplayer]
    path: res/bgm.ogg    # Sound file path
    length: 33.680           # Sound length
    ```
- `f_readgen_epd` and `f_readgen_cp(mask, *(initval, func))` check for duplicates using the function's bytecode.
    ```python
    # Example
    # a and b share the same mask and (initial value, function) pair, so they use the same function.
    a = f_readgen_epd(0xFF, (0, lambda x: x))
    b = f_readgen_epd(255, (0, lambda edac: edac))
    ```
- Add `EUDLoopNewUnit(allow=2)`
    ```python
    # Example
    for ptr, epd in EUDLoopNewUnit():
        ...
    ```
- Add Position-type read functions: read functions for BW::Position and BW::Target types have been added. (CUnit::nextMovementWaypoint, nextTargetWaypoint, position, rally, moveTarget, orderTarget, etc.) They read map coordinates and return x, y. The maximum value depends on the map size.
  * `f_posread_epd(epd)`, `f_posread_cp(cpoffset)`

- Add location functions
  * `f_setloc(location, x, y)`: set the left/right coordinates of the location to x and the top/bottom coordinates to y.
  * `f_addloc(location, x, y)`: (translation) add x to the left/right coordinates and y to the top/bottom coordinates of the location.
  * `f_dilateloc(location, x, y)`: (expansion) subtract x, y from the left/top coordinates and add x, y to the right/bottom coordinates.
    - Example) Applying `f_dilateloc(location, 10, 6);` to a dot location makes the location size **20x12**. Applying `f_dilateloc(location, -10, -6);` again makes it **0x0**.
  * `f_getlocTL(location)`: get the left and top coordinates of the location.
  * `f_setloc_epd(location, epd)`: set the location's coordinates to the Position at epd. Same as the code below.
    ```javascript
    x, y = posread_epd(epd);
    setloc(locIndex, x, y);
    ```


## [0.8.4.8] - 2019.03.29

### Added

- Add StringBuffer`.print(*args)`: a shortcut combining the 3 calls below.

```javascript
StringBuffer.insert(0);
StringBuffer.append(*args);
StringBuffer.Display();
```
- Optimize ptrmemio
    * `f_dwread`, `f_dwwrite`: use epd when ptr is constant and a multiple of 4.
    * `f_wread`, `f_wwrite`: use epd when ptr is constant and ptr mod 4 is not 3.
    * `f_bread`, `f_bwrite`: use epd when ptr is constant.
- Add `[MurakamiShiinaQC]` and `[cammove]` to the default plugins.
- Reduce trigger count for StringBuffer initialization triggers.

### Removed

- Remove _f_initextstr


## [0.8.4.7] - 2019.03.26

### Bugfix

- Fix compile error with `Disabled(condition/action)`.
- Fix StringBuffer address going off 4-byte alignment when strings are added after declaring StringBuffer.
  - The string space saving feature added in [0.8.4.5] missed this case...


## [0.8.4.6] - 2019.03.24

### Bugfix

- (Contributed by 트리거왕) Fix `f_wwrite_epd(epd, subp, word)` bug:
    - Fix it behaving like f_bwrite_epd when subp is constant. This was added on Dec 27 but only found now.

### Added

- Apply Cython to improve compile times.
- (Contributed by 트리거왕) Add password encryption/decryption based triggers.


## [0.8.4.5] - 2019.03.24

### Bugfix

- Fix `TextFX_Remove` bug.
- Fix same-sized StringBuffers pointing to the same string.
- Fix StringBuffer not being declarable globally.

### Added

- Add SCMDraft2 default unit names.
  * See [1e6fae3] for the added names.
- Save StringBuffer triggers: make the CurrentPlayer check trigger a classmethod.
- Save string space:
  * New strings now fill empty slots first.
  * Remove `This map requires EUD Enabler to run` message.


## [0.8.4.4] - 2019.03.10

### Added

- Add function `GetTBLAddr(TBLId)`: get the address of the stat_txt.tbl text with the given number.
- Add many `QueueGameCommand` related functions:
    * `QueueGameCommand_MinimapPing(xy)`: the user pings the minimap at xy coordinates.
    *` QueueGameCommand_QueuedRightClick(xy)`: selected units Shift + right-click to the coordinates.
    * `QueueGameCommand_PauseGame()`: pause the game.
    * `QueueGameCommand_ResumeGame()`: resume the game.
    * `QueueGameCommand_RestartGame()`: restart the game. (single player only)
    * `QueueGameCommand_LeaveGame()`
    * `QueueGameCommand_UseCheat(flags)`
    * `QueueGameCommand_TrainUnit(unit)`: order selected units to train a unit.
    * `QueueGameCommand_MergeArchon()`: order selected units to merge into an Archon.
    * `QueueGameCommand_MergeDarkArchon()`
- Add function `f_getgametick()`:
    Read the value at offset 0x57F23C and cache it like f_getcurpl(). Use it instead of f_dwread_epd(0x57F23C).
- Add function `f_gettextptr()`: read the value at offset 0x640B58.
- Add function `f_eprintln2(*args)`:
    Overwrite the contents of stat_txt.tbl[831]: "Unit's waypoint is full.". Use when you want to print more than 218 bytes to the error message line. Use together with `QueueGameCommand_QueuedRightClick(xy)`.
- Add `StringBuffer.DisplayAt(line)` method:
    If line is 0, print to the topmost line; if line is 10, print to the bottommost line.
- Add text effects:
    * `StringBuffer.fadeIn(*args, color=(3, 4, 5, 0x14), reset=True, wait=1, tag="?")`
    * `StringBuffer.fadeOut(*args, color=(3, 4, 5, 0x14), reset=True, wait=1, tag="?")`
    * `TextFX_SetTimer(tag, modtype, value)`
    * `TextFX_Remove(tag)`
    * `TextFX_FadeIn(*args, color=(3, 4, 5, 0x14), reset=True, wait=1, tag="?")`
    * `TextFX_FadeOut(*args, color=(3, 4, 5, 0x14), reset=True, wait=1, tag="?")`
    * `f_cpchar_print(*args)`:
        Print one DWORD per character (color code + character) at the CurrentPlayer location. With EOS.
```javascript
// Example code
function afterTriggerExec() {
    const xy = dwrand() & 0x1FFF1FFF;
    QueueGameCommand_MinimapPing(xy);

    setcurpl(getuserplayerid());
    const buffer = StringBuffer(1000);
    const lastLine = TextFX_Remove("FAH");
    buffer.insert(0);
    if(buffer.fadeIn(
        "\x13\x1F\x02Fade \x19In:\t\x07Star\x04Craft \x02ED\x1Fitor \x1BAC\x08ademy",
        tag=py_str("FAH")) == 0
    ) {
        buffer.insert(2);
        if(buffer.fadeOut(
            "\x13\x1F\x02Fade \x19Out:\t\x07Star\x04Craft \x02ED\x1Fitor \x1BAC\x08ademy",
            tag=py_str("AceRPG")) == 0
        ) {
            TextFX_Remove("FAH");
            TextFX_SetTimer("FAH", SetTo, 0);
        }
    }
    if(lastLine <= 10) {
        const txtPtr = gettextptr();
        SetMemory(0x640B58, SetTo, lastLine);
        buffer.Display();
        SetMemory(0x640B58, SetTo, txtPtr);
    } else {
        buffer.DisplayAt(6);
    }
}
```


## [0.8.4.3] - 2019.03.06

### Removed

- Remove the need for OptimizeSetPName.


## [0.8.4.2] - 2019.03.06

### Bugfix

- Fix various errors including unsupported EUD errors.


## [0.8.4.1] - 2019.03.06

### Bugfix

- Fix `SetKills` action behaving abnormally.

Note) `SetKills(player, Modifier, number, unit)`
- `player`: Player1~12 and CurrentPlayer are supported. AllPlayers, Force1~4, etc. are not implemented.
- `unit`: *Only when the player is CurrentPlayer*, `"(men)"`, `"(any unit)"`, etc. can also be used.

### Added

- Now units placed on the map with 100% HP are placed with normal HP even if their max HP is higher.
- Add player nickname change and title features:
  - Function `SetPName(player, *name)`
    : Change the player's nickname to "name".
    `PName`, `PColor`, `ptr2s`, `epd2s`, `hptr`, etc. can be used as arguments.
```javascript
// Player title example
function afterTriggerExec() {
    const title = PVariable();

    OptimizeSetPName();

    EUDPlayerLoop()();
    const cp = getcurpl();
    const my_title = title[cp];
    switch(my_title) {
        case 0:
            SetPName(cp, "\x16Took down a bear in one room ", PColor(cp), PName(cp));
            break;
        case 1:
            SetPName(cp, "\x16Project Ceres member ", PColor(cp), PName(cp));
            break;
        case 2:
            SetPName(cp, "\x16Beta tester ", PColor(cp), PName(cp));
            break;
    }
    EUDEndPlayerLoop();
}
```


## [0.8.4.0] - 2019.03.04

### Bugfix

- Fix auto-update failing due to git-lfs.


## [0.8.3.8] - 2019.03.04

### Added

- Optimize function `GetMapStringAddr`.
- Add `StringBuffer`.
- Add function `f_eprintln(*args)`. (same role as ct.f_chatAnnouncement)
- Add function `f_raise_CCMU(player)`. Show the player the `Cannot create more unit.` error message.
- Add function `f_cpstr_print(*args)`.
Write text at the current CurrentPlayer position.
Similar to f_dbstr_print, but it takes no address, uses CurrentPlayer, and does not add EOS.
To mark the end of the string, add `DoActions(SetDeaths(CurrentPlayer, SetTo, 0, 0))`.
Unlike f_dbstr_print, which later needs f_bwrite(dst, 0) to add null, this intentionally omits it so you can flexibly use a single SetDeaths.
```javascript
function afterTriggerExec() {
    f_setcurpl(P1);
    // StringBuffer example

    // Create with StringBuffer(capacity) or StringBuffer("initial content").
    const s = StringBuffer(1023);

    // StringBuffer.insert(EPD index, contents, ...)
    // Since it does not insert a null character marking the end of the string,
    // it can be used to replace only the middle of the string.
    s.insert(0, "sound\\Zerg\\Devourer\\");

    // StringBuffer.append(contents, ...)
    // Append contents at the last position and add EOS.
    s.append("ZDvPss00.WAV");

    // StringBufer.Display()
    // Print the string buffer to the screen.
    s.Display();

    // StringBufer.Play()
    // Play a sound using the string buffer contents as the path.
    s.Play();

    const my_name = PName(getuserplayerid());
    const my_color = PColor(getuserplayerid());
    s.insert(0);
    s.append(my_color, my_name, "\x16, hello ^^;");
    s.Display();

    // eprintln prints to the error line.
    eprintln(my_color, my_name, "\x16hello");
}
```

#### Tips for writing contents with StringBuffer's `insert` and `append` methods and the `f_dbstr_print` and `f_cpstr_print` functions.
- `PColor(number)`: return the default color code of the given player number. (same as ct.color)
- `PName(number)`: get the player name. (same as ct.str(0x57EEEB + 36 * player))
- `ptr2s(address)`: load and append the string at the given address. (same as ct.str)
- `epd2s(epd)`: load and append the string at the given epd. (same as ct.strepd)
- `hptr(value)`: print the value in hexadecimal.
- `GetMapStringAddr(stringNumber)`: get the address of the string with the given number. (same as ct.strptr)
- `f_dbstr_print` also supports `PName` and `ptr2s`.

#### StringBuffer member variables
- StringBuffer`.StringIndex`: the buffer string's string number
- StringBuffer`.epd`: the epd of the buffer string's start address (read-only, do not modify.)
- StringBuffer`.pos`: the last written position (epd)
- StringBuffer`.capacity`: the maximum available capacity
* Other StringBuffer methods
  - StringBuffer`.delete(startEpdIndex, lengthEpd)`: fill from the index for the length with \r.
  - StringBuffer`.length()`: return the current buffer string length. Same as `f_strlen_epd(StringBuffer.epd)`.


## [0.8.3.7] 2019.03.03

### Added

- Add `PVariable`.
```javascript
// Example
// import customText as ct;

const a = PVariable();
const b = PVariable();
const c = PVariable();

function onPluginStart() {
    for(var i = 0; i < 4; i++) {
        a[i] = i;
        b[i] = i * i;
        c[i] = i * i * i;
        ct.printAll(i, ": a=", a[i], ", b=", b[i], ", c=", c[i]);
    }
    foreach(j: py_range(4, 8)) {
        a[j] = j;
        b[j] = j * j;
        c[j] = j * j * j;
        ct.printAll(j, ": a=", a[j], ", b=", b[j], ", c=", c[j]);
    }
}
```


## [0.8.3.6] - 2019.02.15

### Bugfix

- Fix `EUDLoopUnit2` error.


## [0.8.3.5] - 2019.02.02

### Bugfix

- Fix zlib error.

### Added

- Add `switch` statement to epScript. (Contributed by 디펜더)
```javascript
switch(expression) {
  case x:
    // code
    break;
  case y:
    // code
    break;
  default:
    // code
}

// Example

switch (day) {
  case 1:
    DisplayText("I like Mondays");
    break;
  case 4:
  case 5:
    DisplayText("The weekend is almost here");
    break;
  case 0, 6:
    DisplayText("It's the weekend!");
    break;
  default:
    DisplayText("Waiting for the weekend");
}
```


## [0.8.3.4] - 2019.01.18

### Bugfix

- (Reported by 사로로) Fix `f_wread_cp` and `f_wwrite_cp` compile errors.

### Changed

- Change `EUDLoopUnit`'s continue condition to when 0x4D (current order) is [0]Die. (Unit loop now works normally on unlimiter-applied maps)

### Added

- (Contributed by 여섯살) Optimize when `EUDFuncPtr` statically points to `EUDFuncN`.
- Add `EUDLoopUnit2` and `EUDLoopPlayerUnit(player)`.
- Add `SetKills(player, modifier, number, unit)` action.
    - Raise `NotImplementedError` when both player and unit are `EUDVariable`, or when both are unusual values (like Force1's "(any unit)").


## [0.8.3.3] - 2019.01.07

### Added

- Backward compatibility: `f_dwepdread_epd_safe`, `f_dwread_epd_safe`, `f_epdread_epd_safe(epd)`.
  - `EUDByteStream.flushdword()` does nothing. (same as pass)
- Add `EUDXVariable(initialValue, bitmask)`.
    - Actions `SetMask`, `AddMask`, `SubtractMask(value)`, `SetMaskX`, `AddMaskX`, `SubtractMaskX(value, bitmask)`.
    - Conditions `MaskExactly`, `MaskAtLeast`, `MaskAtMost(value)`, `MaskExactlyX`, `MaskAtLeastX`, `MaskAtMostX(value, bitmask)`.


## [0.8.3.2] - 2019.01.01

### Bugfix

- (Reported by 디펜더) Fix bug where True and False could not be used as condition/action arguments.
- (Reported by 여섯살) Fix `f_strlen` return value bug.
- Fix `EUDVariable is not iterable` error in `f_readcp_gen`.

### Added

- Optimize bit operation functions: `f_bitand`, `f_bitor`, `f_bitxor`, `f_bitnand`, `f_bitnor`, `f_bitnxor`.
- Add functions `f_readepd_gen` and `f_readcp_gen(mask, *(initialValue, function pair))` and example functions `f_cunit(epd)read_epd/cp` and `f_maskread_epd/cp`.
  - The f_readepd/cp_gen functions create user-defined read functions.
  - Example 1) CUnit values (0x59CCA8 + 336 * index) use only 23 bits (0x7FFFF8), so a CUnit-specific read function f_cunitread_epd can be made as follows.
  - ```f_cunitread_epd = f_readgen_epd(0x7FFFF8, (0, lambda x: x))```
  - Example 2) For reading unit coordinates on a 256x256 map, where 8191 pixels is the max (0x1FFF), make it as follows.
  - ```f_posread_epd = f_readgen_epd(0x1FFF1FFF, (0, lambda x: x if x < 8192 else 0), (0, lambda y: y // 65536))```


## [0.8.3.1] - 2018.12.28

### Bugfix

- Fix Freeze being unusable (thanks to 트리거왕 for help) and replace `*_safe` functions used in Freeze.
- Fix epScript libgcc related errors.
- Add `DeathsX`, `MemoryX`, `MemoryXEPD`, `SetDeathsX`, `SetMemoryX`, and `SetMemoryXEPD` to epScript. (2018.12.31)

### Added

- Add conditions `AtLeastX`, `AtMostX`, and `ExactlyX(value, mask),` and actions `SetNumberX`, `AddNumberX`, and `SubtractNumberX(value, mask)` to `VariableBase` methods.
- Merge `EUDByteReader` and `EUDByteWriter` into `EUDByteStream`. Remove `flushdword` method. (Thanks to 여섯살 for the idea)
  - For backward compatibility, `EUDByteReader` and `EUDByteWriter` are aliased to `EUDByteStream`.
- Add string related functions: `f_memcmp(buf1, buf2, count)`, `f_strlen_epd(epd)`, `f_strlen(src)`, `f_strnstr(string, substring, count)`.
(2018.12.29)


## [0.8.3.0] - 2018.12.27

### Added

- Add EUDX support.
  - Add conditions `DeathsX`, `MemoryX`, and `MemoryXEPD`.
  - Add actions `SetDeathsX`, `SetMemoryX`, and `SetMemoryXEPD`.
  - Add `eudx` keyword argument to `Action` and `Condition`.
  - Apply EUDX to memio functions: `f_bwrite_epd`, `f_wwrite_epd`, `EUDByteReader`, `EUDByteWriter`, `f_dwepdread_cp`, `f_dwread_cp`, `f_epdread_cp`, `f_dwepdread_epd`, `f_dwread_epd`, `f_epdread_epd`, `f_flagread_epd`, `f_wwrite`, `f_bwrite`, `f_dwread`, `f_wread`, `f_bread`.
- Add EUD functions `f_wread_cp(cpo, subp)`, `f_bread_cp(cpo, subp)`, `f_wwrite_cp(cpo, subp, w)`, and `f_bwrite_cp(cpo, subp, b)`.
- Add argument type `TrgLocationIndex` and function `EncodeLocationIndex`.
- Add action `AddCurrentPlayer` and EUD function `f_addcurpl`.

### Removed

- Remove safedwmemio: `f_dwepdread_epd_safe`, `f_dwread_epd_safe`, `f_epdread_epd_safe`.


## [0.8.2.9] - 2018.10.29

### Bugfix

- Fix `OSError: [WinError 126] The specified module could not be found.` error on Windows.

[TBL 문자열 목록]: https://cafe.naver.com/edac/82819
[SQC 사용법]: https://cafe.naver.com/edac/74735
[soundlooper 사용법]: http://kein0011.blog.me/221409128228
[1e6fae3]: https://github.com/armoha/eudplib/commit/1e6fae3ac884e980741199c22fbddb06414f7f03

[0.11.0.1]: https://github.com/armoha/euddraft/releases/tag/v0.11.0.1
[0.11.0.0]: https://github.com/armoha/euddraft/releases/tag/v0.11.0.0
[0.10.2.5]: https://github.com/armoha/euddraft/releases/tag/v0.10.2.5
[0.10.2.3]: https://github.com/armoha/euddraft/releases/tag/v0.10.2.3
[0.10.2.2]: https://github.com/armoha/euddraft/releases/tag/v0.10.2.2
[0.10.2.1]: https://github.com/armoha/euddraft/releases/tag/v0.10.2.1
[0.10.1.6]: https://github.com/armoha/euddraft/releases/tag/v0.10.1.6
[0.10.1.5]: https://github.com/armoha/euddraft/releases/tag/v0.10.1.5
[0.10.1.4]: https://github.com/armoha/euddraft/releases/tag/v0.10.1.4
[0.10.1.3]: https://github.com/armoha/euddraft/releases/tag/v0.10.1.3
[0.10.1.1]: https://github.com/armoha/euddraft/releases/tag/v0.10.1.1
[0.10.1.0]: https://github.com/armoha/euddraft/releases/tag/v0.10.1.0
[0.10.0.2]: https://github.com/armoha/euddraft/releases/tag/v0.10.0.2
[0.10.0.1]: https://github.com/armoha/euddraft/releases/tag/v0.10.0.1
[0.10.0.0]: https://github.com/armoha/euddraft/releases/tag/v0.10.0.0
[0.9.11.2]: https://github.com/armoha/euddraft/releases/tag/v0.9.11.2
[0.9.11.1]: https://github.com/armoha/euddraft/releases/tag/v0.9.11.1
[0.9.11.0]: https://github.com/armoha/euddraft/releases/tag/v0.9.11.0
[0.9.10.12]: https://github.com/armoha/euddraft/releases/tag/v0.9.10.12
[0.9.10.11]: https://github.com/armoha/euddraft/releases/tag/v0.9.10.11
[0.9.10.10]: https://github.com/armoha/euddraft/releases/tag/v0.9.10.10
[0.9.10.9]: https://github.com/armoha/euddraft/releases/tag/v0.9.10.9
[0.9.10.7]: https://github.com/armoha/euddraft/releases/tag/v0.9.10.7
[0.9.10.6]: https://github.com/armoha/euddraft/releases/tag/v0.9.10.6
[0.9.10.5]: https://github.com/armoha/euddraft/releases/tag/v0.9.10.5
[0.9.10.4]: https://github.com/armoha/euddraft/releases/tag/v0.9.10.4
[0.9.10.3]: https://github.com/armoha/euddraft/releases/tag/v0.9.10.3
[0.9.10.2]: https://github.com/armoha/euddraft/releases/tag/v0.9.10.2
[0.9.9.9]: https://github.com/armoha/euddraft/releases/tag/v0.9.9.9
[0.9.9.7]: https://github.com/armoha/euddraft/releases/tag/v0.9.9.7
[0.9.9.5]: https://github.com/armoha/euddraft/releases/tag/v0.9.9.5
[0.9.9.4]: https://github.com/armoha/euddraft/releases/tag/v0.9.9.4
[0.9.9.3]: https://github.com/armoha/euddraft/releases/tag/v0.9.9.3
[0.9.9.2]: https://github.com/armoha/euddraft/releases/tag/v0.9.9.2
[0.9.9.1]: https://github.com/armoha/euddraft/releases/tag/v0.9.9.1
[0.9.9.0]: https://github.com/armoha/euddraft/releases/tag/v0.9.9.0
[0.9.8.13]: https://github.com/armoha/euddraft/releases/tag/v0.9.8.13
[0.9.8.12]: https://github.com/armoha/euddraft/releases/tag/v0.9.8.12
[0.9.8.11]: https://github.com/armoha/euddraft/releases/tag/v0.9.8.11
[0.9.8.10]: https://github.com/armoha/euddraft/releases/tag/v0.9.8.10
[0.9.8.9]: https://github.com/armoha/euddraft/releases/tag/v0.9.8.9
[0.9.8.7]: https://github.com/armoha/euddraft/releases/tag/v0.9.8.7
[0.9.8.6]: https://github.com/armoha/euddraft/releases/tag/v0.9.8.6
[0.9.8.5]: https://github.com/armoha/euddraft/releases/tag/v0.9.8.5
[0.9.8.4]: https://github.com/armoha/euddraft/releases/tag/v0.9.8.4
[0.9.8.3]: https://github.com/armoha/euddraft/releases/tag/v0.9.8.3
[0.9.8.2]: https://github.com/armoha/euddraft/releases/tag/v0.9.8.2
[0.9.8.1]: https://github.com/armoha/euddraft/releases/tag/v0.9.8.1
[0.9.7.10]: https://github.com/armoha/euddraft/releases/tag/v0.9.7.10
[0.9.7.9]: https://github.com/armoha/euddraft/releases/tag/v0.9.7.9
[0.9.7.3]: https://github.com/armoha/euddraft/releases/tag/v0.9.7.3
[0.9.6.1]: https://github.com/armoha/euddraft/releases/tag/v0.9.6.1
[0.9.6.0]: https://github.com/armoha/euddraft/releases/tag/v0.9.6.0
[0.9.5.9]: https://github.com/armoha/euddraft/releases/tag/v0.9.5.9
[0.9.5.8]: https://github.com/armoha/euddraft/releases/tag/v0.9.5.8
[0.9.5.4]: https://github.com/armoha/euddraft/releases/tag/v0.9.5.4
[0.9.5.3]: https://github.com/armoha/euddraft/releases/tag/v0.9.5.3
[0.9.5.2]: https://github.com/armoha/euddraft/releases/tag/v0.9.5.2
[0.9.5.1]: https://github.com/armoha/euddraft/releases/tag/v0.9.5.1
[0.9.5.0]: https://github.com/armoha/euddraft/releases/tag/v0.9.5.0
[0.9.4.8]: https://github.com/armoha/euddraft/releases/tag/v0.9.4.8
[0.9.4.7]: https://github.com/armoha/euddraft/releases/tag/v0.9.4.7
[0.9.4.6]: https://github.com/armoha/euddraft/releases/tag/v0.9.4.6
[0.9.4.5]: https://github.com/armoha/euddraft/releases/tag/v0.9.4.5
[0.9.4.4]: https://github.com/armoha/euddraft/releases/tag/v0.9.4.4
[0.9.4.3]: https://github.com/armoha/euddraft/releases/tag/v0.9.4.3
[0.9.4.2]: https://github.com/armoha/euddraft/releases/tag/v0.9.4.2
[0.9.4.1]: https://github.com/armoha/euddraft/releases/tag/v0.9.4.1
[0.9.4.0]: https://github.com/armoha/euddraft/releases/tag/v0.9.4.0
[0.9.3.8]: https://github.com/armoha/euddraft/releases/tag/v0.9.3.8
[0.9.3.6]: https://github.com/armoha/euddraft/releases/tag/v0.9.3.6
[0.9.3.4]: https://github.com/armoha/euddraft/releases/tag/v0.9.3.4
[0.9.3.3]: https://github.com/armoha/euddraft/releases/tag/v0.9.3.3
[0.9.2.0]: https://github.com/armoha/euddraft/releases/tag/v0.9.2.0
[0.9.1.5]: https://github.com/armoha/euddraft/releases/tag/v0.9.1.5
[0.9.1.4]: https://github.com/armoha/euddraft/releases/tag/v0.9.1.4
[0.9.1.3]: https://github.com/armoha/euddraft/releases/download/v0.9.1.3/euddraft0.9.1.3.zip
[0.9.0.9]: https://github.com/armoha/euddraft/releases/tag/v0.9.0.9
[0.9.0.8]: https://github.com/armoha/euddraft/releases/tag/v0.9.0.8
[0.9.0.5]: https://github.com/armoha/euddraft/releases/download/v0.9.0.5/euddraft0.9.0.5.zip
[0.9.0.4]: https://github.com/armoha/euddraft/releases/tag/v0.9.0.4
[0.9.0.3]: https://github.com/armoha/euddraft/releases/tag/v0.9.0.3
[0.8.9.9]: https://github.com/armoha/euddraft/releases/tag/v0.8.9.9
[0.8.9.8]: https://github.com/armoha/euddraft/releases/tag/v0.8.9.8
[0.8.9.7]: https://github.com/armoha/euddraft/releases/tag/v0.8.9.7
[0.8.2.9]: https://github.com/phu54321/euddraft/raw/master/latest/euddraft0.8.2.9.zip

