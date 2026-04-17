# Handout Note: Bell-LaPadula

## Scope

This handout studies Bell-LaPadula (BLP), the classic confidentiality model for multilevel secure systems.

## Security Labels And Lattices

BLP assumes security labels with ordered levels such as:

- Top Secret
- Secret
- Confidential
- Unclassified

Labels can also include categories or compartments, producing a lattice rather than a simple line.

Key idea:

- information flow is constrained by dominance relations between labels.

## Core Rules

### Simple Security Condition

A subject may read an object only if the object's label is dominated by the subject's clearance and discretionary permission exists.

Memorize it as:

- no read up

### Star Property

A subject may write an object only if the subject's current level is dominated by the object's level and discretionary permission exists.

Memorize it as:

- no write down

Why it matters:

- this prevents a high subject from reading secret data and then writing it into a low object.

### Discretionary Security Property

Even if label rules allow an operation, the access must still be permitted by the discretionary matrix.

So BLP combines:

- mandatory control from labels
- discretionary control from permissions

## Subjects, Current Levels, And Trust

The handout stresses several subtleties:

- the model applies to subjects, not directly to users
- users are assumed to be trusted persons, but subjects may run Trojan horses
- a subject has both a maximum level and a current level
- trusted subjects may be exempt from some star-property restrictions

This is important because the model is really about controlling information flow through executing entities.

## Formal State-Transition View

BLP is built as a state-transition model with:

- subject set `S`
- object set `O`
- rights `P`
- security labels
- current state and actions

The Basic Security Theorem says, informally:

- if the system starts in a secure state and every action preserves security, then the system remains secure

This is methodologically important because later security models borrow the same proof style.

## Main Limitations

The handout spends significant time on BLP's weaknesses.

- It is not sufficient to stop all illegal information flow across sequences of states.
- It is not necessary either; some states may violate the formal rule set without creating a meaningful leak.
- It does not solve covert channels.
- State-based definitions can be too weak to capture higher-level information-flow intent.

This is why later criticism, including McLean's, matters.

## Why BLP Still Matters

Even with flaws, BLP contributed major ideas:

- lattice-based confidentiality reasoning
- the star property
- state-transition analysis of secure systems
- a clean separation between discretionary and mandatory parts of control

## What To Remember

- BLP is a confidentiality model, not a full security model for every property.
- "No read up, no write down" is the memory hook, but the real model is more formal than the slogan.
- The model is historically foundational even where its exact notion of security is too limited.

## Review Checklist

- Can I explain dominance in a multilevel lattice?
- Do I know why "no write down" blocks Trojan horse style leakage?
- Can I distinguish simple security, star property, and discretionary security property?
- Do I understand why BLP can still miss illegal information flow across state sequences?
