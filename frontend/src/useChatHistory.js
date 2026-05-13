import { useEffect, useMemo, useState } from "react";

import {
  createEmptyConversation,
  loadActiveConversationId,
  loadConversations,
  saveConversations,
} from "./chatStorage";

export function useChatHistory() {
  const [chatState, setChatState] = useState(() => {
    const loadedConversations = loadConversations();

    return {
      conversations: loadedConversations,
      activeConversationId: loadActiveConversationId(loadedConversations),
    };
  });

  const { conversations, activeConversationId } = chatState;

  const activeConversation = useMemo(() => {
    return (
      conversations.find((conversation) => conversation.id === activeConversationId) ||
      conversations[0]
    );
  }, [activeConversationId, conversations]);

  useEffect(() => {
    if (!activeConversationId && conversations[0]) {
      setChatState((current) => ({
        ...current,
        activeConversationId: conversations[0].id,
      }));
    }
  }, [activeConversationId, conversations]);

  useEffect(() => {
    saveConversations(conversations, activeConversationId);
  }, [activeConversationId, conversations]);

  function startNewChat() {
    const activeHasMessages = activeConversation?.messages?.length > 0;

    if (!activeHasMessages && activeConversation) {
      setChatState((current) => ({
        ...current,
        activeConversationId: activeConversation.id,
      }));
      return;
    }

    const newConversation = createEmptyConversation();

    setChatState((current) => ({
      conversations: [newConversation, ...current.conversations],
      activeConversationId: newConversation.id,
    }));
  }

  function updateActiveConversation(updater) {
    updateConversation(activeConversationId, updater);
  }

  function updateConversation(conversationId, updater) {
    setChatState((current) => ({
      ...current,
      conversations: current.conversations.map((conversation) => {
        if (conversation.id !== conversationId) {
          return conversation;
        }

        const updated = updater(conversation);
        return {
          ...updated,
          updatedAt: new Date().toISOString(),
        };
      }),
    }));
  }

  function selectConversation(conversationId) {
    setChatState((current) => ({
      ...current,
      activeConversationId: conversationId,
    }));
  }

  return {
    conversations,
    activeConversation,
    activeConversationId,
    selectConversation,
    startNewChat,
    updateActiveConversation,
    updateConversation,
  };
}
