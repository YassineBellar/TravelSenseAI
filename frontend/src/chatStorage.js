const CONVERSATIONS_KEY = "travelsense_conversations";
const ACTIVE_CHAT_KEY = "travelsense_active_chat_id";

export function createChatId() {
  return `chat_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

export function createMessageId(role) {
  return `${role}_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

export function createEmptyConversation() {
  const now = new Date().toISOString();

  return {
    id: createChatId(),
    title: "New trip",
    createdAt: now,
    updatedAt: now,
    messages: [],
  };
}

export function makeChatTitle(message) {
  const cleaned = message
    .replace(/[^\w\s'-]/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  if (!cleaned) {
    return "New trip";
  }

  const withoutHelpPrefix = cleaned.replace(/^help me\s+/i, "");
  return withoutHelpPrefix.length > 40
    ? `${withoutHelpPrefix.slice(0, 40).trim()}...`
    : withoutHelpPrefix;
}

function normalizeConversation(conversation) {
  const now = new Date().toISOString();

  return {
    id: conversation.id || createChatId(),
    title: conversation.title || "New trip",
    createdAt: conversation.createdAt || now,
    updatedAt: conversation.updatedAt || conversation.createdAt || now,
    messages: Array.isArray(conversation.messages)
      ? conversation.messages.map((message) => ({
          id: message.id || createMessageId(message.role || "message"),
          role: message.role === "user" ? "user" : "assistant",
          content: message.content || "",
          isError: Boolean(message.isError),
        }))
      : [],
  };
}

export function loadConversations() {
  try {
    const parsed = JSON.parse(localStorage.getItem(CONVERSATIONS_KEY) || "[]");
    const conversations = Array.isArray(parsed) ? parsed.map(normalizeConversation) : [];

    return conversations.length ? conversations : [createEmptyConversation()];
  } catch {
    return [createEmptyConversation()];
  }
}

export function loadActiveConversationId(conversations) {
  const savedId = localStorage.getItem(ACTIVE_CHAT_KEY);

  if (savedId && conversations.some((conversation) => conversation.id === savedId)) {
    return savedId;
  }

  return conversations[0]?.id;
}

export function saveConversations(conversations, activeConversationId) {
  const safeConversations = conversations.map((conversation) => ({
    ...conversation,
    messages: conversation.messages
      .filter((message) => !message.pending)
      .map((message) => ({
        id: message.id,
        role: message.role,
        content: message.content,
        isError: Boolean(message.isError),
      })),
  }));

  localStorage.setItem(CONVERSATIONS_KEY, JSON.stringify(safeConversations));

  if (activeConversationId) {
    localStorage.setItem(ACTIVE_CHAT_KEY, activeConversationId);
  }
}
