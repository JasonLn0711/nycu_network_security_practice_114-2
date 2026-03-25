# Handout Note: Windows Access Control

## Scope

This handout explains Windows authorization as a combination of identities, tokens, descriptors, integrity levels, UI isolation, and compatibility-era elevation design.

## Core Authorization Model

The slides define three core entities:

- principal: user, machine, service, group, or domain identity
- subject: process, thread, or COM object acting for a principal
- object: file, registry key, pipe, process, thread, mutex, shared memory segment, and more

Windows maps these through:

- SIDs for principals
- access tokens for subjects
- security descriptors for objects

This is the Windows analogue of thinking in terms of identities, running code, and protected resources.

## Security Components To Remember

- Winlogon / LogonUI handle interactive logon flow
- SAM stores local account information
- LSASS participates in authentication and secret handling
- SRM enforces access checks

The handout also points to practical tooling such as WinDbg, Sysinternals, and VirtualBox for inspection and experimentation.

## Discretionary Access Control

Windows uses DACLs with ACEs to decide who gets which access.

Important nuance from the slides:

- absence of an ACE for one user does not necessarily deny access, because access can still arrive through group membership or inherited rules
- explicit deny ACEs matter in some cases

This is a good reminder that Windows ACL evaluation is richer than a simple owner/group/other model.

## Access Tokens And Impersonation

Processes carry access tokens describing:

- user and group SIDs
- privileges
- default DACL
- integrity information

Threads can also use different tokens for impersonation.

Why that matters:

- server code can temporarily act on behalf of a client,
- token handling becomes part of the attack surface.

## Security Descriptors

Each securable object can carry:

- owner SID
- group SID
- DACL
- SACL

The handout also ties integrity labels into the descriptor model.

Quick mental split:

- DACL: who can do what
- SACL: what should be audited and what integrity metadata applies

## Mandatory Integrity Control

Windows adds integrity levels to create security boundaries within or across accounts.

Main ideas from the slides:

- tokens carry a SID representing subject integrity
- objects can carry integrity information
- low-integrity processes should not be able to modify higher-integrity objects
- a child process usually inherits integrity constraints from parent and executable context

This addresses a major weakness of pure DAC: processes under the same account do not all deserve equal trust.

## Sessions, Desktops, And UI Attacks

The handout spends a lot of time on Windows GUI and session boundaries:

- sessions isolate multi-user namespaces
- window stations and desktops further isolate UI-related resources
- earlier Windows designs allowed message-based attacks such as shatter attacks

Defensive evolution includes:

- Session 0 isolation
- User Interface Privilege Isolation (UIPI)

Security lesson:

- GUI and message systems are part of access control, not just usability plumbing.

## UAC

The handout presents UAC as a compatibility compromise, not a magic defense.

Key points:

- filtered admin token keeps day-to-day work closer to standard-user privilege
- elevation prompts allow privileged operations when needed
- UAC is not itself a security boundary
- the real long-term goal is least-privilege application design

This is one of the most important conceptual points in the deck.

## What To Remember

- Windows authorization depends on tokens and security descriptors, not only usernames.
- Integrity levels add an important dimension beyond DACLs.
- GUI/session isolation was introduced partly because UI channels became privilege-escalation paths.
- UAC helps move users and developers toward least privilege, but it does not replace secure design.

## Review Checklist

- Can I explain principal, subject, and object in Windows terms?
- Do I know what lives in an access token vs a security descriptor?
- Can I explain why DACLs alone were not enough and why MIC/UIPI were added?
- Do I understand why UAC should be treated as a transition aid rather than a complete security boundary?
