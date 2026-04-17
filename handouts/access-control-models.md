# Handout Note: Access Control Models

## Scope

This handout moves from implementation details to abstraction. It asks not only "how does a system enforce access?" but also "what policy is the system trying to enforce in the first place?"

## Policy vs Model

- Security policy: a statement of which system states are allowed or forbidden
- Security model: a formal abstraction of that policy

Why the distinction matters:

- a model strips away irrelevant details so claims can be analyzed or proved
- a system can still be insecure even if the model is elegant, because implementations add complexity and bugs

## Families Of Security Models

The slides organize models by what property they primarily protect:

- confidentiality: Bell-LaPadula and multilevel/lattice models
- integrity: Biba and Clark-Wilson
- hybrid confidentiality/integrity conflict control: Chinese Wall
- availability: reliability block diagrams, fault trees, stochastic Petri nets

Study point:

- "security" is not one thing. Different models optimize different properties.

## Access Control And The Reference Monitor Idea

The handout presents access control as a decision point between subjects and objects.

The reference validation mechanism should be:

- tamperproof
- non-bypassable
- verifiable

This is the classic reference-monitor mindset: every sensitive access should be checked by a trusted mechanism.

## Access Matrix Model

The core abstraction is the access matrix:

- rows: subjects
- columns: objects
- cells: rights

Rights in a cell define what a subject may do to an object.

This is the conceptual parent of many concrete mechanisms.

## Users, Principals, Subjects, Objects

The handout carefully separates concepts that are often blurred together:

- user: real-world person
- principal: security identity used for authorization
- subject: executing program acting for a principal
- object: resource being accessed

Important accountability lesson:

- one user may map to many principals,
- but each principal should map back to one user,
- shared accounts weaken accountability.

## Implementations Of The Matrix

The matrix can be stored in multiple forms:

- ACLs: store each column with the object
- capability lists: store each row with the subject
- access-control triples: represent rights as `(subject, access, object)` relations

## ACLs vs Capabilities

The handout compares them directly.

ACL strengths:

- per-object review
- per-object revocation
- natural fit for file systems

Capability strengths:

- per-subject review
- per-subject revocation
- better fine-grained least privilege for dynamic subjects

Important difference:

- ACL systems depend on subject authentication
- capability systems depend on unforgeability and propagation control

## Beyond Simple Object Permissions

The handout also sketches richer control styles:

- content-based controls
- context-based controls
- attribute-based controls

These often exceed what a basic OS can do alone and may require database or application-layer support.

## DAC vs MAC

- DAC allows rights to propagate through authorized subjects
- MAC constrains access through labels and fixed policy relationships

Why DAC alone is weak:

- Trojan horses can abuse a user's legitimate rights to leak data

This leads into covert-channel concerns and later mandatory models such as Bell-LaPadula.

## Beyond The DAC/MAC Split

The slides mention later models that sit beyond the simple binary:

- HRU
- TAM
- RBAC

These matter because real organizations often want structured delegation, workflow constraints, and role-centered administration rather than only raw ownership or label dominance.

## What To Remember

- Access-control mechanisms are implementations; models describe the intended rule system behind them.
- The access matrix is the central abstraction tying ACLs, capabilities, and relational representations together.
- A strong model still needs a trustworthy enforcement mechanism.

## Review Checklist

- Can I distinguish user, principal, subject, and object?
- Do I know how ACLs and capabilities represent the same underlying matrix differently?
- Can I explain why DAC is vulnerable to Trojan horse style leakage?
- Do I understand why different models target confidentiality, integrity, or availability separately?
