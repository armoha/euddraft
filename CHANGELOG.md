# Changelog

## [0.9.8.3] - 2022.11.03
### Changed
- `EPDOffsetMap` rollbacked to accept a tuple of *(name, offset, type)* pairs
- Added and changed types `EPDOffsetMap` takes
  * Available type: bool, 1, 2, 4, "CUnit", "CSprite", "Position", "PositionX", "PositionY", `Flingy`, `TrgPlayer`, `TrgUnit`, `UnitOrder`, `Upgrade`, `Tech`

### Improved
- Updated eudplib 0.71.7, cx-freeze 6.13.1, pybind11
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
- Encode functions like `EncodeLocation` fixed to try both UTF-8과 CP949
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
      서울여자 : 20200721
      서울여자 : 13

      :: Duplicate key 서울여자 in [chatEvent]
      :: [Line 120] 서울여자 : 20200721
      :: [Line 121] 서울여자 : 13
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
- Updated`cx_Freeze`
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
- **[chatEvent]** 채팅 인식했을 때도 `ptrAddr` 설정하도록 수정. `lenAddr`과 `ptrAddr`도 0으로 초기화 추가
- 맵에 (0000.00) null 지형이 있으면 (0000.01) 타일로 대체하고 경고

## [0.9.0.1] - 2020.09.09
- `ctypes/create_string_buffer` 오류 수정

## [0.9.0.0] - 2020.08.08
- 컴파일 시간에 페이로드 초기화
  * `CreateVector/PayloadRelocator` 삭제 ( 참고: https://cafe.naver.com/edac/88753 )

- `Encode~/Get~Index` 함수 동일화. `TrgLocationIndex` 삭제
  * 두 함수 다 1부터 시작합니다. `0x58DC60` 쓴 코드들 - 20 하세요. (참고: https://cafe.naver.com/edac/83158 )
  * 이제 로케이션에 언제는 1 더하고 이런거 신경 쓸 필요 없어요.
  ```js
  $L("Anywhere")  // = 64
  ```
- `SaveMap`에 키워드 전용 인자 `sectorSize` 추가
  * 값: 3~15. 일반 에디터는 3 쓰고 워크 옵티마이저는 7 씁니다.
  * 테스트 목적으로 `euddraft`에서 **15** 씁니다.
  * MPQ 압축 기본단위로 생각하면 됩니다. 높을수록 맵 용량이 줄어듭니다.
  * `sectorSize`를 설정하는 경우 (listfile)에 있는 파일만 output 맵으로 옮겨옵니다.
    ```cs
    [main] 아래에
    sectorSize: 3  # 이런식으로 작성하면 됩니다.
    ```
    - **freeze**나 **SCDB** 사용 맵에선 설정이 무시됩니다.

### 버그 수정
- 인라이닝한 트리거에 `Disable` 체크된 `PreserveTrigger` 액션 있어도 반복시키는 버그 수정
- input맵이 `STRx` 단락 사용할 때 **[MSQC]** 오류 수정

### 기타
- MPQ 압축 알고리즘 변경
- TBL 시작 주소 4의 배수로 설정
- `eudplib` 내부 에러 메세지에 있는 파일 경로 가독성 올림
- `StormLib` 업데이트
- `"Switch 256"` 빠진거 수정
- `f_settblf2` 오타 수정
- EUD Editor 2에서 tempcustomText rwcommon 오류 수정
- `MPQCheckFile(파일명)` 추가: 해당하는 파일 이름이 이미 MPQ에 있는지 체크하는 함수
- `StringBuffer.print("크기 32 이상인 텍스트")`를 `DisplayText`로 변환
- `OpenSSL`, `mpaq` 기능 제거, freeze 업데이트
- `UNIT`, `UNIx`, `UPGx`, `TECx`에서 안 쓰이는 값/플래그 삭제
- SCDB랑 freeze 같이 사용하면 컴파일 오류나게 수정 (08.03)

## [0.8.9.9] - 2019.12.09
**eudplib 0.61** 업데이트

### 버그 수정

- **StringBuffer** 문자열 주소가 4의 배수가 아닌 버그 수정
- `DisplayTextAt` 컴파일 안 되는 버그 수정

### 기능 추가

- **eudplib** 메시지 한글화(다국어 지원)

    - 기본으로 시스템 로케일을 불러옵니다. 환경변수 `LANG`으로 설정할 수 있습니다.
    - 윈도우 `cmd`에서는 `setx LANG en`으로 영어로 설정합니다.
- eudplib 오류 메시지 한글화 + 모든 경고/오류가 stderr로 출력하게 수정
- 모든 문자열 주소를 4의 배수로 변경
- `EUDByteStream` 추가

  `.readbyte()`, `.writebyte(b)`를 모두 사용할 수 있고,\
  `.copyto(byterw)`로 현재 위치를 다른 `EUDByteReader`/`Writer`/`Stream`한테 전달할 수 있습니다.
- `ep_warn`, `EPWarning`, `ep_eprint` 추가
- `CPByteWriter`, `f_strnstr` 성능 최적화

### 기능 변경

- `_safe` 읽기 함수 지원 중단(deprecated) 경고

  **eudplib 0.63**에서 `f_dwepdread_epd_safe`, `f_dwread_epd_safe`, `f_epdread_epd_safe`를 삭제할 예정입니다.


## [0.8.9.8] - 2019.12.05

### 기능 변경

- `StringBuffer` 롤백

  `soundlooper`도 사운드 파일마다 스트링 넣는 방식에서 플레이어마다 스트링 쓰게 변경했어요.


## [0.8.9.7] - 2019.11.23

### 버그 수정

- `"Protoss Unused type   1"`이 어시밀레이터로 코딩된 버그 수정.
- `StringBuffer.fadeInf`, `.fadeOutf`가 텍스트 효과 종료 여부를 리턴하지 않는 문제 수정. (아스나님 제보 감사합니다.)

### 기능 추가

- Python 3.8, cx_Freeze 6.1로 업데이트.
- `*=`, `//=`, `%=`는 좌항에 직접 리턴하게 최적화.


## [0.8.9.6] - 2019.11.13

### 기능 추가

- 압축 안 되는 트리거는 인라이닝 안 하게 개선.

    트리거 크기 컷오프 결정하는데 아스나님이 도와주셨습니다.


## [0.8.9.5] - 2019.11.12

### 기능 추가

- TRIG 트리거 공유 기능 추가.

    `Wait`나 `Transmission` 액션이 없는 반복 트리거는 하나만 삽입되고 모든 트리거 플레이어가 공유합니다. 인라이닝율이 1일때만 시행합니다.\
    트리거 플레이어 2~8명 체크했어도 트리거 1개만 삽입되고 `nextptr`을 변경해서 연결합니다.

    - 트리거 4005개 맵 (TrigEditPlus 16만줄) 용량 감소 예시

        ```
        basemap: 2.17MB
        공유 X: 3.01MB (프리즈: 3.23MB)
        트리거 공유: 1.76MB (프리즈: 2.09MB)
        ```

### 버그 수정

- 여러명에게 `StringBuffer`로 11줄의 텍스트 출력할 때 내용 덮어쓰는 버그 수정.

### 동작 변경

- **기본 인라이닝율 1로 설정.**

    `PRT_SetInliningRate(1)`을 기본으로 적용합니다. 대부분의 경우 용량 감소 효과가 있을겁니다. **패치 이후로 트리거가 이상하게 작동되는 경우, `PRT_SetInliningRate(0)`로 끄면 해결되는 경우에는 제보해주세요!** `Wait` 액션 말고도 공유하면 안 되는 액션이 있을 수도 있어서요.

- TRIG 트리거의 `Always` 조건, `Comment`, `PreserveTrigger` 액션 제거.

    `PreserveTrigger` 액션 대신에 트리거의 `preserved` 플래그를 사용합니다.


## [0.8.9.4] - 2019.11.04

### 기능 추가

- [freeze], inline_eudplib 사용맵도 모든 트리거 인라이닝 기능 `PRT_SetInliningRate(1)` 사용 가능.

### 버그 수정

- `f_wwrite`에서 subp가 3일 때 앞 바이트만 작성되는 버그 수정.


## [0.8.9.3] - 2019.11.04

### 버그 수정

- [freeze] 핫픽스.
- 인라이닝된 트리거의 크기가 항상 2408 바이트인 버그 수정.

### 기능 추가

- 실험적 모든 트리거 인라이닝 기능 추가.

    `PRT_SetInliningRate(1)` 넣으면 활성화됩니다. 모든 트리거를 스트링으로 옮깁니다. 트리거 플레이어가 1명인 트리거의 비중이 높으면 용량 감소 효과가 있습니다.


## [0.8.9.2] - 2019.11.02

### 버그 수정

- **[freeze] 프로텍션 버그 수정**

    - [0.8.9.0]까지 input 맵에서 CP트릭 사용하면 해당 트리거가 일정 확률로 실행되지 않는 버그가 났습니다. [0.8.9.1]은 최적화, 난독화하다가 실수해서 CP트릭 안 썼어도 버그날 확률이 있었습니다.


## [0.8.9.1] - 2019.10.29

### 기능 추가

- `DoActions`가 가변 인자를 받습니다.

  리스트 없이 `DoActions(액션1, 액션2, 액션3, ...)` 으로 쓸 수 있어요.
- EUD 함수 리턴 최적화.
  - 함수 리턴 관련 액션을 모두 호출 트리거로 옮겼습니다. 이제 리턴값 있는 함수도 호출할때마다 트리거 1개만 씁니다. 실행되는 액션 개수도 줄었어요.
  - EUD함수 호출에 `ret=[변수 리스트]` 키워드 인자 추가.
    ```python
    v << f_bitxor(v, key)  # 리턴값이 임시변수에 저장되고 다시 v에 대입함.
    f_bitxor(v, key, ret=v)  # 리턴값을 v에 바로 대입함.
    ```
- `stat_txt.tbl` 문자열을 해당하는 번호로 바꿔주는 `EncodeTBL("문자열")` 함수 추가.
  - **epScript**에서는 `$B("문자열")`로 사용합니다.
  - 이제 `f_settbl`, `f_settbl2`, `GetTBLAddr`이 문자열도 인자로 받습니다.
  - [TBL 문자열 목록] 참고하세요.
- `VProc` 액션 개수 제한 없게 수정. 트리거 2개 이상인 경우 트리거의 리스트를 리턴합니다.
- `EUDXTypedFunc(bitmasks, argtypes, rettypes)`, EUDXVariable`.getMaskAddr()` 추가.
- `[freeze]` 취약점 보완. unFreeze 방지.
  - freeze 자동 언프로텍터가 나온 관계로 eudplib 코드 비공개합니다. pip도 내렸어요.

### 동작 변경

- **freeze 프로텍터가 기본 적용됩니다.** 끄려면 .eds, .edd에 아래 문구 추가하세요.
    ```
    [freeze]
    freeze: 0
    ```
- 비트 연산 최적화.
    - `AND, OR, NAND, NOR`는 이제 EUD함수가 아닙니다. 트리거 1개로 계산합니다.

### 버그 수정

- 함수의 반환 값 개수가 일정하지 않을 때 오류 메시지에 함수 이름이 안 나오는 버그 수정;
```EPError: Numbers of returned value should be constant. (From function caller)```
- 메소드 StringBuffer`.insertf(index, format_string, *args)` 인자 오류 수정.


## [0.8.9.0] - 2019.10.19

기능 추가 위주의 대형 업데이트입니다.

### 동작 변경

- `f_simpleprint`가 모든 플레이어에게 출력되게 수정.
- `EUDByteReader`/`Writer` 최적화. `EUDByteStream` 삭제.

    이제 EUDByteReader`.writebyte()`, EUDByteWriter`.readbyte()` 하면 `AttributeError`납니다. EUDByteStream은 아무도 안 쓰는 거 같아서 지웠는데 쓰는 분 있다고 하면 다시 만들게요.

### 기능 추가

- 함수 `f_parse(dst, radix=10)` 추가:
  * `dst`: 스트링 주소.
  * `radix`: 0 또는 2~36, (기본값: 10진법).

    스트링을 특정 진수(기본값: 10진법)로 변환한 정수값과, 자리수를 리턴합니다. 수로 변환할 수 없으면 `0, 0`을 리턴합니다. 음수도 지원되며, 선행 공백 문자를 무시합니다. `radix`가 0이면 `0b`나 `0B`로 시작하면 2진법, `0o`나 `0O`로 시작하면 8진법, `0x`나 `0X`로 시작하면 16진법으로 읽습니다.
  * 숫자로 인식하는 패턴 예시 (정규표현식)

    - 2진법: `\s*[+-]?(0[bB])?[01]+`
    - 10진법:` \s*[+-]?\d+`
    - 16진법: `\s*[+-]?(0[xX])?[\da-fA-F]+`
  * 예외 처리: 숫자 0을 파싱하면 `0, 1`을 리턴합니다. 숫자가 아니면 `0, 0`을 리턴합니다. 처음에 EUDGetErrno 같은거 만들까 하다가 자리수 리턴하는 방식이 더 나아보여서 제작 방향 바꿨어요.
  * 오버플로 방지: 절대값이 0x7FFFFFFF보다 크면 `±0x7FFFFFFF, 자리수`를 리턴합니다.

    10진법이 아닌 경우 자리수가 1 더 클 수 있습니다. (오버플로 직전에 0x7FFFFFFF ÷ radix의 몫 이하인데, 자리수는 0x7FFFFFFF랑 같은 경우 1 더 커집니다. 아닐때는 같습니다.)

- 포맷 출력 지원: 이제 스트링 조합할 때 `"",`이나 `epd2s` 등 쓰느라 가독성 떨어지는 일 없어요.
    ```javascript
    // 플레이어 칭호 예시
    SetPNamef(cp, "{:t} \x07레벨: \x04{} {:c}{:n}", title, level, cp, cp);
    // 옛날 방식
    SetPName(cp, epd2s(title), " \x07레벨: \x04", level, " ", PColor(cp), PName(cp));
    ```
    #### 지원하는 포맷타입
    - `c` : 해당하는 번호의 플레이어 색상 (=PColor)
    - `n` : 해당하는 번호의 플레이어 이름 (=PName)
    - `s` : 연결할 스트링 주소 (=ptr2s)
    - `t` : 연결할 스트링의 EPD주소 (=epd2s)
    - `x` 나 `X`: 값을 16진법으로 출력 (hptr)

    나중에 `{:02}` 넣으면 한 자리수도 앞에 0 넣어서 두자리로 출력하는 기능 추가될거에요. (소수.점, 시:분:초 출력 등에 쓰이는 용도)
  * 지원하는 함수 목록
    - 함수 `SetPNamef(player, format_string, *args)`, `f_eprintf(format_string, *args)`
    - 메소드 StringBuffer`.printf(format_string, *args)`, `printfAt(line, format_string, *args)`, `insertf`, `appendf(format_string, *args)`, `fadeInf`, `fadeOutf(format_string, *args, color=(tuple), wait=1, reset=True, line=-1, tag=hashable)`
    - 함수 `f_settblf`, `f_settblf2(tblID, offset, format_string, *args)`
    - 함수 `f_sprintf(dst, format_string, *args)`, `f_sprintf_cp(format_string, *args)`: f_dbstr_print, f_cpstr_print의 포맷 출력 버전.

- 조건 `IsUserCP()` 추가:

    CurrentPlayer가 유저와 일치하는지 비교하는 컨디션입니다. 비공유 조건입니다. RawTrigger에도 쓸 수 있습니다. 옛날 eudplib의 _f_initextstr처럼 게임 시작 때 값 주소에 `f_getuserplayerid()` 값을 작성하는 방식이에요.

### 기능 개선

- `f_dbstr_print` 인자 2개 이상일 때 성능 개선.
- `EUDExecuteOnce` 최적화.
- 초기화 트리거 500개 -> 427개로 감소.
- `EUDLightVariable` 기능 추가:
  - EUDVariable처럼 조건에 eudlv 넣으면 eudlv`.AtLeast(1)`로 바뀝니다. SeqCompute등의 dst로 쓸 수 있습니다.


## [0.8.8.1] - 2019.10.10

### 기능 추가

- 이제 `f_dbstr_print`도 `epd2s`를 지원합니다. (`PColor`, `ct.color` 관련 오류 수정)
- EPDOffsetMap`.getdwepd(name)` 추가.

  `f_dwepdread_epd(오프셋)`을 리턴합니다.
- `SeqCompute`, EUD함수 콜 최적화: https://cafe.naver.com/edac/82207
- 로케이션 함수(`f_setloc`, `f_addloc`, `f_dilateloc`)에서 로케이션이 상수, 좌표가 변수일 때 성능 최적화.


## [0.8.7.9] - 2019.10.02

### 버그 수정

- `EUDLoopUnit2`에서 `EUDContinue` 이후로 값 밀려나는 버그 수정.
- [chatEvent] `__Addr__`, `__lenAddr__`, `__ptrAddr__`, `__patternAddr__` 중에 중복 있으면 오류나게 수정.

### 동작 변경

- [MSQC] `val`, `xy` 문법에서 전달 없을 때 기본값 *-1* 로 변경.

  기존에는 0이 초기값인건지 0을 전달한건지 구분이 안 가는 문제가 있어서 바꿉니다.
- 항상 `STRx`를 스트링 단락으로 사용. (크기 2GB, 개수 65535 개)
- `EUDLoopUnit2`가 [unlimiter] 사용할 때는 현재 명령이 [0]Die 일때, 미사용맵은 CSprite가 0일 때 건너뛰게 변경.

### 기능 추가

- `EPDCUnitMap` 추가: https://cafe.naver.com/edac/82244
- [MSQC] `val` 문법 추가. `QCDebug` 사용 시 끄는 법 알려주는 텍스트 출력되게 추가.
    ```
    추가조건 ; val, src : dst
    ```
  - `src`: 전달할 비공유 주소나 `EUDVariable`.
  - `dst`: 공유 유닛(데스값)이나 `EUDArray`, `PVariable`.
  - 전달 가능한 값 범위
    - 256x256맵 기준 0~16,777,215
    - 64x64맵 기준 0~1,048,575
  - 로케이션, 화면좌표같은 좌표값이 아닌 비공유 값 전달 할때는 `xy`대신 `val` 쓰세요.

- `soundlooper`: 사운드 재생 됩니다. (아티아님 테스트 감사합니다.)

    - 사운드 개수 1000개까지 받게 변경(0~999)
    - 사운드 파일명 다양하게 받게 변경: 사운드1.ogg, 사운드02.ogg, 사운드003.ogg, 사운드4.ogg
- 함수 `GetGlobalStringBuffer()` 추가. DBString`.Display()`가 전역 스트링버퍼로 출력됩니다.
- EUD함수 `DisplayTextAt(line, TrgString)` 추가.
  - `line`: 0~10, 첫번째 줄 = 0, 11번째 줄 = 10.
  - 액션 아닙니다. 텍스트 조합이 필요 없을 때는 StringBuffer`.printAt` 대신 이거 쓰는 게 빨라요. 어차피 스트링 공간 많아서... 채팅이랑 `DisplayText` 동시에 볼 수 있는거 함수 하나로 쓸 수 있게 한거에요.
- `f_cp949_to_utf8_cpy(dst, src)` 최적화, `dst` 리턴하게 수정.


## [0.8.7.8] - 2019.09.25

### 변경사항

- (임시버전) `StringBuffer`가 채팅 출력을 사용합니다. (`SetPName`처럼 화면을 직접 수정합니다.)
    - StringBuffer`.Play()` (사운드 재생)은 작동 안 합니다. 다음 패치 나오는 동안 쓰세요.


## [0.8.7.7] - 2019.09.25

### 버그 수정

- [MSQC] 다른 언어 환경에서 콘솔 메시지로 인한 인코딩 오류 수정.

### 기능 추가

- `CRGB` (플레이어 색) 단락 지원 추가.
- `STRx` 단락 지원 추가.

    input맵이 리마스터 전용 맵이고, STRx 단락이 존재하면 사용합니다.
    아마 다음 SCMDraft2 배포판에서 STRx (스트링 개수 65536, 전체 크기 2GB) 기능 지원할거라 예상되서 대응했습니다.

#### 스트링 수정 관련 공지

이번 SC:R 1.23.1.6623 패치로 스트링 내용 수정이 막혀서 `StringBuffer`, `customText`, `soundlooper` 작동이 안 되고 있는데, eudplib/euddraft에서 해결하는 건 불가능하고 추가 패치를 기다려야 합니다. 먼저 DisplayText를 하고 출력된 텍스트를 수정하는 채팅 출력은 지금도 작동하니 급한 경우는 이 쪽을 써야할 거 같네요. (`eprintln`, `customText.chatprint` 등)


## [0.8.7.6] - 2019.09.21

### 동작 변경

- [0.8.7.5]에서 했던 `f_settbl` 변경 취소합니다. (기존 코드에서 함수 변경되서 문제 생긴거 해결)
- TBL 부분 수정하는 용도로 `f_settbl2(tblID, offset, *args)` 추가되었습니다. *\0*을 넣지 않습니다.

### 기능 개선

- 해쉬 테이블 크기가 추가 파일을 넣기 충분하면 크기를 변경하지 않게 수정.
- 해쉬 테이블 크기 늘리거나, 파일 삽입하다 실패하면 해당하는 윈도우 오류 나오게 수정.
- `f_dbstr_adddw` 성능 소폭 개선.
- 루프 성능 소폭 개선(`EUDLoopList`, `EUDLoopUnit`, `EUDLoopNewUnit`, `EUDLoopUnit2`, `EUDLoopPlayerUnit`, `EUDLoopSprite`)


## [0.8.7.5] 2019.09.20

PyPI에 eudplib 0.59.1 업데이트 됐습니다. `pip install eudplib -U` 로 업데이트 해주세요.

### 동작 변경

- `f_settbl(tblID, offset, *contents)`이 스트링 끝(\0)을 표기하지 않습니다. (갈대님 제보)

### 기능 추가

- 추가한 파일 개수에 맞게 해쉬 테이블 / 블럭 테이블 크기를 늘립니다. (아티아님 제안)

### 기능 개선

- freeze 최적화: 빈 맵 기준 오브젝트 약 500개 감소.


## [0.8.7.4] - 2019.09.12

### 버그 수정

- 인터넷 연결 없을 때 자동 업데이트 관련 오류 수정.
- edd 강제 리컴파일이 (R키) 계속 수행되는 오류 수정.


## [0.8.7.3] - 2019.09.02

### 버그 수정

- euddraft.exe에 맵파일을 드래그-드랍해서 freeze 프로텍션 적용하는데서 있었던 오류 수정
- `f_strnstr`에 `UnboundLocalError` 수정. (34464님 제보 감사합니다.)
- 로케이션 함수 오류 수정.
- `PColor` 오류 수정.
- `SetKills` 액션에 CurrentPlayer 사용했을 때 오류 수정.
- **[epScript]** `SetKills` 액션이 DoActions 추가 안 되는 버그 수정.

### 변경 사항

- `PColor(player)` 가 현재 플레이어 색을 인식해서 비슷한 텍스트 색으로 변환하게 변경.

  기존엔 기본 플레이어 색상 (빨강~노랑) 쓰는 맵에서만 쓸 수 있었는데, 아무 맵에서 쓸 수 있게 수정(혼돈과 무질서님이 조사한 정글 팔레트 256색 참고했어요). <05>는 안 씁니다.
- 스트링 출력 함수에서 `str`, `int`, `bytes` 인자 동작을 `CPString` -> `epd2s` 로 변경.

  customText가 랙 있다는 의견 때문에 CPString을 추가했는데, 랙은 EUD Editor 2 TriggerEditor 사용 미숙 및 Classic 트리거 사용이 주 원인에 가깝다고 봐서 `epd2s(EPD(Db(...)))` 로 바꿉니다. 성능은 32배 정도로 많이 들지만 맵 용량 측면에선 10배 정도 절약 되서 변경해보고 문제 있으면 돌려놓을 예정입니다.
- 스트링 출력 함수에 Db 인자 넣으면 `epd2s(EPD(...))` 로 출력.

### 기능 추가

- 메소드 StringBuffer`.printAt(line, *args)` 추가.
- 함수 `f_setloc`, `f_addloc`, `f_dilateloc`이 좌상우하 좌표 받을 수 있게 추가:
    - `f_setloc("loc", x, y)` : 로케이션 좌표가 (x, y, x, y)인 점 로케이션으로 설정.
    - `f_setloc("loc", left, top, right, bottom)` : 로케이션 좌표를 (left, top, right, bottom)으로 설정
    - `f_addloc("loc", x, y)` : 로케이션을 x, y로 평행 이동.
    - `f_addloc("loc", left, top, right, bottom)` : 로케이션 좌표에 (left, top, right, bottom)을 더함.
    - `f_dilateloc("loc", x, y)` : 로케이션 좌표를 좌우 좌표는 x만큼, 상하 좌표는 y만큼 넓힌다.
    - `f_dilateloc("loc", left, top, right, bottom)` : 로케이션 좌표에 (-left, -top, right, bottom)을 더함.
- MRGN PRT, ORT 트리거 겹침: 크기 4816 -> 3244 bytes로 감소.
- `_f_mul` (변수×변수 곱셈 함수) 성능 개선
  - 100×변수 기준 실행되는 SetDeaths 수 62 -> 41 개로 감소.
- 함수 `f_setloc`, `f_addloc`, `f_dilateloc`의 인자가 모두 상수면 트리거 1개만 사용하게 변경.

#### To. 맛빙

- [freeze] prompt 옵션 추가.
    ```
    [freeze]
    prompt: 1
    ```
    일반 scx를 생성하고, 일시정지 후에 아무 키를 누르면 MPQ 프로텍션을 적용합니다.


## [0.8.7.2] - 2019.06.11

### 버그 수정

- f_raise_CCMU가 캔낫 상황에서 실행되면 유닛 제한을 낮추는 버그 수정.

  기존에는 유닛 제한을 낮추는 경우가 *0x628438을 수정하고, 원래 값으로 돌려놓지 않았을 때*만 알려졌는데, *캔낫 상황에서 0x628438을 수정하면* 캔낫을 해소한 이후에 유닛 제한이 줄어드네요. 캔낫일때는 0x628438이 0인데도 SetMemory(0x628438, SetTo, 0)이 유닛 제한을 낮추네요. 캔낫 상황일 땐 절대로 0x628438을 액션으로 접근하면 안 되겠습니다.

### 변경 사항

- `pip install eudplib`으로 eudplib 설치할 때 C++ 빌드 툴 필요없게 변경. (eudplib 버전 0.59.0)
  - euddraft 0.8.4.8에서 패스워드 기반 basemap 언프로텍션이 추가됐었습니다. 아직 eudplib에서만 쓸 수 있고 euddraft에서는 오류나서 기능을 막아두었는데, 새로 생긴 bsdiff4 의존성 때문에 eudplib 설치에 C++ 빌드 툴을 요구하게 되었습니다. 대부분의 사용자들이 euddraft를 사용하고, eudplib은 텍스트 에디터 자동완성만을 위해 설치하는 관계로 배포판에서 별도 브랜치로 옮겼습니다.


## [0.8.7.1] - 2019.06.08

### 버그 수정

- [MSQC] xy 문법에서 src가 주소일 때 오류나는 버그 수정.

### 기능 추가

- 플러그인 [chatEvent] 추가.

  기존 [채팅인식4]가 EUDX 나오기 전에 만든거라 작동이 잘 안되서 EUDX 써서 새로 만들었습니다. eds/edd 작성법은 [채팅인식4]랑 동일합니다.
  - [chatEvent] eds/edd 작성법
    ```
    [chatEvent]
    채팅인식할말: 2보다 크거나 같은 숫자
    @GG: 10
    └ 유저가 "@GG"라고 채팅치면, 주소 __addr__의 값이 10으로 설정됩니다.
    　주소 __addr__을 지정하지 않으면 0x58D900을 씁니다.
    　유저가 채팅을 했지만, 채팅내용이 eds/edd에 해당되지 않으면 주소 __addr__의 값이 1로 설정됩니다.
    ```

  - `^시작.*중간.*끝$: 숫자`
  - `^맛빙.*.*$: 1`

    유저가 "맛빙~"으로 시작하는 채팅을 치면, 주소 `__patternAddr__`의 값이 1로 설정됩니다.
  - `^.*.*팧$: 2`

    유저가 "~팧"으로 끝나는 채팅을 치면, 주소 `__patternAddr__`의 값이 2로 설정됩니다.
  - `^.*알타.*$: 3`

    유저가 "~알타~"를 포함하는 채팅을 치면, 주소 `__patternAddr__`의 값이 3으로 설정됩니다. 주소 `__ptrAddr__`을 지정하면, 주소 `__ptrAddr__`의 값이 채팅시작주소로 설정됩니다. 주소 `__lenAddr__`을 지정하면, 주소 `__lenAddr__`의 값이 채팅길이(바이트 수)로 설정됩니다.

  - 다음 버전에 EUD변수도 `__addr__`, `__ptrAddr__`, `__patternAddr__`, `__lenAddr__`로 쓸 수 있게 추가할 예정입니다.


## [0.8.7.0] - 2019.06.06

### 버그 수정

- [MSQC] `QCUnit`, `QCLoc`, `QCPlayer`가 기본값에서 변경되지 않는 버그 수정
- `EUDFunc`, `EUDMethod`가 inspect.getargspec 대신 `inspect.getfullargspec` 를 사용하게 수정

### 기능 추가
- `f_setcurpl2cpcache()` 추가.  ** 고급 **

  CurrentPlayer(오프셋 0x6509B0의 값)을 eudplib의 CurrentPlayer 캐시값으로 설정합니다. CP 트릭 사용 후 원래 CurrentPlayer로 복구할 때 씁니다. 사용 시 주의할 점은 0x6509B0 변경하고, 다시 `f_setcurpl2cpcache`로 돌려놓는 사이에 다른 CP 트릭 함수가 실행되면 CP 캐시 미스로 성능 저하가 일어납니다. (내부적으로 CP 트릭을 사용하는 함수: ptr, epd 읽기/쓰기 함수; `dwread_epd`, `wread`, `bwrite` 등등, `EUDByteStream`, `f_readgen_epd`, `f_strlen_epd`, `f_strlen`) CP 트릭 사용 중간에 다른 함수를 불러올 일이 없는, 단순한 함수에서만 쓸 수 있고, f_cpstr_print처럼 CP 트릭 중간에 다른 함수들이 사용되는 상황에선 쓰면 성능 손해가 큽니다.

  사용 례: https://github.com/armoha/eudplib/commit/18fd56c0775373d4da7041974c763975142f2c63

### 기능 개선

- `f_repmovsd_epd` 간단하고 빠르게 교체
- `VProc`에 `FlattenList` 적용
- 공용 `EUDByteStream` 개수 절약


## [0.8.6.9] - 2019.05.24

eudplib도 0.58.9로 버전업했습니다.

### 버그 수정

- 맵에 에너지 100%로 배치된 유닛이 게임에서 기본 마나(50)인 버그 수정.
(나도모름님 제보 감사합니다)

### 기능 추가

- `EUDVariable`에 새 메소드 추가. ** 고급 **
    * EUDVariable`.getDestAddr()`
      - EUD변수의 SetDeaths 액션에서 EPD주소의 주소입니다.
      - 값의 주소인 EUDVariable.getValueAddr()과 비슷한 용도입니다.
    * EUDVariable`.SetDest(epd)`
    * EUDVariable`.AddDest(epd)`
    * EUDVariable`.SubtractDest(epd)`: EUDVariable`.QueueAssignTo(epd)`처럼 `VProc`에서 쓰는 액션입니다.

        한 변수의 값을 여러 주소로 복사할 때, `QueueAssignTo`를 매번 쓰면 변수를 매번 SetTo로 설정하니까, 첫번째 복사에만 `QueueAssignTo`를 쓰고 이후에는 주소만 바꿔서 액션 1개씩 아끼는 용도로 씁니다.
* `f_setcurpl(player)`에서 `player`가 변수일 때 성능 최적화.
  - 실행되는 액션 수: 15개 → 10개
* CP 트릭 사용하는 함수 최적화. (실행되는 액션 최소 22개 감소)
  - ptr, epd 읽기/쓰기 함수, `EUDByteStream`, `f_readgen_epd`, `f_strlen_epd`, `f_strlen`.
* `f_dwrand`, `f_rand`에서 불필요한 값 복사 제거
* 그 외 eudplib/trigger/filler.py 등 최적화.
- 중복되는 dll 파일 정리, lib 폴더로 이동.


## [0.8.6.8] - 2019.05.06

### 변경사항

- 로케이션, 스위치 이름 스트링을 outmap 맵에서 삭제합니다.
- 로케이션이 사용하는 스트링 번호 정보를 output 맵에서 삭제합니다.
  - 스트링 용량 절약 + 언팧플맵 수정을 조금이나마 귀찮게 하는 목적입니다. 유닛 이름, 맵 제목, 맵 설명, 포스 이름으로 쓰인 경우에는 삭제하지 않습니다.
  - 로케이션/스위치와 사운드/주석/DisplayText 등이 같은 스트링을 공유하는 경우 삭제되니 주의하세요.


## [0.8.6.7] - 2019.05.06

### 버그 수정

- 모든 스트링이 `utf-8`로 인코딩되는 버그 수정


## [0.8.6.6] - 2019.05.06

### 버그 수정

- 텍스트 효과가 기본색으로 나오는 버그 수정. (아티아님 제보 감사합니다)

### 기능 추가

- `f_randomize` 성능 개선 및 `EUDFunc`으로 변경.
- `VProc`은 이제 첫번째 인자로 EUDVariable의 iterable도 받습니다.
  - VProc -> 변수1 -> 변수2 -> 변수3 -> ... -> 다음 트리거 순으로 nextptr을 설정합니다.

### 변경사항

- 이제 output 맵은 스타크래프트: 리마스터 버전 scx로 저장됩니다. (1.16에서 플레이 불가)
- 이제 `u2b`는 cp949로 인코딩되지 않는 텍스트를 utf-8로 인코딩합니다.
  - 중국어 간체자같이 cp949로 인코딩할 수 없는 문자가 있으면 utf-8 인코딩을 사용하여, DisplayText에서 오류나는 문제를 수정했습니다. 중국의 EUD Editor 사용자를 위해 변경된 사항입니다.
- 유닛 이름으로 쓰이는 스트링은 이제 utf-8로 인코딩됩니다.
  - 유닛 이름을 스트링 조합에 넣기 쉬워졌습니다. 대신에 유닛 이름을 stat_txt.tbl 조합에 사용하려면 cp949로 다시 변환해야합니다.
- **[epScript]** 이제 액션 뒤에 세미콜론이 올 때만 트리거로 바뀝니다.
  - 이제 eps에서 DoActions, RawTrigger, Trigger를 py_eval 없이 쓸 수 있습니다.


## [0.8.6.5] - 2019.04.17

### 기능 추가

- **[epScript]** `list(...)`, `VArray(...)` 문법 추가.
  - `VArray(초기값들)` : 해당 초기값으로 `EUDVArray`를 생성합니다.
  - `list(원소들)` : 파이썬 리스트를 만듭니다.
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
#### 참고 : epScript에서 배열 초기화
```javascript
// 인게임 초기화: 해당 코드에서 매번 초기화합니다(전역 스코프면 게임 시작 때).
// 함수 리턴값처럼 게임 안에서 정해지는 값도 넣을 수 있습니다.
const a = [getuserplayerid(), 0, 0];
const b = VArray(GetTBLAddr(1), GetTBLAddr(2), GetTBLAddr(3));

// 컴파일시간 초기화: 맵에 삽입될 때 초기화합니다. 상수 표현식만 넣을 수 있습니다.
const a = EUDArray(list(1, 2, 3, 4));
const b = EUDVArray(4)(list(EPD(a), EPD(a)+1, EPD(a)+2, EPD(a)+3));
```


## [0.8.6.4] - 2019.04.15

### 버그 수정

- `PVariable[i]` 상수 인덱스로 읽을 때 생기는 버그 수정. (아스나님 제보 감사합니다.)


## [0.8.6.3] - 2019.04.15

### 변경사항

- `EUDVArray` 성능 개선
    * `EUDVArray[EUDVariable]`로 읽을 때 성능 3배 이상 개선.
    * 읽기/쓰기에서 `EUDVArray`와 인덱스가 상수일 때 트리거 1개 사용.
- 인덱스가 `EUDVArray`의 길이를 넘겼을 때 동작 변경

    * 인덱스가 EUD변수일때는 상위 비트를 무시합니다.
    예시) `EUDVArray`의 크기가 5,6,7,8이면, 인덱스에서 비트 4, 2, 1만 읽습니다.

        ```javascript
        const a = EUDVArray(8)();
        var i8, i9 = 8, 9;
        a[i8];  // a[0]
        a[i9];  // a[1]
        ```

    * 배열 크기를 넘기는 건 정의되지 않은 동작(undefined behavior)으로, 언제든 변경될 수 있습니다! 쓰지마세요!

    * 상수일때는 `ep_assert "EUDVArray index out of bounds"`로 컴파일 때 잡습니다.

- 이제 PVariable도 타입캐스팅 가능합니다.


## [0.8.6.2] - 2019.04.10

### 버그 수정

- 1로 나눌 때 컴파일 오류 수정. (아스나님 제보 감사합니다)


## [0.8.6.1] - 2019.04.08

### 버그 수정

- `f_wwrite_epd(epd, subp, w)`, `f_wwrite(ptr, w)`에서 주소가 상수이고 w가 EUD변수일 때, 0으로 작성하는 버그 수정. (Photon님 제보 감사합니다.)
    - EUD Editor 2 TriggerEditor에서 무기 공격력같은 2byte 데이터를 수정할 때 (Set/Add 둘 다) EUDX를 안 쓰고 wwrite를 쓰는데, [0.8.4.6]부터 생긴 이 버그 때문에 주소가 상수인 SetDatfile/AddDatfile로 무기 공격력을 올렸는데 공격력이 0이 되는 등 의도치않은 현상이 나타나니 업데이트해주세요.

### 기능 변경

- -1, 0, 1로 곱셈, 나눗셈할 때 트리거 감소. 2, 4, 8, ... , 128로 곱셈할 때 `f_bitlshift` 사용하게 변경
- `f_dwbreak`, `f_dwbreak2` 최적화


## [0.8.6.0] - 2019.04.04

### 변경사항

- StringBuffer`.fadeIn/fadeOut` 사용법 변경, `line` 인자 추가
- CurrentPlayer가 불일치하면 StringBuffer`.fadeIn/fadeOut`이 *-1*을 리턴합니다.
- `TextFX_FadeIn/FadeOut` 줄바꿈 (\n) 지원 추가

#### 기존 텍스트효과 작성법이 복잡해서 간단하게 바꿨습니다.
* `line`:
  * *0~10*은 위에서부터 첫째줄~열한번째줄에 고정 출력
  * *-1~-11*은 처음 출력할 때는 아래에서 첫째줄~열한번째줄에 출력, 화면에 이미 있으면 예전 위치에 출력 (채팅/DisplayText처럼 올라가는 텍스트)
    ```javascript
    // epScrit 예제
    const s = StringBuffer(1023);

    function texteffect() {
        const tecolor = 4, 2, 0x1E, 5, 0;

        const t = s.fadeIn("\x13\x04세상은 \x19하나의 빛\x04으로부터 창조되었다.
    \n \n\x13\x04빛은 공허를 두개로 갈라 하늘과 땅을 만들었고
    \n\x13\x04그곳을 자신의 이름을 따 \x19아티아월드\x04라고 이름지었다.",
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

### 버그 수정

- 텍스트 효과가 탭, 줄바꿈도 색상 코드처럼 처리하던 버그 수정 (아티아님이 발견)
  - <09> 탭, <0A>, <0C> 줄바꿈도 <12>, <13> 정렬처럼 예외로 처리해야했는데, 색상 코드처럼 다루는 바람에 colors가 탭/줄바꿈 문자를 덮어쓰는 버그 수정.
  - 그래도 TextFX에서 \n을 쓰면 다음 줄은 `TextFX_Remove`로 지울 수가 없고, 한 줄씩 쓰면 줄마다 텍스트 효과 진행을 독립적으로 돌릴 수 있기에 한 줄씩 쓰는 걸 권장합니다.


## [0.8.5.7] - 2019.04.03

### 버그 수정

- Object를 트리거 필드에 넣을 때 생기는 오류 수정 (디펜더님 제보)
- GetTBLAddr 오류 수정


## [0.8.5.5] - 2019.04.02

### 버그 수정

- f_constdiv 잘못 고쳐서 생긴 버그 수정: 나머지 계산에 오류로 나머지=피제수 그대로 나온 것에서 비롯된 다채로운 버그였습니다. ㅠㅠ

### 기능 추가

- 변수×상수 곱셈 성능 최적화.
- `f_dbstr_print`, `f_cpstr_print`에 키워드 인자 `encoding` 추가 (기본값: *"UTF-8"*)
- `f_settbl(tblID, offset, *contents)` 추가


## [0.8.5.2] - 2019.04.02

### 버그 수정

- tpatcher 버그 수정 (아티아님 빠른 피드백 감사합니다)

### 변경사항

- `f_dbstr_print`, `DBString`이 *UTF-8* 인코딩을 기본으로 사용합니다.

### 기능 추가

- `f_dwrand` 최적화 (트리거 17개 감소)
- 컨디션, 액션의 word, byte에 변수 넣을 시 성능 최적화
  - 유닛/자원,점수 타입/(컨디션)스위치/(액션)플래그/동맹종류는 트리거 37개 → 3개 실행, 그 외의 byte는 곱셈이 필요해서 트리거 12개가 실행됩니다.
  - 컨디션: 스위치 상태, 비교타입, 컨디션 종류, 플래그
  - 액션: 유닛 수, 스위치 상태, 액션 종류, modifier, 명령
- EUDLoopPlayer 추가: P1 ~ P8 중에서 조건에 맞는 게임 중인 플레이어만 순환합니다.
  - 플레이어 타입(사람, 컴퓨터, 중립, 구조가능), 포스(0~3), 종족(ZTP, 유저선택 등)을 조건으로 사용 가능합니다. EUDPlayerLoop처럼 패배했거나 빈 자리인 플레이어는 건너뜁니다.
  - EUDPlayerLoop랑 달리 CurrentPlayer를 변경하지 않습니다.
    ```javascript
    // epScript 예제

    foreach(h : EUDLoopPlayer()) {
        // 모든 게임 중인 사람 플레이어 미네랄 +1
        SetResources(h, Add, 1, Ore);
    }

    foreach(f1 : EUDLoopPlayer("Human", Force1)) {
        // 게임 중인 Force1 팀 사람 플레이어 가스 +1
        SetResources(f1, Add, 1, Gas);
    }
    ```

    ```python
    # eudplib 예제

    for u in EUDLoopPlayer("Human", None, "User selectable"):
        # 종족이 User selectable 설정인 모든 사람 플레이어 미네랄 +1
        DoActions(SetResources(u, Add, 1, Ore))

    for z in EUDLoopPlayer(None, Force2, "Zerg"):
        # Force2의 저그 종족 플레이어 가스 +1
        # (User selectable로 로비에서 저그 고른건 해당 안 됩니다.)
        DoActions(SetResources(z, Add, 1, Gas))
    ```


## [0.8.5.1] - 2019.04.01

### 버그 수정

- `SetPName` 초기화 트리거 관련 버그 수정.


## [0.8.5.0] - 2019.04.01

### 버그 수정

- `SetPName`이 채팅 내용 1바이트 덜 가져오는 버그 수정 (아티아님 제보 감사합니다.)
- `SetPName` 닉네임 비교 버그 수정.
- [MSQC]에서 `EUDArray`, `PVariable` 사용 시 `no attribute` 오류 나는 버그 수정

### 기능 추가

- 로케이션 함수(`f_setloc`, `f_addloc`, `f_dilateloc`, `f_getlocTL`, `f_setloc_epd`)의 첫 인자로 로케이션 이름도 쓸 수 있게 수정.
- `f_cpstr_print`에 `EOS` 키워드 인자 추가.(기본값=*True*)
    - `EOS=False`로 두면 문자열 끝을 표시하지 않습니다.


## [0.8.4.9] - 2019.04.01

### 버그 수정

- 플레이어 닉네임이 다른 사람 닉네임을 포함할 때 SetPName이 같이 수정하는 버그 수정 (아티아님 제보 감사합니다.)

### 기능 추가

- 이제 `Db`를 스트링으로도 생성할 수 있습니다.
  - `Db("스트링")`은 `Db(u2utf8("스트링\0"))` 과 같습니다.
- 조건/액션의 word, byte 자리에 변수 대입 시 성능 최적화
  - Unit, Modifier 자리에 변수를 넣는 경우, Player, Location 같은 dword 자리보다 32배 이상 느렸는데, word, byte 때 성능을 약 50%, 75%로 개선했습니다. 성능 향상할 여지가 많아서, 다음 업데이트 때 tpatcher.py를 재작성할 예정입니다.
- `SQC` 라이브러리 추가.
  - 사용법은 [SQC 사용법] 링크 참고해주세요. 96, 192 크기인 맵에서 마우스 로케이션이 작동 안 되는 버그 수정됐습니다.
- 플러그인 이름 [MurakamiShiinaQC] ▶ [MSQC] 로 변경, 기능 추가.
  - `QCSafety` ▶ `QCDebug` 로 변경
  - 키보드, 마우스 클릭 등 비공유 인식 추가로 내장:
    * `KeyDown(Q)`: Q키를 누른 순간 1번 인식됩니다. 꾹 눌러도 1번만 작동해요.
    * `KeyUp(W)`: 누르고 있던 W키를 뗀 순간 1번 인식됩니다.
    * `KeyPress(E)`: E키를 꾹 누르는 동안 계속 인식됩니다.
    예전대로 Q ; W ; E 처럼 키만 달랑 쓰면 KeyDown으로 적용됩니다.

    - `MouseDown(L)`  마우스 좌클릭한 순간 1번 인식됩니다.
    - `MouseUp(R)`       누르고 있던 우클릭을 뗀 순간 1번 인식됩니다.
    - `MosePress(M)`    마우스 가운데(휠) 버튼을 누르는 동안 계속 인식됩니다.

  - `NotTyping`: 채팅 입력 창이 없으면 참입니다. 채팅 중이면 작동 안해요.
  - 이제 [MSQC]에서 `EUDArray`, `PVariable`, `EUDVariable` 도 쓸 수 있습니다. [MSQC]에 사용할 변수/배열은 미리 `EUDRegisterObjectToNamespace("a", a)`로 등록해야합니다.
    * `EUDVariable`: 조건에서만 쓸 수 있습니다.
    * `EUDArray`, `PVariable`: 반환값에서만 쓸 수 있습니다.
  - #### [MSQC] eds/edd 작성법 예시
    ```
    [MSQC]
    NotTyping ; KeyDown(A) : EUDArray, 1
    ∴ 채팅 중이 아니고, A키를 눌렀을 때 ▶ EUDArray[플레이어]에 1 더함.
    ```
- `soundlooper` 라이브러리 추가
  - 사용법은 그대로고 customText, `eudx.py` 대신 StringBuffer, EUDX 액션 사용하게 변경했습니다. [soundlooper 사용법] 글 참고해주세요.
- `[bgmplayer]` 플러그인 다시 추가
: 제가 만든 soundlooper나 EUDEditor2의 BGMPlayer에 비해 기능이 적어서 아무도 안 쓰는 거 같아서 뺐는데 수요가 있는 듯해서 다시 추가합니다. soundlooper, EUDEditor2의 BGMPlayer처럼 bgmplayer 플러그인도 역시스템시간(0x51CE8C)을 사용하므로 랙/배속 영향 안 받습니다. 배경음악 1개만 재생합니다.
  - #### [bgmplayer] 사용법
    ```
    [bgmplayer]
    path: res/bgm.ogg    # 사운드 파일 경로
    length: 33.680           # 사운드 길이
    ```
- `f_readgen_epd`, `f_readgen_cp(mask, *(initval, func))`이 함수의 바이트코드로 중복 여부를 평가합니다.
    ```python
    # 예시
    # a, b는 mask와 (시작값, 함수) 쌍이 동일하므로 같은 함수를 씁니다.
    a = f_readgen_epd(0xFF, (0, lambda x: x))
    b = f_readgen_epd(255, (0, lambda edac: edac))
    ```
- `EUDLoopNewUnit(allow=2)` 추가
    ```python
    # 예제
    for ptr, epd in EUDLoopNewUnit():
        ...
    ```
- Position 형 읽기 함수 추가: BW::Position, BW::Target 타입 용 읽기 함수가 추가되었습니다. (CUnit::nextMovementWaypoint, nextTargetWaypoint, position, 랠리, moveTarget, orderTarget 등) 맵의 좌표를 읽고 x, y로 반환합니다. 맵 크기에 따라 최대값이 달라집니다.
  * `f_posread_epd(epd)`, `f_posread_cp(cpoffset)`

- 로케이션 함수 추가
  * `f_setloc(로케이션, x, y)`: 로케이션의 좌·우 좌표를 x, 상·하 좌표를 y로 설정합니다.
  * `f_addloc(로케이션, x, y)`: (평행이동) 로케이션의 좌·우 좌표에 x, 상·하 좌표에 y만큼 더합니다.
  * `f_dilateloc(로케이션, x, y)`: (팽창) 로케이션의 좌·상 좌표를 x, y만큼 빼고, 우·상 좌표를 x, y만큼 더합니다.
    - 예시) 점로케이션을 `f_dilateloc(로케이션, 10, 6);` 하면 로케이션 크기는 **20x12**가 됩니다. 다시 `f_dilateloc(로케이션, -10, -6);` 하면 **0x0** 됩니다.
  * `f_getlocTL(로케이션)`: 로케이션의 왼쪽, 위쪽 좌표를 얻어냅니다.
  * `f_setloc_epd(로케이션, epd)`: 로케이션의 좌표를 epd의 Position으로 설정합니다. 아래 코드랑 같은 기능입니다.
    ```javascript
    x, y = posread_epd(epd);
    setloc(locIndex, x, y);
    ```


## [0.8.4.8] - 2019.03.29

### 기능 추가

- StringBuffer`.print(*args)` 추가 : 아래 3개를 묶어놓은 역할입니다.

```javascript
StringBuffer.insert(0);
StringBuffer.append(*args);
StringBuffer.Display();
```
- ptrmemio 최적화
    * `f_dwread`, `f_dwwrite`: ptr이 상수이고 4의 배수일 때 epd 사용.
    * `f_wread`, `f_wwrite`: ptr이 상수이고 4로 나눈 나머지가 3이 아닐 때 epd 사용.
    * `f_bread`, `f_bwrite`: ptr이 상수일 때 epd 사용.
- 기본 플러그인에 `[MurakamiShiinaQC]`, `[cammove]` 추가.
- StringBuffer 초기화 트리거 트리거 수 줄임.

### 기능 삭제

- _f_initextstr 삭제


## [0.8.4.7] - 2019.03.26

### 버그수정

- `Disabled(컨디션/액션)`이 컴파일 오류나는 버그 수정.
- StringBuffer를 선언한 이후에 스트링을 추가하면, StringBuffer 주소가 4의 배수를 벗어나는 버그 수정.
  - 스트링 공간 절약 기능을 [0.8.4.5]에서 추가했는데 이 부분은 생각 못 했네요...


## [0.8.4.6] - 2019.03.24

### 버그수정

- (트리거왕님 기여) `f_wwrite_epd(epd, subp, word)` 버그 수정:
    - subp가 상수일 때 f_bwrite_epd처럼 작동하는 버그. 12월 27일에 추가된 내용인데 이제 발견됐네요 ㅠㅠ

### 기능 추가

- Cython 적용해서 컴파일 시간이 개선됐습니다.
- (트리거왕님 기여) 패스워드 암호화 / 복호화 기반 트리거 추가.


## [0.8.4.5] - 2019.03.24

### 버그수정

- `TextFX_Remove` 버그 수정.
- 같은 크기의 StringBuffer가 같은 스트링을 가리키는 버그 수정.
- StringBuffer를 전역으로 선언할 수 없었던 버그 수정.

### 기능 추가

- SCMDraft2의 기본 유닛 이름 추가.
  * 추가된 이름은 [1e6fae3] 참고.
- StringBuffer 트리거 수 절약: CurrentPlayer 체크 트리거를 classmethod로.
- 스트링 공간 절약:
  * 이제 새 스트링은 빈 자리를 우선해서 채웁니다.
  * `This map requires EUD Enabler to run` 메시지 삭제.


## [0.8.4.4] - 2019.03.10

### 기능 추가

- 함수 `GetTBLAddr(TBLId)` 추가: 해당 번호의 stat_txt.tbl 텍스트의 주소를 가져옵니다.
- `QueueGameCommand` 관련 함수 다수 추가:
    * `QueueGameCommand_MinimapPing(xy)`: 유저가 xy좌표로 미니맵 핑을 찍습니다.
    *` QueueGameCommand_QueuedRightClick(xy)`: 선택한 유닛이 좌표로 Shift + 우클릭합니다.
    * `QueueGameCommand_PauseGame()`: 게임 일시정지.
    * `QueueGameCommand_ResumeGame()`: 게임 재개.
    * `QueueGameCommand_RestartGame()`: 게임 재시작. (싱글플레이 전용)
    * `QueueGameCommand_LeaveGame()`
    * `QueueGameCommand_UseCheat(flags)`
    * `QueueGameCommand_TrainUnit(unit)`: 선택한 유닛에 유닛 생산 명령을 내립니다.
    * `QueueGameCommand_MergeArchon()`: 선택한 유닛에 아칸 합체 명령을 내립니다.
    * `QueueGameCommand_MergeDarkArchon()`
- 함수 `f_getgametick()` 추가:
    오프셋 0x57F23C의 값을 읽고 f_getcurpl()처럼 캐싱합니다. f_dwread_epd(0x57F23C) 대신 쓰세요.
- 함수 `f_gettextptr()` 추가: 오프셋 0x640B58의 값을 읽습니다.
- 함수 `f_eprintln2(*args)` 추가:
    stat_txt.tbl[831]: "Unit's waypoint is full."의 내용을 덮어씁니다. 오류 메시지 줄에 내용을 218 바이트 이상 출력하고 싶을 때 쓰는 용도입니다. `QueueGameCommand_QueuedRightClick(xy)`랑 같이 사용하세요.
- `StringBuffer.DisplayAt(line)` 메소드 추가:
    line이 0이면 가장 윗 줄에, line이 10이면 가장 아랫 줄에 출력합니다.
- 텍스트 효과 추가:
    * `StringBuffer.fadeIn(*args, color=(3, 4, 5, 0x14), reset=True, wait=1, tag="?")`
    * `StringBuffer.fadeOut(*args, color=(3, 4, 5, 0x14), reset=True, wait=1, tag="?")`
    * `TextFX_SetTimer(tag, modtype, value)`
    * `TextFX_Remove(tag)`
    * `TextFX_FadeIn(*args, color=(3, 4, 5, 0x14), reset=True, wait=1, tag="?")`
    * `TextFX_FadeOut(*args, color=(3, 4, 5, 0x14), reset=True, wait=1, tag="?")`
    * `f_cpchar_print(*args)`:
        CurrentPlayer 위치에서 글자마다 한 DWORD에 (색상 코드 + 글자)로 출력합니다. EOS 有.
```javascript
// 예제 코드
function afterTriggerExec() {
    const xy = dwrand() & 0x1FFF1FFF;
    QueueGameCommand_MinimapPing(xy);

    setcurpl(getuserplayerid());
    const buffer = StringBuffer(1000);
    const lastLine = TextFX_Remove("FAH");
    buffer.insert(0);
    if(buffer.fadeIn(
        "\x13\x1F\x02페\x1E이\x16드 \x19인:\t\x07Star\x04Craft \x02ED\x1Fitor \x1BAC\x08ademy",
        tag=py_str("FAH")) == 0
    ) {
        buffer.insert(2);
        if(buffer.fadeOut(
            "\x13\x1F\x02페\x1E이\x16드 \x19아웃:\t\x07Star\x04Craft \x02ED\x1Fitor \x1BAC\x08ademy",
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

### 기능 제거

- OptimizeSetPName 필요 없게 수정.


## [0.8.4.2] - 2019.03.06

### 버그 수정

- EUD 미지원 오류 등 여러 오루 수정.


## [0.8.4.1] - 2019.03.06

### 버그 수정

- `SetKills` 액션이 비정상적으로 작동하는 버그 수정.

참고) `SetKills(플레이어, Modifier, 숫자, 유닛)`
- `플레이어`: Player1~12, CurrentPlayer 사용 가능합니다. AllPlayers, Force1~4 등은 미구현입니다.
- `유닛`: *플레이어가 CurrentPlayer일때만* `"(men)"`, `"(any unit)"` 등도 사용 가능합니다.

### 기능 추가

- 이제 체력 100% 유닛을 맵에 배치하면 최대 체력이 높아도 정상 체력으로 배치됩니다.
- 플레이어 닉네임 변경, 칭호 기능 추가:
  - 함수 `SetPName(플레이어, *이름)`
    : 플레이어의 닉네임을 "이름"으로 변경합니다.
    인자로 `PName`, `PColor`, `ptr2s`, `epd2s`, `hptr` 등 사용 가능합니다.
```javascript
// 플레이어 칭호 예시
function afterTriggerExec() {
    const title = PVariable();

    OptimizeSetPName();

    EUDPlayerLoop()();
    const cp = getcurpl();
    const my_title = title[cp];
    switch(my_title) {
        case 0:
            SetPName(cp, "\x16한 방에 곰을 잡은 ", PColor(cp), PName(cp));
            break;
        case 1:
            SetPName(cp, "\x16프로젝트 세레스 팀원 ", PColor(cp), PName(cp));
            break;
        case 2:
            SetPName(cp, "\x16베타테스터 ", PColor(cp), PName(cp));
            break;
    }
    EUDEndPlayerLoop();
}
```


## [0.8.4.0] - 2019.03.04

### 버그 수정

- git-lfs 때문에 자동 업데이트 안 되는 오류 수정.


## [0.8.3.8] - 2019.03.04

### 기능 추가

- 함수 `GetMapStringAddr` 성능 최적화.
- `StringBuffer`가 추가되었습니다.
- 함수 `f_eprintln(*args)` 추가되었습니다. (ct.f_chatAnnouncement랑 같은 역할)
- 함수 `f_raise_CCMU(player)` 추가. 플레이어에게 `Cannot create more unit.` 오류 메시지를 띄웁니다.
- 함수 `f_cpstr_print(*args)` 추가되었습니다.
현재 CurrentPlayer 위치에 텍스트를 작성하는 함수입니다.
f_dbstr_print랑 비슷한데 주소를 입력받지 않고 CurrentPlayer를 쓰고, EOS를 안 넣습니다.
스트링 끝을 표시하려면 `DoActions(SetDeaths(CurrentPlayer, SetTo, 0, 0))`을 넣으세요.
f_dbstr_print는 추후에 null 넣으려면 f_bwrite(dst, 0)해야되는 반면에 SetDeaths하나로 쉽게 되니까 유연하게 쓰려고 일부러 안 넣었습니다.
```javascript
function afterTriggerExec() {
    f_setcurpl(P1);
    // StringBuffer 예시

    // StringBuffer(용량) 또는 StringBuffer("초기내용")으로 생성합니다.
    const s = StringBuffer(1023);

    // StringBuffer.insert(EPD인덱스, 내용들, ...)
    // 스트링 끝을 표시하는 null 문자를 넣지 않기 때문에,
    // 스트링 중간 내용만 교체하는 용도로 쓸 수 있습니다.
    s.insert(0, "sound\\Zerg\\Devourer\\");

    // StringBuffer.append(내용들, ...)
    // 마지막 위치에 내용을 덧붙이고, EOS를 넣습니다.
    s.append("ZDvPss00.WAV");

    // StringBufer.Display()
    // 스트링 버퍼를 화면에 출력합니다.
    s.Display();

    // StringBufer.Play()
    // 스트링 버퍼의 내용을 경로로 사운드를 재생합니다.
    s.Play();

    const my_name = PName(getuserplayerid());
    const my_color = PColor(getuserplayerid());
    s.insert(0);
    s.append(my_color, my_name, "\x16님 안녕하세요 ^^;");
    s.Display();

    // eprintln은 에러줄에 출력합니다.
    eprintln(my_color, my_name, "\x16님 안녕하세요");
}
```

#### StringBuffer의 메소드 `insert`, `append`, 함수 `f_dbstr_print`, `f_cpstr_print` 내용 작성 팁.
- `PColor(번호)`: 해당 번호 플레이어 기본색 칼라코드를 반환합니다. (ct.color랑 같음)
- `PName(번호)`: 플레이어 이름을 가져옵니다. (ct.str(0x57EEEB + 36 * player)와 같음)
- `ptr2s(주소)`: 해당 주소의 스트링을 불러와 연결합니다. (ct.str과 같음)
- `epd2s(epd)`: 해당 epd의 스트링을 불러와 연결합니다. (ct.strepd와 같음)
- `hptr(값)`: 값을 16진법으로 출력합니다.
- `GetMapStringAddr(스트링번호)`: 해당 번호인 스트링의 주소를 구합니다. (ct.strptr과 같음)
- `f_dbstr_print`도 `PName`, `ptr2s` 사용 가능합니다.

#### StringBuffer 멤버 변수
- StringBuffer`.StringIndex`: 버퍼 스트링의 스트링 번호
- StringBuffer`.epd`: 버퍼 스트링의 시작 주소의 epd (참조만 하고 수정하지 마세요.)
- StringBuffer`.pos`: 마지막 작성 위치 (epd)
- StringBuffer`.capacity`: 사용 가능한 최대 용량
* StringBuffer 그 외 메소드
  - StringBuffer`.delete(시작점epd인덱스, 길이epd)`: 인덱스부터 길이만큼 \r로 채웁니다.
  - StringBuffer`.length()`: 현재 버퍼 스트링의 길이를 반환합니다. `f_strlen_epd(StringBuffer.epd)`랑 같습니다.


## [0.8.3.7] 2019.03.03

### 기능 추가

- `PVariable` 추가.
```javascript
// 예시
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

### 버그 수정

- `EUDLoopUnit2` 오류 수정.


## [0.8.3.5] - 2019.02.02

### 버그 수정

- zlib 오류 수정.

### 기능 추가

- epScript에 `switch` 문 추가되었습니다. (디펜더님 기여)
```javascript
switch(표현식) {
  case x:
    // 코드
    break;
  case y:
    // 코드
    break;
  default:
    // 코드
}

// 예시

switch (day) {
  case 1:
    DisplayText("월요일 좋아");
    break;
  case 4:
  case 5:
    DisplayText("곧 주말이네 얼마 안 남았다");
    break;
  case 0, 6:
    DisplayText("와 주말이다");
    break;
  default:
    DisplayText("주말을 기다립니다");
}
```


## [0.8.3.4] - 2019.01.18

### 버그 수정

- (사로로님 제보) `f_wread_cp`, `f_wwrite_cp` 컴파일 오류 수정.

### 기능 변경

- `EUDLoopUnit`의 continue 조건을 0x4D(현재명령)이 [0]Die일 때로 변경. (unlimiter 적용맵도 유닛 루프 정상 작동)

### 기능 추가

- (여섯살님 기여) `EUDFuncPtr`이 `EUDFuncN`을 정적으로 가리킬 때 최적화.
- `EUDLoopUnit2`, `EUDLoopPlayerUnit(player)` 추가.
- `SetKills(player, modifier, number, unit)` 액션 추가.
    - player와 unit 둘 다 `EUDVariable`이거나, 둘 다 일반적이지 않은 값(Force1의 "(any unit)" 등)이면 `NotImplementedError` 발생합니다.


## [0.8.3.3] - 2019.01.07

### 기능 추가

- 하위호환 지원: `f_dwepdread_epd_safe`, `f_dwread_epd_safe`, `f_epdread_epd_safe(epd)`.
  - `EUDByteStream.flushdword()`는 아무것도 안 합니다. (pass랑 같습니다)
- `EUDXVariable(초기값, 비트마스크)` 추가.
    - 액션 `SetMask`, `AddMask`, `SubtractMask(값)`, `SetMaskX`, `AddMaskX`, `SubtractMaskX(값, 비트마스크)`.
    - 조건 `MaskExactly`, `MaskAtLeast`, `MaskAtMost(값)`, `MaskExactlyX`, `MaskAtLeastX`, `MaskAtMostX(값, 비트마스크)`.


## [0.8.3.2] - 2019.01.01

### 버그 수정

- (디펜더님 제보) 조건, 액션 인자에 True, False를 못 넣는 버그 수정.
- (여섯살님 제보) `f_strlen` 리턴값 버그 수정.
- `f_readcp_gen`에서 `EUDVariable is not iterable` 오류 수정.

### 기능 추가

- 비트 연산 함수 최적화: `f_bitand`, `f_bitor`, `f_bitxor`, `f_bitnand`, `f_bitnor`, `f_bitnxor`.
- 함수 `f_readepd_gen`, `f_readcp_gen(mask, *(초기값, 함수 쌍))`과 예제 함수 `f_cunit(epd)read_epd/cp`, `f_maskread_epd/cp` 추가.
  - 함수 f_readepd/cp_gen는 사용자 정의 읽기 함수를 만드는 함수입니다.
  - 예시1) CUnit 값 (0x59CCA8 + 336 * index)는 23개 비트(0x7FFFF8)만 사용하므로, CUnit 전용 읽기 함수 f_cunitread_epd는 다음과 같이 만들 수 있습니다.
  - ```f_cunitread_epd = f_readgen_epd(0x7FFFF8, (0, lambda x: x))```
  - 예시2) 256x256맵에서 유닛 좌표를 읽는 함수는, 8191 픽셀이 최대니까(0x1FFF) 다음처럼 만들면 됩니다.
  - ```f_posread_epd = f_readgen_epd(0x1FFF1FFF, (0, lambda x: x if x < 8192 else 0), (0, lambda y: y // 65536))```


## [0.8.3.1] - 2018.12.28

### 버그 수정

- Freeze 사용 불가능한 문제 수정 (트리거왕님 도움), Freeze에 쓰인 `*_safe` 함수 교체.
- epScript libgcc 관련 오류 수정.
- epScript에 `DeathsX`, `MemoryX`, `MemoryXEPD`, `SetDeathsX`, `SetMemoryX`, `SetMemoryXEPD` 추가. (2018.12.31)

### 기능 추가

- `VariableBase`의 메소드에 조건 `AtLeastX`, `AtMostX`, `ExactlyX(value, mask),` 액션 `SetNumberX`, `AddNumberX`, `SubtractNumberX(value, mask)` 추가.
- `EUDByteReader`와 `EUDByteWriter`를 `EUDByteStream으로` 통합. 메소드 `flushdword` 삭제. (여섯살님 아이디어 감사합니다)
  - 예전 코드 호환성을 위해 `EUDByteReader`, `EUDByteWriter는` `EUDByteStream`으로 연결됩니다.
- 스트링 관련 함수 추가: `f_memcmp(buf1, buf2, count)`, `f_strlen_epd(epd)`, `f_strlen(src)`, `f_strnstr(string, substring, count)`.
(2018.12.29)


## [0.8.3.0] - 2018.12.27

### 기능 추가

- EUDX 지원.
  - 조건 `DeathsX`, `MemoryX`, `MemoryXEPD` 추가.
  - 액션 `SetDeathsX`, `SetMemoryX`, `SetMemoryXEPD` 추가.
  - `Action`, `Condition`에 키워드 인자 `eudx` 추가.
  - memio 함수에 EUDX 적용: `f_bwrite_epd`, `f_wwrite_epd`, `EUDByteReader`, `EUDByteWriter`, `f_dwepdread_cp`, `f_dwread_cp`, `f_epdread_cp`, `f_dwepdread_epd`, `f_dwread_epd`, `f_epdread_epd`, `f_flagread_epd`, `f_wwrite`, `f_bwrite`, `f_dwread`, `f_wread`, `f_bread`.
- EUD함수 `f_wread_cp(cpo, subp)`, `f_bread_cp(cpo, subp)`, `f_wwrite_cp(cpo, subp, w)`, `f_bwrite_cp(cpo, subp, b)` 추가.
- 인자 타입 `TrgLocationIndex`, 함수 `EncodeLocationIndex` 추가.
- 액션 `AddCurrentPlayer`, EUD함수 `f_addcurpl` 추가.

### 기능 삭제

- safedwmemio 삭제: `f_dwepdread_epd_safe`, `f_dwread_epd_safe`, `f_epdread_epd_safe`.


## [0.8.2.9] - 2018.10.29

### 버그 수정

- 윈도우에서 `OSError: [WinError 126] 지정된 모듈을 찾을 수 없습니다.` 오류 수정.

[0.9.1.3]: https://github.com/armoha/euddraft/releases/download/v0.9.1.3/euddraft0.9.1.3.zip
[0.9.0.9]: https://github.com/armoha/euddraft/releases/download/v0.9.0.9/euddraft0.9.0.9.zip
[0.9.0.8]: https://github.com/armoha/euddraft/releases/download/v0.9.0.8/euddraft0.9.0.8.zip
[0.9.0.5]: https://github.com/armoha/euddraft/releases/download/v0.9.0.5/euddraft0.9.0.5.zip
[0.9.0.4]: https://github.com/armoha/euddraft/releases/download/v0.9.0.4/euddraft0.9.0.4.zip
[0.9.0.3]: https://github.com/armoha/euddraft/releases/download/v0.9.0.3/euddraft0.9.0.3.zip
[0.8.9.9]: https://github.com/armoha/euddraft/releases/download/v0.8.9.9/euddraft0.8.9.9.zip
[TBL 문자열 목록]: https://cafe.naver.com/edac/82819
[SQC 사용법]: https://cafe.naver.com/edac/74735
[soundlooper 사용법]: http://kein0011.blog.me/221409128228
[1e6fae3]: https://github.com/armoha/eudplib/commit/1e6fae3ac884e980741199c22fbddb06414f7f03
[0.8.2.9]: https://github.com/phu54321/euddraft/raw/master/latest/euddraft0.8.2.9.zip