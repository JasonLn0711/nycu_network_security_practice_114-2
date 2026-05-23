# Speaker Script - 10 Minute Project II Report

Language: Taiwan Traditional Chinese.

Use this as speaker notes. Keep slide text shorter than the spoken version, and
keep the spoken delivery direct and technical.

## 0:00-0:30 - Slide 1

大家好，我們這次 Project II 的題目是 Autonomous APT Agent。這個 project
的目標不是做一個泛用攻擊工具，而是在課程提供的 Docker lab 裡，實作
External Container 端的 agent，讓它可以透過 `/shared` 跟 Internal
Container 互動，最後觸發 IC 裡的 `/backdoor`。

我們是兩人分組分工完成這個 Project II package。今天報告會聚焦在我們這組
最後 package 的系統功能、系統特色，以及保存下來的成功證據。

## 0:30-1:20 - Slide 2

作業的 interface 很明確。External Container 需要提供兩個入口：
`/exploit` 和 `/triage`。

每一輪 grader 會先跑 `/exploit`。`/exploit` 要修改
`/shared/config.data`，然後建立 `/shared/exploit_done`。IC 看到
`exploit_done` 之後會執行 `blogic`，讀取剛剛寫入的 config。

如果成功觸發 IC 裡的 `/backdoor`，就會產生 `/shared/success.txt`，grading
結束。如果沒有成功，就會有 coredump 或 no-success feedback，再由
`/triage` 更新下一輪策略。

所以這份作業的核心不是單純寫一段 payload，而是要符合 EC/IC/shared volume
這個 grading loop。

## 1:20-2:20 - Slide 3

我們的系統可以分成三個模組。

第一個是 Target Analyzer，也就是 `analyze_target.py`。它會讀
`/shared/blogic.copy` 或 `/shared/blogic`，分析 binary 的 metadata、
symbol、string、risky import 和 ret gadget。

第二個是 Exploit Generator，也就是 `/exploit`。它會先跑 analyzer，再根據
`target_info.json` 選擇 target function、ret gadget 和 offset，最後寫出
`config.data` 並建立 `exploit_done`。

第三個是 Triage Feedback，也就是 `/triage`。它會看 `success.txt`、
coredump 或 no-success 狀態，再更新 `state.json`，讓下一輪可以調整策略。

這樣整個系統就形成 Analyze、Generate、Execute、Observe、Update 的 loop。

## 2:20-3:25 - Slide 4

Target Analyzer 的重點是：它讓 `/exploit` 不是完全 blind 或只靠固定字串。

Analyzer 會確認 target 是 x86_64 ELF、是否 non-PIE、stack / NX 狀態、symbol
table，以及 risky imports，例如 `memcpy` 和 `system`。

這次成功 package 裡最重要的發現是 `execute_task`。Analyzer 找到
`execute_task = 0x401415`，也找到 preferred ret gadget `0x401414`。

`execute_task` 很關鍵，因為它是一個無參數 helper function，內部會呼叫
`maintenance_task(user_input)`。這代表 exploit 不需要自己在 return 的瞬間
設定第一個參數，只要讓 global `user_input` 裡有 `/backdoor`，再跳到
`execute_task`，就能接到成功路徑。

## 3:25-4:45 - Slide 5

成功 payload 的邏輯可以簡化成這個 layout：

`user_input = /backdoor\0 + padding + ret gadget + execute_task`

前面放 `/backdoor` 加上 null terminator，讓之後 `system()` 看到的是正確的
command。接著 padding 到 saved return address，這次有效 offset 是 `104`。
最後接一個 ret gadget 和 `execute_task` 的 address。

當 `log_message` 裡的 stack overwrite 影響 return address 後，控制流會先到
ret gadget，再到 `execute_task`。`execute_task()` 會執行
`maintenance_task(user_input)`，而 `maintenance_task()` 裡面是
`system(arg)`。

所以真正成功的原因，是 target binary 裡剛好有一個 helper，把 controlled
data，也就是 `user_input`，接到 `/backdoor` 執行路徑。

## 4:45-5:45 - Slide 6

除了 fast mode，系統也有 adaptive probing 的設計。

如果進入 adaptive mode，`/exploit` 不會一開始就只用固定 offset，而是根據
`state.json` 裡的 offset candidate 一個一個嘗試。`/triage` 會根據上一輪是
success、crash，還是 no-success，去更新下一個 candidate。

報告裡展示的 sequence 是從 `64, 72, 80, 88, 96` 一路嘗試，最後到 `104`。
在 `96` 時會觀察到 crash，下一輪推進到 `104`，就到達有效 offset。

所以 fast mode 是正式 grading 的穩定路徑；adaptive mode 則用來展示 agent
具有 feedback loop 和自動嘗試能力。

## 5:45-6:50 - Slide 7

系統特色可以整理成六點。

第一，analysis-driven。它會先分析 binary，再選擇 target 和 gadget。

第二，state-driven。它把 round、offset candidate、target function、gadget
等資訊存在 `/shared/state.json`。

第三，feedback-aware。`/triage` 會依據 success、crash、no-success 來決定
下一步。

第四，bounded design。它只操作 `/shared` 和課程提供的 binary，不掃描外部
網路，也不攻擊其他系統。

第五，fast mode 提供穩定 grading path。

第六，adaptive mode 展示 agent 的探索能力。

這些功能合起來，就是這份 Project II package 的系統特色。

## 6:50-9:20 - Slide 8 / Optional Demo

接下來我展示成功證據。

第一個是 `success.txt`。這個檔案裡可以看到 `Backdoor triggered`，以及成功
的 timestamp。這代表 `/backdoor` 在 IC 端被觸發過。

第二個是 `exploit-log.txt`。這裡可以看到 `/exploit` 先跑 analyzer，接著選出
`execute_task = 0x401415`，選出 ret gadget `0x401414`，使用 offset `104`，
寫入 final exploit payload，最後建立 `/shared/exploit_done`。

第三個是 `target_info.json`。這裡可以看到 analyzer 的結構化輸出，包括 target
是 non-PIE、找到 `execute_task`、`user_input`、`user_input_len`，以及 ret
gadget。

如果現場環境很穩，我可以用已經 build 好的 Docker image 跑一次短 demo；
如果環境慢或 Docker 啟動有問題，就以這些保存下來的 evidence 為準，避免
把 10 分鐘花在 debug 環境。

## 9:20-10:00 - Slide 9

總結來說，這份 Project II package 完成了作業要求的 External Container
interface：有 `/exploit`、`/triage`、會寫 `config.data`、會建立
`exploit_done`，並且在成功 package 中留下 `/shared/success.txt` 作為證據。

技術上最重要的成功點，是 target binary 裡有 `execute_task()` 這個 helper。
它把 global `user_input` 接到 `system()` 執行路徑，讓 exploit 不需要另外解決
return 時的 first-argument setup。

限制上，這個系統是 bounded course-lab agent，不是泛用攻擊工具；成功證據也
應該綁定在這份 package 的 binary context 裡。

以上是我們 Project II 的系統功能展示與特色說明。
