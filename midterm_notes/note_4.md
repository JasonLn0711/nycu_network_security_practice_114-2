# Access Control 與 Bell-La Padula 筆記

這份版本改成比較適合台灣高中生閱讀的白話說法。

目標不是只背：

- `no read up`
- `no write down`
- DAC
- MAC
- ACL
- capability

而是真的知道：

- access control 到底在解什麼問題
- 為什麼光有 DAC 不夠
- Trojan horse 為什麼會讓機密外洩
- BLP 到底是在補哪個洞
- 它為什麼重要
- 它又為什麼不是最後答案

---

## 先講一句最重要的

**Access control 是整個保護機制的骨架。**

它在回答：

**誰，可以對什麼，做什麼。**

而 BLP（Bell-La Padula）不是另一個完全分開的章節，
它是架在 access control 上面、
專門處理「機密資訊不能亂流出去」的一個模型。

所以正確順序不是先死背：

- `no read up`
- `no write down`

而是先懂：

1. access control 想保護什麼
2. 為什麼 DAC 有洞
3. 為什麼 Trojan 會利用這個洞
4. BLP 怎麼用標籤把這個洞補起來

---

## 一、先從最上位概念開始：Security Policy 和 Security Model

這兩個超容易混，但其實不一樣。

### Security Policy 是什麼？

Security policy 是：

**你真正想遵守的安全規則。**

也就是：

「什麼可以，什麼不可以。」

例如：

- 一般學生不能改學校伺服器時間
- 只有某些老師能看成績系統
- 只有特定網段可以用某個付費資料庫

這些都叫 policy。

### Security Model 是什麼？

Security model 是：

**把 policy 抽象化、形式化，變成可推理的模型。**

它不會把現實世界所有細節都留下來，
而是只保留那些和安全推理最有關的部分。

### 白話理解

你可以把 policy 想成：

「學校規定。」

把 model 想成：

「為了檢查這個規定是否合理，我們畫出來的一張規則藍圖。」

### 很重要的一句

**model 是藍圖，不是實際大樓。**

也就是說：

- 模型看起來安全

不代表

- 真正的系統就一定安全

因為現實世界還會有：

- 實作 bug
- side channel
- covert channel
- 設計沒考慮到的細節

### 這裡最重要的觀念

**模型可以是安全的，但實際系統仍可能不安全。**

---

## 二、Access Control 的核心問題：誰對什麼做什麼

這章最基本的骨架可以壓成一句：

**某個主體，是否有權限，對某個目標，做某個動作？**

課程裡會拆成四個詞：

- user
- principal
- subject
- object

這四個不能混。

---

## 三、User、Principal、Subject、Object 到底差在哪？

### 1. User

User 就是真實世界的人。

例如：

- Joe
- Jane

這是「現實身分」。

### 2. Principal

Principal 是授權單位。

它比較像：

**系統拿來做權限判斷的身分。**

同一個 user 可以有多個 principals。

例如同一個人可以同時有：

- `JOE.TOP-SECRET`
- `JOE.SECRET`
- `JOE.UNCLASSIFIED`

或是：

- `JANE.FACULTY`
- `JANE.CHAIRPERSON`
- `JANE.SUPER-USER`

### 為什麼同一個人要有多個 principal？

因為同一個人可能在不同情境扮演不同角色。

### 白話理解

像同一個老師在學校裡可能同時是：

- 普通老師
- 導師
- 系主任

不同角色看到的資料、能做的事也不同。

所以不要只用「同一個人」去想，
而是要用「同一個人目前以什麼角色或安全等級行動」去想。

### 3. Subject

Subject 是：

**代表 principal 正在執行的程式。**

也就是會真的發出 access request 的東西。

例如：

- mail application
- database program
- word processor

### 白話理解

Principal 比較像「你現在拿的是哪一張工作證」。

Subject 比較像「你現在真的派出去辦事的那個人或那個程式」。

### 4. Object

Object 是 subject 可以操作的東西。

例如：

- file
- directory
- memory segment
- device

甚至某些情況下，
另一個 subject 也可能成為 object，
例如被 suspend、kill、resume。

### 最短記法

- User：真實世界的人
- Principal：授權身分
- Subject：正在執行、發出存取請求的程式
- Object：被操作的東西

---

## 四、Reference Monitor 是什麼？

有了上面那些概念後，
你還需要一個真正決定：

「這次能不能存取？」

的東西。

那就是 reference monitor。

### 它的工作是什麼？

當某個 subject 想對某個 object 做某件事時，
它來回答：

- 可以
- 不可以

### 課程為什麼很重視它？

因為如果你說有 access control，
但實際上任何人都能繞過那個檢查，
那就不是真正的安全邊界。

### 一個合格的 reference monitor 應該有三個特性

1. tamperproof

不能被隨便改掉。

2. non-bypassable

不能被繞過。

3. verifiable

你要能檢查、驗證它真的有照規則做。

### 白話理解

像學校門口警衛系統如果要有用，
至少要滿足：

- 不能讓學生隨手關掉
- 不能旁邊還有一個沒人管的小門
- 學校要能確認它規則真的正確

不然那個警衛系統只是擺好看的。

---

## 五、Access Matrix：把 access control 畫成一張表

這是整章很核心的抽象。

你可以把 access matrix 想成一張大表格：

- 行是 subjects
- 列是 objects
- 每個格子裡寫 rights

例如：

- subject A 對 file X 有 `read`
- subject A 對 file Y 有 `write`
- subject B 對 file Y 有 `read`

### 白話理解

像教務系統裡有一張表：

- 哪個人
- 對哪份資料
- 可以做什麼

例如：

- 老師能看成績
- 助教能輸入成績
- 學生只能看自己的成績

這就是 access matrix 的味道。

### 它為什麼重要？

因為後面很多東西：

- ACL
- capability
- DAC
- MAC
- BLP

其實都可以看成是在這張大表上用不同方式管理權限。

---

## 六、ACL、Capability、Triples：同一張矩陣的三種落地方式

課程常說 access matrix 很漂亮，
但真實系統不一定真的用一張超大表存它。

所以會有不同落地方式。

---

## 七、ACL 是什麼？

ACL 是 Access Control List。

它可以想成：

**每個 object 自己帶一份名單，寫誰能對我做什麼。**

### 也就是說

ACL 是從 object 角度出發。

問題變成：

**這個檔案允許哪些人做哪些事？**

### 白話理解

像一間教室門口貼一張表：

- 老師可進
- 助教可進
- 學生不可進

這就是 ACL 的感覺。

### ACL 的優點

- 你想檢查某個 object 開放給誰時很方便
- 你想撤銷某個 object 的權限時很方便

### UNIX 那種 owner / group / other 算什麼？

它可以看成一種簡化版 ACL。

---

## 八、Capability 是什麼？

Capability 可以想成：

**每個 subject 自己拿著一堆權限 token。**

它是從 subject 角度出發。

問題變成：

**這個 subject 目前手上拿著哪些可用權限？**

### 白話理解

像不是每間教室門口貼名單，
而是每個人自己手上拿著幾把鑰匙和通行證。

他有哪把鑰匙，
就能開哪扇門。

### Capability 的優點

- 你想檢查某個 subject 目前擁有哪些權限時很方便
- 對動態建立、生命週期短的 subject 很有用
- 很適合談 least privilege

---

## 九、ACL 和 Capability 的本質差異

這裡是很常考的重點。

### ACL 的邏輯

**你是誰？我查名單。**

所以它很依賴：

- authentication

也就是你得先知道這個 subject 是誰。

### Capability 的邏輯

**你手上有沒有合法 token？我認 token。**

所以它比較依賴：

- capability 不可偽造
- capability 的傳播要能控制

### 白話理解

ACL 比較像門口保全看你的名字有沒有在名單上。

Capability 比較像保全看你手上的票是真是假。

### 最短記法

**ACL 是 object-centric 的名單式控制。**

**Capability 是 subject-centric 的持有式控制。**

---

## 十、Access Control Triples 是什麼？

這個比較像把整張 matrix 攤平成很多筆資料。

格式像：

`(Subject, Access, Object)`

例如：

`(Alice, read, file1)`

### 白話理解

像資料庫裡不是畫一張大表，
而是一筆一筆記錄：

- 誰
- 對哪個東西
- 有哪種權限

這種做法常見在 relational DBMS 裡。

---

## 十一、DAC 和 MAC：兩種完全不同的控制哲學

這一段是整章真正的核心之一。

因為 BLP 會出現，
就是因為 DAC 不夠。

---

## 十二、DAC 是什麼？

DAC 是 Discretionary Access Control。

它的核心精神是：

**subject 只要持有某種權利，就可以依自己的裁量使用它。**

簡單講就是：

- 你有權限
- 你就能用

而且很多時候你還能把這種權限再分享、再轉交。

### 白話理解

像你拿到某份講義的閱讀權，
老師沒有再多管你之後怎麼用，
你可能：

- 自己看
- 傳給別人
- 抄到別的地方

這就是 DAC 比較偏「由持有者自己裁量」的感覺。

### 常見例子

很多傳統檔案系統權限就是 DAC 思維。

---

## 十三、MAC 是什麼？

MAC 是 Mandatory Access Control。

它的核心精神是：

**不是你有權限就夠了，系統還要看安全標籤和強制規則。**

也就是：

- subject 想不想這樣做不重要
- 系統規則允不允許才重要

### 白話理解

像你即使是老師，
也不代表你想把某份機密文件給誰看就給誰看。

因為學校或政府可能額外規定：

- 只有某安全等級以上的人能看
- 某些類別資料不能流到較低等級

這就是 MAC 的味道。

### 最短差異

**DAC 比較像持有者裁量。**

**MAC 比較像系統強制。**

---

## 十四、為什麼 DAC 不夠？

課程最想讓你看到的問題是：

**DAC 會管 access，但不真正管 information flow。**

這句很重要。

### 什麼意思？

假設某個 subject：

- 可以讀高敏感檔案 F
- 也可以寫低敏感檔案 G

那它就可能把 F 的內容複製到 G。

從 DAC 角度看，
每一步都合法：

- 讀 F 合法
- 寫 G 合法

但從機密性角度看，
事情已經炸了。

因為本來不能看到 F 的人，
現在可以透過 G 間接看到 F 的內容。

### 白話理解

像某老師可以看機密會議紀錄，
也可以在學校公告欄貼一般通知。

如果他把機密內容抄到公告欄，
那每個動作在表面上都可能有權限，
但秘密還是洩漏了。

### 這就是 DAC 的根本洞

**它只看“你能不能做這個動作”，不夠關心“資訊最後流到哪裡”。**

---

## 十五、Trojan Horse 為什麼會把 DAC 打穿？

這段是 access control 和 BLP 之間最重要的橋樑。

課程一直提 Trojan，
不是離題，
而是因為 Trojan 剛好證明了 DAC 的弱點。

### 經典場景

假設：

- File F 是高敏感資料
- Principal A 能讀寫 F
- File G 是低敏感資料
- A 能寫 G
- B 能讀 G，但不能讀 F

此時 A 執行一個看起來正常的程式，
但那其實是 Trojan horse。

Trojan 做的事很簡單：

1. 用 A 的合法權限讀 F
2. 用 A 的合法權限寫 G

結果：

- B 雖然不能讀 F
- 卻能透過 G 讀到 F 的內容

### 這裡每一步都有違法嗎？

沒有。

這就是最可怕的地方。

DAC 看的是：

- 你有沒有權利讀 F
- 你有沒有權利寫 G

答案都可能是有。

但整體資訊流還是出事了。

### 白話理解

像你信任某位老師能看機密文件，
也信任他能在公開板發布消息。

但如果他電腦裡有一個假裝是正常工具的 Trojan，
那個程式就會利用老師本來就有的合法權限，
偷偷把機密內容抄到公開板上。

### 這段最重要的一句

**使用者也許是可信的，但 subject 不一定可信。**

也就是：

- 人本身不一定想洩密
- 但他執行的程式可能會替他洩密

---

## 十六、BLP 為什麼會出現？

到了這裡，
你就會知道 BLP 不是憑空冒出來的。

它是為了補 DAC 的洞。

### BLP 在解什麼問題？

它主要處理的是：

**confidentiality**

也就是機密性。

更精準地說，
它處理的是：

**高敏感資訊不能流到低敏感主體或低敏感物件。**

### 它特別適合哪種情境？

Multilevel Security（MLS）。

也就是系統裡有不同安全等級，
例如：

- Top Secret
- Secret
- Confidential
- Unclassified

### 白話理解

像某系統裡不同文件分成：

- 絕密
- 機密
- 內部
- 公開

BLP 就是在管：

「這些不同等級的資料之間，能不能流來流去？」

---

## 十七、Security Label 是什麼？

在 BLP 裡，
每個 subject 和 object 都可能帶有 security label。

### 對 subject

常會講 clearance，
也就是它能接觸到什麼等級。

### 對 object

常會講 classification，
也就是這份資料本身的敏感等級。

### 白話理解

像人身上有工作證等級，
文件身上也有保密標章。

系統要決定能不能存取時，
就會比對：

- 這個人現在的等級
- 這份資料的等級

---

## 十八、BLP 的 label 不只是高低，還有 categories

很多人一學到 BLP，
就只記：

- Top Secret
- Secret
- Confidential
- Unclassified

但完整一點的 label，
常常不只是一個上下高低而已。

它還可能帶 categories / compartments。

例如：

- `(Top Secret, {army, navy})`
- `(Secret, {army})`
- `(Secret, {navy})`

### 這代表什麼？

不只是等級高低要符合，
類別也要符合。

如果用比較正式的寫法，
常會寫成：

`(e1, C1) <= (e2, C2)` 當且僅當：

- `e1 <= e2`
- `C1 ⊆ C2`

也就是：

- 等級不能比較高
- 類別集合也不能超出對方

### 白話理解

像不是只有「你是不是老師」這麼簡單，
還要看你是不是：

- 教務處
- 學務處
- 輔導室

有時候兩份資料都同樣是「高機密」，
但分屬不同部門，
你也不一定都能看。

### 這就是為什麼會出現 lattice

因為這些 label 之間不一定是單純一條直線排下來。

有些 label 之間彼此根本不能直接比較。

例如：

- `Secret, {army}`
- `Secret, {navy}`

它們同樣是 `Secret`，
但類別不同，
所以不能簡單說誰比較高。

### 最重要的觀念

**BLP 控制的不是只有高低，而是誰支配誰（dominate）。**

---

## 十九、Lattice 用白話怎麼理解？

Lattice 可以先把它想成：

**一個不是只有單一路線上下排的權限結構。**

### 為什麼不是一條線？

如果只有：

- Top Secret
- Secret
- Confidential
- Unclassified

那還像一條線。

但一旦加上 categories，
就變成有些東西雖然同級，
卻屬於不同箱子。

### 白話理解

像學校裡有兩個維度：

1. 等級：校級、處室級、班級級
2. 類別：教務、學務、輔導

這時一個人在「教務處級」不代表他就自動能看「學務處級」資料。

所以權限不只是往上往下，
而像一個格狀結構。

---

## 二十、BLP 最有名的兩條規則：Simple Security Condition 和 *-Property

現在才輪到最常背的兩句口號。

但你現在應該知道，
它們不是憑空出現，
而是為了擋住：

**DAC + Trojan horse 導致的非法資訊流。**

---

## 二十一、Simple Security Condition 是什麼？

這是讀取規則。

簡單說就是：

**subject 只能讀不高於自己等級的 object。**

### 最短口號

**no read up**

如果用符號寫，
常會看到像：

`s` can read `o` iff `L(o) <= L(s)`

再加上它本來也真的有 DAC 的 read permission。

### 白話理解

低等級的人不能往上偷看更高等級的資料。

### 例如

如果你是 `Secret` 等級，
那你不能直接去讀 `Top Secret` 文件。

### 但要注意

BLP 這裡不是只看 label。

它通常還會結合：

- DAC permission

也就是說：

就算 label 上看起來可讀，
你還是得真的有權限讀它。

### 這點很重要

**BLP 不是把 DAC 完全丟掉，而是把 DAC 放在 MAC 約束下面。**

---

## 二十二、*-Property 是什麼？

這是寫入規則。

簡單說就是：

**subject 不能往比自己低的地方寫。**

### 最短口號

**no write down**

如果用符號寫，
常會看到像：

`s` can write `o` iff `L(s) <= L(o)`

同時還要真的有 DAC 的 write permission。

### 白話理解

如果你手上現在有高機密資訊，
你不能把它寫到低等級的地方。

### 例如

如果你目前在 `Secret` 等級上下文工作，
你不能把內容寫進 `Unclassified` 檔案。

### 它允許什麼？

課程裡常會整理成：

- read down：可以
- read up：不行
- write up：可以
- write down：不行

### 白話理解

你可以把低等級資訊寫去更高等級的位置，
因為這通常不會造成機密往下流。

但你不能把高等級資訊往低處倒。

---

## 二十三、為什麼一定要 no write down？

這是整章最值得真的弄懂的地方。

### 如果只有 no read up 夠不夠？

不夠。

因為即使低等級主體不能直接往上偷看，
高等級主體還是可能把資料往下寫出去。

### 經典場景再看一次

假設：

- 高等級檔案 X
- 低等級檔案 Y
- A 能讀 X，也能寫 Y
- B 能讀 Y，但不能讀 X

如果 A 執行 Trojan，
Trojan 只要：

1. 合法讀 X
2. 合法寫 Y

那 X 的秘密就掉到 Y 裡了。

### 白話理解

像一位能進機密會議室的人，
同時也能在公開社群貼文。

如果他的電腦中木馬，
木馬就能偷偷把會議內容貼到公開地方。

### 所以 no write down 在補什麼洞？

它補的是：

**高資訊流向低地方的洞。**

### 這句一定要會

**BLP 的重點不只是防止低的人讀高資料，更是在防止高資訊被搬到低處。**

---

## 二十四、BLP 不只兩條口號，還有第三個條件

很多人只背兩條，
其實完整的 secure state 通常還要滿足第三個條件。

### 1. Simple Security Condition

禁止不當讀取。

### 2. *-Property

禁止不當寫入。

### 3. Discretionary Security Property

即使 label 關係允許，
你還是得真的擁有那個權限。

也就是說：

- label 允許 ≠ 自動就能做
- 還要通過 DAC 那層授權

### 白話理解

像你等級夠高，
不代表你就能看所有同級文件。

還要看：

- 你是不是名單內的人
- 你有沒有真的被授權

### 這裡最重要的一句

**BLP 是 MAC 約束下再加上 DAC，不是只有 MAC 沒有 DAC。**

---

## 二十五、BLP 其實是 state-transition model

這裡是比較抽象的一段，
但理解它會讓你知道為什麼後面會談 theorem 和 criticism。

### 什麼意思？

BLP 不是只在看單一瞬間的一次存取。

它其實是在看：

**系統從一個 state 轉到下一個 state 時，能不能一直維持安全。**

### 課程裡常用的 state 表示

像：

`(b, m, f, h)`

你不用死背每個符號，
但要知道它在表示：

- 目前生效的 access 狀態
- access control matrix
- subjects / objects 的 labels
- 其他輔助資訊或歷史資訊

### 白話理解

像不是只看一張照片，
而是看整部影片：

- 現在系統在哪個狀態
- 下一步做了什麼
- 做完後是不是還安全

---

## 二十六、Basic Security Theorem 在講什麼？

BST 想講的其實很直觀。

### 核心意思

如果系統一開始在 secure state，
而且每一個操作都只會把它帶到另一個 secure state，
那整個系統就會一路保持安全。

### 白話理解

像你一開始站在安全區，
而且每一步都只踩進下一塊安全地板，
那你整條路走完都會留在安全範圍裡。

### 為什麼這看起來合理？

因為如果每一步都沒踩出界，
整段路自然也沒出界。

### 但這裡有個後續大問題

這只是對「你定義的 state-based 安全概念」來說成立。

它不代表真實世界資訊流就一定完全安全。

這也是後面批評 BLP 的起點。

---

## 二十七、Trusted Subject 是什麼？

課程有時會提到 trusted subject。

這類 subject 比較特別，
因為現實世界中有些程式確實需要跨等級處理資訊。

### 例如

某些系統管理工具、
某些資料整理工具、
某些經過特別信任的安全程式，
可能會被允許不完全套用一般 star property。

### 白話理解

像一般人不能隨便把機密資料轉換後送到別處，
但某個被特別信任的正式流程可能可以，
前提是它真的值得信任。

### 這也說明一件事

**真實世界安全系統常常需要例外，但例外必須非常小心。**

---

## 二十八、Maximum Level 和 Current Level 差在哪？

這也是容易漏掉的點。

課程裡常說 subject 可能不只一個 level，
而是有：

- maximum level
- current level

### Maximum level

代表它最高可以接觸到哪個等級。

### Current level

代表它現在這一刻以什麼安全上下文運作。

### 白話理解

像某位老師理論上有權限接觸校級機密資料，
但他現在正在處理普通行政文件。

那：

- 他的 maximum level 很高
- 但 current level 可能是比較低的工作模式

### 為什麼這樣設計？

因為你不希望一個本來能接觸高機密的人，
每分每秒都永遠處在最高等級狀態。

那樣太危險。

---

## 二十九、BLP 為什麼後來被批評？

這段很重要，
因為它讓你知道：

**BLP 很有影響力，但不是最後真理。**

課程常總結成一句：

**BLP notion of security is neither sufficient nor necessary.**

這句要理解，不要硬背。

---

## 三十、為什麼說 BLP 不是 sufficient？

意思是：

**就算每個單一 state 看起來都符合 BLP，也不代表整體資訊流真的安全。**

### 經典問題

假設某個高等級 subject：

1. 先讀高等級資料
2. 接著釋放那個 access
3. 再把自己的 current level 降成低
4. 然後去寫低等級物件

如果它把前面記在自己內部記憶裡的高資訊寫出去，
那跨 state 來看，
高資訊還是流到低處了。

### 白話理解

像某人先在機密室把內容背起來，
走出來後換成低權限身份，
再把剛剛記住的內容寫到公開板上。

每個當下動作可能都看起來沒違規，
但整體結果還是洩密。

### 這代表什麼？

**state-by-state 安全，不等於整段執行 history 安全。**

---

## 三十一、為什麼說 BLP 也不是 necessary？

意思是：

**不是所有違反 BLP 某條形式規則的狀態，都一定真的會造成非法資訊流。**

有些情況可能形式上不符合某條規則，
但實際上沒有真的洩密。

### 這代表什麼？

BLP 不是唯一正確的安全判準。

它是一個有用的模型，
但不是你看到偏離它就能立刻斷言：

「這一定不安全。」

---

## 三十二、BLP 處理不了 covert channels

這是另一個很大的限制。

### BLP 主要在管什麼？

它主要在管 overt channels，
也就是明面上的讀寫流向。

例如：

- subject 讀 object
- subject 寫 object

### 那 covert channel 是什麼？

就是：

**利用原本不是設計來傳資訊的資源，偷偷傳資料。**

例如：

- timing
- CPU load
- resource exhaustion
- file lock
- paging behavior

### 白話理解

像學校明明規定不能傳紙條，
但兩個人改用：

- 敲桌子節奏
- 開關燈
- 拖椅子聲音

來傳訊息。

你表面上沒看到他們直接交紙條，
但資訊還是在流。

### 為什麼 *-property 擋不了這個？

因為 *-property 主要管的是：

- 能不能往哪個 object 寫

但 covert channel 可能根本不是靠正式 object write 在傳。

### 這裡最重要的一句

**BLP 擋 overt channel 很重要，但它擋不住 covert channel。**

---

## 三十三、所以 BLP 到底有什麼真正貢獻？

雖然它有缺點，
但它還是非常重要。

### 1. 它把 confidentiality 形式化了

這很大。

因為它把原本口頭上的「機密不能亂流」，
變成可以推理、可以驗證的模型。

### 2. 它提出了 *-property

這是超重要的歷史貢獻。

因為如果只有：

- no read up

那還不夠。

`no write down` 才真正補上 Trojan 洩密那個洞。

### 3. 它成為 multilevel security 的基石

後面很多 MLS 系統和思路，
都受它影響。

### 白話理解

BLP 也許不是完美法律，
但它像是一部很重要的早期憲法。

後面很多制度都會從它出發、修正、補強。

---

## 三十四、把 Access Control 和 BLP 串成一條完整主線

這樣記會最不容易散掉。

### 第一步：先定義 access control 的基本問題

誰對什麼有什麼權利？

所以有：

- subject
- object
- rights
- access matrix

### 第二步：用 ACL、capability 等方式落地

也就是把那張抽象矩陣真正做成可運作的控制方式。

### 第三步：發現 DAC 有洞

因為它只看 access，
不真正管 information flow。

### 第四步：Trojan 利用這個洞

只要某個 subject：

- 能讀高資料
- 又能寫低物件

就可能偷偷把秘密往下搬。

### 第五步：BLP 出現

BLP 用 labels、dominance 和 `no write down`
來限制機密外流。

### 第六步：再發現 BLP 也不是萬能

因為跨 state 的資訊流和 covert channel 仍可能繞過它。

### 這條主線如果你抓住

這整章就不再是散裝名詞，
而會變成一條很完整的推理線。

---

## 三十五、整份內容壓成考試能寫的理解模型

你可以把這章整理成下面這條邏輯線：

1. Access control 的基本問題是 subject 是否能對 object 執行某種 right。
2. User、principal、subject、object 分別代表真實使用者、授權身份、執行中的程式、被操作的目標。
3. Access matrix 是最乾淨的抽象，ACL 和 capability 是它的兩種不同實作視角。
4. ACL 偏 object-centric，capability 偏 subject-centric。
5. DAC 的弱點是它只控制 access，不足以阻止 information flow。
6. Trojan horse 可以利用合法權限把高資訊寫到低物件，導致機密外洩。
7. BLP 是針對 confidentiality / multilevel security 的模型，用 labels 和 dominance 限制資訊流。
8. Simple security condition 對應 no read up，*-property 對應 no write down，另加 discretionary security property 才構成 secure state。
9. BLP 很重要，但不是完整答案，因為它不處理 integrity，也無法充分處理跨 state 資訊流與 covert channels。
10. BLP 的歷史價值在於把 confidentiality 形式化，並把 multilevel security 的核心規則建立起來。

---

## 三十六、最短背誦版

**Access control 的骨架是：subject 對 object 擁有哪些 rights。**

**ACL 是從 object 角度列名單，capability 是從 subject 角度持有權限 token。**

**DAC 的主要弱點是不能阻止合法權限被 Trojan 利用來造成非法資訊流。**

**BLP 是處理 confidentiality 的 multilevel security 模型，用 labels 與 dominance 控制資訊流。**

**Simple security 是 no read up，*-property 是 no write down，再加 discretionary security property 才構成 secure state。**

**但 BLP 不是萬能：它不處理 integrity，也擋不住所有跨 state 流動與 covert channels。**

---

## 三十七、如果你想用一句超白話記住這章

**Access control 像是在管誰能進哪個房間、能拿什麼東西。**

**BLP 則像是進一步規定：高機密資料不能被帶到低機密房間。**

**DAC 只看你手上有沒有鑰匙，BLP 則開始管你手上的秘密能不能被帶去別處。**
