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
