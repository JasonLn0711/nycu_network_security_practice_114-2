# Environment Variables And Privilege Boundaries

This week-2 lecture note expands the environment-variable topic into process inheritance, dynamic-linker abuse, Set-UID behavior, access control, and defensive system design.

## 一、 核心概念：環境變數 (Environment Variables)

當一個行程 (Process) 在作業系統中運行時，它需要知道當前的外在環境狀態（例如：我是誰？我在哪裡？我要去哪裡找工具？）。作業系統透過環境變數來傳遞這些資訊。

### 1. 專有名詞定義

* **環境變數 (Environment Variables)**：一組動態的具名數值（Key-Value Pairs），構成了行程執行的作業環境，並會直接影響執行中程式的行為 。此機制最早於 Unix 系統引入，隨後也被 Windows 採用 。
* **PATH (路徑變數)**：最常見的環境變數。當使用者在終端機輸入指令（如 `ls`）卻沒有提供絕對路徑時，Shell 會依據 `PATH` 變數中所列出的目錄順序，去尋找該程式的執行檔 。



### 2. 程式如何存取環境變數？

在 C 語言中，有兩種主要方式可以獲取環境變數：

1. **透過 `main` 函式參數**：`void main(int argc, char *argv[], char *envp[])`，其中 `envp` 是一個字串陣列指標 。
2. **透過全域變數 `environ**`：宣告 `extern char** environ;` 。這比 `envp` 更可靠，因為當程式執行期間新增環境變數時，原本存放在堆疊 (Stack) 的變數可能會因為空間不足而被作業系統搬移到堆積 (Heap) 區 。此時全域變數 `environ` 的指標會跟著更新，但 `main` 函式裡的 `envp` 則不會改變 。



---

## 二、 變數的繼承機制與 Shell 變數

理解環境變數如何在行程間傳遞，是挖掘系統漏洞的基礎。

### 1. 行程的繼承 (Inheritance)

* **`fork()` 系統呼叫**：當建立新的子行程時，子行程會完美繼承父行程的環境變數 。
* **`execve()` 系統呼叫**：當行程要在自身內部執行另一個新程式時，記憶體空間會被覆寫，舊的環境變數會全部遺失 。除非在呼叫 `execve()` 時，透過第三個參數顯式地將環境變數陣列傳遞過去（`int execve(const char *filename, char *const argv[], char *const envp[])`） 。



### 2. Shell 變數 vs. 環境變數

人們常將兩者混淆，但它們在安全範圍上完全不同 。

* **Shell 變數**：僅供 Shell 程式內部使用的變數 。當您在終端機輸入 `LOGNAME2=alice` 時，它只存在於目前的 Shell 中 。
* **轉換機制**：當 Shell 啟動新的子程式時，它**不會**把內部的 Shell 變數傳給子程式。必須使用 `export` 指令（如 `export LOGNAME3=bob`），將 Shell 變數「匯出」成環境變數，子程式才能接收到 。



### 3. 特殊檔案系統 `/proc`

Linux 提供了一個虛擬檔案系統 `/proc` 。每個正在執行的行程都有一個以其 PID 命名的資料夾。您可以透過讀取 `/proc/$$/environ`（`$$` 代表當前 Shell 的 PID）來查看該行程最原始的環境變數內容 。

---

## 三、 環境變數的四大攻擊面 (Attack Surfaces)

由於環境變數可以由使用者任意設定，如果具有高權限的 Set-UID 程式在底層「隱性」地依賴了這些變數，就會成為極危險的攻擊面 。

攻擊面主要分為四個層次 ：

1. **Linker (動態連結器)** 
2. **Application Code (應用程式碼本身)** 
3. **Library (外部函式庫)** 
4. **External Program (呼叫外部程式)** 



### 重點解析：透過動態連結器攻擊 (Attacks via Dynamic Linker)
![image](https://hackmd.io/_uploads/H1B35wBFbe.png)

* **動態連結 (Dynamic Linking)**：為了節省記憶體，現代程式多半採用動態連結。程式碼碼中不包含標準函式（如 `printf` 或 `sleep`）的實作，而是在執行期間由動態連結器（如 `ld.so`）去尋找並載入共享函式庫（Shared Libraries） 。
* **危險變數 `LD_PRELOAD`**：這個變數包含一個清單，指示動態連結器在載入任何東西之前，**優先搜尋**這個清單上的函式庫 。
* **攻擊手法 (Library Hijacking)**：
攻擊者可以自己寫一個惡意的 `sleep()` 函式，編譯成 `libmylib.so`，然後執行 `export LD_PRELOAD=./libmylib.so` 。當系統程式嘗試執行標準的 `sleep()` 時，就會被劫持，轉而執行攻擊者的惡意程式碼 。



### 作業系統的防禦反制機制

如果駭客對擁有 root 權限的 Set-UID 程式使用 `LD_PRELOAD`，系統不就立刻被攻陷了嗎？
為了解決這個問題，動態連結器內建了安全機制：**當它發現程式的有效使用者 ID (EUID) 與真實使用者 ID (RUID) 不一致時（這正是 Set-UID 程式運作的特徵），它會直接「忽略」 `LD_PRELOAD` 和 `LD_LIBRARY_PATH` 這些危險的環境變數** 。這確保了高權限程式只會使用系統標準的、安全的函式庫。

---

## 四、 現實生活實例與應用場景

* **PATH 劫持攻擊 (現實應用)**：
假設系統中有一支擁有高權限的程式，原始碼裡寫了 `system("cal");` 來呼叫日曆功能 。因為它沒有寫出絕對路徑（如 `/usr/bin/cal`） ，攻擊者可以在自己的資料夾裡寫一支名為 `cal` 的惡意腳本，然後設定 `export PATH=.:$PATH`，把「當前目錄」塞到尋找清單的最前面 。高權限程式就會不小心執行了攻擊者的惡意腳本，導致系統被植入後門或取得 root shell 。
* **安檢門禁模型 (解釋 EUID != RUID 防禦)**：
想像您是一位維修工（RUID=一般權限），拿著經理的特許感應卡（Set-UID 程式，EUID=高權限）要去機房維修。安檢人員（動態連結器）核對後發現：您的真實身分和卡片權限不符。雖然允許您進入，但絕對**禁止**您帶自己的私人工具箱（`LD_PRELOAD`）進去，只能用機房內標準配置的公家工具（標準系統函式庫），以此防範內部破壞。

---

## 五、 延伸教材補充：現代資安與系統開發的整合

將環境變數的攻防邏輯應用到高階開發與安全認證領域，會發現其極高的實用價值：

### 1. 滲透測試 (CEH) 中的權限提升 (Privilege Escalation)

在準備 CEH 等資安認證時，「環境變數劫持」是 Linux 本機權限提升（Local Privilege Escalation）的必考題與實務常態。除了 `LD_PRELOAD`，若目標系統管理員設定了不安全的 `sudo` 規則（例如設定了 `env_keep` 允許保留使用者的環境變數），滲透測試工程師便能利用上述的 `PATH` 污染或 `LD_PRELOAD` 技巧，在無需密碼的情況下將普通權限躍升為 Root。

### 2. 高安全性 AI 系統開發 (Rust 的環境變數處理)

在開發用於即時語音辨識 (ASR) 或部署高併發 AI 推論的底層系統時，若使用 C 語言的 `getenv()` 讀取未受信任的環境變數（如 `PWD`）並使用 `sprintf`，極易引發**緩衝區溢位 (Buffer Overflow)** 漏洞 。
相較之下，在 Ubuntu 環境中使用 **Rust** 進行開發時，其標準函式庫 `std::env::var` 在設計上就強制開發者處理 `Result` 型別（包含變數不存在或包含非 Unicode 無效字元的錯誤）。Rust 的所有權與動態字串 (`String`) 機制，從編譯階段就徹底根絕了因為環境變數長度異常所導致的記憶體溢位問題，是打造堅固地端應用的絕佳選擇。

### 3. 醫療器材軟體 (SaMD) 的資安威脅建模 (Threat Modeling)

在準備 FDA 醫療軟體上市前審查（Premarket Submission）時，網路安全（Cybersecurity）是極為嚴格的審查項目。若 SaMD 產品底層依賴 Linux 系統運作，架構設計上應遵循「Secure by Design」原則。這意味著系統應避免使用高風險的 Set-UID 程式來執行高權限的醫療數據存取。如講義後續將探討的，應改用 **Service Approach (服務途徑)**，將特權操作隔離在獨立的背景 Daemon 中，藉此切斷一般使用者透過環境變數感染高權限醫療軟體的攻擊面，這在撰寫滲透測試報告與漏洞緩解策略時是強而有力的架構級防禦證明。

---

## Access Control And User Identity

This second part of the week-2 note moves from environment-variable attack surfaces into operating-system defense: access control, user identity, Set-UID tradeoffs, and basic file-permission mechanisms.

作業系統要防止惡意程式或未授權的使用者搞破壞，第一步就是要「認人」。在 Linux/Unix 系統中，系統並不認識您的英文字母帳號（如 `jason`），而是認數字。

### 1. 專有名詞定義

* **存取控制 (Access Control)**：系統用來決定「誰（主體）」可以對「什麼資源（客體）」執行「什麼操作（權限）」的防護機制。
* **UID (User Identifier，使用者識別碼)**：系統分配給每個帳號的唯一整數。`root` 的 UID 永遠是 `0`。
* **RUID (Real User ID，真實使用者 ID)**：代表「究竟是誰啟動了這個行程」。它記錄了最初登入系統的使用者身分。
* **EUID (Effective User ID，有效使用者 ID)**：作業系統在程式執行期間，**實際用來檢查檔案存取與特權操作權限**的身分。通常 EUID 會等於 RUID，但在特定情況下（如執行 Set-UID 程式）會發生改變。

---

## 二、 權限提升的兩難與 Set-UID 機制

這是 Unix 系統設計上一個經典的安全妥協。

**情境難題**：
使用者的密碼存放在 `/etc/shadow` 檔案中，這個檔案基於安全理由，權限設定為「只有 root 可以讀寫」。但是，一般使用者總需要修改自己的密碼，如果他們沒有 root 權限，要怎麼寫入新密碼到 `/etc/shadow`？

### 1. 專有名詞定義與解決方案

* **Set-UID (SUID，設置使用者 ID)**：一種特殊的檔案權限旗標（Flag）。當一個執行檔被設定了 Set-UID 屬性，且擁有者為 root 時，**任何使用者執行這支程式時，該行程的 EUID 會瞬間暫時變成「檔案擁有者 (root)」的 UID (即 0)**，而 RUID 保持不變。
* **指令舉例**：`passwd` 指令。
當您輸入 `passwd` 修改密碼時，因為這支程式具有 Set-UID root 屬性，您在執行它的當下「暫時化身為 root」，因此程式有權限幫您把新密碼寫入 `/etc/shadow`。執行結束後，權限即刻繳回。

### 2. Set-UID 的巨大安全風險

誠如上半堂課所述，如果這支 Set-UID 程式寫得不夠嚴謹（例如盲目信任 `PATH` 等環境變數，或有緩衝區溢位漏洞），攻擊者就可以在它「帶著 root 權限執行」的期間，劫持它的控制流，進而取得系統的最高控制權。

---

## 三、 安全架構的演進：Service 架構 (Service Architecture)

為了解決 Set-UID 帶來的龐大攻擊面，現代高安全性系統提出了另一種架構。

### 1. 專有名詞定義

* **IPC (Inter-Process Communication，行程間通訊)**：作業系統提供的一種機制（如 Socket、Message Queue），允許兩個獨立運作的行程互相交換資料。
* **Service Architecture (服務導向架構 / Daemon 模式)**：系統在背景啟動一個已經擁有 root 權限的常駐服務（Daemon）。當一般使用者需要執行特權操作時（例如修改網路設定），使用者不是去執行一個 Set-UID 程式，而是透過 IPC 發送一個「請求訊息」給背景服務。背景服務檢查請求合法後，**「代為」**執行操作，再把結果傳回給使用者。

### 2. 架構安全性比較

| 比較項目 | Set-UID 架構 | Service 架構 (現代推薦) |
| --- | --- | --- |
| **權限所在** | 一般使用者的行程被提升權限 (危險) | 權限始終被隔離在受信任的背景服務中 (安全) |
| **環境變數風險** | 極高 (會繼承使用者的惡意環境變數) | 極低 (背景服務不繼承一般使用者的環境變數) |
| **代表系統** | 傳統 Linux/Unix | **Android 系統** (已全面移除 Set-UID 機制) |

---

## 四、 Linux 檔案權限管理機制 (File Permissions)

在確認了 EUID 之後，系統會去檢查檔案的權限設定，來決定是否放行操作。

### 1. 權限的三種身分與三種操作

當我們輸入 `ls -l` 觀察檔案時，會看到如 `-rwxr-xr--` 的 9 個字元，它們被分為三組：

* **Owner (擁有者)**：檔案的主人。
* **Group (群組)**：檔案所屬的群組成員。
* **Other (其他人)**：系統上既不是擁有者也不是群組成員的所有其他人。

每一組都有三種權限可以設定：

* **r (Read，讀取)**：可讀取檔案內容；若為目錄，則可列出目錄下的檔名。
* **w (Write，寫入)**：可修改檔案內容；若為目錄，則可在該目錄內新增/刪除檔案。
* **x (Execute，執行)**：可將檔案當作程式執行；若為目錄，則可「進入（cd）」該目錄。
![image](https://hackmd.io/_uploads/BkF8CwBY-g.png)
![image](https://hackmd.io/_uploads/rkn3RDSFWx.png)

### 2. 系統的權限檢查邏輯 (System Call 觸發)

當程式發出 `open()` 或 `read()` 的 System Call 時，OS Kernel 檢查順序如下：

1. **你是 root 嗎？** 如果 EUID = 0，無條件放行。
2. **你是 Owner 嗎？** 檢查 EUID 是否等於檔案擁有者的 UID。如果是，只看 Owner 的那三碼權限，**決定後即刻停止檢查**（即使 Group 有更高權限也不管）。
3. **你是 Group 嗎？** 如果不是 Owner，檢查你是否在該群組中。如果是，套用 Group 權限並停止檢查。
4. **套用 Other**：如果都不是，套用 Other 的權限。

---

## 五、 現實生活中應用的實例

* **Set-UID (特許通行證)**：
就像您是一位基層警員，平時不能進入證物室。但今天局長給了您一張「特許感應卡 (Set-UID)」，您刷這張卡進去放東西的期間，門禁系統把您當作局長 (EUID=局長) 來放行。
* **Service 架構 (銀行櫃檯模式)**：
為了防止基層警員拿特許卡在證物室亂搞（Set-UID 風險），現在證物室改成「銀行櫃檯模式」。您永遠不能進去，只能在窗口填寫申請單（IPC 請求），由裡面戴著防毒面具、身家清白的專職管理員（Daemon Service）確認單據無誤後，**代您**把證物放進去。
* **檔案權限 (辦公大樓門禁)**：
* `Owner`：您的個人辦公室（您可以自由讀寫）。
* `Group`：NYCU 網工所的實驗室（屬於這個實驗室的學生都可以進入）。
* `Other`：一樓大廳（所有人都可以進來）。



---

## 六、 延伸教材補充 (結合您的專業背景)

### 1. CEH 滲透測試與 SUID 提權 (Privilege Escalation)

在準備 CEH (Certified Ethical Hacker) 時，尋找系統中設定錯誤的 SUID 程式是本機提權（Local Privilege Escalation, LPE）的標準起手式。

* **實務指令**：攻擊者通常登入系統後，第一步會下達 `find / -perm -4000 -type f 2>/dev/null`。這個指令會找出系統中所有帶有 SUID (4000) 屬性的檔案。
* 如果發現如 `vim`、`nmap` 或您自己寫的不良程式帶有 SUID root，攻擊者就能利用這些工具執行 Shell 逃逸（Shell Escape），瞬間取得 Root 權限。

### 2. FDA 醫療軟體 (SaMD) 的資安架構設計 (Secure by Design)

您正在為醫療科技公司處理 AI SaMD (如 DeepBT Detector-Plus) 的 FDA 送件，網路安全（Cybersecurity）架構審查極為嚴格。

* **防禦應用**：在設計地端 AI 醫療推論主機的底層架構時，**絕對應避免使用 Set-UID 程式**來讓前端介面存取高敏感的病患資料（PHI）。
* **建議架構**：應採用課堂提到的 **Service 架構**。前端的 UI (例如 Streamlit 介面) 應以最低權限 (Least Privilege) 運行，當需要調用後端 RTX 5080 GPU 進行 AI 推論或讀取醫療影像時，透過 FastAPI 或 gRPC (IPC 機制) 發送請求給後端受保護的 Inference Service。這能在 FDA 滲透測試報告中證明，即使前端遭到 RCE (遠端程式碼執行) 攻擊，攻擊者也無法直接取得系統 Root 權限。

### 3. Rust 開發中的權限操作

您目前使用 Rust 進行 Ubuntu 本機端的即時轉譯系統開發。當需要開發背景服務 Daemon 時，Rust 提供了極佳的安全性。

* 相較於 C 語言容易在處理 IPC 訊息時發生 Buffer Overflow，Rust 的記憶體安全特性天然免疫此類攻擊。配合 Linux 的 `systemd` 服務管理，您可以輕易打造出符合 Service Architecture 精神的堅固守護行程，徹底阻絕環境變數與 SUID 帶來的歷史包袱。
