好。下面把 **malware 這一段完整重建成一份可讀、可背、可拿來應付考試的講義**。你現在不要把它當成一堆名詞，而要把它看成三條主線：

**定義是什麼 → 怎麼進來／怎麼傳 → 進來後做什麼壞事。**

這三條沒抓住，後面所有案例都只是雜訊。這份 Malware 投影片本身就是沿著這三條線在講：先講歷史，再講分類，再講 virus／worm／zombie／rootkit／keylogger／ransomware，最後講偵測與繞過偵測。

---

## 一、先把最上位概念釐清：什麼叫 malware？

**Malware** 就是帶有惡意目的、會違反系統安全政策的程式。重點不是它「寫得怪」，而是它的**目標**是未授權地存取、破壞、竊取、隱藏、勒索、控制，或利用別人的系統。這份講義把它拆成幾種典型形態：trapdoor、logic bomb、trojan horse、virus、worm、zombie／botnet、rootkit，後面還展示了 keylogger 與 ransomware。

理解 malware 最有效的方式，不是背定義，而是用四個問題去看每一個惡意程式：

1. **它需不需要宿主程式？**
2. **它會不會自己複製？**
3. **它怎麼傳播？**
4. **感染後的 payload 是什麼？**

你把這四個問題問完，virus、worm、trojan 的差異幾乎就清光了。

---

## 二、來龍去脈：malware 為什麼一路演化成今天這樣？

這份投影片前半段其實不是在叫你背年份，而是在告訴你 malware 的**演化方向**。最早期是「發現與實驗」：像 1981 的 Elk Cloner、1986 的 Brain、1988 的 Morris worm、1990 的第一個 polymorphic virus。這個時期重點是：惡意程式開始展示「可自我傳播、可感染系統、可用變形規避偵測」這些核心能力。

接著進入「轉型期」與「成名期」：例如 Michaelangelo、第一個 Word macro virus、CIH、Melissa、LoveLetter、Code Red、Nimda。這表示 malware 不再只是低階系統實驗，而是開始利用**大家真的會用的軟體與網路環境**：Word、e-mail、Web server、瀏覽器。也就是說，攻擊面從 boot sector 與本機檔案，擴大到使用者文件、電子郵件、網路服務與 Web。

再往後就是「大規模網路犯罪時代」：Zeus、Storm、Conficker、Koobface、Aurora、Stuxnet。這一階段的本質改變只有一句話：

**malware 從炫技，變成產業。**

不再只是「我能感染你」，而是「我能用你賺錢、偷帳密、組 botnet、做 DDoS、做工控破壞」。這就是為什麼你在後面看到的 payload 會集中在：憑證竊取、垃圾郵件、DDoS、後門、滲透控制、勒索與破壞。

---

## 三、分類總圖：你要先知道每一類到底在系統裡扮演什麼角色

### 1. Trapdoor / Backdoor

Trapdoor 是**秘密入口**。也就是系統裡藏了一個繞過正常驗證流程的入口，可能是一組特殊帳號、密碼，或某個未公開的呼叫路徑。投影片特別說這種東西常被開發者使用，甚至可能被藏進 compiler。它的危險不在於複製，而在於**繞過正常安全程序**。

### 2. Logic Bomb

Logic bomb 是**藏在合法程式中的延遲觸發惡意邏輯**。平常不動，等到特定條件滿足才發作，例如某個日期、某個使用者存在與否、某個檔案是否出現。投影片給的定義很直接：嵌在合法程式中、在特定條件滿足時觸發、典型結果是刪檔或破壞系統。重點是它不是靠傳播取勝，而是靠**條件觸發**。

### 3. Trojan Horse

Trojan horse 的核心不是複製，而是**偽裝**。它表面上做一件你期待的事，但暗地裡做另一件違反安全政策的事。投影片把它定義成具有 overt effect 與 covert effect 的程式：明面上的功能正常，隱藏效果才是問題；而且使用者是被騙去執行它，所以惡意動作常帶著使用者的授權一起發生。這是它最毒的地方。

### 4. Virus

Virus 是**需要宿主、能感染宿主、會自我複製的惡意碼**。它通常改寫原本正常的程式、文件或開機區塊，把自己嵌進去。宿主被執行時，virus 也就跟著運作。投影片明確說 virus 會把正常程式改成 infected version，通常試圖保持隱蔽，並在感染程式被執行時運作。

### 5. Worm

Worm 是**不需要宿主、能獨立執行、會自己找下一個受害者的惡意程式**。它可以自己掃描、自己利用漏洞、自己複製到別台機器，再展開 payload。投影片很清楚：worm runs independently，不需要 host program，會把一份完整可執行的自己傳到其他機器，並且典型流程是 Probing → Exploitation → Replication → Payload。

### 6. Zombie / Botnet

這是一種**被控制的受害主機集合**。個別主機被植入 agent 後，會「phone home」連回 master server，之後可被統一指揮去做 DDoS、spam、phishing、cracking 等。這裡重點不是單一惡意程式，而是**控制架構**。惡意程式的價值變成：把大量主機轉成可編排的算力與頻寬。

### 7. Rootkit

Rootkit 是**入侵之後用來隱藏自己、維持控制權、方便再次進入的軟體**。投影片直接寫：用途是 hide attacker’s presence，provide backdoors for easy reentry。它不是一定負責初始感染，而是負責**隱身與持久化**。

---

## 四、你最該牢記的三個：Trojan、Virus、Worm 到底差在哪？

這三個最容易混。你要用「宿主、複製、傳播」三個維度分。

### Trojan

Trojan 不以自我複製為本質。它的本質是**騙你執行**。
它可以長得像正常工具、修復程式、文件附件、看似無害的應用，真正關鍵是它藉由使用者的信任與授權完成惡意動作。

### Virus

Virus 會複製，但通常是靠**感染別的宿主**來複製。
它不需要主動掃網路，只要有人帶著受感染的可執行檔、巨集文件或 boot media 去執行，它就有機會擴散。

### Worm

Worm 會複製，而且通常是靠**網路自主擴散**。
它不等人幫它搬運，它自己找目標、自己打洞、自己進去、自己複製。這也是為什麼 worm 的爆發速度通常遠高於 virus。

一句話硬背版：

**Trojan 靠騙。Virus 靠感染宿主。Worm 靠網路自傳。**

---

## 五、Virus 深入講：它怎麼活、怎麼傳、怎麼躲？

### 1. 核心定義

Virus 是 self-replicating code，但它不是像 worm 那樣整包獨立跑，而是「像會複製的 trojan」。它的工作流程大致是：找到目標檔案、判斷是否未感染、修改目標把自己塞進去、做惡意動作，再把原本正常程式繼續執行。也就是說，它一邊寄生、一邊偽裝成正常行為。

### 2. 典型感染向量

投影片列出三個最典型的 infection vectors：

* **Boot sector**：感染開機區。這類 virus 一開機就可能先於作業系統主邏輯運作。
* **Executable**：感染 .exe、.dll、.sys 等可執行檔。
* **Macro files**：感染 Word 等文件巨集。

這三種其實對應三個時代：早期靠磁碟與開機媒體，之後靠可執行檔，後來靠大家最常交換的辦公文件。

### 3. 為什麼 virus 很難抓？

因為它不只是複製，它還會**隱藏**。投影片列了四種重要能力：

**Terminate and Stay Resident (TSR)**：程式結束後仍停留在記憶體裡，攔截執行流程或持續感染其他檔案。
**Stealth**：隱藏感染痕跡，例如讀檔時回傳乾淨內容，執行時才放出感染版本。
**Encryption**：把病毒主體加密，避免被固定 signature 抓到。
**Polymorphism / Metamorphism**：每次產生不同外觀。前者通常是加密主體固定、解密器變；後者連程式本身結構都改成語意等價但樣子不同。

### 4. Encryption、Polymorphism、Metamorphism 的差異

這三個常考，而且很多人背混。

**Encryption**：主體被加密，但解密邏輯可能固定。偵測者仍可找固定解密 stub。
**Polymorphism**：解密邏輯也在變，所以 signature 更難下。
**Metamorphism**：更狠，連自身指令序列都重寫成不同但等價的形式，不一定依賴加密。

所以難度是：
**Encryption < Polymorphism < Metamorphism**。

---

## 六、Worm 深入講：為什麼它是網路時代最兇的東西？

### 1. 核心定義

Worm 是獨立執行的惡意程式，不需要 host。它能把一個完整可用的自己複製到其他機器，並在受害主機上繼續找新目標。這讓它的擴散速度呈指數型成長。

### 2. Worm 的四階段模型

投影片直接給你最重要的流程：

**Probing → Exploitation → Replication → Payload**

這四段非常重要。考試若問 worm，你照這個回答最穩。

* **Probing**：掃描誰可能有洞。
* **Exploitation**：利用漏洞進去。
* **Replication**：把自己複製／丟過去。
* **Payload**：開始偷帳密、發垃圾信、組 DDoS、留後門等。 

### 3. Morris worm 為什麼是經典？

因為它把 worm 的幾個本質一次講清楚。投影片指出 Morris worm 是 1988 年第一個 Internet 上的大型 worm，也是第一個利用 buffer overflow 的知名案例。它不是靠單一路徑，而是同時利用 Unix 服務弱點、trusted logins、weak passwords 等方式擴散。

更重要的是，Morris worm 告訴你一個考點：

**Worm 不一定要「刪檔」才有傷害。**
單是大量複製、重複感染、吃光 CPU、網路頻寬與系統資源，就足以造成重大停機與清理成本。投影片明講：Morris 的直接破壞不在刪檔，而在 replication 與系統負載，導致大量系統關閉防止進一步擴散。

### 4. 為什麼後來 worm 傳播越來越快？

後面的 Code Red、SQL Slammer、Nimda 幾乎都在回答這件事。原因很簡單：

* 目標服務越來越多直接暴露在網路上
* 漏洞利用可完全自動化
* 掃描與複製邏輯更精簡
* 傳播媒介更多元（IIS、e-mail、shared drives、browser bug、network service）

投影片甚至直接比較：Code Red 在 14 小時內感染大量脆弱主機；SQL Slammer 把易受害族群在不到 10 分鐘內打滿。這不是因為它「更邪惡」，而是因為它更接近理想化的自動化傳播機器。

### 5. Email worm 是什麼？

Email worm 是 worm 的一個傳播分支。它透過電子郵件附件或訊息內容自我散播。Mydoom、Storm 都是投影片上的代表案例。這說明 worm 的本質不是只限於掃 port；只要能**自動找到下一個受害者並把自己送出去**，都可算 worm。

---

## 七、Trojan horse 深入講：為什麼它常比 virus 更陰？

Trojan horse 的難點在於，它常常不靠技術漏洞，而靠**人類判斷失誤**。投影片給的例子本質上是在說：攻擊者提供一個看起來像正常工具的程式，使用者執行時看到表面預期功能正常，但程式暗中做了不該做的事。這代表：

1. 惡意動作是在**使用者授權上下文**裡完成的。
2. 系統表面看起來是「合法執行」。
3. 問題常不是 access control 被直接打穿，而是信任鏈被利用。 

Trojan 最常見的幾種來源你可以自己腦中補成一張圖：
假更新、假修復工具、假附件、假破解器、假防毒程式、假登入頁。投影片裡也提到「Nimda fix Trojan」這種假冒安全公告與移除工具的例子。這就是 trojan 的典型精神：**看起來像在幫你，實際上在利用你。** 

---

## 八、Payload：惡意程式進來之後，到底做什麼？

這一段很重要。因為**傳播方式不是目的，payload 才是目的**。

### 1. Backdoor

讓攻擊者之後更容易再進來。這類 payload 追求的是持久控制，而不是立即大破壞。worm 與 trojan 都可能帶 backdoor。

### 2. Credential theft

偷帳密、銀行資訊、使用者憑證。投影片在 Zeus、Storm、Mebroot 等案例裡都強調 credential stealing。這類 payload 的經濟價值很高。

### 3. Spam relay / Botnet workhorse

把受害機器變成垃圾信發送點或 botnet 節點。這種 payload 不一定讓單一受害者覺得自己「壞掉」，但整體上很有規模經濟。

### 4. DDoS

利用大量 zombie 主機對目標發送洪水流量，讓正常使用者無法服務。投影片在 zombie / botnet 六步驟圖中把這個流程畫得很清楚。

### 5. Stealth / Persistence

例如 rootkit，重點不是立刻攻擊，而是躲起來、不要被看見、留下再次進入的手段。

### 6. Sabotage / Destruction

例如 logic bomb 觸發刪檔、破壞 boot sector，甚至像 Stuxnet 這類針對工控系統的定向攻擊。這類 payload 的目標是破壞可用性或實體流程。

### 7. Ransomware

把資料加密，要求贖金。投影片最後一頁直接給了典型勒索畫面：你的檔案被加密、要付款才能解密。這本質上是把「資料可用性」直接拿來變現。

---

## 九、Zombie / Botnet：把單機惡意變成軍隊

投影片第 34–39 頁其實就是一個 botnet 指揮鏈的標準模型。它分成六步：

1. 攻擊者掃描網路上可被攻陷的系統。
2. 在這些機器上安裝 zombie agent。
3. zombie agent 回連 master server。
4. 攻擊者對 master server 下指令。
5. master server 命令所有 zombies 發動攻擊。
6. 目標系統被大量請求淹沒，正常使用者被拒絕服務。 

這裡最該理解的是：botnet 的價值在於**集中控制**。
單一惡意主機能力有限；但如果你能控制幾萬台，就可以做 DDoS、發垃圾信、散播 phishing、做挖礦、做代理跳板。這就是 malware 商業化之後最核心的基礎設施。

---

## 十、Rootkit：為什麼有些惡意程式你就是看不到？

Rootkit 的定位不是「一定先感染你」，而是**感染之後讓你以為沒事**。投影片把 rootkit 分成幾層：

* **Traditional rootkit**：修改使用者層工具，例如 `ls`、`ps`、`ifconfig` 之類，讓你用一般工具看不到異常。
* **Kernel-level rootkit**：改核心本身或核心模組，從更底層攔截資訊。
* **Application-level rootkit**：在應用層做隱藏。
* **Under-kernel rootkit**：更底層，例如惡意 VMM。 

越底層越麻煩，因為你在上層看到的現象都可能已經被它改寫。投影片也提到簡單 rootkit 可能會被 Tripwire 這類工具查出來，但 kernel 級或更低層的就很難從 userland 發現。這裡你要記住的不是工具名字，而是原理：

**檢查工具如果跑在被汙染的視角上，它看到的世界也可能是假的。** 

---

## 十一、Keylogger：一種很典型的 payload

投影片後段用 keylogger 範例說明 malware 不一定追求大爆炸，它可能只想**靜靜記錄你的輸入**。使用者以為自己只是在瀏覽器裡輸入資料，實際上鍵盤事件已被另一個元件攔截、紀錄，再透過共享記憶體或其他 IPC 傳回惡意程式。這類 payload 特別適合偷帳密、信用卡資料與敏感輸入。

你要把 keylogger 看成 payload 類型，而不是獨立分類的核心代表。它告訴你的是：**malware 的目的常是資料竊取，而不是立即破壞。** 

---

## 十二、偵測與對抗：為什麼偵測一直是攻防拉鋸？

投影片在後面把偵測大致分成 **static analysis**。它列出 signature、hash、string pattern、regular expression、static decryptor、packer code，並提到像 ClamAV 這類簽章式偵測。這代表最直觀的防禦方式是：

**找到惡意程式穩定不變的特徵。** 

問題是，malware 作者也知道這件事，所以才有前面講的 encryption、polymorphism、metamorphism。它們本質上都在做同一件事：

**讓你找不到穩定特徵。**

* 你找固定字串，我就加密。
* 你找固定解密器，我就把解密器也改掉。
* 你找固定程式結構，我就做 metamorphic rewriting。

這就是為什麼 malware detection 永遠不是「找到一次特徵就永遠贏」。投影片最後幾頁用這三種 evasion 直接對應前面的簽章式偵測困難。

---

## 十三、你考試最該會寫的三個標準答案

### 題型 1：Explain the difference between virus, worm, and Trojan horse.

標準寫法：

Virus 是需要宿主程式的自我複製惡意碼，透過感染可執行檔、boot sector 或文件巨集來散播；宿主執行時病毒跟著運作。
Worm 是不需要宿主、可獨立執行的惡意程式，通常經過 probing、exploitation、replication、payload 四階段透過網路自動傳播。
Trojan horse 的核心不是自我複製，而是偽裝成正常程式，讓使用者主動執行，表面提供預期功能，暗中做未授權行為。

### 題型 2：What is propagation? What is payload?

Propagation 是惡意程式從一個系統擴散到下一個系統的方法與流程，例如感染檔案、郵件附件、網路掃描、自動利用漏洞。
Payload 是惡意程式成功執行後的實際惡意目的，例如後門、DDoS、垃圾郵件、竊取帳密、rootkit 隱藏、勒索。

### 題型 3：Why are worms often more dangerous in network environments?

因為 worm 不需要宿主，可獨立執行，且能自動掃描、利用漏洞與複製自身，因此傳播速度極快，容易在短時間內造成大規模感染、資源耗盡、服務中斷與 botnet 建立。Morris、Code Red、SQL Slammer 都是這類現象的代表。

---

## 十四、最後幫你壓成一個腦中模型

整段 malware，你只要牢記下面這個骨架：

**入口**：是騙你執行，還是自己打洞進來？
**依附**：是寄生宿主，還是獨立運作？
**擴散**：是靠感染檔案，還是靠網路自動傳播？
**目的**：是偷資料、控制主機、隱藏蹤跡、做 DDoS，還是勒索？

把這四層套上去：

* Trojan：騙你執行。
* Virus：寄生宿主並感染。
* Worm：獨立、掃描、利用、複製。
* Zombie：被納入遠端控制網。
* Rootkit：躲起來，留下控制權。
* Ransomware：把可用性變現。 

---

## 十五、你現在最該背的極短版

**Trojan 靠偽裝。Virus 靠感染宿主。Worm 靠自主網路傳播。**
**Propagation 是怎麼擴散；payload 是進來後做什麼。**
**Rootkit 負責隱藏；botnet 負責集中控制；ransomware 負責勒索。** 

下一步最合理：直接進入 **malware 題型演練**，我把這份講義轉成「考卷會怎麼問、你要怎麼答」。
