import { MessageCircle, Plus } from "lucide-react";

function formatChatDate(value) {
  if (!value) {
    return "";
  }

  const date = new Date(value);
  const now = new Date();
  const sameDay = date.toDateString() === now.toDateString();

  if (sameDay) {
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  return date.toLocaleDateString([], { month: "short", day: "numeric" });
}

function ChatHistory({
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewChat,
  disabled,
  variant = "sidebar",
  limit,
}) {
  const sortedConversations = conversations
    .filter((conversation) => conversation.messages.length > 0)
    .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime());
  const visibleConversations = limit ? sortedConversations.slice(0, limit) : sortedConversations;
  const isHome = variant === "home";

  return (
    <aside
      className={`flex min-h-0 flex-col text-left backdrop-blur-xl ${
        isHome
          ? "mx-auto w-full max-w-5xl rounded-2xl border border-white/[0.08] bg-navy/[0.22] px-3 py-2"
          : "h-full rounded-2xl border border-white/[0.08] bg-navy/[0.28] p-3"
      }`}
    >
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs font-extrabold uppercase tracking-normal text-mist">
            {isHome ? "Recent trips" : "Saved chats"}
          </p>
          {!isHome ? (
            <p className="mt-0.5 text-xs font-semibold text-white/[0.52]">Recent trips</p>
          ) : null}
        </div>
        <button
          className="inline-flex h-8 items-center gap-1.5 rounded-full bg-mist px-2.5 text-xs font-extrabold text-navy transition hover:-translate-y-0.5 hover:bg-snow disabled:opacity-60"
          type="button"
          onClick={onNewChat}
          disabled={disabled}
        >
          <Plus size={14} />
          New
        </button>
      </div>

      <div
        className={`mt-2 flex min-h-0 flex-1 flex-col gap-1.5 overflow-y-auto pr-1 ${
          isHome ? "max-h-[10.5rem]" : ""
        }`}
      >
        {visibleConversations.length ? (
          visibleConversations.map((conversation) => {
            const isActive = conversation.id === activeConversationId;

            return (
              <button
                className={`grid w-full grid-cols-[18px_minmax(0,1fr)] items-center gap-2 rounded-xl border px-2.5 py-2 text-left transition duration-200 ${
                  isActive
                    ? "border-mist/35 bg-mist/[0.16] text-white"
                    : "border-white/[0.08] bg-white/[0.05] text-white/[0.74] hover:border-white/[0.14] hover:bg-white/[0.09]"
                }`}
                key={conversation.id}
                type="button"
                onClick={() => onSelectConversation(conversation.id)}
                disabled={disabled}
              >
                <MessageCircle className="text-mist" size={15} />
                <div className="min-w-0">
                  <p className="truncate text-[0.82rem] font-semibold leading-5">
                    {conversation.title}
                  </p>
                  <p className="truncate text-[0.72rem] font-semibold leading-4 text-white/[0.48]">
                    {conversation.messages.length
                      ? formatChatDate(conversation.updatedAt)
                      : "No messages yet"}
                  </p>
                </div>
              </button>
            );
          })
        ) : (
          <p className="rounded-xl border border-white/[0.08] bg-white/[0.04] px-2.5 py-2 text-xs font-semibold text-white/[0.48]">
            No saved trips yet
          </p>
        )}
      </div>
    </aside>
  );
}

export default ChatHistory;
