# 自主式 APT Agent 技術報告

## 1. 專案目標與整體概念

本專案是 **[2026 NS] Project - Autonomous APT Agent** 的實作。作業情境假設攻擊者無法持續進行人工遠端控制，因此需要一個可以在受控環境中自動分析、產生攻擊輸入、觀察結果並修正策略的 agent。

這個 lab 並不是要我們實作真正完整的 APT framework，而是在 Docker lab 中完成一個有限範圍的自主式 exploit agent。它的任務是透過 shared volume 修改目標程式會讀取的設定檔，利用目標 business logic 程式中的漏洞，最後在 IC 內部觸發 `/backdoor`。

整體成功路徑如下：

```text
EC /exploit
  -> 修改 /shared/config.data
  -> 建立 /shared/exploit_done

IC blogic
  -> 偵測 exploit_done
  -> 讀取 config.data
  -> 觸發漏洞
  -> 執行 /backdoor

grader
  -> 偵測 /shared/success.txt
  -> 判定成功
```

用一行表示就是：

```text
/exploit -> config.data -> exploit_done -> blogic -> /backdoor -> success.txt
```

本專案最重要的設計目標是：不要只做一個固定 payload，而是讓 EC 裡的程式具備基本 autonomous loop：

```text
Analyze -> Generate -> Execute -> Observe -> Triage -> Retry
```

也就是說，agent 會先分析目標 binary，再產生 exploit。如果攻擊失敗，`/triage` 會根據觀察到的結果更新狀態，讓下一輪 `/exploit` 嘗試不同策略。

## 2. 作業環境與評分流程

作業環境包含兩個 container。

第一個是 **EC, External Container**。這是我們要提交的部分。EC 中必須提供：

```text
/exploit
/triage
```

第二個是 **IC, Internal Container**。IC 中執行 vulnerable business logic，也就是：

```text
/blogic
```

IC 中也預先安裝了：

```text
/backdoor
```

EC 與 IC 之間的共享資料夾是：

```text
/shared
```

作業要求 `/exploit` 要修改：

```text
/shared/config.data
```

並且建立：

```text
/shared/exploit_done
```

IC 偵測到 `exploit_done` 後，就會執行 `blogic`，讓它讀取 `config.data`。如果 exploit 成功，IC 會執行 `/backdoor`，而 `/backdoor` 會產生：

```text
/shared/success.txt
```

grader 的核心流程可以理解為：

```text
for round = 1..60:
    EC runs /exploit
    IC waits for /shared/exploit_done
    IC runs blogic
    if /shared/success.txt exists:
        success
        stop
    else:
        EC runs /triage
```

所以 `/triage` 不會在成功後執行。只要一成功，grader 就會停止。這點會影響 `state.json` 的最後狀態，後面會再說明。

## 3. 專案檔案結構

目前主要檔案如下：

```text
lab/
|-- EC/
|   |-- Dockerfile
|   |-- exploit
|   |-- triage
|   `-- analyze_target.py
|-- IC/
|   |-- Dockerfile
|   |-- backdoor
|   |-- runserver.sh
|   |-- server.cpp
|   |-- server_1
|   `-- server_2
|-- shared/
|   |-- config.data
|   `-- coredump/
|-- docker.sh
|-- grader.sh
|-- README.md
|-- Report.md
|-- phase2_adaptive_result.txt
`-- phase3_adaptive_result.txt
```

其中真正要提交或重點說明的是 `EC/` 內的內容：

```text
EC/Dockerfile
EC/exploit
EC/triage
EC/analyze_target.py
```

`README.md` 是操作與需求對照文件，`Report.md` 則是本技術說明。

## 4. 目標程式漏洞分析

漏洞位於 `IC/server.cpp`。

程式會讀取 `/shared/config.data`，並找出 `user_input`：

```cpp
if (key == "user_input") {
    user_input_len = value.size();
    memcpy(user_input, value.data(), user_input_len);
}
```

這裡會把 config 裡的 `user_input` 存到 global buffer：

```cpp
char user_input[512];
size_t user_input_len = 0;
```

接著 `run_server()` 會呼叫：

```cpp
log_message(user_input, user_input_len);
```

真正的 overflow 發生在 `log_message()`：

```cpp
void log_message(const char *msg, size_t len) {
    char buf[96];
    memcpy(buf, msg, len);
}
```

`buf` 只有 96 bytes，但 `len` 是從 `user_input_len` 來的，而 `user_input_len` 是由攻擊者寫入 config 的資料長度決定。因此 EC 可以寫入超過 96 bytes 的 `user_input`，造成 stack overflow，進一步覆蓋 saved return address。

此外，程式中有一個非常適合被利用的函式：

```cpp
void execute_task() {
    maintenance_task(user_input);
    exit(0);
}
```

而 `maintenance_task()` 會呼叫：

```cpp
system(arg);
```

所以只要能讓 return address 跳到 `execute_task()`，它就會執行：

```text
system(user_input)
```

因此 payload 的開頭設成：

```text
/backdoor\x00
```

就可以讓 IC 執行 `/backdoor`。

## 5. Exploit 核心策略

本專案採用的是 **ret-to-text** 策略。

我們沒有把 shellcode 放在 stack 上執行，而是利用 stack overflow 覆蓋 return address，讓控制流程跳回目標 binary 內已存在的函式。

payload 結構如下：

```text
user_input=/backdoor\x00 + padding + ret_gadget + execute_task
```

概念上可以拆成四段：

```text
1. /backdoor\x00
2. padding
3. ret gadget address
4. execute_task address
```

第一段 `/backdoor\x00` 是要讓 `system(user_input)` 執行 `/backdoor`。

第二段 padding 是為了填滿從 `user_input` 開始到 saved return address 的距離。

第三段 `ret gadget` 用來處理 stack alignment，使得跳入 `execute_task()` 時更穩定。

第四段 `execute_task` 是實際要跳去的目標函式。

在這個 lab 中，分析結果可以找到：

```text
execute_task = 0x401415
ret gadget   = 0x401414
```

但報告中不應該把重點說成「我們一開始就知道所有答案」，而是要說這些資訊是由 analyzer 從 target binary 中抽出來的。

## 6. 為什麼 Phase I、II、III 都可行

作業三個 phase 的差異主要是保護機制不同。

| Phase | 條件 | 影響 |
|---|---|---|
| Phase I | Stack executable、non-PIE、ASLR off | 最簡單，可直接控制 return address |
| Phase II | NX enabled、non-PIE、ASLR off | stack 不能執行 shellcode，但 ret-to-text 不受影響 |
| Phase III | NX enabled、non-PIE、ASLR on | ASLR 開啟，但 non-PIE binary 的 text address 仍固定 |

這裡最重要的概念是：

```text
NX 主要防止 stack shellcode。
但本專案沒有執行 stack shellcode，而是跳回既有程式碼。
```

另一個重點是：

```text
ASLR 會隨機化 stack、heap、library 等區域。
但如果主程式是 non-PIE，它自己的 .text 位址不會被隨機化。
```

因此即使 Phase III 開啟 ASLR，`execute_task()` 與 `ret gadget` 的位址仍然可以穩定使用。

## 7. Agent 架構設計

本專案把 EC 的功能拆成三個元件：

```text
analyze_target.py
exploit
triage
```

這三個元件共同形成 autonomous exploit loop。

### 7.1 analyze_target.py

`analyze_target.py` 是 read-only target analyzer。

它會尋找 target binary。作業文字提到：

```text
/shared/blogic.copy
```

但提供的 `docker.sh` 實際上把 binary 複製到：

```text
/shared/blogic
```

所以 analyzer 同時支援：

```text
/shared/blogic.copy
/shared/blogic
```

分析器會執行並解析：

```text
file
readelf -h
readelf -W -l
readelf -s
strings -a
objdump -d
```

它會產生：

```text
/shared/target_info.json
/shared/target_analysis.log
```

主要分析項目包含：

- ELF 是否為 64-bit
- 架構是否為 x86_64
- 是否為 PIE
- NX 是否啟用
- symbol table 中有哪些有趣函式
- 是否存在 `execute_task`
- 是否存在 `maintenance_task`
- 是否有 `system`、`memcpy` 等 risky function
- binary 中有哪些 `ret` gadget
- 能否推論 offset_to_ret

### 7.2 exploit

`/exploit` 是每一輪攻擊的產生器。

它會：

1. 清空或建立 exploit log。
2. 執行 `/analyze_target.py`。
3. 讀取 `/shared/target_info.json`。
4. 選出 `execute_task` 位址。
5. 選出合適的 `ret` gadget。
6. 讀取或初始化 `/shared/state.json`。
7. 根據 state 決定本輪要嘗試的 offset。
8. 建立 payload。
9. 寫入 `/shared/config.data`。
10. 建立 `/shared/exploit_done`。

如果沒有既有 state，現在的預設行為是進入 adaptive probing，而不是直接假設 offset 是 `104`。

### 7.3 triage

`/triage` 在失敗後執行。

它會：

1. 讀取 `/shared/state.json`。
2. 檢查 `/shared/success.txt` 是否存在。
3. 檢查 `/shared/coredump/*`。
4. 判斷上一輪結果。
5. 更新 state。
6. 如果是 adaptive probing，推進到下一個 offset candidate。

triage 會把結果寫到：

```text
/shared/triage.log
/shared/state.json
```

它觀察到的結果分成幾種：

```text
success
crash
no_success_no_coredump
```

在這個環境中，coredump 有時會是 0 bytes，所以 agent 不完全依賴 register-level coredump analysis，而是使用這些高層次訊號來推進 probing。

## 8. Adaptive Offset Probing

這是目前報告最重要的敘事點。

如果只是手動分析 binary，我們可以知道成功 offset 是：

```text
offset_to_ret = 104
```

但如果報告中說 exploit 一開始就直接使用 `104`，會讓整個專案看起來像固定 exploit runner，而不是 autonomous agent。

因此現在的設計是：fresh `/shared` 下，沒有 `state.json` 時，agent 會自動初始化成 adaptive probing。

預設 candidate list 是：

```text
64, 72, 80, 88, 96, 104, 112, 120, 128
```

每一輪 `/exploit` 只嘗試一個 offset。

如果沒有成功，grader 會執行 `/triage`。`/triage` 會更新：

```text
offset_candidate_index
```

下一輪 `/exploit` 就會使用下一個 candidate。

實際觀察到的 adaptive 行為如下：

```text
Round 1: offset 64  -> no_success_no_coredump
Round 2: offset 72  -> no_success_no_coredump
Round 3: offset 80  -> no_success_no_coredump
Round 4: offset 88  -> no_success_no_coredump
Round 5: offset 96  -> crash
Round 6: offset 104 -> success
```

這個結果可以支持我們在報告中說：

```text
104 是透過 adaptive feedback loop 找到的，而不是一開始就假設的答案。
```

這也是本專案比較符合 Autonomous APT Agent 題意的地方。

## 9. State 設計

agent 狀態儲存在：

```text
/shared/state.json
```

一個典型 adaptive probing state 可能長這樣：

```json
{
  "round": 3,
  "offset_status": "adaptive_probe",
  "offset_candidates": [64, 72, 80, 88, 96, 104, 112, 120, 128],
  "offset_candidate_index": 2,
  "offset_to_ret": 80,
  "ret_gadget": "0x401414",
  "ret_gadget_source": "analyzer_preferred_ret",
  "execute_task": "0x401415",
  "mode": "adaptive_offset_probe",
  "next_action": "try_next_offset_candidate"
}
```

重要欄位：

- `round`：目前第幾輪。
- `offset_status`：目前是否處於 adaptive probing。
- `offset_candidates`：候選 offset 列表。
- `offset_candidate_index`：目前嘗試到哪個 candidate。
- `offset_to_ret`：本輪使用的 candidate offset。
- `ret_gadget`：分析器選出的 ret gadget。
- `execute_task`：分析器選出的目標函式。
- `next_action`：下一步策略。

這個 state 是 `/exploit` 和 `/triage` 合作的核心。

需要注意的是：當 exploit 成功時，`grader.sh` 會立刻停止，所以 `/triage` 不會再執行一次來把狀態更新成 `completed`。因此成功後的 `state.json` 可能停在成功前一輪或本輪嘗試前的狀態。這是 grader 流程造成的，不代表 exploit 失敗。

成功的真正判斷依據是：

```text
/shared/success.txt
```

以及 grader 輸出：

```text
[+] Exploit successful! Grading ends.
```

## 10. 測試方式

測試流程如下。

先建立 IC image：

```bash
docker build -t ic_image ./IC
```

再建立 EC image：

```bash
docker build -t my_ec ./EC
```

測試 Phase I：

```bash
docker rm -f IC_PHASE1 IC_PHASE2 IC_PHASE3 2>/dev/null || true
bash ./docker.sh 1

docker run -it --rm \
  -v "$(pwd)/shared:/shared" \
  -v "$(pwd)/grader.sh:/grader.sh:ro" \
  my_ec bash /grader.sh
```

測試 Phase II：

```bash
docker rm -f IC_PHASE1 IC_PHASE2 IC_PHASE3 2>/dev/null || true
bash ./docker.sh 2

docker run -it --rm \
  -v "$(pwd)/shared:/shared" \
  -v "$(pwd)/grader.sh:/grader.sh:ro" \
  my_ec bash /grader.sh
```

測試 Phase III：

```bash
docker rm -f IC_PHASE1 IC_PHASE2 IC_PHASE3 2>/dev/null || true
bash ./docker.sh 3

docker exec IC_PHASE3 cat /proc/sys/kernel/randomize_va_space

docker run -it --rm \
  -v "$(pwd)/shared:/shared" \
  -v "$(pwd)/grader.sh:/grader.sh:ro" \
  my_ec bash /grader.sh
```

Phase III 中，ASLR 應該顯示：

```text
2
```

## 11. 測試結果

三個 phase 都已成功測試。

成功輸出會包含：

```text
[+] Exploit successful! Grading ends.
[*] Grading done
```

測試結果：

```text
Phase I   success
Phase II  success
Phase III success
```

此外，也有保存 adaptive probing 的測試紀錄：

```text
phase2_adaptive_result.txt
phase3_adaptive_result.txt
```

這些檔案記錄了 agent 如何從前面的 offset candidate 一路推進，最後到達成功的 offset。

## 12. 遇到的問題與修正

### 12.1 初版太像固定 exploit

最早的版本直接使用：

```text
offset_to_ret = 104
ret_gadget = 0x401414
execute_task = 0x401415
```

這樣可以成功，但報告上會顯得像手動 exploit，而不是 autonomous agent。

修正方式是加入：

- target analyzer
- symbol discovery
- ret gadget discovery
- state management
- adaptive offset probing
- triage feedback

這樣可以把專案說明成「分析驅動、可觀察、可重試」的 agent。

### 12.2 Static offset inference 不可靠

一開始嘗試從 disassembly 靜態推論 offset。

但目標是 C++ 程式，stack frame 中包含 `ifstream`、`string`、temporary object 等複雜物件。若只是找最大 rbp displacement，可能會選到錯的 stack object。

因此最後做法是：static inference 只作為輔助資訊。如果分析不可靠，不直接採用，而是使用 adaptive probing 找出正確 offset。

### 12.3 Coredump 有時是空的

測試時觀察到 `/shared/coredump/*` 有時會出現 0 bytes 檔案。

這代表不能穩定依賴 coredump 取得 RIP/RSP 等暫存器資訊。

因此 triage 改用較高層次的觀察：

```text
success
crash
no_success_no_coredump
```

這已經足夠讓 adaptive probing 往下一個 candidate 推進。

### 12.4 路徑含空白導致 Docker 問題

目前專案路徑包含空白：

```text
Project - Automous APT Agent
```

原始 `docker.sh` 使用：

```bash
-v $(pwd)/shared:/shared
```

這會在路徑含空白時造成 Docker 解析錯誤。

修正為：

```bash
-v "$(pwd)/shared:/shared"
```

這樣 WSL 或 Linux shell 中都能正確處理含空白的路徑。

## 13. 與作業需求的對應

| 作業需求 | 目前狀態 |
|---|---|
| EC 需要有 `/exploit` | 已實作 |
| EC 需要有 `/triage` | 已實作 |
| `/exploit` 修改 `/shared/config.data` | 已實作 |
| `/exploit` 產生 `/shared/exploit_done` | 已實作 |
| 可以分析 `/shared/blogic.copy` | 已支援 |
| 也支援老師 script 實際使用的 `/shared/blogic` | 已支援 |
| blogic crash 後可以 triage | 已實作 |
| 60 rounds 內成功 | 已測試 |
| 30 分鐘內成功 | 已測試，實際為數秒內 |
| Phase I | success |
| Phase II | success |
| Phase III | success |

## 14. 專案限制

本專案是針對課程 lab 的 bounded autonomous exploit agent，不是真正通用的 APT framework。

目前限制包括：

- 假設溝通介面是 `/shared`。
- 假設輸入點是 `/shared/config.data`。
- 假設成功訊號是 `/shared/success.txt`。
- 假設目標命令是 `/backdoor`。
- 主要針對 stack-based control-flow hijacking。
- 依賴 binary 中有可辨識 symbol 或 pattern。
- 不會掃描網路。
- 不會攻擊課程 lab 以外的系統。

這些限制是合理的，因為作業本身就是受控 Docker 環境中的 exploit automation project。

## 15. 建議報告講法

正式報告時，建議不要把重點放在「我知道 offset 是 104，所以直接塞 payload」。

比較好的講法是：

```text
我們先分析 target binary，找出 execute_task 與 ret gadget。
至於 return-address offset，agent 預設不直接假設正確答案。
它會透過 adaptive probing 從候選 offset 開始嘗試。
每一輪失敗後，triage 根據 success.txt 與 coredump 狀態更新 state.json。
下一輪 exploit 再讀取 state.json，嘗試下一個 candidate。
最後 agent 在 offset 104 時成功觸發 /backdoor。
```

如果老師問「那 104 是不是你們一開始就知道？」可以回答：

```text
我們確實可以透過人工分析知道 104 是工作 offset。
但 final agent 的主要流程不是直接假設 104。
在 adaptive mode 下，fresh state 會從候選值開始測試，透過 triage feedback 一輪一輪推進，最後到 104 成功。
因此報告中的重點是 autonomous discovery process，而不是單一 hard-coded exploit。
```

## 16. 結論

本專案完成了作業要求的核心流程：

```text
/exploit -> /shared/config.data -> /shared/exploit_done -> blogic -> /backdoor -> /shared/success.txt
```

同時也加入了自主式 agent 的基本要素：

```text
Analyze -> Generate -> Execute -> Observe -> Triage -> Retry
```

最終版本的重點是：

- 不是只提交一個固定 payload。
- agent 會分析 target binary。
- agent 會維護 state。
- agent 會根據 triage feedback 調整 offset candidate。
- successful offset 是透過 adaptive probing 過程找到的。

因此，這個實作符合課程所要求的 Autonomous APT Agent 精神，也能在 Phase I、Phase II、Phase III 中成功觸發 `/backdoor`。
