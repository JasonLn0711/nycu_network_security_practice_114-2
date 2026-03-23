Absolutely. I’m going to tailor this for **a beginner student starting from zero and preparing for a binary-analysis assignment**, so the handout will stay concrete, use school-style examples, and keep connecting each idea to the kind of work you’ll later do with executables, Ghidra, and the command line. For level-setting, Harvard’s CS50 is explicitly described as an **entry-level** course for learners “with or without prior programming experience,” which is roughly the level I’m aiming at here. ([Harvard University][1])

## Week 1 mission

This week has one job: **build the mental map**.

By the end of Week 1, you should be able to explain:

* what a program is
* how source code differs from a compiled binary
* what an operating system does
* what files, folders, and paths are
* what an executable file is
* why the command line matters

You do **not** need to know assembly, registers, decompilers, or reverse-engineering techniques yet.

## Week 1 overview

| Day | Theme                             | Main outcome                                              | Small deliverable                             |
| --- | --------------------------------- | --------------------------------------------------------- | --------------------------------------------- |
| 1   | What is a program?                | Explain input, processing, output                         | 3 real-life program examples                  |
| 2   | Source code vs binary             | Explain why humans read one and computers run the other   | One comparison chart                          |
| 3   | What does an operating system do? | Explain how programs, files, and hardware are coordinated | One system diagram                            |
| 4   | Files, folders, and paths         | Read and write simple path examples                       | One folder tree sketch                        |
| 5   | What is an executable?            | Distinguish “readable file” vs “runnable file”            | One classification exercise                   |
| 6   | GUI vs command line               | Understand terminal, shell, command, argument             | Open a terminal once and record what happened |
| 7   | Review and connect everything     | Build a concept map of the week                           | One-page summary + mini quiz                  |

## How to use this handout

Each day, spend about **60–90 minutes** like this:

1. Read the lesson once slowly.
2. Rewrite the core idea in your own words.
3. Do the short exercise.
4. Answer the checkpoint question without looking back.
5. Write one sentence: “Why will this matter later in my assignment?”

## The 3 running examples for this week

I’ll keep reusing these so the ideas feel connected instead of random:

1. **Calculator app**: input numbers, process them, output the answer.
2. **School portal login**: input username/password, process verification, output success or failure.
3. **Future crackme assignment**: input a key, process verification, output “wrong” or “correct/flag.”

---

# Day 1 — What is a program?

### Goal

Understand that a computer program is a **precise set of instructions** that turns **input** into **output**.

### Core lesson

A computer is very powerful, but it is also extremely literal. It does not “guess what you meant.” A program works only because someone described a sequence of steps in a form the computer can follow.

A good beginner model is:

**Input → Processing → Output**

Examples:

* Calculator
  Input: `7 + 5`
  Processing: addition
  Output: `12`

* School portal
  Input: account + password
  Processing: check database
  Output: login success / failure

* Your future crackme assignment
  Input: key
  Processing: verify key
  Output: accepted / rejected / flag

So when someone says “this binary is a program,” they really mean:
**this file contains instructions that the computer can execute**.

### Extended example for you

Because you are learning this for an assignment, think of a program like a very strict grading robot.

A teacher can say, “Give partial credit if the logic is close.”
A grading robot cannot. It needs exact rules such as:

* read student answer
* compare to answer key
* if equal, print “Correct”
* otherwise, print “Wrong”

That is already almost the same structure as a password checker or crackme.

### Today’s work

Write down **three programs you already use** and fill in:

* What is the input?
* What is the processing?
* What is the output?

Then choose one of them and describe its behavior in **5–8 steps**.

### Checkpoint

Can you explain, in one sentence, why a program is **not** the same thing as “an app icon”?

### Common confusion

A program is the logic and instructions.
An app icon is just one way your system lets you launch it.

---

# Day 2 — Source code vs binary

### Goal

Understand the difference between the **human-readable version** of a program and the **machine-runnable version**.

### Core lesson

**Source code** is the version humans write and edit.
**Binary** (or executable/object code, depending on context) is the version the machine can use more directly.

A useful analogy:

* **Source code** = the editable Google Doc of an essay
* **Binary** = the final locked version handed to the machine to act on

This analogy is imperfect, but good enough for Week 1.

In real toolchains, the journey from source to runnable output goes through stages such as **preprocessing, compilation, assembly, and linking**. GCC’s documentation explicitly describes compilation as potentially involving those four stages, ending in object files and then an executable. You do **not** need to memorize those stages yet; just know that “source code” and “executable” are not the same thing. ([GCC][2])

### Why this matters later

In your assignment, you are not being given the teacher’s editable notes.
You are being handed the **finished compiled program** and asked to work backward from it.

That is why reverse engineering exists.

### Extended example for you

Imagine a math teacher writes a quiz in Word, edits it, fixes typos, and rearranges questions. That editable file is like source code.

After printing and distributing the quiz, students receive the final version, not the editable draft. That printed version is not identical to the original authoring experience. In the same way, a binary is the “final distributed form,” not the comfortable authoring form.

### Today’s work

Make a 2-column chart:

| Source code           | Binary                                |
| --------------------- | ------------------------------------- |
| Human-readable        | Machine-oriented                      |
| Easy to edit          | Hard to read directly                 |
| Written by developers | Generated by build/compile process    |
| Shows intent clearly  | Hides details behind lower-level form |

Then write one paragraph answering:

**Why is binary analysis harder than reading source code?**

### Checkpoint

If a program is compiled, does that mean the original source code is stored neatly inside it for you to read?

Correct idea: usually, no.

### Common confusion

“Binary” does **not** mean you literally open a file and only see `101010...`.
It means the file is in a low-level machine-oriented format, not meant for easy human reading.

---

# Day 3 — What does an operating system do?

### Goal

Understand the operating system as the **manager** that helps programs run.

### Core lesson

The operating system (OS) is the big coordinator. It helps manage:

* memory
* files
* processes / running programs
* input and output devices
* communication between software and hardware

A very good beginner analogy is:

**The operating system is like the school administration plus building management.**

It does not do your homework for you.
But it decides things like:

* which room is used
* who gets access to what
* where records are stored
* how requests are routed
* what happens when multiple people need resources at once

Microsoft’s Windows kernel documentation gives a nice concrete picture: it lists managers for objects/files, memory, processes and threads, and I/O communication. That is a very practical way to think about what an OS is doing underneath the surface. ([Microsoft Learn][3])

### Why this matters later

When you run a program, the OS helps:

* load the file into memory
* start the process
* connect keyboard input and screen output
* enforce permissions
* manage file access

Later, when you run a Linux binary, the OS is part of the story.

### Extended example for you

Suppose you open a game, a browser, and a music app at the same time.

You did not manually assign:

* how much RAM each gets
* which one talks to the screen
* which one reads files from disk
* how keyboard input is delivered

The OS handles that coordination.

### Today’s work

Draw a simple diagram:

**You → Program → Operating System → Hardware**

Then add examples:

* keyboard input
* reading a file
* showing text on screen

### Checkpoint

Is the operating system the same thing as “the whole computer”?

Correct idea: no. The OS is core system software running on the computer.

### Common confusion

People often mix up:

* computer
* operating system
* application

These are different layers.

---

# Day 4 — Files, folders, and paths

### Goal

Understand how computers organize information.

### Core lesson

A **file** is a named piece of stored data.
A **folder** (or directory) is a container that holds files and other folders.

A **path** is the address that tells you where something is.

Beginner analogy:

* school campus = file system
* building = folder
* classroom = subfolder
* worksheet = file
* full room number = path

There are two especially important kinds of paths:

* **Absolute path**: full address from the top/root
* **Relative path**: address based on where you are now

Ubuntu’s official beginner command-line tutorial explains this very clearly: a relative path depends on the **current working directory**, while an absolute path starts from the root; on Unix-like systems, a path beginning with `/` is absolute. ([Ubuntu Documentation][4])

### Example

If you are “standing in” `/home/student`, then:

* `notes/week1.txt` is a **relative path**
* `/home/student/notes/week1.txt` is an **absolute path**

Same destination, different way of describing it.

### Why this matters later

Your future assignment will involve things like:

* where the binary file is
* where Ghidra is installed
* where a plugin lives
* where a script should be launched from

A lot of beginner frustration is really just path confusion.

### Extended example for you

Think of two ways to describe a classroom:

* Absolute: “Taipei High School, Building A, Floor 3, Room 305”
* Relative: “From where you are now, go upstairs and turn left”

The second description only works if I know your starting point.

### Today’s work

Draw a folder tree for an imaginary study setup:

* `study/`

  * `week1/`
  * `notes/`
  * `practice/`
  * `assignment/`

Then invent:

* 2 absolute paths
* 2 relative paths

### Checkpoint

What changes the meaning of a relative path?

Correct idea: your current location / current working directory.

### Common confusion

A file name is not the same as a path.
`notes.txt` tells you **what**; a path tells you **where**.

---

# Day 5 — What is an executable?

### Goal

Learn the difference between a file you **read** and a file you **run**.

### Core lesson

Not every file is meant to be opened as a document.

Some files are mainly meant to be:

* read (`.txt`, `.pdf`, `.jpg`)
* edited (`.docx`, `.py`, `.c`)
* run (executables)

An **executable** is a file the operating system can load and start as a program.

For your later reverse-engineering work, one key fact is this: Linux systems commonly use the **ELF** format for executable binary files, while Windows uses **PE/COFF** for executable image and object files. The ELF man page explicitly says ELF defines executable binary files (among other related file types), and Microsoft’s PE documentation describes PE/COFF as the format for executable image and object files on Windows. ([man7.org][5])

### Why this matters later

Your assignment target is not a story, spreadsheet, or picture.
It is an **executable binary**.

That means your job is not “read what it says,” but “analyze what it does.”

### Extended example for you

Think of the difference between:

* a **math worksheet**: meant to be read
* a **calculator**: meant to be used to perform actions

An executable is much closer to the calculator than the worksheet.

### Today’s work

Classify these as mainly **read**, **edit**, or **run**:

* `essay.docx`
* `photo.png`
* `hello.py`
* `calculator.exe`
* `notes.txt`
* `game_binary`

Then write one sentence:
**Why is a crackme challenge almost always given as an executable, not as source code?**

### Checkpoint

Is every file with a familiar extension automatically safe or automatically understandable?

Correct idea: no.

### Common confusion

On Linux especially, file behavior is not determined only by the file name. Permissions and file format matter too.

---

# Day 6 — GUI vs command line

### Goal

Understand why text-based control matters.

### Core lesson

A **GUI** (graphical user interface) lets you click buttons and menus.
A **CLI** (command-line interface) lets you type precise instructions.

A **terminal** is the window.
A **shell** is the program that interprets your commands.
A **command** is the action word.
An **argument** gives extra detail.

GNU Bash’s reference manual describes a simple shell command as a command followed by space-separated arguments. That is the basic shape you will keep seeing later. ([GNU][6])

Example:

```bash
echo hello
```

* command: `echo`
* argument: `hello`

### Why this matters later

A lot of security and reverse-engineering workflows happen through commands because commands are:

* precise
* repeatable
* easy to document
* scriptable

Later you may need to do things like:

* run a binary
* launch a Python bridge script
* start tools from a specific folder

Ubuntu’s beginner command-line tutorial is designed exactly for this stage: it assumes **no prior knowledge** and introduces basic commands, file manipulation, and command chaining. ([Ubuntu][7])

### Extended example for you

GUI is like ordering food by pointing at pictures.

CLI is like writing:

> “One bowl of noodles, no cilantro, extra egg, less spicy.”

It feels harder at first, but it is much more exact.

### Today’s work

Open a terminal on your machine.
Type one harmless command, such as:

```bash
echo hello
```

Then write down:

* What did you type?
* What appeared?
* Did it feel strange, scary, or surprisingly simple?

That emotional note actually matters. Many beginners think the command line is “for experts only,” when really it is just a more explicit interface.

### Checkpoint

What is the difference between a terminal and a shell?

Correct idea:

* terminal = the window/interface
* shell = the command interpreter inside it

### Common confusion

The command line is not a “different computer world.”
It is just another way of interacting with the same system.

---

# Day 7 — Review, connect, and test yourself

### Goal

Turn isolated vocabulary into one connected picture.

### Core lesson

By now, the ideas should chain together like this:

A **program** starts as **source code**.
A build process turns it into a **binary/executable**.
The **operating system** helps run it.
The executable sits somewhere in the **file system**, so you need its **path**.
You may launch it through a **GUI** or through the **command line**.

That entire chain is the foundation for your later assignment.

### Your end-of-week task

Make a one-page concept map connecting these terms:

* program
* source code
* binary
* executable
* operating system
* file
* folder
* path
* terminal
* shell
* command
* argument

Then answer this in 5–8 sentences:

**How does Week 1 connect to my future binary-analysis assignment?**

### Mini quiz

1. What is the difference between input and output?
2. Why is source code easier for humans than binary?
3. What does an operating system do for a running program?
4. What is the difference between an absolute path and a relative path?
5. What makes an executable different from a plain text file?
6. What is the difference between a terminal and a shell?

### Answer key

1. Input goes into the program; output comes out after processing.
2. Source code is written for humans to read/edit; binary is machine-oriented.
3. The OS manages resources and helps the program interact with files, memory, devices, and execution.
4. Absolute path gives the full address; relative path depends on current location.
5. An executable is meant to be run by the OS as a program.
6. Terminal is the window/interface; shell is the interpreter for commands.

---

# Week 1 glossary

| Term               | Plain-English definition                                    |
| ------------------ | ----------------------------------------------------------- |
| Program            | A set of instructions a computer can follow                 |
| Input              | Data given to a program                                     |
| Output             | Result produced by a program                                |
| Source code        | Human-readable version of a program                         |
| Binary             | Machine-oriented compiled form of a program                 |
| Operating system   | Core software that manages resources and helps programs run |
| File               | A named piece of stored data                                |
| Folder / Directory | A container that holds files and other folders              |
| Path               | The address of a file or folder                             |
| Absolute path      | Full address from the top/root                              |
| Relative path      | Address based on your current location                      |
| Executable         | A file the OS can run as a program                          |
| Terminal           | A text window for command-line interaction                  |
| Shell              | The command interpreter running inside the terminal         |
| Command            | An instruction you type                                     |
| Argument           | Extra detail attached to a command                          |

---

# Further reading, chosen for you

Because you seem to be learning this **from scratch for a class assignment**, I would keep the reading stack small and deliberate.

Start with **CS50’s course page** for big-picture orientation. It is explicitly aimed at entry-level learners, including people with no prior programming experience, so it is a good confidence-building “you are allowed to be a beginner” resource. Read it to understand the landscape, not to master everything at once. ([Harvard University][1])

For hands-on command-line learning, use Ubuntu’s **“The Linux command line for beginners.”** It assumes no prior knowledge, introduces basic commands and file manipulation, and later explains relative vs absolute paths clearly. This is probably the single best extension reading for Days 4–6. ([Ubuntu][7])

Use the **GNU Bash manual** only as a reference, not as a book to read cover to cover right now. The manual itself says the Bash man page is the definitive reference on shell behavior, so it is excellent when you want to check “what exactly does this command structure mean?” but too heavy for casual first-pass reading. ([GNU][8])

Bookmark the **official Ghidra beginner student guide** for later weeks. Also know that Ghidra’s getting-started docs say tutorials and documentation live in the installation directory’s `docs` area, and that Ghidra itself has context-sensitive help. You do not need to study it this week, but it is a great “future you” resource. ([Ghidra][9])

For a curiosity-only preview, skim the **ELF** and **PE/COFF** documentation just to see what executable file formats look like. Do not try to understand the whole spec yet. The goal is only to make the word “executable format” feel real instead of mysterious. ([man7.org][5])

---

# What success looks like at the end of Week 1

If you can do these three things, Week 1 worked:

1. Explain the main terms in your own words.
2. Draw the chain from source code to executable to operating system.
3. Say, without panicking, why command-line and file paths will matter later.

Next, I can turn this into a **printable Day 1 worksheet with exercises and model answers**.

[1]: https://pll.harvard.edu/course/cs50-introduction-computer-science?utm_source=chatgpt.com "CS50: Introduction to Computer Science | Harvard University"
[2]: https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html "https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html"
[3]: https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/ "https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/"
[4]: https://documentation.ubuntu.com/desktop/en/latest/tutorial/the-linux-command-line-for-beginners/ "https://documentation.ubuntu.com/desktop/en/latest/tutorial/the-linux-command-line-for-beginners/"
[5]: https://man7.org/linux/man-pages/man5/elf.5.html "https://man7.org/linux/man-pages/man5/elf.5.html"
[6]: https://www.gnu.org/s/bash/manual/html_node/Shell-Commands.html "https://www.gnu.org/s/bash/manual/html_node/Shell-Commands.html"
[7]: https://ubuntu.com/tutorials/command-line-for-beginners "https://ubuntu.com/tutorials/command-line-for-beginners"
[8]: https://www.gnu.org/s/bash/manual/bash.html "https://www.gnu.org/s/bash/manual/bash.html"
[9]: https://ghidra.re/ghidra_docs/GhidraClass/Beginner/Introduction_to_Ghidra_Student_Guide.html "https://ghidra.re/ghidra_docs/GhidraClass/Beginner/Introduction_to_Ghidra_Student_Guide.html"
