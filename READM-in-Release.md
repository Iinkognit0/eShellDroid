Verstanden. Du brauchst konkret: wohin mit README + Python + Bundle, und du willst die 3 Files nochmal sauber als Copy/Paste (jeweils mit Pfad oben).

Wo kommt die README hin (GitHub, iPhone)
	•	README.md gehört ins Root des Repos (oberste Ebene, nicht in einen Ordner).
	•	Der Nano Translator und das Android-Bundle ebenfalls ins Root oder in einen Ordner /release/ – aber dann muss README auch dort liegen oder du machst zusätzlich ein kurzes Root-README, das auf /release/README.md zeigt.

Einfachste, „weniger ist mehr“ Variante (empfohlen):
	•	Repo Root enthält genau:
	•	README.md
	•	nano_translator.py
	•	APK_MONOLITH_SOURCE_BUNDLE.md
	•	optional LICENSE

So lädst du es am iPhone hoch (GitHub App / Safari):
	1.	Repo öffnen → Add file → Create new file
	2.	Dateiname oben exakt eingeben, z.B. README.md
	3.	Inhalt einfügen → Commit changes
	4.	Wiederholen für nano_translator.py und APK_MONOLITH_SOURCE_BUNDLE.md

⸻

✅ v2 Release — 3 Dateien (je ein Copy/Paste Block)

/release/README.md
# eArc · First Release (Frames-only) — PoC
Status: release · deterministic · open-source · no-auto-send  
Quelle (canonical): iinkognit0.de

HEUREKA 🌋

## Was ist das?
Dieses Release ist ein **Proof-of-Concept**:
- **Frames sind das einzige Datenformat** (Maschinensprache).
- Ein **Nano Translator** macht Frames **lesbar** (Text).
- Ein **Android PoC Source Bundle** zeigt, wie Frames **lokal gespeichert**, **aus RSS gepullt** und **in Draft-Frames** konvertiert werden.

## Deliverables (3 Files)
1) `README.md` (dieses Dokument)  
2) `nano_translator.py` (Frame → Text, read-only, stdlib-only)  
3) `APK_MONOLITH_SOURCE_BUNDLE.md` (Android PoC: Struktur + Code, rekonstruktionsfähig)

## Prinzipien (hard)
- **Archiv vor Aktion**
- **Pull statt Push**
- **COMM default OFF**
- **No tracking**
- **No auto publish**
- **Append-only Logs (wenn genutzt)**
- **Determinismus** (reproduzierbare Struktur)

## Frame Format (Canonical Minimal)
Ein Frame ist eine Datei (JSON oder MD mit YAML-Header).

### Option A — JSON Frame
```json
{
  "id": "FRM-EXAMPLE-0001",
  "status": "drafted",
  "created_utc": "2026-01-11T00:00:00Z",
  "source": "local",
  "content": "Minimal unit of meaning."
}

Option B — MD Frame (YAML Frontmatter)

---
id: FRM-EXAMPLE-0001
status: drafted
created_utc: 2026-01-11T00:00:00Z
source: local
---
Minimal unit of meaning.

GitHub: Wo kommt README hin?
	•	README.md liegt im Root des Repos.
	•	Wenn du „Add file“ nutzt: Datei heißt exakt README.md (ohne Ordner).
	•	Optional zusätzlich:
	•	LICENSE (z.B. MIT)
	•	NOTICE (wenn du Dritt-Lizenzen referenzierst)

Quick Use (ohne Android, nur iPhone möglich)
	•	Du kannst Frames schon jetzt als .md oder .json sammeln.
	•	nano_translator.py ist dafür da, die Frames später read-only in Text zu rendern.

Roadmap (nur Essenz)
	•	v0.1: Frames-only PoC ✅
	•	v0.2: Android Shell (FrameStore + Inbox + RSS Pull) ✅ in Source Bundle
	•	v0.3: Export (Share/Files) + deterministische Hashes + Manifest
	•	v1.0: stabile Shells (Android/iOS) + kompatible Server-Ableitung (Linux)

—
Quelle: iinkognit0.de
As I State Iinkognit0.

```python
/release/nano_translator.py
"""
eArc · Nano Translator (Python)
Status: minimal · deterministic · read-only · stdlib-only

Purpose:
- Load a Frame from:
  - JSON (.json)
  - Markdown with YAML frontmatter (.md)
- Render to human-readable text (no interpretation beyond structure)
- No writing, no modification, no network, no side effects on import

License: MIT (recommendation; align with your repo license)
Source (canonical): iinkognit0.de
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Tuple, Optional


# -----------------------------
# Model
# -----------------------------

@dataclass(frozen=True)
class Frame:
    id: str
    status: str
    created_utc: str
    source: str
    content: str
    meta: Dict[str, Any]


# -----------------------------
# YAML frontmatter (minimal parser)
# stdlib-only: supports "key: value" lines, no nesting.
# -----------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)

def _parse_frontmatter(md: str) -> Tuple[Dict[str, str], str]:
    m = _FRONTMATTER_RE.match(md)
    if not m:
        return {}, md.strip()

    raw_yaml = m.group(1)
    body = m.group(2).strip()

    meta: Dict[str, str] = {}
    for line in raw_yaml.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body


# -----------------------------
# Loaders
# -----------------------------

def load_frame(path: Path) -> Frame:
    if not path.exists():
        raise FileNotFoundError(str(path))

    text = path.read_text(encoding="utf-8", errors="replace").strip()

    if path.suffix.lower() == ".json":
        data = json.loads(text)
        return _frame_from_dict(data, meta_extra={"_format": "json", "_path": str(path)})

    # default: markdown
    meta, body = _parse_frontmatter(text)
    data: Dict[str, Any] = dict(meta)
    data.setdefault("content", body)
    return _frame_from_dict(data, meta_extra={"_format": "md", "_path": str(path)})


def _frame_from_dict(data: Dict[str, Any], meta_extra: Optional[Dict[str, Any]] = None) -> Frame:
    meta = dict(data)
    if meta_extra:
        meta.update(meta_extra)

    fid = str(data.get("id", "unknown")).strip()
    status = str(data.get("status", "undefined")).strip()
    created_utc = str(data.get("created_utc", "") or data.get("timestamp_utc", "") or "UNKNOWN_UTC").strip()
    source = str(data.get("source", "unknown")).strip()
    content = str(data.get("content", "")).strip()

    return Frame(
        id=fid,
        status=status,
        created_utc=created_utc,
        source=source,
        content=content,
        meta=meta,
    )


# -----------------------------
# Renderers (density levels)
# -----------------------------

def render(frame: Frame, density: int = 2) -> str:
    """
    density:
      1 = RAW-ish (meta + content)
      2 = Standard (id/status/time/source + content)
      3 = Max compression (id + content only)
    """
    density = int(density)

    if density <= 1:
        lines = []
        lines.append("FRAME (RAW)")
        for k in sorted(frame.meta.keys()):
            lines.append(f"{k}: {frame.meta[k]}")
        lines.append("")
        lines.append(frame.content)
        return "\n".join(lines).strip()

    if density == 3:
        return f"{frame.id}\n\n{frame.content}".strip()

    # density 2 default
    lines = []
    lines.append(f"Frame ID: {frame.id}")
    lines.append(f"Status:   {frame.status}")
    lines.append(f"UTC:      {frame.created_utc}")
    lines.append(f"Source:   {frame.source}")
    lines.append("")
    lines.append(frame.content)
    return "\n".join(lines).strip()


# -----------------------------
# Convenience
# -----------------------------

def translate_file(frame_path: str, density: int = 2) -> str:
    frame = load_frame(Path(frame_path))
    return render(frame, density=density)


# No execution on import.
# Optional CLI (explicit only):
if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="eArc Nano Translator (read-only)")
    p.add_argument("path", help="Path to frame (.md or .json)")
    p.add_argument("--density", type=int, default=2, choices=[1, 2, 3], help="Render density (1/2/3)")
    args = p.parse_args()

    print(translate_file(args.path, density=args.density))

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

⸻

FILE: eShellDroid/settings.gradle.kts

rootProject.name = "eShellDroid"
include(":app")

⸻

FILE: eShellDroid/build.gradle.kts

plugins { }

⸻

FILE: eShellDroid/app/build.gradle.kts

plugins {
  id("com.android.application")
  kotlin("android")
}

android {
  namespace = "com.earc.eshelldroid"
  compileSdk = 34

  defaultConfig {
    applicationId = "com.earc.eshelldroid"
    minSdk = 26
    targetSdk = 34
    versionCode = 1
    versionName = "0.2"
  }

  buildTypes {
    release { isMinifyEnabled = false }
  }

  kotlinOptions { jvmTarget = "17" }
}

dependencies {
  implementation("androidx.core:core-ktx:1.12.0")
  implementation("androidx.activity:activity-ktx:1.8.2")
  implementation("androidx.work:work-runtime-ktx:2.9.0")
}

⸻

FILE: eShellDroid/app/src/main/AndroidManifest.xml

<manifest xmlns:android="http://schemas.android.com/apk/res/android">
  <uses-permission android:name="android.permission.INTERNET"/>

  <application
    android:label="eShellDroid"
    android:allowBackup="true"
    android:supportsRtl="true">
    <activity android:name=".MainActivity"
      android:exported="true">
      <intent-filter>
        <action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
      </intent-filter>
    </activity>
  </application>
</manifest>

⸻

FILE: eShellDroid/app/src/main/java/com/earc/eshelldroid/MainActivity.kt

package com.earc.eshelldroid

import android.os.Bundle
import androidx.activity.ComponentActivity
import com.earc.eshelldroid.jobs.FeedPullScheduler
import com.earc.eshelldroid.stores.FrameStore
import com.earc.eshelldroid.stores.InboxStore
import com.earc.eshelldroid.convert.InboxToFrame

class MainActivity : ComponentActivity() {

  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)

    // --- TEST 1: FrameStore.putFrame(context, exampleFixedFrame()) ---
    FrameStore.putFrame(this, exampleFixedFrame())

    // --- TEST 2: FrameStore.listFrames(context) ---
    val ids = FrameStore.listFrames(this)

    // --- TEST 3: scheduleFeedPull(context, url, everyHours=12) ---
    FeedPullScheduler.scheduleFeedPull(
      context = this,
      feedUrl = "https://example.com/feed.xml",
      everyHours = 12
    )

    // --- TEST 4: Inbox → Frame Konvertierung ---
    val inboxIds = InboxStore.listInbox(this)
    if (inboxIds.isNotEmpty()) {
      val first = inboxIds.first()
      InboxToFrame.convertInboxItemToDraftedFrame(
        context = this,
        inboxId = first,
        sourceUrl = "https://example.com/feed.xml"
      )
    }

    // No UI needed for PoC.
    finish()
  }

  private fun exampleFixedFrame(): Map<String, Any> = mapOf(
    "id" to "FRM-EXAMPLE-FIXED-0001",
    "status" to "fixed",
    "created_utc" to "2026-01-11T00:00:00Z",
    "source" to "local",
    "content" to "Example fixed frame (PoC)."
  )
}

⸻

FILE: eShellDroid/app/src/main/java/com/earc/eshelldroid/stores/FrameStore.kt

package com.earc.eshelldroid.stores

import android.content.Context
import com.earc.eshelldroid.util.Hash
import com.earc.eshelldroid.util.Time
import java.io.File
import org.json.JSONObject

object FrameStore {
  private fun baseDir(context: Context): File {
    val dir = File(context.filesDir, "AppSandbox/Frames")
    dir.mkdirs()
    return dir
  }

  fun putFrame(context: Context, frame: Map<String, Any>): String {
    val id = (frame["id"] as? String)?.trim().orEmpty()
    require(id.isNotEmpty()) { "Frame id required" }

    val json = JSONObject(frame).toString(2)
    val bytes = json.toByteArray(Charsets.UTF_8)
    val sha = Hash.sha256Hex(bytes)

    val file = File(baseDir(context), "$id.json")
    file.writeText(json, Charsets.UTF_8)

    LogStore.append(context, "FRAME_PUT id=$id sha256=$sha utc=${Time.nowUtcIso()}")
    return id
  }

  fun listFrames(context: Context): List<String> {
    val files = baseDir(context).listFiles() ?: return emptyList()
    return files
      .filter { it.isFile && it.name.endsWith(".json") }
      .map { it.name.removeSuffix(".json") }
      .sorted()
  }

  fun readFrameJson(context: Context, id: String): String {
    val file = File(baseDir(context), "$id.json")
    return file.readText(Charsets.UTF_8)
  }
}

object LogStore {
  private fun logFile(context: Context): File {
    val dir = File(context.filesDir, "AppSandbox/Logs")
    dir.mkdirs()
    return File(dir, "events.log")
  }

  fun append(context: Context, line: String) {
    val f = logFile(context)
    f.appendText(line + "\n", Charsets.UTF_8)
  }
}

⸻

FILE: eShellDroid/app/src/main/java/com/earc/eshelldroid/stores/InboxStore.kt

package com.earc.eshelldroid.stores

import android.content.Context
import com.earc.eshelldroid.util.Time
import java.io.File

object InboxStore {
  private fun baseDir(context: Context): File {
    val dir = File(context.filesDir, "AppSandbox/Inbox")
    dir.mkdirs()
    return dir
  }

  fun putInboxItem(context: Context, sourceUrl: String, rawXml: String): String {
    val id = "INBOX-" + Time.nowUtcCompact()
    val f = File(baseDir(context), "$id.xml")
    f.writeText(rawXml, Charsets.UTF_8)
    LogStore.append(context, "INBOX_PUT id=$id source=$sourceUrl utc=${Time.nowUtcIso()}")
    return id
  }

  fun listInbox(context: Context): List<String> {
    val files = baseDir(context).listFiles() ?: return emptyList()
    return files
      .filter { it.isFile && it.name.endsWith(".xml") }
      .map { it.name.removeSuffix(".xml") }
      .sorted()
  }

  fun readInboxXml(context: Context, inboxId: String): String {
    val f = File(baseDir(context), "$inboxId.xml")
    return f.readText(Charsets.UTF_8)
  }
}

⸻

FILE: eShellDroid/app/src/main/java/com/earc/eshelldroid/convert/InboxToFrame.kt

package com.earc.eshelldroid.convert

import android.content.Context
import com.earc.eshelldroid.stores.FrameStore
import com.earc.eshelldroid.stores.InboxStore
import com.earc.eshelldroid.stores.LogStore
import com.earc.eshelldroid.util.Time

object InboxToFrame {
  fun convertInboxItemToDraftedFrame(
    context: Context,
    inboxId: String,
    sourceUrl: String
  ): String {
    val xml = InboxStore.readInboxXml(context, inboxId)
    val frameId = "FRM-INBOX-$inboxId"

    val frame = mapOf(
      "id" to frameId,
      "status" to "drafted",
      "created_utc" to Time.nowUtcIso(),
      "source" to "rss_pull",
      "source_url" to sourceUrl,
      "inbox_id" to inboxId,
      "content" to xml.trim()
    )

    FrameStore.putFrame(context, frame)
    LogStore.append(context, "INBOX_TO_FRAME inbox=$inboxId frame=$frameId utc=${Time.nowUtcIso()}")
    return frameId
  }
}

⸻

FILE: eShellDroid/app/src/main/java/com/earc/eshelldroid/jobs/FeedPullScheduler.kt

package com.earc.eshelldroid.jobs

import android.content.Context
import androidx.work.Constraints
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.NetworkType
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import java.util.concurrent.TimeUnit

object FeedPullScheduler {
  fun scheduleFeedPull(context: Context, feedUrl: String, everyHours: Int) {
    val constraints = Constraints.Builder()
      .setRequiredNetworkType(NetworkType.CONNECTED)
      .build()

    val request = PeriodicWorkRequestBuilder<FeedPullWorker>(everyHours.toLong(), TimeUnit.HOURS)
      .setConstraints(constraints)
      .setInputData(FeedPullWorker.input(feedUrl))
      .build()

    WorkManager.getInstance(context).enqueueUniquePeriodicWork(
      "FEED_PULL_" + feedUrl.hashCode(),
      ExistingPeriodicWorkPolicy.UPDATE,
      request
    )
  }
}

⸻

FILE: eShellDroid/app/src/main/java/com/earc/eshelldroid/jobs/FeedPullWorker.kt

package com.earc.eshelldroid.jobs

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.Data
import androidx.work.WorkerParameters
import com.earc.eshelldroid.stores.InboxStore
import com.earc.eshelldroid.stores.LogStore
import com.earc.eshelldroid.util.Time
import java.net.HttpURLConnection
import java.net.URL

class FeedPullWorker(
  appContext: Context,
  params: WorkerParameters
) : CoroutineWorker(appContext, params) {

  override suspend fun doWork(): Result {
    val url = inputData.getString(KEY_URL) ?: return Result.failure()

    return try {
      val xml = httpGet(url)
      InboxStore.putInboxItem(applicationContext, url, xml)
      LogStore.append(applicationContext, "FEED_PULL_OK url=$url utc=${Time.nowUtcIso()}")
      Result.success()
    } catch (e: Exception) {
      LogStore.append(applicationContext, "FEED_PULL_FAIL url=$url err=${e.message} utc=${Time.nowUtcIso()}")
      Result.retry()
    }
  }

  private fun httpGet(urlStr: String): String {
    val conn = (URL(urlStr).openConnection() as HttpURLConnection).apply {
      requestMethod = "GET"
      connectTimeout = 15000
      readTimeout = 20000
      setRequestProperty("User-Agent", "eShellDroid/0.2 (eArc; pull-only)")
    }
    conn.inputStream.use { ins ->
      return ins.readBytes().toString(Charsets.UTF_8)
    }
  }

  companion object {
    private const val KEY_URL = "feed_url"
    fun input(feedUrl: String): Data = Data.Builder().putString(KEY_URL, feedUrl).build()
  }
}

⸻

FILE: eShellDroid/app/src/main/java/com/earc/eshelldroid/util/Hash.kt

package com.earc.eshelldroid.util

import java.security.MessageDigest

object Hash {
  fun sha256Hex(bytes: ByteArray): String {
    val md = MessageDigest.getInstance("SHA-256")
    val dig = md.digest(bytes)
    return dig.joinToString("") { "%02x".format(it) }
  }
}

⸻

FILE: eShellDroid/app/src/main/java/com/earc/eshelldroid/util/Time.kt

package com.earc.eshelldroid.util

import java.time.Instant
import java.time.ZoneOffset
import java.time.format.DateTimeFormatter

object Time {
  private val ISO = DateTimeFormatter.ISO_INSTANT
  private val COMPACT = DateTimeFormatter.ofPattern("yyyyMMddHHmmss").withZone(ZoneOffset.UTC)

  fun nowUtcIso(): String = ISO.format(Instant.now())
  fun nowUtcCompact(): String = COMPACT.format(Instant.now())
}

⸻

Notes (Aikido / Safety)
	•	Keine Auto-Send Funktion.
	•	Nur Pull (RSS) + lokale Ablage.
	•	Logs sind append-only, minimal.
	•	Keine Nutzer-Identität, kein Tracking.

—
Quelle: iinkognit0.de
As I State Iinkognit0.

---

Wenn du mir **nur den Repo-Namen** sagst, den du jetzt gerade auf GitHub erstellt hast (oder „egal“), gebe ich dir **die exakte Root-Liste** (Dateinamen in der Reihenfolge + optionales LICENSE), so dass du es am iPhone ohne Umwege hochlädst.
