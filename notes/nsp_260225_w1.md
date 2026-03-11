# Course Lecture Notes (1): Introduction

This version is organized around the materials you uploaded, especially **A. Introduction** and **B1. Malware**, while also integrating the four books you requested:

* **Operating System Concepts, 10th Edition**
* **CEH Study Guide**
* **Attacking Network Protocols**
* **Computer Security: Art and Science, 2nd Edition**

Among them, **Operating System Concepts** should be treated as the most important core text, because it gives you the system-level foundation needed to truly understand both attacks and defenses.

This course is not just about memorizing attack names. It is fundamentally about three things:

1. how systems actually work,
2. how attackers exploit weaknesses in those systems and networks,
3. how defenders use operating-system mechanisms, privilege control, cryptography, monitoring, and auditing to reduce risk.

That is also why the course requires background knowledge in **operating systems**, **computer networks**, and **programming**.

---

## 1. What is this course really about?

This course is best understood as a bridge across three layers:

* **system mechanisms**
* **network behavior**
* **security attack and defense**

In other words, you are not only learning “what malware is,” but also:

* how a program becomes a **process**,
* how a process gets access to **memory**,
* how it talks to the **kernel**,
* how it uses the **file system** and **network stack**,
* and how malicious behavior eventually appears as system calls, processes, memory changes, files, sockets, and logs.

That is the mindset you should develop from the very first lecture.

---

## 2. Key technical terms

## (1) Operating System, OS

**Definition:**
An operating system is software that manages hardware resources, provides an execution environment for programs, and acts as an intermediary between users/applications and the hardware.

**Examples:**
Windows, Linux, macOS, Android, iOS.

**Real-world application:**
On your phone, every app that wants to access the camera, microphone, files, or network must go through the OS.

**Why it matters in security:**
In security, the OS is the foundation of both attack and defense. Malware eventually has to become a process, allocate memory, call system services, access files, or communicate through the network.

**Reading note:**
When reading *Operating System Concepts*, always ask:
“What resource is the OS managing here, and how could that resource be abused?”

---

## (2) Kernel

**Definition:**
The kernel is the core part of the operating system that stays resident and runs with the highest privilege. It manages system calls, memory, processes, devices, and file systems.

**Example:**
The Linux kernel.

**Real-world application:**
When your browser opens a file, sends network traffic, or allocates memory, it ultimately depends on services provided by the kernel.

**Why it matters in security:**
If an attacker escalates from **user mode** to **kernel mode**, the impact becomes much more serious. At that point, the attacker may be able to disable protections, hide malware, or alter system-wide permissions.

---

## (3) System Call

**Definition:**
A system call is the formal interface through which a user program requests services from the operating system kernel.

**Examples:**
`open()`, `read()`, `write()`, `fork()`, `exec()`.

**Real-world application:**
A messaging app sending an image may:

* open and read the image file,
* access memory,
* then send the data through the network stack.

**Why it matters in security:**
Many security tools and analysts inspect **system call traces**, because malicious behavior eventually leaves traces in kernel interactions.

**How to think about it:**
Whenever you see a malware sample, ask:
“What system calls must it use to achieve its goal?”

---

## (4) Process

**Definition:**
A process is a **program in execution**. A program on disk is passive; once loaded into memory and executed, it becomes an active process.

**Examples:**
A Chrome tab, a chat application, a background synchronization service.

**Real-world application:**
Modern browsers isolate tabs into separate processes so that one crashing or being compromised does not necessarily take down the whole browser.

**Why it matters in security:**
Malware usually runs as a process, disguises itself as a legitimate process, or injects code into an existing process.

---

## (5) Thread

**Definition:**
A thread is a lightweight unit of execution within a process. Threads in the same process share code and data, but each thread has its own program counter, registers, and stack.

**Examples:**
A UI thread, a network thread, a background worker thread.

**Real-world application:**
A chat app can keep the interface responsive while downloading files in the background.

**Why it matters in security:**
Thread behavior is important when analyzing:

* race conditions,
* synchronization bugs,
* time-of-check to time-of-use problems,
* and concurrent exploitation scenarios.

---

## (6) Interrupt

**Definition:**
An interrupt is a signal that tells the CPU an event has occurred and needs attention.

**Examples:**
Keyboard input, incoming network packets, completed disk I/O.

**Real-world application:**
When you press a key, the CPU does not need to keep constantly polling the keyboard. The device can interrupt the processor to notify it.

**Why it matters in security:**
At lower levels of the system, device drivers, I/O handling, and hardware interaction can all become attack surfaces.

---

## (7) User Mode / Kernel Mode

**Definition:**
Modern systems operate in at least two privilege levels:

* **user mode** for ordinary applications,
* **kernel mode** for privileged OS operations.

**Example:**
A normal app cannot directly modify page tables or control privileged hardware instructions.

**Real-world application:**
A mobile app cannot simply access another app’s private storage area unless the OS explicitly allows it.

**Why it matters in security:**
Privilege escalation is, in essence, an attempt to break through this boundary.

---

## (8) Memory Management / Virtual Memory

**Definition:**
The OS manages which programs are loaded into memory, how addresses are translated, and which memory pages remain in RAM or get moved out.

**Examples:**
Paging, segmentation, virtual address translation, swapping.

**Real-world application:**
If you open many browser tabs or many mobile apps at once, the OS decides which memory pages stay active and which ones are compressed, swapped out, or reclaimed.

**Why it matters in security:**
This is directly related to:

* buffer overflows,
* use-after-free,
* memory corruption,
* executable vs non-executable pages,
* and memory forensics.

---

## (9) Security vs. Protection

**Definition:**
These two concepts are related, but not identical.

* **Protection** is about controlling who can access which resources and in what ways.
* **Security** is about preserving confidentiality, integrity, and availability against unauthorized or harmful actions.

**Example:**

* File permissions, ACLs, capabilities, and RBAC belong mainly to **protection**.
* MFA, encryption, IDS, vulnerability scanning, and incident response belong more broadly to **security**.

**Real-world application:**
On a company file server:

* “You cannot access someone else’s folder” is a protection issue.
* “The server must resist ransomware” is a security issue.

---

## (10) OSI Reference Model / TCP-IP

**Definition:**
These are layered ways of understanding network communication.

**Examples:**

* Application: HTTP, SMTP
* Transport: TCP, UDP
* Network: IP
* Data Link: Ethernet, Wi-Fi frames

**Real-world application:**
This explains why Wireshark shows frames, packets, and segments differently, and why firewalls, IDS, proxies, and load balancers work at different layers.

**Why it matters in security:**
Without understanding layers, it is very hard to truly understand:

* sniffing,
* spoofing,
* session hijacking,
* TLS,
* DNS attacks,
* and protocol abuse.

---

## 3. The thinking framework this lecture should build

You can reduce the Introduction lecture to four recurring questions:

### (1) What resources exist in the system?

CPU, memory, files, devices, network.

### (2) Who uses those resources?

Processes, threads, users, services, daemons.

### (3) Through what interfaces and boundaries are they used?

System calls, APIs, device drivers, protocols, permissions.

### (4) Where is the attack surface?

Input paths, memory, files, privileges, network protocols, administration interfaces.

These four questions will continue to apply throughout the entire course.

---

# Course Lecture Notes (2): Malware

The **B1. Malware** lecture places malware evolution into several historical phases, such as:

* Discovery
* Transition
* Fame and Glory
* Mass Cybercrime

It also highlights classic cases such as:

* Elk Cloner
* Brain
* Morris Worm
* Melissa
* LoveLetter
* Code Red
* Nimda
* Zeus
* Conficker
* Stuxnet

The point is not just to memorize names, but to understand how malware evolved from curiosity and experimentation into large-scale cybercrime and strategic attacks.

---

## 1. Malware categories and explanations

## (1) Trapdoor / Backdoor

**Definition:**
A backdoor is a secret entry point into a system that bypasses normal authentication or access control.

**Examples:**
Hard-coded admin passwords, forgotten developer maintenance accounts, hidden service access.

**Real-world application:**
Many insecure IoT devices are shipped with default maintenance credentials, which effectively act like backdoors if left unchanged.

**Extended note:**
A backdoor is not always created with malicious intent at the beginning. Sometimes it begins as a “convenient shortcut” for development or maintenance and later becomes a serious security risk.

---

## (2) Logic Bomb

**Definition:**
A logic bomb is malicious logic embedded in an otherwise legitimate program that is triggered only when a specific condition is met.

**Trigger examples:**

* a specific date,
* the presence or absence of a file,
* a particular user account,
* a certain system state.

**Real-world application:**
A disgruntled insider may plant code that deletes records after they leave the company.

**Why it matters:**
This type of attack highlights the danger of insider sabotage and hidden conditional behavior.

---

## (3) Trojan Horse

**Definition:**
A Trojan horse looks like a legitimate or useful program, but secretly performs malicious actions that violate security policy.

**Examples:**
A fake PDF reader, a fake game installer, a fake crack tool, a fake software update.

**Real-world application:**
Banking Trojans, remote-access Trojans, infostealers, and disguised installers remain common in real attacks.

**Study tip:**
In the CEH material, Trojans are useful for understanding how attackers combine deception, execution, persistence, and post-compromise control.

---

## (4) Virus

**Definition:**
A virus is malware that attaches itself to another program, document, or boot area, and typically requires the host to be executed in order to spread.

**Examples:**

* macro viruses,
* file infectors,
* boot sector viruses.

**Real-world application:**
An infected Office document may spread through internal email forwarding inside an organization.

**Important features:**
Viruses often use techniques such as:

* stealth,
* encryption,
* polymorphism,
* metamorphism,
* resident behavior.

These are meant to hide the infection or evade detection.

---

## (5) Worm

**Definition:**
A worm is self-contained malware that can spread across systems and networks without requiring a host file in the same sense as a traditional virus.

**Examples:**
Morris Worm, Code Red, SQL Slammer, Conficker.

**Real-world application:**
In a corporate network, one unpatched host may be compromised and then used to spread laterally to many others.

**Why it matters:**
Worms show how a security issue can turn from “one vulnerable machine” into “an organization-wide incident” very quickly.

**Typical lifecycle:**

* probing,
* exploitation,
* replication,
* payload execution.

---

## (6) Rootkit

**Definition:**
A rootkit focuses on hiding malicious presence and maintaining privileged control.

**Examples:**

* user-mode rootkits,
* kernel-mode rootkits,
* bootkits,
* firmware rootkits.

**Real-world application:**
After gaining access to a system, an attacker may install a rootkit to hide processes, files, drivers, or network connections from administrators and security tools.

**Why it matters:**
This connects directly to operating-system internals, especially the kernel, privilege rings, boot process, and low-level persistence.

---

## (7) Zombie / Bot / Botnet

**Definition:**
A compromised machine under remote control is often called a **bot** or **zombie**. A collection of such machines forms a **botnet**.

**Examples:**
Mirai-style IoT botnets, DDoS botnets, spam botnets.

**Real-world application:**
Home routers, cameras, and NAS devices are often hijacked and used in distributed attacks.

**Why it matters:**
A single infected system may seem minor, but a coordinated network of thousands of them becomes a strategic weapon.

---

## (8) Fileless Malware

**Definition:**
Fileless malware tries to avoid leaving traditional executable files on disk. Instead, it relies more on memory, scripts, system tools, and built-in components.

**Examples:**
PowerShell-based attacks, WMI persistence, living-off-the-land techniques.

**Real-world application:**
An enterprise endpoint may show no obvious malicious EXE, yet the attack is actively running in memory.

**Why it matters:**
This forces defenders to look beyond file scanning and pay more attention to process behavior, memory, logging, and endpoint telemetry.

---

## (9) Ransomware

**Definition:**
Ransomware blocks access to systems or encrypts data, then demands payment for restoration.

**Examples:**
Petya, SamSam, modern double-extortion families.

**Real-world application:**
Hospitals, schools, and local governments are common victims because service availability matters as much as confidentiality.

**Why it matters:**
Ransomware is a direct attack on **availability**, one of the core pillars of security.

---

## 2. Why the Morris Worm is worth studying carefully

The Morris Worm remains one of the most important classic cases because it shows that real attacks rarely rely on only one weakness.

It exploited multiple paths, including:

* a sendmail debug feature,
* a buffer overflow in fingerd,
* trusted remote login relationships,
* weak password guessing.

### Why this case matters so much

It teaches three big lessons:

### (1) Large attacks are usually multi-vector

Attackers often combine software flaws, network services, weak authentication, and trust relationships.

### (2) Security failures are often cross-layer

An incident is rarely “just a coding problem” or “just a network problem.”
It may involve OS design, service configuration, weak credentials, and insecure trust assumptions all at once.

### (3) Convenience is often the enemy of security

Debug features, trust shortcuts, and poor password practices may each seem small by themselves, but together they become disaster.

---

## 3. Mapping malware to real life

Here is a practical mapping from malware categories to realistic situations:

* **Backdoor**: default credentials in a router, hidden maintenance access, leftover developer access.
* **Logic bomb**: conditional deletion or sabotage planted in payroll, ERP, or scheduling systems.
* **Trojan**: fake update software, fake cracked software, fake attachment.
* **Virus**: infected Office macro or document-based infection.
* **Worm**: exploitation and lateral movement through SMB, RDP, or unpatched services.
* **Rootkit**: hidden drivers, kernel hooks, stealth persistence.
* **Botnet**: hijacked consumer devices used for DDoS.
* **Fileless malware**: PowerShell, WMI, registry-based persistence, memory-only execution.
* **Ransomware**: encryption, operational shutdown, backup destruction, extortion.

This is how you should connect textbook terminology to real attack scenarios.

---

## 4. Defense is not just “install antivirus”

A major mistake in beginners’ thinking is to assume that malware defense equals antivirus.

That is far too narrow.

A solid defense strategy should be seen in at least five layers:

### (1) Policy layer

What services are allowed?
What media can enter the environment?
What accounts are permitted?

### (2) System layer

Patch management, least privilege, hardening, process isolation, application control.

### (3) Network layer

Segmentation, firewalls, IDS/IPS, DNS monitoring, encrypted traffic inspection where appropriate.

### (4) Detection layer

Logs, auditing, EDR, memory analysis, IOC hunting, process and network telemetry.

### (5) Recovery layer

Backups, incident response, isolation, reimaging, credential reset, restoration planning.

The goal is not merely “stop malware,” but to reduce likelihood, detect early, contain damage, and recover reliably.

---

# How to read the four books together

---

## A. Most important: *Operating System Concepts, 10th Edition*

This should be your **main backbone**.

It does not primarily teach attack tricks.
Instead, it teaches the system mechanisms that make attacks possible and defenses meaningful.

### Recommended chapters

* **Chapter 1: Introduction, pp. 3–54**
  OS basics, interrupts, I/O, architecture, security/protection, virtualization, distributed systems.

* **Chapter 2: Operating-System Structures, pp. 55–101**
  OS services, system calls, linkers/loaders, design goals, policy vs. mechanism.

* **Chapter 3: Processes, pp. 106–156**
  Process concept, PCB, context switch, IPC.

* **Chapter 4: Threads & Concurrency, pp. 160–198**
  Multithreading and parallel execution.

* **Chapter 9–10: Main Memory / Virtual Memory, pp. 349–444**
  Address translation, paging, demand paging, replacement.

* **Chapter 16: Security, pp. 621–665**

* **Chapter 17: Protection, pp. 667–697**

* **Chapter 18–19, pp. 701–770**
  Virtual machines, networks, distributed systems.

### How to read it effectively

Whenever you encounter an attack, ask these four questions:

1. **Which OS abstraction is being targeted?**
   Process, thread, memory, file, network, device?

2. **Which privilege boundary is being crossed?**
   User/kernel? Local/remote? Normal/admin?

3. **What persistent state is being changed?**
   Files, registry, credentials, boot loader, scheduled tasks?

4. **What traces should this leave behind?**
   System calls, logs, processes, memory changes, sockets, audit events?

If you can describe an attack through those four questions, you truly understand it at the systems level.

---

## B. *CEH Study Guide*

Use this as your **attack vocabulary and scenario book**

This book is useful for naming, categorizing, and recognizing many offensive techniques, tools, and common exam-style situations.

### Recommended sections

* **Chapter 1, p. 25: Getting Started**

  * **Security 101, p. 27**
  * **The OSI Reference Model, p. 27**
  * **TCP/IP Overview, p. 34**

* **Chapter 3, p. 145: Scanning and Enumeration**

  * **TCP/IP Networking, p. 147**

* **Chapter 4, p. 224: Sniffing and Evasion**

* **Chapter 5, p. 290: Attacking a System**

  * **Buffer Overflows, p. 340**

* **Chapter 10, p. 549: Trojans and Other Attacks**

  * Malware Attacks, p. 551
  * Definitions, p. 552
  * Trojans, p. 556
  * Viruses and Worms, p. 565
  * Fileless Malware, p. 568
  * Malware Analysis, p. 572
  * Mitigation, p. 576

### How to use it

Do **not** use CEH as your main theoretical foundation.
Use it after you already understand the system mechanism from OS concepts.

A good sequence is:

1. learn the mechanism from **Operating System Concepts**,
2. use **CEH** to learn the attack names, patterns, tools, and scenarios,
3. then return to the mechanism again and explain how the attack actually works.

---

## C. *Attacking Network Protocols*

Use this as your **wire-level and protocol-level intuition book**

This book is very good for learning how abstract networking concepts become real packets, headers, fields, sessions, and protocol states.

### Recommended chapter flow

* **Chapter 1: The Basics of Networking, pp. 1–10**
* **Chapter 2: Capturing Application Traffic, pp. 11–36**
* **Chapter 3: Network Protocol Structures, pp. 37–62**
* **Chapter 4: Advanced Application Traffic Capture, pp. 63–78**
* **Chapter 5: Analysis from the Wire, pp. 79–110**
* **Chapter 6: Application Reverse Engineering, pp. 111–144**
* **Chapter 7: Network Protocol Security, pp. 145–178**
* **Chapter 8: Implementing the Network Protocol, pp. 179–206**
* **Chapter 9: The Root Causes of Vulnerabilities, pp. 207–232**
* **Chapter 10: Finding and Exploiting Security Vulnerabilities, pp. 233–276**

### How to read it

This book is best read together with a packet capture tool such as Wireshark or tcpdump.

Your goal is to convert abstract ideas like:

* TCP/IP,
* sessions,
* application data,
* protocol parsing,
* state machines

into concrete observations:

* bytes on the wire,
* headers,
* flags,
* field lengths,
* malformed packets,
* and protocol transitions.

That is how protocol knowledge becomes useful in real security work.

---

## D. *Computer Security: Art and Science, 2nd Edition*

Use this as your **theory and design-principles reinforcement book**

This book is excellent for answering:
“Why is this defense sound?”
“What principle makes this design secure or insecure?”

### Recommended chapters

* **Chapter 1: An Overview of Computer Security, pp. 3–25**
* **Chapter 5: Confidentiality Policies, pp. 141–171**
* **Chapter 14: Design Principles, pp. 455–468**
* **Chapter 23: Malware, pp. 775–820**
* **Chapter 24: Vulnerability Analysis, pp. 825–876**
* **Chapter 26: Intrusion Detection, pp. 917–956**

### How to use it

This book is especially good after you have already seen attack examples.

It helps you connect attacks to deeper ideas such as:

* least privilege,
* fail-safe defaults,
* economy of mechanism,
* complete mediation,
* open design,
* policy vs. mechanism,
* detection models,
* and vulnerability taxonomy.

A simple way to remember the roles of the books is:

* **Operating System Concepts** teaches you **how the system works**
* **CEH** and **Attacking Network Protocols** teach you **how attacks happen**
* **Computer Security: Art and Science** teaches you **why defenses are designed the way they are**

---

# Final study method: use a three-column note system

For every topic you study, organize your notes into three columns:

## Mechanism

What is the underlying OS, network, or cryptographic mechanism?

## Attack

What assumption, boundary, bug, or weakness is the attacker exploiting?

## Defense

What policy, privilege control, monitoring, isolation, encryption, or detection approach should be used to mitigate it?

### Example: Morris Worm

**Mechanism**

* sendmail
* fingerd
* trusted login
* password authentication

**Attack**

* debug feature abuse
* buffer overflow
* trust exploitation
* weak password guessing

**Defense**

* disable dangerous functionality
* use safer coding practices
* remove trust shortcuts
* enforce stronger authentication and monitoring

This method will help you integrate all four books into one mental map instead of treating them as four unrelated piles of terminology.

---

If you want, I can also convert this into a more formal **English lecture handout style**, with cleaner section numbering and exam-review formatting.
