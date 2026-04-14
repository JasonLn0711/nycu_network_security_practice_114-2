好。這一段不要背成零碎 API。
真正主線只有一句話：

**environment variable 是 process 的隱性輸入通道。**
它原本是為了方便把執行環境傳給程式；但一旦這些值會影響 **dynamic linker、shell、library、或 privileged program** 的行為，它就從「方便機制」變成「攻擊面」。而且這個攻擊面是系統層的，所以課綱把它放在 **System-level Attacks** 下面，不是意外。

## 一、什麼是 environment variable？

課程裡把它定義成：**一組動態命名值**，屬於 process 執行時的 operating environment，會影響 running process 的行為。它最早在 Unix 引入，後來 Windows 也採用。最典型的例子就是 `PATH`：當你執行一個命令卻沒寫完整路徑時，shell 會根據 `PATH` 去找那個程式在哪裡。

這裡最重要的，不是背「它是一組字串」，而是理解它的**角色**：
它不是程式的顯式參數，不在 `argv` 裡，不一定出現在 UI，也不一定出現在 config file。它常常是**看不見的輸入**。也就是說，一個程式表面上看起來沒有接收使用者輸入，實際上卻可能早就在吃使用者控制的 environment。這就是為什麼投影片特別強調 **Hidden usage of environment variables is dangerous**。

---

## 二、程式怎麼拿到 environment variables？

在 C 程式裡，常見有兩種方式：

第一種，是從 `main()` 的參數取得，也就是常見的 `envp`。
第二種，是用全域變數 `environ`。課程特別說 `environ` 比較可靠，因為 `envp` 只在 `main()` 裡可見，而且一開始 `envp` 跟 `environ` 雖然指向同一塊資料，但如果之後有新增或修改 environment variable，系統可能把 environment storage 搬到 heap，這時 `environ` 會更新，`envp` 不會。也就是說，**`envp` 更像初始快照，`environ` 才是當前狀態**。

這個細節很容易被忽略，但它很重要。因為它告訴你：
environment 不是一個抽象的「名字對值的映射」而已，它有**實際的記憶體位置與生命周期**。一旦程式中途更動 environment，原本你以為穩定的 pointer 可能就不再代表當前真相。

---

## 三、environment 是怎麼傳下去的？

這是整段最關鍵的機制。

一個 process 取得 environment，主要有兩種路徑：

**第一條：`fork()`**
如果用 `fork()` 建立 child process，child 會**繼承 parent 的 environment variables**。也就是說，environment 會隨著 process tree 往下傳。

**第二條：`execve()`**
如果一個 process 在自己身上跑新程式，通常會用 `execve()`。這時原本的 address space 會被新程式覆蓋，所以舊的 environment 也會消失；但 `execve()` 可以用第三個參數，把一組新的 environment 明確傳給新程式。課程用 `/usr/bin/env` 當例子，說明可以刻意建構一個新 environment 並傳給被執行的程式。

所以 environment 不是系統全域狀態，它其實是：

**每個 process 自己帶著的一包環境資料，透過 inheritance 或 explicit passing 傳遞。** 

把它畫成流程就是：

使用者 shell
→ export 成 environment
→ `fork()` 時 child 繼承
→ `execve()` 時可丟掉舊環境並傳入新環境
→ 新程式、dynamic linker、libraries 再根據這份 environment 決定行為。 

---

## 四、shell variable 跟 environment variable 不是同一件事

很多人這裡直接混掉，然後整題就死。

**shell variable** 是 shell 自己內部用的變數。
**environment variable** 是 shell 會帶給 child process 的那部分變數。

課程強調：當 shell 啟動時，它會把 environment variables 複製成自己的 shell variables。但反過來不成立——你在 shell 裡改一個 shell variable，**不代表 child process 看得到**。只有被 export 的變數，才會進入 child process 的 environment。投影片用例子指出：某些變數會進 child process，某些不會，原因不是名字不同，而是 **有沒有被 export**。

這件事的本質是：

**child process 看見的是 environment，不是整個 shell state。** 

這也是為什麼 `env` 命令常讓人誤判。課程補充說，在 bash 裡執行 `env` 時，shell 其實是啟動一個 child process 來跑它，所以它印出的是 child 的 environment；而 `/proc/<pid>/environ` 這個虛擬檔案則能直接看到某個 process 的 environment。像 `strings /proc/$$/environ` 會顯示當前 shell process 的 environment。

---

## 五、為什麼它會變成 attack surface？

因為**使用者可以在程式啟動前先設定 environment variables**。
如果這些值會影響程式行為，那它們本質上就是 untrusted input。投影片直接講得很白：隱性使用 environment variables 是危險的；因為使用者能設定它們，所以它們會成為 **Set-UID programs 的 attack surface**。

這裡一定要搭配 Set-UID 才看得出危險。
Set-UID 的意思是：使用者執行程式時，程式可以暫時用**程式擁有者**的權限跑。Linux 中每個 process 有 `RUID` 與 `EUID`；`RUID` 是真正執行者，`EUID` 是 access control 用的有效身分。一般程式執行時兩者相同；Set-UID 程式執行時，`RUID` 還是一般使用者，但 `EUID` 可能變成 root。也就是說，**使用者提供 environment，卻讓高權限程式來消費它**。這就是 privilege boundary。

一句話總結：

**不可信的 environment + 被提升的權限 = 系統級攻擊面。**

---

## 六、第一大攻擊面：dynamic linker

這是整段最核心的攻擊來源之一。

課程先對比 **static linking** 與 **dynamic linking**。
static linking 在編譯時就把需要的 library code 合進可執行檔，所以檔案會大很多。dynamic linking 則把連結延到 runtime；程式先載入 executable，之後再由 shared library 與 dynamic linker 完成解析。課程還提到可以用 `ldd` 看一個程式依賴哪些 shared libraries，並指出 **dynamic linker 自己也是 shared library，而且它在 `main()` 執行之前就先跑了**。

這個設計很省記憶體、很彈性，但代價很直接：

**程式有一部分行為，在 compile time 其實還沒決定。**
如果使用者能影響這個 runtime linking 的結果，就有機會破壞程式完整性。投影片原句就是：dynamic linking saves memory，但也意味著 part of the program’s code is undecided during compilation time；若使用者能 influence the missing code，就能 compromise integrity。

### `LD_PRELOAD` / `LD_LIBRARY_PATH` 為什麼危險？

課程的 case study 1 直接點名兩個環境變數：

* `LD_PRELOAD`：指定一組 shared libraries，讓 linker 優先搜尋
* `LD_LIBRARY_PATH`：指定額外 library 搜尋路徑 

對普通程式來說，這等於把某些函式的實作權交給使用者。如果程式是動態連結的，使用者可以讓 linker 先載入他指定的 library，於是某個原本來自 libc 的函式，可能先被別的版本攔截。課程用 `sleep()` 當例子，就是在說：**你以為你呼叫的是系統函式，實際上 linker 可能先幫你接到別的實作去。** 

這件事對 normal programs 已經足夠危險；對 Set-UID programs 就更危險。
所以 dynamic linker 有防禦：當 `EUID` 與 `RUID` 不同時，會忽略 `LD_PRELOAD` 與 `LD_LIBRARY_PATH`。也就是進入 secure execution context 時，這兩個變數不再可信。

但不要犯低級錯誤：
**忽略兩個變數，不代表 environment variable 攻擊整體被解決。**
它只代表這兩個最明顯的 linker-based 向量被封了一部分。

---

## 七、為什麼課程還要講 OS X 的 `DYLD_PRINT_TO_FILE`？

因為這個案例在告訴你：
**問題不只是“能不能換 library”，而是“environment 能不能驅動 privileged runtime 做額外事情”。** 

課程 case study 2 說，OS X 10.10 在 dynamic linker `dyld` 加入了 `DYLD_PRINT_TO_FILE` 這個 environment variable，允許使用者指定輸出檔名。表面看只是 debug 功能；但如果目標是 Set-UID 程式，`dyld` 會在 elevated privilege 下開那個檔案。更糟的是，投影片指出這裡出現 **capability leak**：檔案 descriptor 沒有被關閉。這表示即使後面的程式把 privilege 降下來，**已經拿到的特權資源仍然留著**。

這個案例要你學到的，不是某個 OS X 細節，而是兩個更深的原理：

第一，**privilege 不只存在於 UID/GID，也存在於已經開啟的資源與 descriptor。**
第二，**只要 privileged runtime 受到 environment 驅動，就可能做出超出你原本設計預期的事。** 

---

## 八、第二大攻擊面：外部程式呼叫與 `PATH`

很多程式自己不直接用 environment variable，但它會去呼叫別的程式。這時 environment 仍然會咬你。

課程指出，應用程式常透過兩類方式叫外部程式：

* `exec()` family
* `system()` 

這裡差很多。
`system()` 不是直接執行你的目標程式，而是先呼叫 shell，再由 shell 去執行命令。投影片明講：`system()` 會透過 `execl()`，最後走到 `execve()` 去執行 `/bin/sh`；而 shell 的行為會受很多 environment variables 影響，其中最重要的就是 `PATH`。當命令沒有給完整路徑時，shell 會依 `PATH` 找它。

所以只要 privileged program 做了這種事：

* 叫 shell
* 命令沒寫絕對路徑
* 使用者可控制 `PATH`

那使用者就能影響「到底哪個程式被執行」。這不是表面上的使用者輸入問題，而是 **command resolution 被 environment 接管**。

課程對這段的結論非常明確：
**`execve()` 的 attack surface 比 `system()` 小，因為 `execve()` 不會叫 shell，因此不會被 shell 的 environment variables 影響。** 在 privileged program 裡呼叫外部程式時，應該用 `execve()`。

更深一層地說，這其實是在實踐同一個原則：

**不要把 code 跟 data 混在一起。**
命令名稱應由程式自己固定；使用者資料只能作為 argument。當 shell 參與解析時，資料與執行邏輯的邊界就變鬆了。

---

## 九、第三大攻擊面：library 本身也會讀 environment

這裡很多人完全沒想到。

程式可能沒有呼叫 `getenv()`，但它用到的 library 會。
課程的 case study 是 UNIX locale subsystem。當程式需要輸出翻譯訊息時，常透過 libc 裡的 `gettext()`、`catopen()` 等函式來取對應語系資源；而這整套機制依賴多個 environment variables，例如 `LANG`、`LANGUAGE`、`NLSPATH`、`LOCPATH`、`LC_ALL`、`LC_MESSAGES`。

這代表什麼？

代表**訊息內容本身，可能已經被使用者控制**。
如果程式後面又把這些訊息以不安全方式丟給 `printf()` 類函式，那就可能把 environment-controlled string 轉成 format string 攻擊入口。投影片講得很直：attacker can use format string vulnerability to format the `printf()` function。這不是說 environment variable 本身直接等於 format string 漏洞，而是它提供了**可控內容來源**，再搭配不安全程式碼，就變成 exploit chain。

課程也給出 countermeasure：某些 libc 版本在 Set-UID context 下，會顯式忽略 `NLSPATH` 這類變數。這是同一個邏輯——**進入 privilege boundary 後，原本方便的環境參數必須視為不可信。** 

---

## 十、第四大攻擊面：application code 自己直接讀 environment

這是最直白，也最常被低估的一種。

投影片的 case 是：程式用 `getenv("PWD")` 來知道目前目錄，然後把這個值複製到固定大小的陣列 `arr`，卻沒有檢查長度，結果變成 buffer overflow。重點不是 overflow 本身，而是 **`PWD` 並不是可信的系統真相，它只是 shell 提供的一個字串**。使用者可以改 shell variable，於是程式就把攻擊者提供的內容當成 metadata 在用。

這裡你一定要理解一個工程原則：

**environment variable 是輸入，不是事實。**
它頂多是「某個先前程式宣稱的環境資訊」，不是 kernel guarantee。凡是 privileged program 直接拿 `getenv()` 的輸出當可信設定、可信路徑、可信目錄、可信模式，再做記憶體操作、字串拼接、檔案開啟、命令執行，都在把隱性輸入當權威。這很蠢。

---

## 十一、`secure_getenv()` 到底在解決什麼？

課程在 countermeasure 那一段點出一個很重要的 API：`secure_getenv()`。
它跟 `getenv()` 幾乎一樣，差別在於：當系統認為目前屬於 **secure execution** 時，它直接回傳 `NULL`。投影片舉的 secure execution 條件之一，就是 process 的 `EUID` 與 `RUID` 不匹配，也就是典型的 Set-UID 情境。

這個 API 的思想很乾淨：

* 普通程式：可以方便讀 environment
* 特權程式：預設 fail closed，不要碰不可信環境 

這不是萬靈丹，但它把責任方向擺對了。
因為真正正確的問題不是「我要不要讀這個 env？」
而是「**在這個 privilege context 下，我有沒有資格相信它？**」

---

## 十二、架構層面的結論：Set-UID approach 為什麼比 service approach 危險？

這是整份講義最後真正該抓住的設計結論。

課程把 privileged operation 拆成兩種做法：

**Set-UID approach**：一般使用者直接執行一個特殊程式，暫時拿到高權限。
**Service approach**：高權限服務自己常駐執行，使用者只是發 request 給它處理。

為什麼 Set-UID 的 environment attack surface 特別大？
因為在 Set-UID 模型裡，**高權限程式是從使用者的 process context 啟動的**。使用者控制 command line、working directory、file descriptor、以及 environment。權限提升發生在這些輸入已經被包進啟動上下文之後。

而 service approach 比較安全，原因不是服務 magically 安全，而是 privilege boundary 放得比較對：
高權限服務通常以自己的乾淨環境啟動，使用者只能透過定義好的 request interface 送資料，而不是把整包 process execution context 一起塞給 privileged code。課程甚至直接寫：Set-UID approach 的 environment variables **cannot be trusted**；而 service approach 的 environment variables **can be trusted**。也因此 Android 乾脆移除了 Set-UID / Set-GID 機制。

這個設計結論，比單一漏洞重要得多：

**最好的防禦不是一直補 env var 黑名單，而是把 privilege boundary 從 user-launched program 改成 controlled service boundary。** 

---

## 十三、把整段壓成一個你考試能寫的模型

你可以把整個 environment variable 單元壓成下面這個流程：

1. Environment variables 是 process 的動態環境參數，會影響程式行為。
2. 它們會透過 `fork()` 繼承，或由 `execve()` 顯式傳遞。
3. Shell variables 不等於 environment variables；只有 export 的部分才會進 child process。
4. 危險在於 environment 是**隱性輸入**，而且很多元件會讀它：dynamic linker、shell、library、application code。
5. 在 privileged context，尤其 Set-UID，這些值來自低權限使用者，卻會影響高權限行為。
6. 典型風險包括：

   * dynamic linker search path / preload 類影響
   * shell 的 `PATH` resolution
   * locale / library 行為被控制
   * `getenv()` 直接成為 untrusted input
   * capability leak 與 privilege downgrade 交錯造成更深問題
7. 典型防禦包括：

   * 不信任 privileged program 的 environment
   * 必要時用 `secure_getenv()`
   * 不用 `system()`，改用 `execve()`
   * 絕對路徑
   * sanitize / whitelist environment
   * 能用 service approach 就不要用 Set-UID approach。

---

## 十四、最短背誦版

**Environment variable 本質上是 process 的隱性輸入。**
**危險不是它本身，而是它能在 `main()` 之前、shell 之內、library 之內、以及 privileged boundary 上改變程式行為。**
**Set-UID 最大問題，就是把使用者可控 environment 帶進高權限執行環境。**
**最常見攻擊面是 dynamic linker、`PATH`、locale library、以及直接 `getenv()`。**
**最可靠的防禦不是補洞，而是縮小 attack surface：`secure_getenv()`、`execve()`、絕對路徑、sanitize environment、改用 service model。**

接下來最合理的是把這份講義壓成 **考試標準答案版**，也就是：「老師會怎麼問、你要怎麼寫才拿分」。
