import { Mic, Paperclip, Plus, Send } from "lucide-react";
import { useEffect, useRef, useState } from "react";

function ChatPanel({ messages, isLoading, error, onSendMessage, hasStartedChat }) {
  const [draft, setDraft] = useState("");
  const messagesAreaRef = useRef(null);

  useEffect(() => {
    const messagesArea = messagesAreaRef.current;

    if (messagesArea) {
      messagesArea.scrollTo({
        top: messagesArea.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages, isLoading]);

  function handleSubmit(event) {
    event.preventDefault();
    const message = draft.trim();

    if (!message) {
      return;
    }

    onSendMessage(message);
    setDraft("");
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      event.currentTarget.form?.requestSubmit();
    }
  }

  return (
    <div
      className={`mx-auto grid w-full transition-all duration-500 ${
        hasStartedChat ? "h-full min-h-0 max-w-5xl grid-rows-[minmax(0,1fr)_auto]" : "max-w-4xl"
      }`}
    >
      {hasStartedChat ? (
        <div
          className="mb-5 min-h-0 space-y-4 overflow-y-auto px-1 text-left animate-chat-open"
          ref={messagesAreaRef}
        >
          {messages.map((message) => (
            <article
              className={`max-w-[82%] rounded-3xl px-5 py-4 text-sm leading-7 shadow-[0_14px_34px_rgba(0,0,0,0.14)] transition duration-300 md:text-base ${
                message.role === "user"
                  ? "ml-auto rounded-br-md bg-white/[0.16] text-white backdrop-blur-xl"
                  : message.isError
                    ? "rounded-bl-md bg-sand/20 text-white"
                    : "rounded-bl-md bg-navy/[0.50] text-white backdrop-blur-xl"
              }`}
              key={message.id}
            >
              {message.pending ? (
                <div className="flex items-center gap-2 py-1">
                  <span className="h-2 w-2 animate-bounce rounded-full bg-mist" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-mist [animation-delay:120ms]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-mist [animation-delay:240ms]" />
                </div>
              ) : (
                <div className="message-content">{message.content}</div>
              )}
            </article>
          ))}
          {error ? (
            <div className="rounded-3xl border border-sand/35 bg-sand/15 px-4 py-3 text-sm font-bold text-white">
              {error}
            </div>
          ) : null}
        </div>
      ) : null}

      <form
        className={`text-left transition-all duration-500 ${
          hasStartedChat
            ? "rounded-[1.55rem] border border-white/[0.12] bg-navy/[0.42] p-3 shadow-[0_18px_54px_rgba(0,0,0,0.20)] backdrop-blur-xl"
            : "rounded-[1.8rem] border border-white/[0.14] bg-navy/[0.46] p-3 shadow-[0_22px_58px_rgba(0,0,0,0.22)] backdrop-blur-xl"
        }`}
        onSubmit={handleSubmit}
      >
        <div className="flex items-start gap-3">
          <button
            className="grid h-11 w-11 flex-none place-items-center rounded-full border border-white/[0.10] bg-white/[0.07] text-white transition hover:bg-white/[0.12]"
            type="button"
            aria-label="Add trip detail"
          >
            <Plus size={18} />
          </button>
          <textarea
            className={`flex-1 resize-none bg-transparent py-2 text-base text-white outline-none placeholder:text-white/[0.50] transition-all duration-300 ${
              hasStartedChat ? "min-h-16" : "min-h-28"
            }`}
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask TravelSense AI anything..."
            disabled={isLoading}
          />
          <div className={hasStartedChat ? "flex flex-none gap-2" : "flex flex-none flex-col gap-2"}>
            <button
              className="grid h-11 w-11 place-items-center rounded-full bg-white/[0.07] text-white transition hover:bg-white/[0.12]"
              type="button"
              aria-label="Attach"
            >
              <Paperclip size={16} />
            </button>
            <button
              className="grid h-11 w-11 place-items-center rounded-full bg-white/[0.07] text-white transition hover:bg-white/[0.12]"
              type="button"
              aria-label="Voice"
            >
              <Mic size={16} />
            </button>
            <button
              className="grid h-11 w-11 place-items-center rounded-full bg-mist text-navy shadow-[0_12px_30px_rgba(179,207,229,0.22)] transition hover:-translate-y-0.5 hover:bg-snow disabled:opacity-60"
              type="submit"
              disabled={isLoading || !draft.trim()}
              aria-label="Send"
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default ChatPanel;
