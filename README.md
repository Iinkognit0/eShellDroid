# eShellDroid

Minimal open-source proof-of-concept for **eArc**.  
Frames-first Android shell with deterministic local storage, passive RSS pull
and zero tracking.

**Status:** PoC · deterministic · offline-first  
**Canonical source:** iinkognit0.de  
**License:** MIT  
**HEUREKA 🌋**

---

## What is this?

**eShellDroid** is an Android Proof-of-Concept that demonstrates:

- **Frames as the only data format** (machine language)
- **Local FrameStore** (read/write, deterministic)
- **Passive RSS pull** (WorkManager, pull-only)
- **Inbox → Frame conversion** (drafted, no interpretation)
- **No tracking · no push · no auto publish**
- **COMM default OFF**

Meaning before interface.  
Archive before action.

---

## Repository contents

- `README.md` — this document
- `LICENSE` — MIT
- `release/nano_translator.py` — read-only Frame → Text translator (Python, stdlib-only)
- `release/APK_MONOLITH_SOURCE_BUNDLE.md` — Android PoC source bundle (structure + code)

---

## Core principles (hard rules)

- Frames are atomic
- Pull instead of push
- No background transmit
- No identity, no tracking
- Deterministic structure
- Append-only logs (if used)

---

## Android PoC (summary)

Implemented test lines:

- `FrameStore.putFrame(context, frame)`
- `FrameStore.listFrames(context)`
- `scheduleFeedPull(context, url, everyHours)`
- `Inbox → Frame` conversion

All data lives in:
