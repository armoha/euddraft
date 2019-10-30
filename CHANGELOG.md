[b]Tons of Changelogs[/b]

[0.8.9.0] 2019-10-19[LIST][*]f_simpleprint is now displayed to AllPlayers.[*]Optimize EUDByteReader/Writer, Remove EUDByteStream.[*]Added f_parse(dst, radix=10)[*]Added formated print functions/methods.[*]Added condition IsUserCP.[*]Optimize f_dbstr_print when # of arguements >= 2.[*]Optimize EUDExecuteOnce.[*]Reduce initialization triggers from 500 to 427.[*]Added EUDLightVariable functionalities.[/LIST]

[0.8.8.1] 2019-10-10[LIST][*]f_dbstr_print supports epd2s (Fixed error with PColor, ct.color)[*]Added EPDOffsetMap.getdwepd(name).
 Returns f_dwread_epd(offset)[*]Optimize SeqCompute, EUDFunc call.[*]Optimize location functions when location is constant and coordinates are variables. (f_setloc, addloc, dilateloc)[/LIST]

[0.8.7.9] 2019-09-25[LIST][*]Fix EUDLoopUnit2 has mismatched epd value with EUDContinue.[/LIST]

[0.8.7.8] 2019-09-25[LIST][*]Temporarily, StringBuffer print to screen directly. (Playing sound does'nt work. fadeIn, fadeOut have 54 bytes limit.)[/LIST]

[0.8.7.7] 2019-09-25[LIST][*]Preserve CRGB section. Add STRx support for input map.[*]Fix text encoding error with MSQC.[/LIST]

[0.8.7.6] 2019-09-20[LIST][*]Add f_settbl2(tblID, offset, *contents). f_settbl2 won't write null character, so it is useful for partial replacing stat_txt.tbl.[*]Won't reset hash table/block table when its size is enough for added files.[*]Raise error when fail to add file, or extend block table.[*]Optimize f_dbstr_adddw and loop functions; EUDLoopList, EUDLoopUnit, EUDLoopNewUnit, EUDLoopUnit2, EUDLoopPlayerUnit, EUDLoopSprite.[/LIST]

[0.8.7.5] 2019-09-20 (eudplib 0.59.1)[LIST][*]Extend hash table/block table based on the number of added files.[*]Optimize freeze: reduce about 500 objects with empty basemap.[/LIST]

[0.8.7.4] 2019-09-12[LIST][*]Fix autoupdate related error, when there is no internet connection.[*]Fix .edd compiles endlessly.[/LIST]

[0.8.7.3] 2019-09-02[LIST][*]Fix error when drag-drop map to euddraft.exe for freeze protection.[*]Fix f_strnstr.[*]Fix SetKills action with CurrentPlayer. Fix SetKills not work in epScript.[*]PColor changed; it gets player's current color and returns closest text color code.[*]Text print functions(f_dbstr_print, f_cpstr_print) changed; default behavior with str changed from CPString to ptr2s/epd2s. It slows but occupies less spaces.[*]Input Db in print functions will print Db as ptr2s(Db)/epd2s(EPD(Db)).[*]Add method StringBuffer.printAt(line, *arguments).[*]f_setloc, f_addloc, f_dilateloc now also accepts 4 coordinates (left, top, right, buttom).
[*]Stack MRGN PTR/ORT triggers; size reduced from 4816 bytes to 3244 bytes.[*]Optimize _f_mul (multiplication between variables). For example, EUDVariable(100) * EUDVariable(~) runs 41 SetDeaths actions, which is reduced from 62 SetDeaths actions.[*]Location functions (f_setloc, f_addloc, f_dilateloc) uses 1 trigger if all arguments are constants.[*]Add freeze prompt option.[/LIST]

[0.8.7.2] 2019-06-11[LIST][*]Fix f_raise_CCMU reduced max unit limit when CCMU.[*]pip install eudplib won't require C++ Build Tool.[/LIST]

[0.8.7.1] 2019-06-08[LIST][*][MSQC]Fix error with xy syntax when src is constant address.[*]Add plugin [chatEvent].
How to use:

[chatEvent]
Text you want to detect: number at least 2
@gg: 10
-> When player send message "@gg", memory address __addr__ SetTo 10. Default __addr__ is 0x58D900, and you can change it by __addr__: address.
^start.*middle.*end$: number
^Star.*.*$: 5
-> When player send message start with "Star", address __patternAddr__ SetTo 5. You should assgin __patternAddr__ by __patternAddr__: address.
-> If __ptrAddr__ is assigned, address __ptrAddr__ SetTo (position of chat message).
-> If __lenAddr__ is assigned, address __lenAddr__ SetTo (chat message length/bytes)).
^.*Edit.*$ : 6
-> When player send message including "Edit", address __patternAddr__ SetTo 6.
^.*.*Network$ : 7
-> When player send message end with "Netwrok", address __patternAddr__ SetTo 7.[/LIST]

[0.8.7.0] 2019-06-06[LIST][*][MSQC]Fix bug QCUnit, QCLoc, QCPlayer won't changed from default values.[*]EUDFunc, EUDMethod uses inspect.getfullargspec instead of inspect.getargspec.[*]Add f_setcurpl2cpcache().[*]Change f_repmovsd_epd to simple and optimized version.[*]Apply FlattenList to VProc.[*]Reduced common EUDByteStream.[/LIST]

[0.8.6.9] 2019-05-24 (eudplib 0.58.9)[LIST][*]Fix bug when unit placed with 100% energy has default energy(50) in game.[*]Add EUDVariable.getDestAddr(), .SetDest(epd), .AddDest(epd), .SubtractDest(epd).[*]Optimize f_setcurpl with EUDVariable argument, cut action execution from 15 actions to 10 actions.[*]Optimize functions using CP-trick; ptr/epd memory io functions, EUDByteStream, f_readgen_epd, f_strlen_epd, f_strlen.[*]Optimize f_dwrand, f_rand by removing excess value copying.[*]Remove duplicate dlls, move dlls to lib folder.[/LIST]

[0.8.6.8] 2019-05-06[LIST][*]Remove location name strings, switch name strings, location name string info from output map.[/LIST]
[0.8.6.7] 2019-05-06[LIST][*]Fix bug all strings encoded to UTF-8.[/LIST]
[0.8.6.6] 2019-05-06[LIST][*]Fix colors of text effects was always default color(<02>).[*]Optimize f_randomize and change it to @EUDFunc.[*]VProc now also accepts iterable of EUDVariable for first argument.[*]Now outmap will save as StarCraft: Remastered SCX(VER).[*]Now u2b will encode string, which failed to encode as cp949, to UTF-8.[*]Now strings used for unit name will encoded to UTF-8.[*]Now in epScript, only action before semicolon will changed to trigger.
It enables DoActions, Trigger in epScript without py_eval.[/LIST]

[0.8.6.5] 2019-04-17[LIST][*]Add list(...), VArray(...) syntax in epScript.[/LIST]

[0.8.6.4] 2019-04-15[LIST][*]Fix bug when index of PVariable was contant.[/LIST]
[0.8.6.3] 2019-04-15[LIST][*]Optimize EUDVArray.[*]Now PVariable can be typecasted.[/LIST]

[0.8.6.2] 2019-04-10[LIST][*]Fix bug with division by 1.[/LIST]

[0.8.6.1] 2019-04-08[LIST][*]Fix bug with f_wwrite_epd(epd, subp, w) and f_wwrite(ptr, w), when address is constant and 'w' is EUDVariable, wrote value as 0.[*]Multiplication/division with -1, 0, 1 uses less triggers.[*]Use f_bitlshift when multiply by power of 2.[*]Optimize f_dwbreak, f_dwbreak2.[/LIST]

[0.8.6.0] 2019-04-04[LIST][*]Change how to use StringBuffer.fadeIn/fadeOut. Add keyword argument 'line'.[*]StringBuffer.fadeIn/fadeOut will return -1 when CurrentPlayer inequal localCurrentPlayer.[*]Add line break(\n) support in TextFX_FadeIn/FadeOut.[/LIST]

example epScript code)
[img=https://i.imgur.com/8VQYkWB.gif]
[sup]
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
}[/sup]