// Voice intake POC — getUserMedia + MediaRecorder + WebSocket.
// Captures the mic in the browser and streams encoded audio to the
// FastAPI server, which transcribes locally and returns a ticket.

const callBtn = document.getElementById("call");
const endBtn = document.getElementById("end");
const cancelBtn = document.getElementById("cancel");
const statusEl = document.getElementById("status");
const dotEl = document.getElementById("dot");
const resultCard = document.getElementById("resultCard");
const resultKv = document.getElementById("resultKv");
const transcriptEl = document.getElementById("transcript");

let ws = null;
let mediaRecorder = null;
let stream = null;

function setStatus(text, recording = false) {
  statusEl.textContent = text;
  dotEl.className = "dot" + (recording ? " rec" : "");
}

function wsUrl() {
  const proto = location.protocol === "https:" ? "wss" : "ws";
  return `${proto}://${location.host}/api/voice/ws`;
}

async function startCall() {
  resultCard.style.display = "none";
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch (err) {
    setStatus("Microphone access denied: " + err.message);
    return;
  }

  ws = new WebSocket(wsUrl());
  ws.binaryType = "arraybuffer";

  ws.onopen = () => {
    const mime = MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
      ? "audio/webm;codecs=opus"
      : "audio/webm";
    mediaRecorder = new MediaRecorder(stream, { mimeType: mime });
    mediaRecorder.ondataavailable = (e) => {
      if (e.data && e.data.size > 0 && ws && ws.readyState === WebSocket.OPEN) {
        ws.send(e.data); // Blob → binary frame
      }
    };
    mediaRecorder.start(250); // emit a chunk every 250ms (streaming feel)
    setStatus("Recording… speak your complaint", true);
    callBtn.disabled = true;
    endBtn.disabled = false;
    cancelBtn.disabled = false;
  };

  ws.onmessage = (evt) => {
    const msg = JSON.parse(evt.data);
    if (msg.type === "ready") {
      // session established
    } else if (msg.type === "result") {
      showResult(msg);
      teardown("Ticket " + msg.ticket_number + " raised.");
    } else if (msg.type === "error") {
      setStatus("Error: " + msg.message);
    } else if (msg.type === "cancelled") {
      teardown("Call cancelled.");
    }
  };

  ws.onerror = () => setStatus("Connection error.");
  ws.onclose = () => { if (mediaRecorder && mediaRecorder.state !== "inactive") stopRecorder(); };
}

function stopRecorder() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") mediaRecorder.stop();
  if (stream) stream.getTracks().forEach((t) => t.stop());
}

function endCall() {
  setStatus("Transcribing…");
  endBtn.disabled = true;
  cancelBtn.disabled = true;
  stopRecorder();
  // small delay so the final chunk flushes before we signal end
  setTimeout(() => {
    if (ws && ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify({ type: "end" }));
  }, 300);
}

function cancelCall() {
  if (ws && ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify({ type: "cancel" }));
  stopRecorder();
  teardown("Call cancelled.");
}

function teardown(finalStatus) {
  stopRecorder();
  if (ws && ws.readyState === WebSocket.OPEN) ws.close();
  ws = null; mediaRecorder = null; stream = null;
  callBtn.disabled = false;
  endBtn.disabled = true;
  cancelBtn.disabled = true;
  setStatus(finalStatus || "Idle");
}

function showResult(msg) {
  const c = msg.classification || {};
  resultKv.innerHTML = "";
  const rows = [
    ["Ticket #", msg.ticket_number],
    ["Application", c.application || "—"],
    ["Fault type", c.fault_type || "—"],
    ["Severity", c.severity || "—"],
    ["Confidence", c.confidence != null ? c.confidence : "—"],
    ["Language", msg.language || "—"],
    ["Status", msg.status],
  ];
  if (msg.stub_stt) rows.push(["Note", "STT stub (whisper not loaded)"]);
  for (const [k, v] of rows) {
    const kEl = document.createElement("div"); kEl.textContent = k;
    const vEl = document.createElement("div"); vEl.textContent = v;
    resultKv.appendChild(kEl); resultKv.appendChild(vEl);
  }
  transcriptEl.textContent = msg.transcript || "";
  resultCard.style.display = "block";
}

callBtn.addEventListener("click", startCall);
endBtn.addEventListener("click", endCall);
cancelBtn.addEventListener("click", cancelCall);
