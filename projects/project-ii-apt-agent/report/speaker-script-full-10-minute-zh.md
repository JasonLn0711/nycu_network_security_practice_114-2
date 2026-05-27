# Speaker Script - Full 10 Minute Project II Presentation

Language: Taiwan Traditional Chinese with technical English terms preserved.

Target deck: `presentation-full-10-minute-zh.md`

Target length: about `10` minutes.

## 0:00-0:25 - Title

大家好，我們今天報告的題目是 Autonomous APT Agent，副標題是 Adaptive Binary Exploitation Workflow with Failure-Aware Coordination。

我們是 313264012 陳靖中，以及 513559004 林家聖。

這份 Project II 的重點，是把 binary exploitation 從單次手動攻擊，整理成一個可以分析、可以產生 payload、可以觀察結果、可以更新狀態的 autonomous cyber operation workflow。

今天我會用系統架構的角度說明這份 lab，並用 exploit 細節與實驗數據作為支撐證據。

## 0:25-1:00 - Slide 1: Vision

現代 cyber operation workflow 已經逐漸走向自動化和協調化。

一個完整流程通常包含 automated analysis、adaptive retry、orchestration-based operations，以及 multi-stage exploitation workflow。

因此，我們這份 Project II 建立的是一個 Autonomous APT Agent。它的核心能力是透過 binary analysis 找出目標資訊，再根據分析結果產生 payload，執行後觀察結果，最後把結果寫回 state，作為下一輪策略的依據。

這就是這份專案的主軸：binary exploitation 可以被組織成一個可協調、可觀察、可重試的 workflow。

## 1:00-1:35 - Slide 2: Project Objective

這張圖是整個 agent 的高層流程。

第一步是 Analyze Binary，也就是分析 target binary。第二步是 Generate Payload，根據分析結果產生攻擊輸入。第三步是 Launch Exploit，把 payload 放進 lab 指定的 shared volume。

接著 Observe Result，觀察是否成功、是否 crash、是否有 coredump。最後 Update State，讓下一輪 Adaptive Retry 可以用新的狀態繼續嘗試。

在本 lab 中，具體目標是 EC 產生 `/shared/config.data`，IC 執行 `blogic` 讀取這份 config，成功時觸發 `/backdoor`，最後產生 `success.txt` 作為成功證據。

## 1:35-2:10 - Slide 3: Real Lab Architecture

這份 lab 是一個 dual-container cyber range。

EC，也就是 External Container，是 agent 端。裡面有 `/exploit`、`/triage`，以及 `analyze_target.py`。

IC，也就是 Internal Container，是 target 端。它會執行 vulnerable binary，也就是 `blogic`，成功目標是 IC 裡的 `/backdoor`。

EC 和 IC 之間的協調通道是 `/shared`。EC 透過 `/shared` 寫入 payload、同步 marker、state 和 log；IC 透過同一個 shared volume 讀取 `config.data`，執行 `blogic`，成功後寫出 `success.txt`。

這份架構的亮點，是它把攻擊端、目標端、coordination channel 都清楚拆開。

## 2:10-2:45 - Slide 4: Actual Lab Package

這是實際 lab package 的結構。

`EC/` 下面有 `exploit`、`triage`、`analyze_target.py` 和 Dockerfile，這是 agent 端的主要實作。

`IC/` 下面有 `server.cpp`、`server_1`、`server_2`、`backdoor` 和 Dockerfile，這是 target 端的程式與 binary。

`shared/` 是保存 payload、state、log 和 success evidence 的地方。`docker.sh` 負責啟動 container，`grader.sh` 負責跑 grading loop。

在我們保存的 successful package 中，extracted lab package 共保留 26 個檔案，而且保存了 `success.txt`、`exploit-log.txt`、`state.json` 和 `target_info.json`，所以這份報告的數據都可以對應到實驗 artifacts。

## 2:45-3:20 - Slide 4.1: Lab Files Work Together

這一張補充檔案之間的關係。

`docker.sh` 的角色是啟動 IC cyber range，準備好 `blogic` 和 `/shared`。`grader.sh` 則控制整個 round loop：它會呼叫 `/exploit`，等待 IC 執行，檢查 success，然後在需要時呼叫 `/triage`。

`EC/analyze_target.py` 讀取 `/shared/blogic`，產生 `target_info.json`。`EC/exploit` 使用 analyzer 結果和 `state.json`，寫入 `config.data` 與 `exploit_done`。

IC 端的 `server.cpp`、`server_1`、`server_2` 提供 vulnerable logic，最後作為 `blogic` 被執行。`IC/backdoor` 是成功目標，被觸發後會寫出 `success.txt`。

所以整體關係是：`docker.sh` 準備環境，`grader.sh` 控制流程，`exploit` 產生 payload，`blogic` 消費 payload，`triage` 把結果轉成下一輪 state。

## 3:20-3:55 - Slide 5: Core Vulnerability

接下來看核心漏洞。

`server.cpp` 裡有這段邏輯：`char buf[96]; memcpy(buf, msg, len);`

`buf` 的大小是 96 bytes，而 `memcpy` 會依照 `len` 複製資料。當 `len` 大於 buffer 可承載的長度時，資料就會碰到 stack 上其他控制資料。

在這個 lab 中，資料流是：`config.data` 提供 attacker-controlled input，`parse_config()` 把資料放到 global `user_input`，然後 `log_message(user_input, user_input_len)` 把資料複製到 `buf`。

這個長度邊界缺口，讓 payload 可以影響 return path，最後把控制流程導向 `execute_task()`。

## 3:55-4:30 - Slide 6: Exploitation Workflow

這張 sequence diagram 是實際 attack chain。

首先，EC 的 `/exploit` 產生 payload，寫入 `/shared/config.data`，再建立 `/shared/exploit_done`。IC 偵測到 marker 後，執行 `blogic`，讀取 `config.data`。

`blogic` 裡的 `memcpy` 讓 payload 觸及 return path，接著控制流程被導向 `execute_task()`。

`execute_task()` 會呼叫 `maintenance_task(user_input)`，而 `maintenance_task` 會進一步呼叫 `system()`。當 `user_input` 前面放的是 `/backdoor`，最後就會執行 `/backdoor`，並寫出 `/shared/success.txt`。

payload 概念可以簡化成：`/backdoor\x00 + padding + ret_gadget + execute_task`。

## 4:30-5:05 - Slide 7: Actual Autonomous Components

EC 裡面可以看成三個 agent component。

第一個是 `analyze_target.py`，它負責 perception，也就是讀取 `blogic`，分析 ELF facts、symbols、strings 和 gadgets，最後輸出 `target_info.json`。

第二個是 `/exploit`，它負責 action，也就是選 target function、建立 payload、寫入 `config.data`，並建立 `exploit_done`。

第三個是 `/triage`，它負責 observation 和 state update。它會讀取結果、檢查 coredump，並更新 `state.json`，讓下一輪知道該換 offset 或策略。

所以這個系統具備 perception、action、observation、state update 的 agent workflow 結構。

## 5:05-5:35 - Slide 8: Stateful Coordination Design

這張投影片說明 `/shared` 的角色。

`/shared` 是 agent memory 和 protocol layer。

`config.data` 是給 `blogic` 消費的 payload input。`exploit_done` 是 EC 告訴 IC：payload 已經準備好了。`target_info.json` 保存 binary analysis 結果。`state.json` 保存 retry state、selected offset、target 和 gadget。

`exploit-log.txt` 是 `/exploit` 的執行紀錄。`success.txt` 則是最後的成功證據。

在 final saved run 裡，strategy 是 `adaptive_static_analysis_driven_agent`，mode 是 `final_exploit`，next action 是 `generate_final_payload`。這表示系統狀態是可以被追蹤和重現的。

## 5:35-6:15 - Slide 9: Experimental Binary Analysis

接下來看實驗數據。

從 `target_info.json` 可以看到，target binary 是 ELF 64-bit，architecture 是 `x86_64`，endianness 是 little-endian，binary 是 not stripped。

PIE 是 false，代表 code address 是固定的。saved final target 的 NX 是 false。analyzer 解析出 108 個 symbols，並找到 20 個 ret gadgets。

幾個重要 symbols 包括：`execute_task` 在 `0x401415`，`maintenance_task` 在 `0x4013f6`，`parse_config` 在 `0x401464`，`user_input` 在 `0x404340`，`user_input_len` 在 `0x404540`。

這些數據證明 analyzer 會從 binary 中抽出可用的 exploitation planning facts。

## 6:15-6:50 - Slide 10: Payload Planning Result

這張是 final payload 的規劃結果。

根據 final exploit log，系統選擇的 target 是 `_Z12execute_taskv`，地址是 `0x401415`。

preferred ret gadget 是 `0x401414`。offset to return address 是 104 bytes。`/exploit` 報告的 payload length 是 120 bytes，而保存下來的 `config.data` 檔案大小是 132 bytes。模式是 `final_exploit`。

payload 結構是：前面放 `/backdoor\x00`，接著 padding 到 offset 104，然後放 ret gadget `0x401414`，最後放 `execute_task` address `0x401415`。

這讓 exploit 從概念變成可量測的工程輸出：address、offset、payload length 和 mode 都有保存證據。

## 6:50-7:30 - Slide 11: Adaptive Retry Workflow

這張圖展示 autonomous 行為最清楚的部分：adaptive retry。

adaptive mode 裡有一串 offset candidates：64、72、80、88、96、104、112、120、128。

在 Phase 2 和 Phase 3 的 adaptive trace 中，round 1 到 round 4 分別測試 64、72、80、88，結果是 no success、no coredump。

round 5 測試 offset 96，產生 crash 和一個 coredump。`/triage` 讀到這個結果後，把下一個 candidate 從 96 推進到 104。

所以這個 agent 的價值在於：它把失敗結果轉換成下一輪策略，讓 retry 有明確方向。

## 7:30-8:05 - Slide 12: Successful Final Run

這張是 final successful run 的證據。

`exploit-log.txt` 顯示，在 `2026-05-22 16:50:15`，analyzer completed successfully。系統選到 `execute_task = 0x401415`，選到 ret gadget `0x401414`，使用 offset `104`，payload length 是 `120 bytes`，並且建立了 `/shared/exploit_done`。

同一個 saved run 的 `success.txt` 記錄：`Backdoor triggered`，時間是 `Fri May 22 16:50:15 UTC 2026`。

這代表 exploit generation 和 success artifact 在同一個 timestamp 對齊。這是我們可以上台展示的直接成功證據。

## 8:05-8:40 - Slide 13: Experimental Results

把成果整理成 capability，可以看到這份專案完成了幾個層次。

第一，binary analysis：它抽取 ELF facts、108 個 parsed symbols、target functions 和 risky imports。

第二，gadget discovery：它找到 20 個 ret gadgets，並選出 preferred gadget `0x401414`。

第三，payload planning：它選定 target `0x401415`，offset `104`，payload length `120 bytes`。

第四，stateful retry：它保存 offset candidates，並且在 crash 後由 triage 推進下一個 offset。

第五，cyber-range operation：它完整運作在 EC、IC 和 `/shared` 的雙 container 架構中。

第六，success evidence：它保存了 `/shared/success.txt`，內容是 `Backdoor triggered`。

這些合起來，就是 binary exploitation as an orchestrated autonomous workflow。

## 8:40-9:15 - Slide 14: Why This Project Matters

這個專案重要的地方，在於它把 exploit detail 提升成 system impression。

單一技術細節可以解釋一個 mechanism，例如 memcpy overflow 或 return address overwrite。

但 autonomous workflow 可以讓觀眾理解整個系統：target 如何被分析，payload parameters 如何被選出，exploit attempt 如何啟動，failure feedback 如何更新下一步，以及 execution evidence 如何被保存。

因此，這份 Project II 展示的是一個在 Docker cyber range 內運作的 lightweight autonomous cyber operation workflow。

## 9:15-9:40 - Slide 15: Future Expansion

未來這個系統可以往 AI-assisted cyber operations 擴展。

第一個方向是 LLM-assisted planning，用來解釋 crash、建議下一輪 probe、整理 state。

第二個方向是 symbolic execution，例如整合 `angr`、Triton 或 Z3，讓 exploit planning 更 path-aware。

第三個方向是 multi-agent architecture，把 reconnaissance、exploit、retry 和 orchestration 拆成不同 agent。

第四個方向是 richer triage，把 coredump 和 registers 轉成更結構化的 next-action evidence。

這些方向會讓 course lab 成為 agentic security research 的入門橋樑。

## 9:40-10:00 - Final Takeaway

最後總結。

這份 Project II 展示的是：binary exploitation can evolve into an adaptive autonomous cyber workflow。

系統整合了 Dockerized cyber range、dual-container attack model、static binary analysis、payload generation、shared-state coordination、adaptive retry，以及 saved experimental evidence。

所以我們今天展示的核心成果，是一個 coordinated autonomous cyber operation workflow。謝謝大家。
