# Voice Intake POC — Capture Complaints Over a (Simulated) Call

> Status: **Approach chosen — Browser WebRTC (Option A).** Asterisk/SIP
> (Option B) deferred to the real-phone integration phase.

## 1. Goal

Let a user report a complaint by **speaking**, as if calling a help desk.
The app receives the audio over the air-gapped dev LAN, transcribes it
locally (faster-whisper, offline), and raises a ticket through the same
pipeline as text intake (classify → app-identify → severity → ticket).

POC now; must be designed so the **fake phone can later be swapped for
real IP phones** with minimal backend change.

## 2. The constraint

- Dev LAN is **air-gapped** → cannot integrate with the real IP phone
  system.
- So we **simulate** the phone: user at another PC + a mic acts as the
  "caller"; the app server acts as the "help desk line".
- All processing (STT) is local; no cloud, no external SIP trunk.

## 3. Approach options (DECISION NEEDED)

### Option A — Browser softphone (WebRTC/WebSocket)  ← **CHOSEN**
User opens a web page on their PC, grants mic access, clicks "Call Help
Desk", speaks. Browser streams audio over WebSocket/WebRTC to the
FastAPI backend → faster-whisper → ticket.
- **+** No telephony stack; pure web + local models; quickest to demo.
- **+** Fully air-gapped, nothing to install on the user PC (just a browser).
- **–** Not "real" SIP; swapping in physical IP phones later is a
  re-integration, not a drop-in.

### Option B — Fake PBX (Asterisk/FreePBX) + SIP softphone  ← most realistic
Stand up **Asterisk** on the app server as the "fake IP thing". User PC
runs a free SIP softphone (Linphone/MicroSIP/Zoiper) with a mic,
registers to Asterisk, and "calls" a helpdesk extension. Asterisk
records the call (or streams via ARI/AudioSocket) → app runs STT → ticket.
- **+** Real SIP. When real IP phones arrive they also speak SIP to the
  PBX → backend integration is a **drop-in**, no rework.
- **+** Genuinely simulates the target production topology.
- **–** Heavier: install/configure Asterisk, dialplan, a softphone on the
  user PC. More moving parts for a POC.

### Option C — Record & upload  ← simplest possible
User records a WAV on their PC and uploads it via the web UI → STT →
ticket. No live "call" feel.
- **+** Trivial to build.
- **–** Least like a phone call; weakest demo of the intended UX.

## 4. Shared pipeline (same for all options)

```
audio (mic) ──▶ transport (A: WebSocket · B: Asterisk · C: file upload)
            ──▶ faster-whisper STT (local, int8, auto lang detect: Hindi/Hinglish/English)
            ──▶ raw complaint text  ──▶ [same intake pipeline as typed complaints]
            ──▶ classify · app-identify · severity · dependency expand
            ──▶ raise ticket  ──▶ (optional) TTS read-back of ticket number
```

Design rule: STT output is just **text** feeding the existing intake
endpoint. Whatever transport we pick, the intake/classify/ticket code is
identical — so the transport is swappable and the phone-vs-fake-phone
choice does not leak into business logic.

## 5. POC scope (proposed)

- One "caller" PC (browser or softphone) + app server on the LAN.
- Capture audio → transcribe → show transcript to operator → raise ticket.
- **Human-in-the-loop**: operator sees the transcript and can edit before
  the ticket is finalised (STT will not be perfect on code-mixed speech).
- Stretch: TTS read-back of the ticket number / confirmation (offline).

## 6. Open questions

1. **Which approach — A, B, or C?** (Recommendation: **B if the real IP
   phones are the definite production target** and you want a drop-in path;
   **A if the priority is a fast, clean POC demo** with least setup.)
2. Live streaming transcription, or record-the-utterance-then-transcribe?
   (Batch per utterance is far simpler and accurate enough for a POC.)
3. Should the caller be **identified** (service number spoken / entered)
   before the complaint, per the intake schema fields?
4. Is TTS confirmation in scope for the POC, or text-only for now?
