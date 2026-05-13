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
}) {
  const sortedConversations = conversations
    .filter((conversation) => conversation.messages.length > 0)
    .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime());

  return (
    <aside className="flex min-h-0 flex-col rounded-[1.4rem] border border-white/[0.10] bg-navy/[0.34] p-3 text-left backdrop-blur-xl">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs font-extrabold uppercase tracking-normal text-mist">
            Saved chats
          </p>
          <p className="mt-1 text-sm font-semibold text-white/[0.58]">Recent trips</p>
        </div>
        <button
          className="inline-flex h-10 items-center gap-2 rounded-full bg-mist px-3 text-sm font-extrabold text-navy transition hover:-translate-y-0.5 hover:bg-snow disabled:opacity-60"
          type="button"
          onClick={onNewChat}
          disabled={disabled}
        >
          <Plus size={16} />
          New
        </button>
      </div>

      <div className="mt-4 min-h-0 flex-1 space-y-2 overflow-y-auto pr-1">
        {sortedConversations.length ? (
          sortedConversations.map((conversation) => {
            const isActive = conversation.id === activeConversationId;

            return (
              <button
                className={`w-full rounded-2xl border px-3 py-3 text-left transition duration-200 ${
                  isActive
                    ? "border-mist/40 bg-mist/[0.18] text-white"
                    : "border-white/[0.08] bg-white/[0.05] text-white/[0.72] hover:bg-white/[0.10]"
                }`}
                key={conversation.id}
                type="button"
                onClick={() => onSelectConversation(conversation.id)}
                disabled={disabled}
              >
                <div className="flex items-start gap-2">
                  <MessageCircle className="mt-0.5 flex-none text-mist" size={16} />
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-extrabold">{conversation.title}</p>
                    <p className="mt-1 text-xs font-semibold text-white/[0.46]">
                      {conversation.messages.length
                        ? formatChatDate(conversation.updatedAt)
                        : "No messages yet"}
                    </p>
                  </div>
                </div>
              </button>
            );
          })
        ) : (
          <p className="rounded-2xl border border-white/[0.08] bg-white/[0.05] px-3 py-4 text-sm font-semibold text-white/[0.54]">
            No saved trips yet
          </p>
        )}
      </div>
    </aside>
  );
}

export default ChatHistory;
