# Project II Beginner Guide - Autonomous APT Agent Lab

這份筆記用「第一次做資安實務專案的大學生」角度，拆解 Project II 的
Autonomous APT Agent Lab。它的用途是先建立系統理解，再進入 exploit
細節。

## Lab Boundary

這是一個 bounded autonomous agent course lab。所有觀察、payload、triage、
state update、backdoor success evidence 都屬於課堂 sandbox、指定 container、
指定 shared volume 與指定 grading flow。

## Core Framing

你現在看到的是一個結合 exploit、feedback loop 與自動化決策的小型系統。

它其實是一個小型的「攻防自動化系統」。

這個 lab 的核心，是讓你理解：

1. 一個漏洞利用如何形成
2. 系統如何分析目標 binary
3. 如何自動化攻擊流程
4. 如何根據失敗結果調整策略
5. container、shared volume、state machine 如何協同工作
6. 為什麼現代資安已經開始走向 agentic workflow

## 1. 先建立系統視角

很多初學者一看到：

- backdoor
- exploit
- coredump
- gadget
- ELF

就會覺得內容爆炸。

先把整個系統當成：

> 一個會自己觀察、嘗試、失敗、修正的程式代理人，也就是 agent。

這樣會清楚很多。

這個 lab 的真正核心是：

> 自動化決策流程。

這跟現在 AI agent 的思維其實很像。

## 2. 整個系統架構

lab 有兩個 container：

```text
EC (External Container)
IC (Internal Container)
```

可以想成：

```text
EC = 攻擊者
IC = 被攻擊的系統
```

這是課堂 sandbox，所有操作都在指定實驗環境內完成。

README 特別強調 bounded autonomous agent。這代表 agent 只能在實驗環境內
運作。這是非常重要的資安倫理概念。

## 3. 整個攻擊流程在做什麼

### Step 1

EC container 執行：

```text
/exploit
```

這是攻擊 agent 的主程式。它會：

1. 分析 target binary
2. 推測漏洞
3. 產生 payload
4. 寫入 shared volume

### Step 2

EC 修改：

```text
/shared/config.data
```

這是攻擊輸入。可以把它想成：

```text
惡意輸入資料
```

IC 之後會讀這個檔案。

### Step 3

EC 建立：

```text
/shared/exploit_done
```

這是訊號，意思是：

```text
我 payload 準備好了
```

### Step 4

IC container 偵測到 `exploit_done`，然後執行：

```text
blogic
```

這是 vulnerable binary。它會讀：

```text
/shared/config.data
```

如果 payload 成功：

```text
/backdoor 被執行
```

grader 就判定成功。

## 4. Shared Volume 是什麼

這是 container 很重要的概念。

EC 跟 IC 是兩台隔離的小 Linux。Normally，它們互相看不到檔案。

但：

```text
/shared
```

是共同資料夾。所以：

```text
EC 寫檔
IC 讀檔
```

這就形成 communication channel。

## 5. 專案中的重要檔案

### README.md

最重要。它描述：

- 系統架構
- flow
- state machine
- adaptive exploit
- triage 機制

很多學生會直接跳過 README。在業界，README 常常就是 architecture spec。

### analyze_target.py

這是 target analyzer。它會分析 binary，這是 reverse engineering 的基礎。

它分析的東西包括：

```text
ELF 架構
PIE
NX
symbol
strings
gadgets
```

## 6. 什麼是 ELF

ELF = Executable and Linkable Format。

這是 Linux 執行檔格式，就像：

```text
Windows -> PE
Linux -> ELF
```

所以：

```text
/shared/blogic
```

其實是一個 Linux binary。

## 7. 什麼是 PIE

PIE = Position Independent Executable。

意思是程式每次執行時：

```text
記憶體位址會變
```

這是提高 exploit 難度的保護機制，因為攻擊者需要先處理 address 變動。

## 8. 什麼是 NX

NX = Non-Executable。

意思是 stack 維持不可執行的資料區。這也是現代 OS 防護。

所以現代 exploit 常常會使用：

```text
ROP
ret2libc
control flow hijacking
```

這和傳統 shellcode 路線不同。

## 9. 什麼是 Gadget

README 提到：

```text
ret gadget
```

這是 ROP 的核心。

ROP = Return Oriented Programming。

概念是：

```text
不自己寫機器碼
而是拼接現有程式片段
```

這些小片段就叫 gadget。

例如：

```assembly
pop rdi
ret
```

這就是經典 gadget。

## 10. 為什麼需要 Adaptive Probing

因為你不知道 overflow offset。

例如 buffer 大小可能是：

```text
64 bytes
72 bytes
80 bytes
```

所以 agent 要：

```text
試
觀察
調整
再試
```

這就是 adaptive exploit，也是整個 lab 最有價值的地方。

## 11. Triage 是什麼

很多學生會誤會。triage 不只是醫療分流。

在資安：

```text
triage = 快速分析與分類結果
```

專案中的 `/triage` 會分析：

```text
上一次 exploit 是否失敗
是否產生 coredump
目前 offset 狀態
下一步策略
```

這其實很像 AI agent 的 reflection loop。

## 12. state.json 為什麼重要

這是 agent memory。

例如：

```json
{
  "round": 3,
  "offset": 72,
  "status": "failed"
}
```

這代表 agent 有「狀態」，可以延續上一輪觀察。

這是 autonomous system 的核心概念。

## 13. 現在真正應該先學什麼

先建立系統理解，再進入 ROP chain、shellcode、advanced pwning。

### 第一層：系統理解

至少要搞懂：

- container 是什麼
- shared volume 是什麼
- binary 是什麼
- process 是什麼
- payload 是什麼
- state machine 是什麼

### 第二層：Linux 基礎

常用指令：

```bash
ls
cat
file
strings
chmod
ps
```

### 第三層：Binary 基礎

開始知道：

```text
stack
heap
register
return address
```

### 第四層：Exploit 思維

核心其實只有一句：

```text
如何控制程式流程
```

## 14. 你現在可以做的第一件事

### Task 1

閱讀：

```text
README.md
```

然後自己畫：

```text
EC -> shared -> IC
```

資料流圖。

### Task 2

進 container，看：

```bash
file blogic
strings blogic
```

觀察輸出。

### Task 3

閱讀：

```text
analyze_target.py
```

並回答：

```text
它如何判斷 target 特性？
```

### Task 4

閱讀：

```text
state.json
```

理解：

```text
agent 如何記住過去狀態
```

## 15. 這個 Lab 真正能學到什麼

這個 lab 同時結合：

```text
資安
Linux
Docker
Binary analysis
Autonomous agent
State machine
Adaptive systems
Failure recovery
```

這已經具備小型 autonomous system 的結構。

## 16. 下一步建議學習順序

### Phase 1

理解整體 flow，建立 exploit 細節前的系統地圖。

### Phase 2

學 Linux process 與 memory。

### Phase 3

學 ELF 與 binary analysis。

工具：

```text
file
strings
readelf
objdump
gdb
```

### Phase 4

學 stack overflow，先從：

```c
gets()
strcpy()
```

開始。

### Phase 5

再進入：

```text
ROP
ASLR
NX bypass
```

## 17. 目前最容易犯的錯誤

### 1. 直接複製 exploit

結果完全不知道自己在做什麼。

### 2. 只想成功 exploit

卻不知道：

```text
為什麼成功
```

### 3. 把資安當 magic

其實本質是：

```text
系統行為控制
```

## 18. 老師會希望你真正學會的事

核心期待是：

```text
你能理解系統如何運作
```

真正厲害的資安人員，是能把系統看清楚的人：

```text
最懂系統的人
```

因為理解系統的人才能：

- 找漏洞
- 修漏洞
- 設計防禦
- 建立架構
- 做 agent
- 做 AI security
- 做安全產品

這才是長期價值。

## 19. 下一次應該做什麼

下一步建議：

1. 逐步閱讀 `analyze_target.py`
2. 理解 Dockerfile
3. 觀察 `/exploit` 做了什麼
4. 畫完整 state machine
5. 最後才進入 exploit payload

這樣會真正看懂整個專案。
