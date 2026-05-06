"use client";

import { useState } from "react";

const API_BASE = "http://localhost:8000";

const fetchJson = async (url: string, options: RequestInit = {}) => {
  const response = await fetch(url, { ...options, headers: { "Content-Type": "application/json", ...(options.headers || {}) } });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || response.statusText);
  }
  return response.json();
};

export default function Home() {
  const [prospectName, setProspectName] = useState("");
  const [prospectEmail, setProspectEmail] = useState("");
  const [threadProspectId, setThreadProspectId] = useState(0);
  const [threadBudget, setThreadBudget] = useState(120);
  const [threadId, setThreadId] = useState(0);
  const [subject, setSubject] = useState("Interview opportunity");
  const [message, setMessage] = useState("Hi there, I wanted to see if you're open to a role that matches your experience.");
  const [senderEmail, setSenderEmail] = useState("candidate@example.com");
  const [budget, setBudget] = useState(120);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [threadDetails, setThreadDetails] = useState<any>(null);
  const [processResult, setProcessResult] = useState<any>(null);

  const handleCreateProspect = async () => {
    try {
      setError("");
      setStatus("Creating prospect...");
      const result = await fetchJson(`${API_BASE}/threads/prospects`, {
        method: "POST",
        body: JSON.stringify({ name: prospectName, email: prospectEmail }),
      });
      setStatus(`Prospect created: #${result.id}`);
      setThreadProspectId(result.id);
    } catch (err) {
      setError((err as Error).message);
      setStatus("");
    }
  };

  const handleCreateThread = async () => {
    try {
      setError("");
      setStatus("Creating thread...");
      const result = await fetchJson(`${API_BASE}/threads`, {
        method: "POST",
        body: JSON.stringify({ prospect_id: threadProspectId, budget_ceiling: threadBudget }),
      });
      setStatus(`Thread created: #${result.id}`);
      setThreadId(result.id);
      setThreadDetails(result);
    } catch (err) {
      setError((err as Error).message);
      setStatus("");
    }
  };

  const handleLoadThread = async () => {
    try {
      setError("");
      setStatus("Loading thread...");
      const result = await fetchJson(`${API_BASE}/threads/${threadId}`);
      setThreadDetails(result);
      setStatus(`Thread #${result.id} loaded`);
    } catch (err) {
      setError((err as Error).message);
      setStatus("");
    }
  };

  const handleProcessEmail = async () => {
    try {
      setError("");
      setStatus("Processing incoming email...");
      const result = await fetchJson(`${API_BASE}/email/process`, {
        method: "POST",
        body: JSON.stringify({
          thread_id: threadId,
          sender_email: senderEmail,
          subject,
          message,
          budget,
        }),
      });
      setProcessResult(result);
      setStatus("Reply generated and sent successfully");
      await handleLoadThread();
    } catch (err) {
      setError((err as Error).message);
      setStatus("");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 px-6 py-8 sm:px-10">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 rounded-3xl border border-slate-800 bg-slate-900/95 p-8 shadow-2xl shadow-slate-950/30 backdrop-blur-sm">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-2xl">
              <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">Email Wake-Up</p>
              <h1 className="mt-4 text-4xl font-semibold tracking-tight text-white sm:text-5xl">
                Modern AI email workflow for hiring outreach.
              </h1>
              <p className="mt-4 max-w-2xl text-slate-300 sm:text-lg">
                Create prospects, manage conversation threads, and generate AI replies using your backend agent. Start with the prospect and thread forms, then process an incoming message instantly.
              </p>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-3xl bg-slate-950/80 p-5 ring-1 ring-slate-700">
                <p className="text-sm uppercase tracking-[0.25em] text-slate-500">Backend</p>
                <p className="mt-3 text-2xl font-semibold text-white">Ready</p>
              </div>
              <div className="rounded-3xl bg-slate-950/80 p-5 ring-1 ring-slate-700">
                <p className="text-sm uppercase tracking-[0.25em] text-slate-500">Frontend</p>
                <p className="mt-3 text-2xl font-semibold text-white">Live UI</p>
              </div>
            </div>
          </div>
        </header>

        <section className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
          <div className="space-y-6">
            <div className="rounded-3xl bg-slate-900/90 p-6 ring-1 ring-slate-700 shadow-xl shadow-slate-950/30">
              <h2 className="text-xl font-semibold text-white">Prospect & Thread Setup</h2>
              <div className="mt-6 grid gap-6 sm:grid-cols-2">
                <div className="space-y-4 rounded-3xl bg-slate-950/70 p-5 ring-1 ring-slate-800">
                  <p className="text-sm font-medium uppercase tracking-[0.2em] text-cyan-300">Step 1: Prospect</p>
                  <label className="block text-sm text-slate-300">
                    Name
                    <input
                      className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/90 p-3 text-white outline-none focus:border-cyan-400"
                      value={prospectName}
                      onChange={(event) => setProspectName(event.target.value)}
                      placeholder="Jane Doe"
                    />
                  </label>
                  <label className="block text-sm text-slate-300">
                    Email
                    <input
                      className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/90 p-3 text-white outline-none focus:border-cyan-400"
                      value={prospectEmail}
                      onChange={(event) => setProspectEmail(event.target.value)}
                      placeholder="jane@example.com"
                    />
                  </label>
                  <button
                    className="w-full rounded-2xl bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
                    onClick={handleCreateProspect}
                  >
                    Create prospect
                  </button>
                </div>
                <div className="space-y-4 rounded-3xl bg-slate-950/70 p-5 ring-1 ring-slate-800">
                  <p className="text-sm font-medium uppercase tracking-[0.2em] text-cyan-300">Step 2: Thread</p>
                  <label className="block text-sm text-slate-300">
                    Prospect ID
                    <input
                      className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/90 p-3 text-white outline-none focus:border-cyan-400"
                      type="number"
                      value={threadProspectId || ""}
                      onChange={(event) => setThreadProspectId(Number(event.target.value))}
                      placeholder="Prospect ID"
                    />
                  </label>
                  <label className="block text-sm text-slate-300">
                    Budget ceiling
                    <input
                      className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/90 p-3 text-white outline-none focus:border-cyan-400"
                      type="number"
                      value={threadBudget}
                      onChange={(event) => setThreadBudget(Number(event.target.value))}
                    />
                  </label>
                  <button
                    className="w-full rounded-2xl bg-white/90 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-white"
                    onClick={handleCreateThread}
                  >
                    Create thread
                  </button>
                </div>
              </div>
            </div>

            <div className="rounded-3xl bg-slate-900/90 p-6 ring-1 ring-slate-700 shadow-xl shadow-slate-950/30">
              <h2 className="text-xl font-semibold text-white">Process an incoming email</h2>
              <div className="mt-6 space-y-4">
                <label className="block text-sm text-slate-300">
                  Thread ID
                  <input
                    className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/90 p-3 text-white outline-none focus:border-cyan-400"
                    type="number"
                    value={threadId || ""}
                    onChange={(event) => setThreadId(Number(event.target.value))}
                    placeholder="Thread ID"
                  />
                </label>
                <label className="block text-sm text-slate-300">
                  Sender email
                  <input
                    className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/90 p-3 text-white outline-none focus:border-cyan-400"
                    value={senderEmail}
                    onChange={(event) => setSenderEmail(event.target.value)}
                    placeholder="sender@example.com"
                  />
                </label>
                <div className="grid gap-4 lg:grid-cols-2">
                  <label className="block text-sm text-slate-300">
                    Subject
                    <input
                      className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/90 p-3 text-white outline-none focus:border-cyan-400"
                      value={subject}
                      onChange={(event) => setSubject(event.target.value)}
                    />
                  </label>
                  <label className="block text-sm text-slate-300">
                    Budget
                    <input
                      className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950/90 p-3 text-white outline-none focus:border-cyan-400"
                      type="number"
                      value={budget}
                      onChange={(event) => setBudget(Number(event.target.value))}
                    />
                  </label>
                </div>
                <label className="block text-sm text-slate-300">
                  Message
                  <textarea
                    rows={5}
                    className="mt-2 w-full rounded-3xl border border-slate-700 bg-slate-950/90 p-3 text-white outline-none focus:border-cyan-400"
                    value={message}
                    onChange={(event) => setMessage(event.target.value)}
                  />
                </label>
                <div className="flex flex-col gap-3 sm:flex-row">
                  <button
                    className="rounded-2xl bg-cyan-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
                    onClick={handleProcessEmail}
                  >
                    Generate reply
                  </button>
                  <button
                    className="rounded-2xl border border-slate-700 bg-slate-950/90 px-5 py-3 text-sm font-semibold text-slate-100 transition hover:border-cyan-400"
                    onClick={handleLoadThread}
                  >
                    Load thread details
                  </button>
                </div>
              </div>
            </div>

            <div className="grid gap-6 lg:grid-cols-2">
              <div className="rounded-3xl bg-slate-900/90 p-6 ring-1 ring-slate-700 shadow-xl shadow-slate-950/30">
                <h2 className="text-xl font-semibold text-white">Latest status</h2>
                <p className="mt-4 text-slate-300">{status || "Waiting for your input..."}</p>
                {error ? <p className="mt-3 rounded-2xl bg-rose-500/10 p-4 text-sm text-rose-300">{error}</p> : null}
              </div>
              <div className="rounded-3xl bg-slate-900/90 p-6 ring-1 ring-slate-700 shadow-xl shadow-slate-950/30">
                <h2 className="text-xl font-semibold text-white">AI reply preview</h2>
                <pre className="mt-4 whitespace-pre-wrap rounded-3xl border border-slate-700 bg-slate-950/90 p-5 text-sm leading-7 text-slate-200">
                  {processResult?.reply || "The generated reply will appear here after processing."}
                </pre>
              </div>
            </div>
          </div>

          <aside className="space-y-6">
            <div className="rounded-3xl bg-slate-900/90 p-6 ring-1 ring-slate-700 shadow-xl shadow-slate-950/30">
              <h2 className="text-xl font-semibold text-white">Thread details</h2>
              {threadDetails ? (
                <div className="mt-5 space-y-4">
                  <div className="rounded-3xl bg-slate-950/80 p-4">
                    <p className="text-sm text-slate-500">Thread ID</p>
                    <p className="mt-1 text-lg font-semibold text-white">{threadDetails.id}</p>
                  </div>
                  <div className="grid gap-4 sm:grid-cols-2">
                    <div className="rounded-3xl bg-slate-950/80 p-4">
                      <p className="text-sm text-slate-500">Budget</p>
                      <p className="mt-1 text-lg font-semibold text-white">${threadDetails.budget_ceiling}</p>
                    </div>
                    <div className="rounded-3xl bg-slate-950/80 p-4">
                      <p className="text-sm text-slate-500">State</p>
                      <p className="mt-1 text-lg font-semibold text-white">{threadDetails.current_state || "NEW"}</p>
                    </div>
                  </div>
                  <div className="rounded-3xl bg-slate-950/80 p-4">
                    <p className="text-sm text-slate-500">Messages</p>
                    <div className="mt-3 space-y-3">
                      {threadDetails.messages?.length ? (
                        threadDetails.messages.map((message: any) => (
                          <div key={message.id} className="rounded-3xl bg-slate-900 p-4 ring-1 ring-slate-800">
                            <p className="text-xs uppercase tracking-[0.2em] text-slate-500">{message.sender}</p>
                            <p className="mt-2 text-sm text-slate-300">{message.body}</p>
                          </div>
                        ))
                      ) : (
                        <p className="text-sm text-slate-500">No messages yet.</p>
                      )}
                    </div>
                  </div>
                </div>
              ) : (
                <p className="mt-4 text-slate-400">Load a thread to inspect its message history and details.</p>
              )}
            </div>

            <div className="rounded-3xl bg-slate-900/90 p-6 ring-1 ring-slate-700 shadow-xl shadow-slate-950/30">
              <h2 className="text-xl font-semibold text-white">Quick tips</h2>
              <ul className="mt-4 space-y-3 text-slate-300">
                <li>1. Create a prospect first.</li>
                <li>2. Create a thread using the prospect ID.</li>
                <li>3. Send an inbound email to generate an AI reply.</li>
                <li>4. Reload the thread to see message history.</li>
              </ul>
            </div>
          </aside>
        </section>
      </div>
    </div>
  );
}
