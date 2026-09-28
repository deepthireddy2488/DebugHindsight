import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function App() {
  const [bug, setBug] = useState("");
  const [response, setResponse] = useState("");
  const [memories, setMemories] = useState([]);
  const [memoryFound, setMemoryFound] = useState(false);
  const [memorySaved, setMemorySaved] = useState(false);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadHistory = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/history");

      if (!res.ok) {
        return;
      }

      const data = await res.json();

      if (Array.isArray(data)) {
        setHistory(data);
      } else if (Array.isArray(data.history)) {
        setHistory(data.history);
      } else if (Array.isArray(data.items)) {
        setHistory(data.items);
      } else {
        setHistory([]);
      }
    } catch {
      setHistory([]);
    }
  };

  const runDebug = async () => {
    if (!bug.trim()) {
      setError("Please describe the bug first.");
      return;
    }

    setLoading(true);
    setError("");
    setResponse("");
    setMemories([]);
    setMemoryFound(false);
    setMemorySaved(false);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/debug", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          bug: bug.trim(),
        }),
      });

      if (!res.ok) {
        throw new Error("Backend request failed.");
      }

      const data = await res.json();

      setResponse(data.response || "");
      setMemories(
        Array.isArray(data.memories)
          ? data.memories
          : []
      );

      setMemoryFound(
        data.memory_found === true
      );

      setMemorySaved(
        data.memory_saved === true
      );

      await loadHistory();
    } catch (err) {
      setError(
        "Could not connect to the debugging agent. Make sure the FastAPI backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const getSection = (text, title) => {
    if (!text) {
      return "";
    }

    const heading = `**${title}**`;
    const start = text.indexOf(heading);

    if (start === -1) {
      return "";
    }

    const contentStart = start + heading.length;
    const remaining = text.substring(contentStart);

    const nextSection = remaining.search(
      /\*\*(Memory Check|Previous Experience|Current Investigation|Recommended Next Steps)\*\*/
    );

    if (nextSection === -1) {
      return remaining.trim();
    }

    return remaining
      .substring(0, nextSection)
      .trim();
  };

  const markdownComponents = {
    p: ({ children }) => (
      <p className="mb-3 text-sm leading-7 text-slate-300 last:mb-0">
        {children}
      </p>
    ),

    strong: ({ children }) => (
      <strong className="font-semibold text-white">
        {children}
      </strong>
    ),

    em: ({ children }) => (
      <em className="text-slate-200">
        {children}
      </em>
    ),

    ul: ({ children }) => (
      <ul className="mb-3 list-disc space-y-2 pl-6 text-sm leading-7 text-slate-300">
        {children}
      </ul>
    ),

    ol: ({ children }) => (
      <ol className="mb-3 list-decimal space-y-2 pl-6 text-sm leading-7 text-slate-300">
        {children}
      </ol>
    ),

    li: ({ children }) => (
      <li className="pl-1">
        {children}
      </li>
    ),

    h1: ({ children }) => (
      <h1 className="mb-3 text-xl font-bold text-white">
        {children}
      </h1>
    ),

    h2: ({ children }) => (
      <h2 className="mb-3 text-lg font-bold text-white">
        {children}
      </h2>
    ),

    h3: ({ children }) => (
      <h3 className="mb-3 text-base font-semibold text-cyan-400">
        {children}
      </h3>
    ),

    blockquote: ({ children }) => (
      <blockquote className="my-3 border-l-4 border-cyan-500/40 pl-4 text-sm italic text-slate-400">
        {children}
      </blockquote>
    ),

    code: ({ children, className }) => {
      const isInline = !className;

      if (isInline) {
        return (
          <code className="rounded bg-slate-800 px-1.5 py-0.5 text-xs text-cyan-300">
            {children}
          </code>
        );
      }

      return (
        <code className="text-sm text-slate-200">
          {children}
        </code>
      );
    },

    pre: ({ children }) => (
      <pre className="my-4 overflow-x-auto rounded-xl border border-slate-700 bg-slate-950 p-4">
        {children}
      </pre>
    ),

    table: ({ children }) => (
      <div className="my-4 overflow-x-auto rounded-xl border border-slate-700">
        <table className="w-full min-w-[600px] border-collapse text-left text-sm">
          {children}
        </table>
      </div>
    ),

    thead: ({ children }) => (
      <thead className="bg-slate-800">
        {children}
      </thead>
    ),

    tbody: ({ children }) => (
      <tbody className="divide-y divide-slate-800 bg-slate-950">
        {children}
      </tbody>
    ),

    tr: ({ children }) => (
      <tr className="transition hover:bg-slate-900">
        {children}
      </tr>
    ),

    th: ({ children }) => (
      <th className="border-r border-slate-700 px-4 py-3 font-semibold text-cyan-300 last:border-r-0">
        {children}
      </th>
    ),

    td: ({ children }) => (
      <td className="border-r border-slate-800 px-4 py-3 align-top text-slate-300 last:border-r-0">
        {children}
      </td>
    ),

    hr: () => (
      <hr className="my-5 border-slate-800" />
    ),
  };

  const memoryCheck = getSection(
    response,
    "Memory Check"
  );

  const previousExperience = getSection(
    response,
    "Previous Experience"
  );

  const currentInvestigation = getSection(
    response,
    "Current Investigation"
  );

  const recommendedSteps = getSection(
    response,
    "Recommended Next Steps"
  );

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      {/* Header */}

      <header className="border-b border-slate-800 bg-slate-950/95">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">

          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              Debug
              <span className="text-cyan-400">
                Hindsight
              </span>
            </h1>

            <p className="mt-1 text-sm text-slate-400">
              AI-powered debugging with persistent memory
            </p>
          </div>

          <div className="flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-4 py-2 text-sm text-emerald-400">
            <span className="h-2 w-2 rounded-full bg-emerald-400"></span>
            Agent Online
          </div>

        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-8">

        {/* Hero */}

        <section className="mb-8">

          <h2 className="text-3xl font-bold">
            Debug smarter with{" "}
            <span className="text-cyan-400">
              memory.
            </span>
          </h2>

          <p className="mt-2 max-w-3xl text-slate-400">
            Describe a software bug. DebugHindsight searches previous
            debugging experiences, investigates the issue, and stores the
            new experience for future bugs.
          </p>

        </section>

        {/* Main Grid */}

        <div className="grid gap-6 lg:grid-cols-3">

          {/* Left Side */}

          <section className="lg:col-span-2">

            {/* Bug Input */}

            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-xl">

              <div className="mb-4">

                <h3 className="text-lg font-semibold">
                  Describe the bug
                </h3>

                <p className="mt-1 text-sm text-slate-500">
                  Give the agent the error or problem you are facing.
                </p>

              </div>

              <textarea
                value={bug}
                onChange={(e) =>
                  setBug(e.target.value)
                }
                placeholder="Example: My FastAPI application becomes slow when many concurrent users make database requests."
                className="min-h-36 w-full resize-none rounded-xl border border-slate-700 bg-slate-950 p-4 text-sm text-white outline-none transition focus:border-cyan-400"
              />

              {error && (
                <div className="mt-3 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">
                  {error}
                </div>
              )}

              <button
                onClick={runDebug}
                disabled={loading}
                className="mt-4 w-full rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading
                  ? "Investigating..."
                  : "Run AI Debugger"}
              </button>

            </div>

            {/* Investigation Result */}

            {response && (
              <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-xl">

                <div className="mb-5 flex items-center justify-between">

                  <div>

                    <h3 className="text-lg font-semibold">
                      AI Investigation
                    </h3>

                    <p className="mt-1 text-sm text-slate-500">
                      Analysis generated using Groq + Hindsight
                    </p>

                  </div>

                  {memorySaved && (
                    <span className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs text-emerald-400">
                      Memory saved
                    </span>
                  )}

                </div>

                <div className="space-y-7">

                  {/* Memory Check */}

                  {memoryCheck && (
                    <div>

                      <h4 className="mb-3 font-semibold text-cyan-400">
                        Memory Check
                      </h4>

                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={markdownComponents}
                      >
                        {memoryCheck}
                      </ReactMarkdown>

                    </div>
                  )}

                  {/* Previous Experience */}

                  {previousExperience && (
                    <div>

                      <h4 className="mb-3 font-semibold text-cyan-400">
                        Previous Experience
                      </h4>

                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={markdownComponents}
                      >
                        {previousExperience}
                      </ReactMarkdown>

                    </div>
                  )}

                  {/* Current Investigation */}

                  {currentInvestigation && (
                    <div>

                      <h4 className="mb-3 font-semibold text-cyan-400">
                        Current Investigation
                      </h4>

                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={markdownComponents}
                      >
                        {currentInvestigation}
                      </ReactMarkdown>

                    </div>
                  )}

                  {/* Recommended Steps */}

                  {recommendedSteps && (
                    <div>

                      <h4 className="mb-3 font-semibold text-cyan-400">
                        Recommended Next Steps
                      </h4>

                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={markdownComponents}
                      >
                        {recommendedSteps}
                      </ReactMarkdown>

                    </div>
                  )}

                </div>

              </div>
            )}

          </section>

          {/* Right Side */}

          <aside className="space-y-6">

            {/* Hindsight Status */}

            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-xl">

              <h3 className="text-lg font-semibold">
                Hindsight Memory
              </h3>

              <div className="mt-5 space-y-3">

                {/* Memory searched */}

                <div className="flex items-center gap-3 rounded-xl bg-slate-950 p-3">

                  <span className="text-lg">
                    🧠
                  </span>

                  <div>

                    <p className="text-sm font-medium">
                      Memory searched
                    </p>

                    <p className="text-xs text-slate-500">
                      Hindsight was queried for prior experience
                    </p>

                  </div>

                  <span className="ml-auto text-emerald-400">
                    ✓
                  </span>

                </div>

                {/* Related Incident Status */}

                <div
                  className={`flex items-center gap-3 rounded-xl p-3 ${
                    memoryFound
                      ? "border border-emerald-500/30 bg-emerald-500/10"
                      : "border border-slate-800 bg-slate-950"
                  }`}
                >

                  <span className="text-lg">
                    {memoryFound
                      ? "🔎"
                      : "○"}
                  </span>

                  <div>

                    <p className="text-sm font-medium">
                      {memoryFound
                        ? "Related incident found"
                        : "No related incident"}
                    </p>

                    <p className="text-xs text-slate-500">
                      {memoryFound
                        ? "Previous debugging experience was used"
                        : "Agent will investigate from scratch"}
                    </p>

                  </div>

                  {memoryFound && (
                    <span className="ml-auto text-emerald-400">
                      ✓
                    </span>
                  )}

                </div>

                {/* Memory Saved */}

                {memorySaved && (
                  <div className="flex items-center gap-3 rounded-xl border border-cyan-500/20 bg-cyan-500/10 p-3">

                    <span className="text-lg">
                      💾
                    </span>

                    <div>

                      <p className="text-sm font-medium">
                        Experience saved
                      </p>

                      <p className="text-xs text-slate-500">
                        This debugging experience can help future bugs
                      </p>

                    </div>

                    <span className="ml-auto text-cyan-400">
                      ✓
                    </span>

                  </div>
                )}

              </div>

            </div>

            {/* Retrieved Memories */}

            {memoryFound && memories.length > 0 && (
              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-xl">

                <div className="mb-4">

                  <h3 className="text-lg font-semibold">
                    Retrieved Experience
                  </h3>

                  <p className="mt-1 text-xs text-slate-500">
                    Relevant memories used by the agent
                  </p>

                </div>

                <div className="space-y-3">

                  {memories.map(
                    (memory, index) => (
                      <div
                        key={
                          memory.id ||
                          index
                        }
                        className="rounded-xl border border-slate-800 bg-slate-950 p-4"
                      >

                        <div className="mb-2 flex items-center justify-between">

                          <span className="text-xs font-medium text-cyan-400">
                            Memory {index + 1}
                          </span>

                          <span className="text-xs text-emerald-400">
                            Relevant
                          </span>

                        </div>

                        <p className="text-sm leading-6 text-slate-300">
                          {memory.text ||
                            memory}
                        </p>

                      </div>
                    )
                  )}

                </div>

              </div>
            )}

            {/* Recent Debugging */}

            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-xl">

              <h3 className="text-lg font-semibold">
                Recent Debugging
              </h3>

              <div className="mt-4 space-y-3">

                {history.length === 0 ? (
                  <p className="text-sm text-slate-500">
                    No debugging sessions yet.
                  </p>
                ) : (
                  history
                    .slice()
                    .reverse()
                    .slice(0, 5)
                    .map(
                      (item, index) => (
                        <div
                          key={
                            item.id ||
                            index
                          }
                          className="rounded-xl bg-slate-950 p-3"
                        >

                          <p className="line-clamp-2 text-sm text-slate-300">
                            {item.bug}
                          </p>

                          <p className="mt-2 text-xs text-slate-600">
                            Debugging session
                          </p>

                        </div>
                      )
                    )
                )}

              </div>

            </div>

          </aside>

        </div>

      </main>

      <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-600">
        DebugHindsight • AI Debugging Agent with Persistent Memory
      </footer>

    </div>
  );
}

export default App;