# 변경 사항 (한국어)

## [0.9.10.11] - 2023.12.29
### 버그 수정
- debug : 1 옵션을 킬 때 컴파일 오류 수정 (스타맵돌이님 제보)

### 기능 개선
- eudplib to 0.76.14 업데이트
- eudplib 프론트엔드 속도 17% 가량 개선 (@phu54321 님 기여: https://github.com/armoha/eudplib/pull/24)
- Writing phase에서 GetObjectAddr 개선
- 빌드 시간 10% 가량 감소

## [0.9.10.10] - 2023.12.27
### 기능 변경
- `ConstExpr`과 `EUDObject`이 `__init__` 대신에 `__new__`를 사용합니다
  * `ConstExpr`과 `EUDObject`의 서브클래싱하는 코드는 `__new__`를 추가로 오버라이드해야 합니다
  * 참고: https://stackoverflow.com/questions/28236516/python-subclassing-a-class-with-custom-new
- `RawTrigger`의 `currentAction` 키워드 인자 삭제

### 기능 추가
- `CUnit.set_collision()` 추가

  상태플래그에서 `NoCollide`와 `IsGathering`을 지웁니다. 유닛 충돌을 없애는 `CUnit.remove_collision()`과 반대로 유닛 충돌을 다시 적용합니다
- `.edd`로 빌드할 때 빌드 소요 시간을 출력합니다

### 기능 개선
- eudplib to 0.76.13 업데이트
- Rust로 재작성: `RlocInt`, `ConstExpr`, `EUDObject`, `RawTrigger.WritePayload` (https://github.com/armoha/eudplib/pull/22)
- 빌드 시간 30% 감소 (euddraft 0.9.10.6 및 이전 버전과 비교하면 총 60% 감소)

## [0.9.10.9] - 2023.12.23
### 버그 수정
- 커스텀 TBL 사용맵에서 settbl2가 작동하지 않는 버그 수정 (neonoew님 제보)

## [0.9.10.7] - 2023.12.19
### 기능 변경
- ConstExpr와 RlocInt_C의 offset과 rlocmode를 부호 없는 정수에서 부호 있는 정수로 변경
- ConstExpr의 연산 결과가 항상 ConstExpr를 리턴하도록 변경 (더 이상 int를 리턴하지 않습니다)
  * 타입 변환이 필요하면 int(ConstExpr) 를 사용하세요

### 기능 추가
- `CUnit.remove()` 추가 (DarkenedFantasies님 기여)

  구조오프셋에 해당되는 유닛을 삭제합니다. RemoveUnit처럼 사망 이펙트가 발생하지 않습니다.

### 기능 개선
- 컴파일 시간 약 40% 개선 (armoha/eudplib#21)
  * Allocating Phase 속도 대폭 개선: Rust로 StackObject와 AllocObject 재작성
  * Writing Phase 속도 개선: Rust로 ConstructPayload 재작성
  * 시간 오래 걸리는 Action/Condition 인자 체크 부분 삭제
- 한국어 번역 파일 갱신

## [0.9.10.6] - 2023.12.15
### 기능 추가
- [epScript] 인덱싱 문법에 "문자열 리터럴" 허용

### 버그 수정
- f_setcurpl2cpcache에서 TypeError: Value after * must be an iterable, not EUDVariable 오류 수정 (WestICE님 제보)

## [0.9.10.5] - 2023.12.15
### 버그 수정
- 비트 시프트 연산(<<, >>)의 우항이 32 이상일 때 생기는 버그 수정
  * EUD Editor 2에서 TriggerEditor를 사용할 때 게임 시작 때 10초 가량 멈추는 버그 수정 (@iDoodler-DS 님 제보)
  * `f_bitlshift(a, b)`의 우항에 32 이상의 변수를 입력하면 트리거를 과도하게 많이 실행하는 버그 수정
  * `f_bitrshift(a, b)`의 우항에 32 이상의 변수를 입력하면 잘못된 값을 반환하는 버그 수정

## [0.9.10.4] - 2023.12.13
### 기능 추가
- [epScript] `py_모듈`이 함수 이름 앞에 f_ 를 안 붙이게 수정

```js
// epScript 원 그리기 예제
import py_math;

function circle() {
    foreach (k : py_range(10)) {
        MoveLocation("effect", "Terran Ghost", P1, "Anywhere");
        // 이제 py_eval 안 써도 됩니다!
        const x = py_int(math.cos(k * math.pi / 5) * 30);
        const y = py_int(math.sin(k * math.pi / 5) * 30);
        addloc("effect", x, y);
        CreateUnit(1, "Scanner Sweep", "effect", P1);
    }
    RemoveUnit("Scanner Sweep", P1);
}
```

## [0.9.10.3] - 2023.12.13
### 버그 수정
- SoundLooper.py : `SoundLooper.initialize()` 컴파일 오류 수정
- [dataDumper] : 커스텀 TBL 사용맵에서 RuntimeError 수정
- `copy.copy(조건 또는 액션)` 컴파일 오류 수정
- `CUnit.setloc(로케이션)` 컴파일 오류 수정
- `ExprProxy.getValue()` 이름 변경 롤백
- `_AddStatText(bytes)`, `_addedFiles` 이름 변경 롤백
- 0.9.10.2의 EUD 함수 관련 변경점 롤백
  * `f_getcurpl()` 변수 트리거 안 거치게 성능 개선
  * `StringBuffer` 초기화 트리거 삭제 (`GetMapStringAddr` 업데이트로 필요 없어짐)

### 기능 개선
- EUDArray의 초기값으로 지원되지 않는 타입이 입력됐을 때 오류 메시지 개선
- `unProxy(object)`가 순환 참조를 감지하여 순환 루프 대신에 오류나게 수정

## [0.9.10.2] - 2023.12.11
### 기능 변경
- 파이썬 3.10.10에서 3.11.6 로 업데이트
- [epScript] `class`와 `subobject` 문법 삭제, `object` (+`extends`) 로 통합
- `GetMapStringAddr(스트링)`은 이제 상수 함수입니다
  * `GetMapStringAddr(상수_스트링)`이 리턴하는 스트링 주소는 상수 표현식(ConstExpr)입니다
- `ExprProxy`에서 inplace 연산자 기본으로 금지하게 변경
- `_Unique`와 상수 타입(`TrgPlayer`, `TrgUnit` 등) 통합
- `StringBuffer`를 `EUDStruct` 타입으로 변경

### 버그 수정
- [freeze] 비압축-암호화 OGG 파일이 첨부된 맵에서 버그 수정 (@phu54321 님 기여)
- [epScript] Python 3.11에서 컴파일 오류 발생 시 StopIteration 오류 수정
- soundlooper.py : 배열 경계를 벗어난 접근 수정
- [MSQC] 마우스 로케이션이 우측 또는 하단 맵 가장자리에 가까워도 작동하도록 수정 (Staminize님 제보)
- Sprite, Image, Iscript 등 오타 수정 (디펜더님 제보)
- 상속한 epScript object/EUDStruct의 멤버 개수가 objFieldN보다 넘치는 버그 수정 (Astro님 제보)
  * 객체 멤버 유효성을 인스턴스가 아니라 클래스 정의할 때 체크하도록 수정
- `UnitGroup.cploop`가 끝나고 CurrentPlayer를 복구하도록 수정
- `EUDLoopNewCUnit`이 끝나고 CurrentPlayer를 복구하도록 수정
- `CUnit.reset_buildq()` 컴파일 오류 수정
- Condition과 Action을 copy.copy(x)하면 순환 루프하는 버그 수정
- `Disabled(조건 또는 액션)`이 None이 아니라 입력한 조건/액션을 리턴하도록 수정

### 기능 추가
- [dataDumper]에 stat_txt.tbl 인코딩 자동 인식 추가
  * `f_settbl` 등 TBL 관련 함수가 인식한 인코딩을 사용합니다
- `CUnit.are_buildq_empty()` 조건 추가
- `CUnit.check_buildq(unit)` 조건 추가
- `CUnit` 멤버에 컴파일 시간 범위 체크 추가
- [epScript] 이제 문자열 리터럴을 비교문과 대입문에서 쓸 수 있습니다
- `LocalLocale` 추가
  * 유저가 사용하는 스타크래프트 언어 설정을 게임 시작 때 인식합니다

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
  * 0 = (알 수 없음), 1~14 = 로케일 값
  * 사용법
    - LocalLocale == "koUS" : 한국어 음역 사용자인지 비교하는 조건
    - LocalLocale != "enUS" : 영어 사용자가 아닌지 비교하는 조건
    - LocalLocale << "zhCN" : 인식 언어를 저장하는 변수의 값을 중국어 간체자로 변경합니다 (사용자의 스타크래프트 언어 설정을 EUD로 변경하는 게 아닙니다)
  * 제한점
    - 스타크래프트 리마스터 비구매자의 언어 설정은 인식할 수 없습니다
    - 한국어 음역(koUS)과 완역(koKR) 구별이 아직 불가능합니다. 현재는 둘 다 음역(koUS)으로 인식됩니다
- `QueueGameCommand_AddSelect(유닛수, ptr배열)` 함수 추가
- `QueueGameCommand_RemoveSelect(유닛수, ptr배열)` 함수 추가

### 기능 개선
- freeze 취약점 개선 (@phu54321 님 제보)
- `CUnit.cgive(플레이어)`, `CUnit.set_color(플레이어)` 성능 개선
- EUD 함수 리턴 성능 개선: 중간 변수 안 거치고 대입 트리거 사용
- `f_getcurpl()` 변수 트리거 안 거치게 성능 개선
- `StringBuffer` 초기화 트리거 삭제 (`GetMapStringAddr` 업데이트로 필요 없어짐)
- `QueueGameCommand_Select(유닛수, ptr배열)` 성능 개선 : 중간 버퍼 삭제

## [0.9.9.9] - 2023.06.13
### 기능 변경
- `atan2_256(y, x)`와 `lengthdir_256(길이, 256각도)`가 스타크래프트에서 사용하는 좌표계를 따르도록 변경
  * 이제 더 이상 게임에서 사용하는 좌표계에서 수학에서 쓰는 좌표계로 변환할 필요가 없습니다
- `$T`, `EncodeString`, `GetStringIndex`가 UTF-8 인코딩 사용하게 변경
- 파이썬 3.11.1에서 3.10.10 으로 다운그레이드
  * `StopIteration` 오류 수정

### 버그 수정
- 32비트 와이어프레임 버그 수정: 시즈탱크, 질럿 등
- `cunitread_cp` 읽기 함수가 값이 0인 주소를 읽을 때 버그 수정 (paols님 제보)
- `EUDLoopPlayerCUnit(플레이어)` 안에서 `cunit.cgive(플레이어);` 사용할 때 버그 수정 (GGrush님 제보)
- `UnitGroup.add(변수);`가 변수의 값을 변경하는 버그 수정 (GGrush님 제보)
- 상대 경로 불러오기가 모듈을 복사하는 버그 수정
- 파일이 파이썬 단계에서 오류가 났을 때 오류 메세지에서 잘못된 줄 번호와 코드 내용을 보여주는 버그 수정
- `CUnit.statusFlags` 플래그 이름에 오타가 있어도 오류나지 않는 버그 수정 (armoha/euddraft#113 수정)
- 인자 타입 없이 리턴 타입만 있는 람다 함수가 타입 없는 함수를 만드는 버그 수정
- `NonSeqCompute`에서 `None` 수정자 넣을 때 버그 수정
- `eps-server`가 CUnit 클래스 멤버 정보를 가져오지 못하는 버그 수정

### 기능 추가
- [epScript] `class`, `extends` 키워드 추가
  * `object` (=`EUDStruct`) 끼리 상속 기능 추가
- `EUDQueue`와 `EUDDeque`의 `foreach` 루프문에서 `break;`, `continue;`, `EUDSetContinuePoint();` 사용 가능하게 수정
- `객체.상수타입멤버 = 상수;` 작성 가능
  * 예시: `instance.player = P1;` (`TrgPlayer` 타입)
- 3개의 부호 있는 나눗셈 함수 추가
  * 인자가 상수면 상수를 리턴합니다
  * `const 몫, 나머지 = div_towards_zero(a, b);`

    (a ÷ b)의 몫과 나머지를 계산합니다. 몫을 0에 가까워지게 양수에서 버림/음수에서 올림합니다.

    부호 없는 나눗셈 함수 `div(a, b)` 와 다르게 제수와 피제수의 부호를 고려합니다.
    JavaScript 같이 C와 유사한 프로그래밍 언어와 일관된 동작입니다.
  * `const 몫, 나머지 = div_floor(a, b);`

    (a ÷ b)의 몫과 나머지를 계산합니다. 몫을 음의 무한대 방향으로 버립니다.

    부호 없는 나눗셈 함수 `div(a, b)` 와 다르게 제수와 피제수의 부호를 고려합니다.
    수학적 모듈로와 일관된 동작입니다.
  * `const 몫, 나머지 = div_euclid(a, b);`

    a와 b의 유클리드 나눗셈 결과를 계산하여 몫과 나머지를 반환합니다.

    부호 없는 나눗셈 함수 `div(a, b)` 와 다르게 제수와 피제수의 부호를 고려합니다.
    `div_euclid(a, b)` 함수는 식 `a = 몫 * b + 나머지`가 성립하면서 `0 <= 나머지 < (b의 절대값)`을 만족하는 몫을 계산합니다.

    다르게 말하면, 결과물은 (a ÷ b)을 반올림하여 몫이 `a >= 몫 * b` 부등식을 만족하게 합니다.
    a가 양수라면, 0을 향해 반올림하는 것과 같습니다; a가 음수라면, +/- 무한대를 향해 반올림하는 것과 같습니다 (0에서 멀어짐).
- `VariableBase`(`EUDVariable`, `EUDLightVariable`)의 제자리 부정 연산, 제자리 절대값 연산 추가
  * `var.ineg();` : 변수의 값을 제자리 부정합니다. (`x = -x;`와 같습니다)
  * `var.iabs();` : 변수의 값을 자신의 절대값으로 대입합니다. (`x = (x & (1 << 31) == 0) ? x : -x;`와 같습니다)
  * `DoActions(var.ineg(action=true));` : 액션 버전
  * `DoActions(var.iabs(action=true));`

### 기능 개선
- `EPD`의 트리거 실행 수 감소
- Rvalue 변수 `EPD` 최적화
- 나누기 (/), 나머지 (%) 연산 트리거 개수 감소
- `EUDArray`, `EUDVArray(크기)` 타입들을 상수로 인덱싱할 때 경계를 벗어나면 오류나게 경계 체크 추가
- 상수 곱셈에서 곱할 상수의 오버플로로 0이 되는 큰 비트들에 대해 트리거 절약
- 객체 필드 이름 중복되면 컴파일 오류나게 추가
- `UnitOrder` 타입에 EUD Editor가 사용하는 이름들도 지원하게 추가
- 연결맵에 존재하지 않는 유닛 이름과 상수 타입에 대해 오류 메시지 개선
- 몇몇 오류 메시지가 `repr` 표현을 출력하도록 개선
- eudplib 0.75.0, cx-freeze 6.15.1, pybind 2.10.4 업데이트

## [0.9.9.7] - 2023.01.29
### 버그 수정
- `ImportError: Module use of python310.dll conflicts with this version of Python.` 오류 수정
- `TypeError: Population must be a sequence.  For dicts or sets, use sorted(d).` 오류 수정

### 기능 개선
- 파이썬 3.11.1 업데이트
  * 이제 eudplib 이 파이썬 3.10과 3.11을 둘 다 지원합니다
- **epScript:** `var v = rvalue변수;` 처럼 지역 변수 초기화에 RValue 변수가 초기값일 때 복사가 일어나지 않도록 수정
  * 일부 상황에서 복사를 잘못 생략하거나 복사 트리거를 생략하지 못하는 버그 수정
- `SetVariables(rvalue변수, 값)`은 이제 컴파일 오류입니다
  * r-value란: `dwread_epd(0)`, `array[index]` 처럼 이름이 없는, 지칭할 수 없는 값을 의미합니다
- 한국어 번역 업데이트
- euddraft의 stdin, stdout, stderr가 항상 UTF-8을 사용하도록 수정
- eudplib 0.74.9, cx-freeze 6.14.2 업데이트

## [0.9.9.5] - 2023.01.24
### 버그 수정
- CUnit.posY 버그 수정 (할루님 제보)
- CSprite(상수) 버그 수정

### 기능 추가
- `CUnit.cgive(플레이어)` 추가

### 기능 개선
- `CUnit`, `CSprite`: 초기화 때 변수 복사하도록 수정, `__slots__` 삭제
- eudplib 0.74.5 업데이트

## [0.9.9.4] - 2023.01.19
### 기능 변경
- `EPDOffsetMap`을 함수에서 추상 클래스로 변경, `EPDCUnitMap`을 `CUnit`의 별칭으로 변경
- `_EUDStructArray`를 동적 클래스에서 정적 클래스로 변경

### 버그 수정
- [dataDumper] 플러그인 작성 순서와 상관없이 가장 먼저 실행되도록 수정 (iDoodler님 제보)
  * EUD Editor 2 TriggerEditor의 onPluginStart에서 실행한 changeStarText와 settblf가 적용되지 않는 버그 수정
- `f_badd_epd`에서 값이 변수일 때 `f_bwrite_epd`가 실행되는 버그 수정 (wdcqc님 제보)
- `RunAIScript("4글자 코드")`가 오류나는 버그 수정 (wdcqc님 제보)
- `EUDDeque.appendleft`가 `foreach` 데큐 순회 트리거를 고장내는 버그 수정

### 기능 추가
- 비공유 조건 `Is64bitWireframe()` 추가
  * 64비트 스타크래프트에서 참, 32비트에서 거짓인 비공유 조건입니다.
  * 와이어프레임 사용맵이 됩니다: 시즈탱크, 하이템플러, 질럿 등 와이어프레임 버그 부작용이 발생합니다.
- 프록시 클래스 `CUnit`, `CSprite` 추가
  * 크게 4가지 방법으로 생성할 수 있습니다.
  * `CUnit(epd)`: 구조오프셋의 epd만 있을 때 CUnit 생성자 (인자타입 또는 CUnit.cast 시 epd만 입력받습니다)
  * `CUnit(epd, ptr=ptr)`: ptr과 epd 둘 다 입력하는 생성자
  * `CUnit.from_read(epd)`: epd 주소에서 CUnit 값을 읽어서 CUnit 클래스를 생성합니다.
  * `CUnit.from_ptr(ptr)`: 게임 중에 트리거로 나눗셈을 하여 ptr에서 epd를 계산하여 CUnit 클래스를 생성합니다.
  * 멤버 목록: https://github.com/armoha/eudplib/blob/master/eudplib/offsetmap/cunit.py#L84-L371
- `EUDLoopCUnit`, `EUDLoopNewCUnit`, `EUDLoopPlayerCUnit` 추가
- `offsetmap` 모듈 추가
  * `offsetmap.EPDOffsetMap`
  * `offsetmap.MemberKind`
  * `offsetmap.BaseMember`
  * `offsetmap.Member`
  * `offsetmap.CUnitMember`
  * `offsetmap.CSpriteMember`
  * `offsetmap.EnumMember`
  * `offsetmap.Flag`

## [0.9.9.3] - 2023.01.14
### 버그 수정
- EUD Editor 3 BGM Player와 노래맞히기 오픈소스 컴파일 오류 수정

## [0.9.9.2] - 2023.01.12
### 기능 변경
- Cython, numpy, matplotlib, pywin32, cffi, idna 의존성 삭제
  * 아직 Cython의 typing 지원이 부족하여 각종 오류를 일으켜서 삭제했습니다. 컴파일이 느려진 건 mypyc를 도입해서 해결할 예정입니다.
  * Cython을 삭제하면서 Cython과 밀접하게 연계되는 numpy도 삭제했습니다.
  * Ren'Py 같은 파이썬 기반 게임 엔진과 달리, euddraft는 eps/py로 작성한 플러그인으로 EUD맵을 만드는 컴파일러이고, 스타크래프트가 게임 엔진 역할을 합니다. 스타크래프트가 실행하는 건 오로지 트리거이고, numpy와 matplotlib는 트리거를 만드는 데 도움을 줄 수는 있어도 스타크래프트에서 직접 사용할 수는 없습니다만 이러한 사실을 잘 모르는 초심자한테 혼란을 주기도 합니다. 추후 cx_freeze가 업데이트되어 파이썬 3.11을 도입하면 numpy의 컴파일 시간 단축 이득도 적어질거라 예상됩니다. 또한 numpy와 matplotlib을 이용한 트리거 생성은 EUD Editor처럼 eps/py 코드 생성으로 해결할 수 있으므로 삭제했습니다.
  * pywin32, cffi, idna는 euddraft에서 오랫동안 사용하지 않아서 삭제했습니다.

### 버그 수정
- [MSQC] 작동 안 되는 버그 수정
- `NotImplementedError: You should not call an overloaded function.` 오류 수정 (택하이님 제보)

### 기능 개선
- openpyxl 의존성 추가: 엑셀 파일을 읽거나 쓸 수 있습니다
- [epScript] 상대 경로로 전역 변수, 함수도 불러올 수 있게 수정 (Low Signal님 제보)
- [epScript] armoha/euddraft#66: 파이썬 키워드를 덮어쓰려할 때 오류나게 수정 (Low Signal님 제보)
- SetVariables, SeqCompute, EUDVariable.SetModifier의 modifier에 변수 사용했을 때 오류 메시지 개선 (Low Signal님 제보)

## [0.9.9.1] - 2023.01.09
### 버그 수정
- [epScript] 단일 비상수 초기값 전역 변수 또는 전역 배열 선언시 컴파일 오류 수정

## [0.9.9.0] - 2023.01.09
### 기능 변경
- 예상되지 않은 상수 값이 조건으로 쓰였을 때 컴파일 오류 또는 경고 추가
  * EUDArray, EUDVArray, EUDStruct (epScript의 object) 등 cast 가능한 상수가 조건에 쓰이면 '이 조건은 항상 참입니다' 경고
  * 그 외 ConstExpr는 컴파일 오류
  * -1, 0, 1 등 정수는 이전과 동일하게 0은 Never(), 0이 아닌 정수는 Always() 조건으로 변환합니다.
- `TrgTBL` -> `StatText` 이름 변경
- `VariableBase`와 `EUDObject`를 추상 클래스로 변경

### 버그 수정
- [epScript] 전역 상수에 ExprProxy를 전방 선언한 함수를 호출하는 등의 경우에만 씌우도록 수정
  * 대부분의 상황에서 더 이상 `전역상수.getValue()` 안 해도 됩니다.
- [MSQC] 우클릭 대신 이동 명령 사용하도록 수정
  * 이제 플레이어가 임의로 QC유닛을 부대지정하여 우클릭으로 조작할 수 없습니다.
- [draw.py] `점x, 점y = 도형[인덱스]` 무한 컴파일 버그 수정 (갈대님 제보)
- [epScript] 상대 경로 불러오기 기능 버그 수정 (유즈맵조아조아님 제보)
  * euddraft 0.9.8.3~0.9.8.13에 존재하는 Artanis 노래맞히기 오픈소스 컴파일 오류 수정했습니다.
- `EPDCUnitMap.set_color(player)` 컴파일 오류 수정 (할루님 제보)
- `TypeError: EncodePlayer() got an unexpected keyword argument 'issueError'` 오류 수정 (HuntRabbit님 제보)
  * [BetterBrain] 플러그인 컴파일 오류 수정
- euddraft 0.9.8.13에서 추가된 모호한 스트링이 있을 때 경고 메시지 삭제, 예전 동작 롤백 및 오류 메시지 개선 (nn2님 제보)
- `f_dwpatch_epd` 지원되지 않는 EUD 오류 수정

### 기능 개선
- [epScript] 전역 변수 초기값이 상수일 때 초기화 트리거 없이 초기값 설정하도록 수정
- CreateUnitWithProperties 액션에서 HP이 100%일 때 최대 체력이 167772를 초과하는 유닛을 최대 체력으로 생성하도록 수정
- UnitProperty가 동일한 결과의 UnitProperty를 재사용하도록 수정: cloaked=None이나 cloaked=False나 같은 프로퍼티를 사용
- EUD 반복문(EUDInfLoop, EUDLoopN, EUDLoopRange, EUDWhile)을 반복할 때 트리거 개수 1개 덜 실행하게 수정 (콤님 제보)
- ConstExpr간의 연산 결과 rlocmode가 0이면 정수 오프셋을 반환하도록 수정
- eudplib 오류 메시지 추가 및 개선
- euddraft의 한국어 번역 파일 업데이트
- eudplib 0.73.16 업데이트

### 기능 추가
- [epScript] 가장 바깥 스코프에서 함수 호출 문법 사용 가능
  * 액션이나 EUD함수처럼 트리거를 가장 밖에 추가하면 오류 메시지로 알려줍니다.
  `"트리거는 onPluginStart, beforeTriggerExec 또는 afterTriggerExec에 작성해야 실행됩니다"`
  * `EUDOnStart`, `InitialWireframe`, `MPQAddFile`, `EUDRegisterObjectToNamespace`  등 eudplib 함수나\
  py라이브러리의 함수를 epScript에서 쉽게 사용하기 위해 추가한 기능이에요.
- 타입 힌트 정정 및 추가
- `TriggerScopeError` 추가: `EPError`의 서브클래스입니다. 트리거를 추가할 수 없는 위치에 작성했을 때 반환됩니다.
- `b2utf8(bytes) -> str` 함수 추가: 바이트를 UTF-8 문자열로 디코딩합니다.

## [0.9.8.13] - 2023.01.01
### 버그 수정
- 여러가지 버그 수정

### 기능 개선
- 타입 힌트 추가
- eudplib에 mypy 타입 체크 적용
- eudplib 0.73.0 업데이트

## [0.9.8.12] - 2022.12.31
### 버그 수정
- `EUDVArray`, `PVariable`에 `a[index] /= (2의 제곱 상수)` 컴파일 오류 수정 (gongnamu님 제보)
- 일부 환경에서 `EUDLoopNewUnit`이 맵에 배치된 유닛을 순회하지 않는 버그 수정 (Oneiro님 제보)

### 기능 개선
- eudplib 일부 함수에 타입 힌트 추가: localize, maprw, trigger, trigtrg, utils
  * core, ctrlstru, epscript, eudlib은 아직 작업 필요
- eudplib 0.72.6 업데이트

## [0.9.8.11] - 2022.12.30
### 변경사항
- `$T`, `EncodeString`, `GetStringIndex`이 새 스트링을 추가할 때 CP949 인코딩을 사용하도록 롤백합니다.

### 버그 수정
- `[chatEvent]` 해시 충돌 시 채팅 내용 비교하도록 수정 (LLAS님 제보)

### 기능 개선
- `[chatEvent]` 패턴 문자열에 간단한 암호화 추가
- eudlib/utilf 함수에 타이핑 추가
- eudplib 0.72.5 업데이트

## [0.9.8.10] - 2022.12.25
### 버그 수정
- `EUDOnStart`를 아무 위치에서 사용할 수 있게 수정
- `println`, `printAt`, `simpleprint` 등 출력 함수가 작동 안 되는 버그 수정 (armoha/euddraft#28)
  * 이제 `onPluginStart`에 `GetGlobalStringBuffer()` 안 넣어도 돼요
- `InitialWireframe`을 안 써도 `SetWireframes`를 쓸 수 있게 수정
- **[epScript]** 전역 상수에 `py_len()` 사용 가능하도록 수정
  * `ExprProxy`에 `len()`을 사용하지 못하는 버그를 수정했습니다.

### 기능 개선
- eudplib 0.72.3 업데이트, pybind11 v2.10.2 업데이트
- `StringBuffer` 초기화 트리거 크기 최적화

## [0.9.8.9] - 2022.12.20
### 변경사항
- `$T`, `EncodeString`, `GetStringIndex`이 새 스트링을 추가할 때 UTF-8 인코딩을 사용합니다.

### 버그 수정
- Null 타일 경고 메시지에 (x, y) 좌표가 반대로 나오는 버그 수정
- 마린 수정 안 했을 때 `InitialWireframe` 버그 수정 (Oneiro님 제보)

### 기능 개선
- eudplib이 Python 3.11을 지원합니다.
- `[chatEvent]` 전역 EUD 이름 공간을 지원합니다.
  ```ini
  :: eds/edd 예시
  [chatEvent]
  __addr__: addr
  __patternAddr__: patternAddr
  __ptrAddr__: ptrAddr
  __lenAddr__: lenAddr
  판매 : 2
  고스트판매 : 3
  히드라판매 : 4
  드라군판매 : 5
  ^'미네랄 .*.*$: 1
  ^'가스 .*.*$: 2
  [test.eps]
  ```
  ```js
  // epScript 예제 (test.eps)
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
          println("\x07채팅 인식 \x04(id: {})", addr);
          return;
      }
      if (patternAddr) {
          println("\x07패턴 인식 \x04(id: {})", patternAddr);
          return;
      }
      DisplayText("\x05[chatEvent] 설정에 해당되지 않는 채팅");
  }
  ```
- `EUDRegisterObjectToNamespace`로 중복된 이름을 추가했을 때 경고 메시지 추가
- `InitialWireframe`와 `EUDOnStart` 오류 메시지 추가.

## [0.9.8.7] - 2022.12.14
### 버그 수정
- `[chatEvent]` 패턴 인식 길이가 바이트 길이 대신 글자수였던 버그 수정 (Yuuki-Asuna님 제보)
- `[unlimiter]` 컴파일 오류 수정 (파냥이님 제보)

## [0.9.8.6] - 2022.12.13
### 버그 수정
- `EPDCUnitMap.isBlind`의 타입을 `bool`에서 바이트로 수정했습니다. (하늘바라군님 제보)
- `[unlimiter]` 맵에서 작동하지 않던 `EPDCUnitMap.is_dying()`을 컴파일 오류를 내도록 수정했습니다.
  * `[unlimiter]` 작동 후 생성된 유닛은 CSprite가 항상 0이기 때문에, 이미 죽은 유닛인지 죽는 중인지를 CUnit만 봐서는 구별할 수 없습니다. `[unlimiter]` 맵에서 유닛이 죽는 중인지 인식하려면 `EUDLoopNewUnit` 등을 이용해 별도의 메모리 공간에 유닛이 사용 중인지 저장해야 하므로 사소하지 않은 과정이 필요하여 유저 재량에 맡기는 방향으로 수정했습니다.

### 기능 추가
- `IsUnlimiterOn()` 추가: 라이브러리 제작자한테 유용할거에요.
- `InitialWireframe` 추가\
  와이어프레임 초기값을 설정합니다. 32비트와 64비트 스타크래프트를 모두 지원합니다.
  * `InitialWireframe.wireframes(unit, wireframe)`\
    - 유닛의 TranWire.grp, GrpWire.grp, Wirefram.grp 초기값을 설정합니다.
    - 가장 바깥 스코프에서만 사용할 수 있습니다!
  * `InitialWireframe.tranwire(unit, wireframe)`
  * `InitialWireframe.grpwire(unit, wireframe)`
  * `InitialWireframe.wirefram(unit, wireframe)`
- `SetWireframes(unit, wireframe)`, `SetTranWire(unit, wireframe)`, `SetGrpWire(unit, wireframe)`, `SetWirefram(unit, wireframe)` 추가
  * 게임 중에 유닛의 와이어프레임을 수정합니다. 32비트와 64비트 스타크래프트를 모두 지원합니다.
  * `InitialWireframe`을 하나라도 사용해야 작동합니다!

## [0.9.8.5] - 2022.12.06
### 버그 수정
- `Trigger(preserved=False)` 와 `DoActions(preserved=False)` 컴파일 오류 수정 (콤님 제보)

### 기능 개선
- 00.0000 경고 메시지에 널 타일 좌표 출력
- `f_atan2(y, x)` 와 `f_lengthdir(length, angle)` 성능 최적화

### 기능 추가
- 함수 `f_atan2_256(y, x)` 와 `f_lengthdir_256(length, angle)` 추가

## [0.9.8.4] - 2022.11.29
### 변경사항
- `EUDLoopNewUnit`이 더이상 **CUnit +0xA5** `uniquenessIdentifier`를 변경하지 않습니다.
  * `EUDLoopNewUnit`을 사용하는 밀리기반 유즈맵에서 게임 시작하자마자 빠르게 본진 건물을 클릭하고 일꾼 생산을 해도 씹히는 문제가 해결되었습니다.
- `EUDLoopNewUnit`이 여러개 있어도 새 유닛인지 각각 체크합니다. (PR프로덕션님 제보)
  * 이전 동작: 가장 처음에 실행된 `EUDLoopNewUnit`만 이전 프레임과 비교해 새로 생긴 유닛들을 순회하고, 다음에 실행되는 `EUDLoopNewUnit`은 두 루프 사이에 생성된 유닛들을 순회했음
- `UnitGroup.cploop`에서 `cunit.remove();`을 이제 여러번 사용할 수 있습니다.

### 버그 수정
- 변수 객체의 메소드에서 `selftype`을 사용하지 못하는 버그 수정
- armoha/euddraft#34 : 변수 객체의 메소드를 호출할 때 인자 타입이 있으면 다음과 같이 오류나는 버그 수정 `EUDTypedMethod` call raises `EPError: Different number of variables(n) from type declarations(n-1)`

### 기능 개선
- `f_playerexist(player)` 최적화
- 주소가 비어있는 상황에서 읽기 함수 성능 최적화
  * **예제)** 비공유 선택 유닛 인식
  ```js
  const localSelect = EPD(0x6284B8);
  for(var mySelect = localSelect; mySelect < localSelect + 12; mySelect++) {
    // 이렇게 쓰는게 훨씬 빠르고 편해요
    const ptr, epd = cunitepdread_epd(mySelect);
    if (epd == 0) break;

    // 아래는 유닛이 있을 때 더 느립니다. 조건에 변수를 대입해야 돼요.
    if (MemoryEPD(mySelect, Exactly, 0)) break;
    const ptr, epd = cunitepdread_epd(mySelect);
  }
  ```
- `switch`문: 비트마스크가 0일 때 비트마스크 내 범위 체크 생략

## [0.9.8.3] - 2022.11.03
### 변경사항
- `EPDOffsetMap`이 *(이름, 오프셋, 타입)* 쌍의 튜플을 받도록 롤백
- `EPDOffsetMap`의 타입 종류 추가 및 변경
  * 현재 사용 가능한 타입: bool, 1, 2, 4, "CUnit", "CSprite", "Position", "PositionX", "PositionY", `Flingy`, `TrgPlayer`, `TrgUnit`, `UnitOrder`, `Upgrade`, `Tech`

### 기능 개선
- eudplib 0.71.7, cx-freeze 6.13.1, pybind11 업데이트
- epScript `object`(=`EUDStruct`)의 제자리 연산과 비교 연산 최적화
- `EPDCUnitMap`의 수정/비교 성능 최적화
- `f_bitlshift(a, b)`가 a, b 둘 다 상수면 컴파일 시간에 `a << b`를 계산하도록 수정

### 버그 수정
- [epScript] armoha/euddraft#73 : 파이썬 컬렉션 내 변수를 수정하면 새 변수가 덮어쓰는 버그 수정
- `dwread(상수객체)`가 컴파일 시간에 *EPD*를 계산하도록 수정 (Cocoa님 제보)
- `EUDDeque.append(value)`에서 꼬리가 왼쪽으로 돌아올 때 버그 수정
- 일부 `Image` 이름 뒤에 공백 문자 오타 수정
- `UnitGroup`의 `.dying` 블럭 조건에 *hp < 0.5* 대신 *hp == 0*으로 수정
- 일부 최적화가 적용되지 않는 버그 수정 (@Chromowolf 님 제보)

### 기능 추가
- `matplotlib` 라이브러리 추가
- `EUDQueue.clear()`, `EUDDeque.clear()` 추가
- `f_wadd_epd(epd, subp, value)`, `f_wsubtract_epd(epd, subp, value)`, `f_badd_epd(epd, subp, value)`, `f_bsubtract_epd(epd, subp, value)` 추가
  * `f_wadd_epd`와 `f_wsubtract_epd`의 *subp*에는 0, 1, 2만 사용 가능합니다.
- 타입 추가: `Weapon`, `Flingy`, `Sprite`, `Upgrade`, `Tech`, `UnitOrder`, `Icon`, `Portrait`
- 함수 추가: `EncodeWeapon`, `EncodeFlingy`, `EncodeSprite`, `EncodeUpgrade`, `EncodeTech`, `EncodeUnitOrder`, `EncodeIcon`, `EncodePortrait`
- 로케이션 함수에 *action* 키워드 인자 추가: `f_(set/add/dilate)loc(loc, x, y, action=true)`

## [0.9.8.2] - 2022.10.24
- eudplib 0.71.2 업데이트
- `pow(a, b)` 거듭제곱 함수에서 b가 2의 제곱수 일 때 항상 1을 리턴하는 버그 수정 (@Chromowolf 님 기여)
- [epScript] 전역변수에 `%` 연산자 썼을 때 오류 수정 (@Chromowolf 님 제보)
- [epScript] armoha/euddraft#56 수정 : 다른 모듈의 변수를 `=`로 대입했을 때 버그 수정
  * 더 이상 `SetVariables`로 우회하지 않아도 됩니다.

## [0.9.8.1] - 2022.10.21
- eudplib 0.71.1 업데이트
- 연결맵의 무한반복 트리거가 고장나는 버그 수정
- `import numpy` 시 컴파일 오류 수정 (PyroManiac님 제보)
- `EUDDeque(크기)()` 기능 추가\
  데크는 데이터를 왼쪽/오른쪽 양쪽으로 추가하고 꺼낼 수 있는 자료구조입니다.\
  데크가 가득 차면 새 항목이 추가될 때 해당하는 수의 항목이 반대쪽 끝에서 삭제됩니다.
  * `.length` : 현재 개수
  * `.append(값)` : 데크의 오른쪽에 값을 추가합니다.
  * `.pop()` : 데크의 오른쪽에서 값을 꺼냅니다.
  * `.appendleft(값)` : 데크의 왼쪽에 값을 추가합니다.
  * `.popleft()` : 데크의 왼쪽에서 값을 꺼냅니다.
  * `.empty()` : 데크가 비어있으면 참인 조건
  * `foreach` 반복문도 지원합니다.\
    왼쪽에서 오른쪽으로 순회합니다.
    ```js
    // dq3은 크기가 3인 데크
    const dq3 = EUDDeque(3)();
    const ret = EUDCreateVariables(6);

    // 빈 데크를 순회하면 아무 일도 안 일어납니다
    foreach(v : dq3) { ret[0] += v; }

    // 1과 2를 오른쪽에 추가
    dq3.append(1);  // dq3 : (1)
    dq3.append(2);  // dq3 : (1, 2)
    foreach(v : dq3) { ret[1] += v; }  // 3 = 1 + 2

    // 3와 4을 오른쪽에 추가
    dq3.append(3);  // dq3 : (1, 2, 3)
    dq3.append(4);  // dq3 : (2, 3, 4)
    foreach(v : dq3) { ret[2] += v; }  // 9 = 2 + 3 + 4

    // 5를 오른쪽에 추가
    dq3.append(5);  // dq3 : (3, 4, 5)
    foreach(v : dq3) { ret[3] += v; }  // 12 = 3 + 4 + 5

    // 왼쪽에서 3을 꺼냄 (제거하고 리턴)
    const three = dq3.popleft();  // dq3 : (4, 5)
    foreach(v : dq3) { ret[4] += v; }  // 9 = 4 + 5

    // 6과 7을 오른쪽에 추가
    dq3.append(6);  // dq3 : (4, 5, 6)
    dq3.append(7);  // dq3 : (5, 6, 7)
    foreach(v : dq3) { ret[5] += v; }  // 18 = 5 + 6 + 7
    ```
  * 파이썬 `collections.deque(maxlen=크기)`와 동일하게 동작합니다.
- [epScript] armoha/euddraft#86 : 함수 인자 뒤에 쉼표 허용하도록 수정
- [epScript] armoha/euddraft#87 : 이진법 숫자 표현 추가 (@Chromowolf 님 건의)
  * `0b1 == 1`, `0b10 == 2`, `0b11 == 3`
- `EUDQueue.empty()`가 항상 참인 버그 수정
- `EUDQueue.popleft()` 없이 `EUDQueue.append(x)`만 사용할 때 컴파일 오류 수정 (HeartKlass님 제보)

## [0.9.7.12] - 2022.10.19
- eudplib 0.70.18 업데이트
- 전역 리스트 순회에서 `TypeError: iter() returned non-iterator of type 'list'` 오류 수정 (줸님 제보)
- `UnitGroup`: `unit.dying` 블럭에서 현재체력도 체크하게 수정 (HP 0 좀비 유닛 방지)
- `getattr(EPDCUnitMap, attrName)`이 `AttributeError` 내도록 수정
- `EUDLoopUnit2`: 이름에 `unlimiter`가 들어간 플러그인이 없으면 `0x0C CSprite`로 사망 인식하도록 롤백

## [0.9.7.10] - 2022.10.18
- eudplib 0.70.12 업데이트
- `PVariable[변수] -= 값;` 이 EUD미지원 오류내는 버그 수정 (갈대님 제보)
- `PVariable`에서 `<<=`, `>>=`, `^=` 컴파일 오류 수정
- `변수 <<= 변수;`가 연산 결과를 변수에 대입하지 않는 버그 수정

## [0.9.7.9] - 2022.10.17
- `numpy` 추가
- 파이썬 3.10.8 업데이트
- eudplib 0.70.9 업데이트
- [epScript] 아이템 비교/쓰기 버그 수정, epScript에서 최적화하도록 구조 변경 (34464님 제보)
  * 비교 연산자 우선순위 버그 수정
  * `>`, `<`, `&=` 버그 수정
- armoha/euddraft#82 : 연결맵의 `Disabled(PreserveTrigger())` 트리거가 반복 실행되는 버그 수정 (@Chromowolf 님 제보)
- 연결맵 트리거 일부가 반복 실행되지 않는 버그 수정 (ehwl 님 제보)
- `var >> 값` 컴파일 오류 수정 (GGrush님 제보)
- `EUDNot` 버그 수정
- `*=`, `/=`, `<<=`, `>>=`가 LValue 변수를 RValue로 변경하는 버그 수정
- armoha/euddraft#65 : `if (액션)` 오류 메시지 개선

## [0.9.7.3] - 2022.10.09
- `EUDArray`와 `EUDVArray`의 아이템 비교/쓰기 연산 최적화
  * 누락되었던 `EUDVArray` 연산들 추가함
- `ItemProxy` % 연산자 빠진 것 추가 (34464 님 제보)
- [epScript] helper.py 오류 수정 (34464 님 제보)
- `ItemProxy`의 EUDVariable 메소드 관련 오류 수정 (택하이 님 제보)
- 배열 + switch 문 오류 수정 (34464 님, Cocoa 님 제보)

## [0.9.7.0] - 2022.10.08
- `EncodeAIScript` 오류 수정 (@joshow 님 기여)
- 기본 트리거 문서화, 설명 추가 (@zuhanit 님 기여)
- `EPDCUnitMap.isBlind()` 오류 수정 (wdcqc 님 제보)
- `EUDArray`와 `EUDVArray`의 아이템 비교/쓰기 연산 최적화
  * `EUDVArray[상수] -= 변수` 랑 `EUDVArray[변수] &= 값` 등은 아직 작업 필요
- `EUDLoopPlayer(플레이어타입, 포스, 종족)` 오류 메시지 개선
- eudplib 0.70.0 업데이트

## [0.9.6.1] - 2022.07.03
- epScript 업데이트
- `PVariable` cast 버그, 인자 타입 버그 수정함
- `PVariable` 성능 추가 개선
- `UnitGroup.cploop`에 읽기전용 프로퍼티 `epd` 추가\
  `const epd = unit.epd;` 처럼 4트리거 실행해서 `epd`를 변수로 가져올 수 있습니다.
- epScript: stubCode들 분리함\
  `_CGFW` 등 헬퍼 함수들 파일 분리함\
  내부 함수에 쓰이는 파이썬 코드들 덮어쓰지 못하게 개선
- `EUDLoopUnit2` 최적화\
  살아있는 유닛마다 트리거 5개 -> 3개 실행\
  (`UnitGroup` 순회랑 같았다가 더 빨라짐)
- `switch` 문 이진탐색 성능 개선
- `EPDCUnitMap`: `unit.is_dying` 버그 수정
- `EncodeLocation`등 Encode 함수들 UTF-8과 CP949 둘 다 시도하도록 수정
- eudplib 0.69.9 업데이트

## [0.9.6.0] - 2022.06.02
- `f_pow(a, b)` 추가
  a의 b제곱 (a ** b)을 계산합니다.
- `EUDLoopUnit2` 최적화
  살아있는 유닛마다 트리거 9개 -> 5개 실행
  (`UnitGroup` 순회보다 느렸는데 이제 같아짐)
- `soundlooper` 버그 수정
- `EncodeUnit`이 UTF-8과 CP949 둘 다 시도하도록 수정
- epScript에서 `AddCurrentPlayer` 작동 안 하는 버그 수정
- eudplib 0.69.8 업데이트

## [0.9.5.9] - 2022.05.22
- `epdswitch`에 변수 썼을 때 버그 수정
- 스위치 버그 수정
- 스위치에서 단순 비교, 점프 테이블, 이진 탐색 세가지 방법 사용하도록 변경
- `UnitGroup` 추가
  ```js
  // epScript 사용법

  // UnitGroup 선언
  const zerglings = UnitGroup(1000);  // 최대 크기

  // 유닛 등록
  zerglings.add(epd);

  // UnitGroup 루프
  foreach(unit : zerglings.cploop) {
      // 여기 트리거는 **모든** zerglings한테 실행 (살았건 죽었건)
      foreach(dead : unit.dying) {
          // 사망한 zerglings한테 트리거 실행
      }  // <- 사망한 유닛은 dying 블럭 끝에서 UnitGroup에서 제거된다
      // 살아있는 zerglings한테 트리거 실행
  }

  // epScript 예제
  function afterTriggerExec() {
      const zerglings = UnitGroup(1000);
      // 새 저글링이 생성되면 UnitGroup에 등록하기
      foreach(ptr, epd : EUDLoopNewUnit()) {
          const cunit = EPDCUnitMap(epd);
          if (cunit.unitId = $U("Zerg Zergling")) {
              zerglings.add(epd);
          }
      }
      foreach(unit : zerglings.cploop) {
          foreach(dead : unit.dying) {
              // 저글링 죽으면 감염된 테란 소환
              dead.move_cp(0x4C / 4);  // 소유주
              const owner = bread_cp(0, 0);
              dead.move_cp(0x28 / 4);  // 유닛 위치
              const x, y = posread_cp(0);

              setloc("loc", x, y);  // 로케이션 설정
              CreateUnit(1, "Infested Terran", "loc", owner);
          }
      }
  }
  ```
- `EUDQueue` 추가
  ```js
  const queue = EUDQueue(20)();  // 최대 크기
  queue.append(1);
  queue.append(4);
  queue.append(2);
  const a = queue.popleft();
  const b = queue.popleft();
  const c = queue.popleft();
  simpleprint(a, b, c);  // 1, 4, 2
  ```

## [0.9.5.8] - 2022.05.16
- 스위치 문에 상수 허용
- 스위치 문에 비트마스크 추가
- `EPDSwitch` 추가
  ```js
  var x = 1 + 256;
  switch (x, 255) {
    // 스위치 문의 마스크가 255이므로,
    // 변수 x의 256은 무시됩니다.
    case 0:
      // 실행 안 됨
      break;
    case 1:
      // 실행됨
      break;
  }

  const unitId = epd + 0x64/4;
  epdswitch (unitId, 255) {
    // 유닛 종류로 스위치 문 실행하기
    case $U("Terran Marine"):
      // 유닛 종류가 마린이면 실행
      break;
    case $U("Terran Ghost"):
      // 유닛 종류가 고스트면 실행
      break;
  }
  ```
- 스위치 문에 케이스가 없거나 케이스 0만 있을 때 버그 수정 (34464님 제보)

## [0.9.5.6] - 2022.05.15

### 변경 사항
- ```ini
  :: 유닛 이름 스트링 강제 재인코딩 기능 삭제
  :: UTF-8 스트링 맵에서 decodeUnitName : UTF-8 안 써도 됩니다.

  :: 이제 CP949 스트링 맵에서 아래 옵션 추가해야
  :: 문자열 조합에 유닛 이름 사용할 수 있어요.
  :: 구버전 맵 에디터 사용자, 또는 신버전에서 65001 로케일 (UTF-8) 안 쓰는 경우에
  :: StringBuffer나 customText에 유닛 이름 넣고 싶으면 필수입니다.
  [main]
  decodeUnitName : CP949
  ```
- epScript: dll에 `/MT` 옵션 적용
  : vcruntime 포함하여 배포
- pybind11 업데이트

### 기능 개선
- `EUDSwitch` 최적화\
  : 이제 모든 cases를 XOR한 비트들만 읽습니다. 이진 탐색 안 해요.\
  내부적으로 0조건 0액션 트리거의 점프 테이블을 사용합니다.
- 트리거 액션/조건 오류 메시지 개선
  ```py
  DoActions(CreateUnit(1, "Artanis", P8, "Anywhere"))
  # EPError: [경고] "P8"는 location가 아닙니다
  ```
- `StringBuffer.print/printAll`, `DisplayTextAll` 최적화
- 한국어 번역 업데이트

### 기능 추가
- 모든 유저 대상 액션 추가 (관전자 포함)\
  : `DisplayTextAll(text)`, `PlayWAVAll(soundpath)`,
  `MinimapPingAll(location)`, `CenterViewAll(location)`,
  `SetMissionObjectivesAll(text)`, `TalkingPortraitAll(unit, time)`
- 간단한 마스크 쓰기 함수 추가\
  : `maskwrite_epd(epd, value, mask)`, `maskwrite_cp(cpoffset, value, mask)`
- CUnit 및 CSprite 읽기 함수 추가
  - `f_epdcunitread_epd`, `f_epdcunitread_cp`\
    : CUnit의 epd를 읽습니다.
  - `f_spriteread_epd`, `f_spriteread_cp`\
    : CSprite의 ptr을 읽습니다.
  - `f_spriteepdread_epd`, `f_spriteepdread_cp`
    : CSprite의 ptr과 epd를 동시에 읽습니다.
  - `f_epdspriteread_epd`, `f_epdspriteread_cp`
    : CSprite의 epd를 읽습니다.
- `EPDOffsetMap`, `EPDCUnitMap` 기능 추가
  - `"cunit"` 타입은 `ptr, epd` 쌍을 리턴합니다.
  - `"sprite"` 타입은 `epd` 를 리턴합니다.
  - `buildQueue` 인덱싱이 1부터 5까지로 변경됐습니다.
  - `EPDCUnitMap` 메소드 추가
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
  - `EPDCUnitMap` 항목 추가\
    : [각 항목 별 타입, 크기, 오프셋 참고용 링크](https://github.com/armoha/eudplib/blob/b94a3ff0fe2a90d189f92b9b24e33fa700efa583/eudplib/eudlib/epdoffsetmap.py#L132-L327)
    ```
    prev, next, hp, hitPoints, sprite, moveTargetXY, moveTargetPosition, moveTargetX, moveTargetY, moveTarget, moveTargetUnit, nextMovementWaypoint, nextTargetWaypoint, movementFlags, direction, currentDirection1, flingyTurnRadius, velocityDirection1, flingyID, _unknown_0x026, flingyMovementType, pos, position, posX, positionX, posY, positionY, haltX, haltY, topSpeed, flingyTopSpeed, current_speed1, current_speed2, current_speedX, current_speedY, flingyAcceleration, currentDirection2, velocityDirection2, owner, playerID, order, orderID, orderState, orderSignal, orderUnitType, cooldown, orderTimer, mainOrderTimer, gCooldown, groundWeaponCooldown, aCooldown, airWeaponCooldown, spellCooldown, orderTargetXY, orderTargetPosition, orderTargetX, orderTargetY, orderTarget, orderTargetUnit, shield, shieldPoints, unitId, unitType, previousPlayerUnit, nextPlayerUnit, subUnit, orderQHead, orderQueueHead, orderQTail, orderQueueTail, autoTargetUnit, connectedUnit, orderQCount, orderQueueCount, orderQTimer, orderQueueTimer, _unknown_0x086, attackNotifyTimer, previousUnitType, lastEventTimer, lastEventColor, _unused_0x08C, rankIncrease, killCount, lastAttackingPlayer, secondaryOrderTimer, AIActionFlag, userActionFlags, currentButtonSet, isCloaked, movementState, buildQ12, buildQ1, buildQueue1, buildQ2, buildQueue2, buildQ34, buildQ3, buildQueue3, buildQ4, buildQueue4, buildQ5, buildQueue5, energy, buildQueueSlot, uniquenessIdentifier, secondaryOrder, secondaryOrderID, buildingOverlayState, hpGain, shieldGain, remainingBuildTime, previousHP, loadedUnitIndex0, loadedUnitIndex1, loadedUnitIndex2, loadedUnitIndex3, loadedUnitIndex4, loadedUnitIndex5, loadedUnitIndex6, loadedUnitIndex7, mineCount, spiderMineCount, pInHanger, pOutHanger, inHangerCount, outHangerCount, parent, prevFighter, nextFighter, inHanger, _unknown_00, _unknown_04, flagSpawnFrame, addon, addonBuildType, upgradeResearchTime, techType, upgradeType, larvaTimer, landingTimer, creepTimer, upgradeLevel, __E, pPowerup, targetResourcePosition, targetResourceX, targetResourceY, targetResourceUnit, repairResourceLossTimer, isCarryingSomething, resourceCarryCount, resourceCount, resourceIscript, gatherQueueCount, nextGatherer, resourceGroup, resourceBelongsToAI, exit, nydusExit, nukeDot, pPowerTemplate, pNuke, bReady, harvestValueLU, harvestValueL, harvestValueU, harvestValueRB, harvestValueR, harvestValueB, originXY, origin, originX, originY, harvestTarget, prevHarvestUnit, nextHarvestUnit, statusFlags, resourceType, wireframeRandomizer, secondaryOrderState, recentOrderTimer, visibilityStatus, secondaryOrderPosition, secondaryOrderX, secondaryOrderY, currentBuildUnit, previousBurrowedUnit, nextBurrowedUnit, rallyXY, rallyPosition, rallyX, rallyY, rallyUnit, prevPsiProvider, nextPsiProvider, path, pathingCollisionInterval, pathingFlags, _unused_0x106, isBeingHealed, contourBoundsLU, contourBoundsL, contourBoundsU, contourBoundsRB, contourBoundsR, contourBoundsB, removeTimer, matrixDamage, defenseMatrixDamage, matrixTimer, defenseMatrixTimer, stimTimer, ensnareTimer, lockdownTimer, irradiateTimer, stasisTimer, plagueTimer, stormTimer, irradiatedBy, irradiatePlayerID, parasiteFlags, cycleCounter, isBlind, maelstromTimer, _unused_0x125, acidSporeCount, acidSporeTime0, acidSporeTime1, acidSporeTime2, acidSporeTime3, acidSporeTime4, acidSporeTime5, acidSporeTime6, acidSporeTime7, acidSporeTime8, bulletBehaviour3by3AttackSequence, pAI, airStrength, groundStrength, _repulseUnknown, repulseAngle, bRepMtxXY, bRepMtxX, bRepMtxY
    ```

## [0.9.5.4] - 2022.05.05
- `EUDVArray`에 키워드 인자 `dest`, `nextptr` 추가
- `nextptr`의 `ConstExpr` 체크 추가
- `SeqCompute`의 nonConstActions에서 `None` 허용
- `EUDVarBuffer`에 메모리 중첩 추가
- 커스텀 변수 사용이 너무 적은 맵에서 생기는 버그 수정 (Ninfia님 제보)\
  eudplib 함수를 적게 불러오는 CTrigAsm 맵에서 발생했습니다.

## [0.9.5.3] - 2022.04.17
- 커스텀 변수 버퍼 버그 수정
- 함수 `ShufflePayload(mode)` 추가\
  오브젝트 수집 단계 후 섞는 단계를 끄거나 킵니다. (기본값: 켬)
- **[main]**\
`shufflePayload : bool` 옵션 추가.

## [0.9.5.2] - 2022.04.14
- (armoha/euddraft#55) 설정 파일 오류 메시지 개선 ([**@zuhanit**](https://github.com/zuhanit) 기여)
![better config error message](https://user-images.githubusercontent.com/36349353/163330102-91b83907-4d6d-4484-a787-22231d1d62ca.png)
- (armoha/eudplib#5) 컴파일 속도 개선: EUD 변수 트리거 생성 개선
- 키워드 인자 `nextptr` 추가: `EUDVariable`, `EUDXVariable`
- (armoha/euddraft#37) `[main] objFieldN : x` 버그 수정
- `RawTrigger`에 키워드 인자 `currentAction` 추가
- eudplib 0.67.3 업데이트

## [0.9.5.1] - 2022.03.29
- `[chatEvent]` 버그 수정
- EUD 변수 계산에서 임시 변수를 필요할 때만 추가하도록 최적화
- `EUDVariable.IsRValue()` 추가
- `EUDLightVariable`에 `>`, `<` 부등호 사용 가능
- `[MSQC]` 조건에서 `EUDLightBool` 사용 가능

## [0.9.5.0] - 2022.03.26

### 변경 사항
- 64비트 업데이트
- `Python 3.10.2`, `cx_Freeze 6.10`, `pybind11` 업데이트
- `StormLib`, `eudplib 0.69.1` 업데이트
- `EUDVariable`를 비트마스크 `0xFFFFFFFF`인 EUDX 트리거로 변경
- `[chatEvent]` `__encoding__` 옵션 삭제. 넣는 경우 무시됩니다

### 기능 개선
- `EUDVariable`의 기본 연산들 비트마스크 활용 성능 최적화\
강좌글: https://blog.naver.com/kein0011/222649764825 \
구현 참고: https://cafe.naver.com/edac/110286
- `epScript`: `var` 초기화 때 RValue 변수를 추가로 복사하지 않도록 개선
  ```js
  // 이제 두 경우 트리거 실행 수 똑같음
  const a = dwread_epd(0);
  var b = dwread_epd(0);
  ```

### 버그 수정
- (#51) 지역 변수를 한 줄에 여러 개 선언할 때 생기는 버그 수정
- EUD Editor 3 컴파일에서 .eds 컴파일 때 `UnicodeEncodeError` 수정\
버그 발생 예시: `[chatEvent]`에 일본어 곡명 작성 https://cafe.naver.com/edac/109969
- `[MSQC]` `xy, src1, src2 : dst1, dst2` 버그 수정 https://cafe.naver.com/edac/109844
- `[MSQC]` 마우스 로케이션 이름 출력 버그 수정

### 기능 추가
- `[chatEvent]` SipHash 기능 추가\
맵 파일에 인식할 채팅 원문을 저장하지 않고, 채팅과 해시값을 비교합니다.\
https://cafe.naver.com/edac/110699
- 함수 `f_strlen_epd(epd, subp=0)` 선택인자 `subp` 추가
- 모든 변수 타입 (EUDLightVariable, EUDVariable, ...) 에 제자리(in-place) 연산 추가\
`&=`, `|=`, `^=`, `<<=`, `>>=`

## [0.9.4.8] - 2022.01.09
- 페이드아웃의 마지막 색이 뒷 내용을 덮어쓰는 색깔일 때 (0: null 문자, 5:  회색, 0x14: 투명색)\
  페이드아웃 텍스트 효과가 끝나도 마지막 색을 맨 앞에 넣도록 수정했습니다.

## [0.9.4.7] - 2022.01.02
- eudplib 0.67.3 업데이트
- 로케이션 프로텍션 버그 수정

## [0.9.4.6] - 2021.12.28
- 로케이션 단락 프로텍션 추가
- `EUDByteWriter.writebyte(상수)` 성능 개선
- `변수 * 변수` 성능 개선
- `pybind11` 업데이트
- `EPDCUnitMap` 좌표 관련 멤버 추가: `originX`, `originY`, `secondaryOrderX`, `secondaryOrderY`, `rallyX`, `rallyY`
  그래도 `EPDCUnitMap.getpos("member")` 를 쓰는 걸 권장합니다.

## [0.9.4.5] - 2021.12.23
- `freezeMpq.pyd` 불러오기 관련 버그 수정
- `StormLib` 업데이트
- `MPQ.Extract(fname)` 유니코드 파일명도 추출 시도하도록 변경
- ~~`orphan condition` 오류 메시지 개선~~
- eudplib 함수 성능 개선
  * 모든 EPD 읽기 함수: 트리거 1개, SetDeaths 3개 감소. 매개변수 안 거치고 CurrentPlayer (0x6509B0) 에 바로 대입
  (`dwread_epd`, `cunitread_epd`, `maskread_epd`, `bread_epd`, `posread_epd`, ...)
  * `cunitread_epd`: 트리거 2개, SetDeaths 5개 감소. 비트마스크 `0x3FFFF0`로 변경, 초기값에 `0x40008` 추가
  * `setloc_epd(loc, epd)`: 트리거 5개, SetDeaths 13개 감소. 내부에서 `posread_cp` 사용, x, y 반환값 로케 설정 액션에 바로 대입

## [0.9.4.4] - 2021.12.09
- `SCArchive` 관련 수정

## [0.9.4.3] - 2021.11.24
- `IsPName(플레이어, "인식할 닉네임")` 조건에서 닉네임 길이가 `(4의 배수+1)`일 때 이름이 끝났는지 체크하지 않는 버그 수정

## [0.9.4.2] - 2021.11.21
- [freeze] 비한국어 윈도우에서 파일명에 비ASCII 문자 있을 때 오류 수정

## [0.9.4.1] - 2021.11.17
- `StringBuffer.DisplayAt`, `StringBuffer.printAt`에서 `line`이 변수일 때 잘못 출력되는 버그 수정

## [0.9.4.0] - 2021.11.16
- 랜덤 함수들, `DisplayTextAt`, `StringBuffer.DisplayAt`, `f_repmovsd_epd` 최적화
- `f_printAll`, `f_printAllAt`, `FixedText` 추가
  - **f_printAll(format_string, \*args)**\
    모든 플레이어한테 텍스트를 출력합니다.
  - **f_printAllAt(line, format_string, \*args)**\
    모든 플레이어한테 해당 줄에 텍스트를 출력합니다.
  - **FixedText(끝에 실행할 액션(옵션))**\
    `FixedText`가 시작할 때 텍스트 포인터를 저장하고, 끝나면 복구합니다.\
    `f_gettextptr` 안 쓰고 간편하게 여러 텍스트를 채팅 보존 출력할 때 씁니다.
    ```py
    # 예시: FixedText 안 쓰고 만든 DisplayTextAt
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

    # FixedText로 만든 DisplayTextAt
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
- Cython 업데이트
- `EUDVariable`, `EUDXVariable`의 초기 주소, 수정자(modifier)
- `EUDFullFunc` 추가
    ```py
    # 예시: EUDFullFunc로 만든 DisplayTextAt
    # 매개변수 line을 채팅 포인터에 더하도록 초기 주소, 수정자 설정
    # 매개변수 text가 DisplayText 액션을 수정하도록 초기 주소, 수정자 설정
    _display_text = DisplayText(0)
    @EUDFullFunc(
        [
            # 매개변수 line의 초기 주소, 수정자, 값, 비트마스크
            (EPD(0x640B58), Add, 0, None),
            # 매개변수 text의 초기 주소, 수정자, 값, 비트마스크
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

    # f_repmovsd_epd 최적화 예시
    _cpmoda = Forward()
    @EUDFullFunc(
        # dstepdp가 _cpmoda한테 더하도록 초기 설정
        # srcepdp가 CurrentPlayer를 수정하도록 초기 설정
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
- `EUDVariable` `<<=`, `>>=` 사용 가능하게 수정
  `상수 << 변수`, `상수 >> 변수` 가능하게 수정
- `ConstExpr` 끼리 비교 추가 (`baseobj`랑 `rlocmode`가 같아야 함.)
  ```py
  from eudplib import *

  array = EUDArray(4)
  a, b = array + 4, array + 8
  if a < b:  # True
      pass
  ```

## [0.9.3.8] - 2021.10.30
- `f_eprintAll(format_string, *args)` 추가
  모든 플레이어한테 에러줄에 출력합니다.

## [0.9.3.6] - 2021.09.10
- eudplib 0.66.3 업데이트
- **[epScript]** 상대 경로 `import` 기능 추가
    예시)
    ```js
    /* c.py
     * folder
     * ├ b.eps
     * └ inner
     *　└ a.eps
     * src
     * └ main.eps (플러그인 파일 [main.eps])
     ***/

    // `src/main.eps` 에서 `c.py` 불러오기
    import ..c;
    // `src/main.eps` 에서 `folder/b.eps` 불러오기
    import ..folder.b;
    // `src/main.eps` 에서 `folder/inner/a.eps` 불러오기
    import ..folder.inner.a;

    // `folder/b.eps` 에서 `folder/inner/a.eps` 불러오기
    import .inner.a;

    // `folder/inner/a.eps` 에서 `folder/b.eps` 불러오기
    import ..b;
    // `folder/inner/a.eps` 에서 `c.py` 불러오기
    import ...c;
    ```
- `StringBuffer.fadeIn`/`fadeOut`에 `tag`가 없을 때 이전에 출력한 텍스트를 안 지우는 버그 수정.
- `StringBuffer.fadeIn`/`fadeOut`에서 `line=10` 또는 `line=-1` 일 때 기존 채팅을 지우지 않고 위로 밀도록 변경.
- `StringBuffer.tagprint(format_string, *args, line, tag)` 추가 \
    태그 기능이 있는 print 함수입니다. `TextFX_Remove(tag)` 로 화면에 있는 이전 메시지를 지우는 식으로 활용할 수 있습니다.

## [0.9.3.4] - 2021.08.31
- `once` 조건문 추가. (eudplib에서는 EUDExecuteOnce()(조건) 입니다)
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
- `once`에 조건 없을 때 트리거 2개 -> 1개 사용하게 개선
- `pybind11` 업데이트

## [0.9.3.3] - 2021.08.25
- eudplib 0.66.1
  * (베타) **epScript** `if`문에서 부작용 없는 기본 조건의 `&&` 최적화 (`EUDSCAnd`)
  * `Condition.Negate()` 추가
  * `EUDLightBool()` 추가
- `[MSQC]` 스트링 제한 넘었을 때 버그 수정
- 플러그인 설정 중복됐을 때 오류 메시지 개선
  * 오류 메시지 예시
  ```cs
  [chatEvent]
  서울여자 : 20200721
  서울여자 : 13

  -> Duplicate key 서울여자 in [chatEvent]
  [Line 120] 서울여자 : 20200721
  [Line 121] 서울여자 : 13
  ```
- Python 3.8.10, cx_Freeze 6.8b3으로 업데이트
  (Python 3.9는 윈도우 7 지원 안 해서 당분간 업데이트 안 할 예정)

## [0.9.2.0] - 2021.04.15
- eudplib 0.65.1
  * StormLib 최신 버전 유니코드 빌드로 업데이트
  * `$T`가 `CP949`로 표현할 수 없는 문자열에서 유니코드 사용하도록 수정.
    관련 질문글: https://cafe.naver.com/edac/99614
- [cammove] 로케이션 번호 오류 수정

## [0.9.1.5] - 2021.03.31
- 포맷 출력 함수의 `{:s}`가 정렬되지 않은 상수 스트링도 `epd2s`로 변환한 버그 수정.
- [MSQC] val / xy 문법으로 0을 전달해도 리턴값이 -1인 버그 수정.

## [0.9.1.4] - 2021.03.17
- TBL 수정 함수에 인코딩 지정 인자 추가 (기본값: "CP949")
`f_settbl(tbl, offset, *args, encoding="cp949")`
`f_settblf2(tbl, offset, format_string, *args, encoding="cp949")`
문자열 타입이 사용할 인코딩을 지정합니다.
UTF-8 인코딩으로 지정하면 "\u2009\0"을 문자열 끝에 추가합니다.
(부분 수정 함수 `f_settbl2`, `f_settblf2`에서는 추가하지 않습니다.)
`bytes`나 `Db` 등 그 외 타입도 같은 인코딩을 쓰는지 검증하셔야합니다.

## [0.9.1.3] - 2021.03.07
- `(Set)Memory(X)` 주소 4의 배수 아닌 경우 컴파일 에러 -> 제외
- `TrgTBL` 오타 수정
- **[unlimiter]** 사용맵 `EUDLoopUnit2` 미작동 문제 수정
- epScript `object` (`EUDStruct`) 필드 개수 지정 옵션 실험적으로 추가
```cs
[main]
...
objFieldN: 16
```

## [0.9.0.9] - 2021.01.28
- 프로텍션 추가
- `EPDCUnitMap` 빠진 내용 추가
- 유닛 이름 디코딩 지정 옵션 추가
```cs
[main]
...
decodeUnitName : utf-8
```

## [0.9.0.8] - 2020.12.11
- MPQ에 크기가 음수인 유효하지 않은 파일 있을 때 다음과 같은 컴파일 오류 나던 것 수정.
```py
    File "C:\Py\lib\ctypes_init_.py", line 62, in create_string_buffer
    ValueError: Array length must be >= 0, not -1
```

## [0.9.0.7] - 2020.12.09
- 마지막 스트링에 null terminator 없는 경우 생기는 오류 수정.

## [0.9.0.6] - 2020.11.21
- `cx_Freeze` 버전업
- `IsPName` 버그 수정.
- `(Set)Memory(X)` 주소 4의 배수 아닌 경우 오류나게 수정.
- **[chatEvent]** 4의 배수 아닌 주소 넣어서 주소 중복 체크를 무시하는 버그 수정.

## [0.9.0.4] - 2020.10.08
- `IsPName(player, name)` 조건 추가
  * `player`: 이름 인식할 플레이어. 변수 또는 `Player1` ~ `Player8` 또는 `CurrentPlayer`
  * `name`: 인식할 이름. `"문자열"` 또는 `Db`.

## [0.9.0.3] - 2020.09.30
- `(0000.00)` null 지형이 `(0000.01)` null 로 안 바뀌었던 버그 수정.

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

### 버그 수정

- `Disabled(컨디션/액션)`이 컴파일 오류나는 버그 수정.
- StringBuffer를 선언한 이후에 스트링을 추가하면, StringBuffer 주소가 4의 배수를 벗어나는 버그 수정.
  - 스트링 공간 절약 기능을 [0.8.4.5]에서 추가했는데 이 부분은 생각 못 했네요...


## [0.8.4.6] - 2019.03.24

### 버그 수정

- (트리거왕님 기여) `f_wwrite_epd(epd, subp, word)` 버그 수정:
    - subp가 상수일 때 f_bwrite_epd처럼 작동하는 버그. 12월 27일에 추가된 내용인데 이제 발견됐네요 ㅠㅠ

### 기능 추가

- Cython 적용해서 컴파일 시간이 개선됐습니다.
- (트리거왕님 기여) 패스워드 암호화 / 복호화 기반 트리거 추가.


## [0.8.4.5] - 2019.03.24

### 버그 수정

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
