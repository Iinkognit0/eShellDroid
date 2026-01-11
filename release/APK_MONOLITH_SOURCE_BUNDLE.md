/release/APK_MONOLITH_SOURCE_BUNDLE.md
# eArc · Android Shell PoC — Source Bundle (Monolith) v0.2
Status: PoC · deterministic · offline-first · pull-based · no tracking  
Quelle (canonical): iinkognit0.de

HEUREKA 🌋

## Ziel (Essenz)
Android Proof-of-Concept, der genau diese Testzeilen erfüllt:

- `FrameStore.putFrame(context, exampleFixedFrame())` → schreibt in `filesDir/AppSandbox/Frames`
- `FrameStore.listFrames(context)` → IDs
- `scheduleFeedPull(context, "https://…/feed.xml", everyHours = 12)` → Pull → Inbox-Datei + Log
- Inbox → Frame Konvertierung (`InboxToFrame.convertInboxItemToDraftedFrame(...)`)

**Wichtig:** Dies ist ein **Source Bundle** (Struktur + Code).  
Es ist so geschrieben, dass du es 1:1 in ein Repo kopieren kannst.

---

## Projektstruktur (rekonstruktionsfähig)
```text
eShellDroid/
  settings.gradle.kts
  build.gradle.kts
  app/
    build.gradle.kts
    src/main/
      AndroidManifest.xml
      java/com/earc/eshelldroid/
        MainActivity.kt
        stores/FrameStore.kt
        stores/InboxStore.kt
        convert/InboxToFrame.kt
        jobs/FeedPullScheduler.kt
        jobs/FeedPullWorker.kt
        util/Hash.kt
        util/Time.kt
      res/values/strings.xml
