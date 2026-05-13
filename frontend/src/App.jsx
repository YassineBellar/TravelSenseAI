import { useRef, useState } from "react";

import { sendChatMessage } from "./api";
import { createMessageId, makeChatTitle } from "./chatStorage";
import DestinationCards from "./components/DestinationCards";
import Footer from "./components/Footer";
import HeroApp from "./components/HeroApp";
import HowItWorks from "./components/HowItWorks";
import MobileAppPromo from "./components/MobileAppPromo";
import Reviews from "./components/Reviews";
import { useChatHistory } from "./useChatHistory";

function App() {
  const {
    conversations,
    activeConversation,
    activeConversationId,
    selectConversation,
    startNewChat,
    updateConversation,
  } = useChatHistory();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const destinationSectionRef = useRef(null);

  const messages = activeConversation?.messages || [];

  function scrollToDestinations() {
    destinationSectionRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function handleNewChat() {
    setError("");
    startNewChat();
  }

  function handleSelectConversation(conversationId) {
    setError("");
    selectConversation(conversationId);
  }

  async function handleSendMessage(message) {
    const cleanMessage = message.trim();

    if (!cleanMessage || isLoading || !activeConversationId) {
      return;
    }

    const targetConversationId = activeConversationId;
    const assistantMessageId = createMessageId("assistant");
    const isFirstMessage = messages.length === 0;

    setError("");
    setIsLoading(true);

    updateConversation(targetConversationId, (conversation) => ({
      ...conversation,
      title: isFirstMessage ? makeChatTitle(cleanMessage) : conversation.title,
      messages: [
        ...conversation.messages,
        { id: createMessageId("user"), role: "user", content: cleanMessage },
        { id: assistantMessageId, role: "assistant", content: "", pending: true },
      ],
    }));

    try {
      const data = await sendChatMessage(cleanMessage);
      updateConversation(targetConversationId, (conversation) => ({
        ...conversation,
        messages: conversation.messages.map((messageItem) =>
          messageItem.id === assistantMessageId
            ? {
                ...messageItem,
                content:
                  data.assistant_response ||
                  "I can help you shape this trip. Tell me a little more.",
                pending: false,
              }
            : messageItem,
        ),
      }));
    } catch {
      setError("TravelSense AI could not respond right now. Please try again in a moment.");
      updateConversation(targetConversationId, (conversation) => ({
        ...conversation,
        messages: conversation.messages.map((messageItem) =>
          messageItem.id === assistantMessageId
            ? {
                ...messageItem,
                content: "I could not reach the planner just now. Please try again in a moment.",
                pending: false,
                isError: true,
              }
            : messageItem,
        ),
      }));
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-navy font-sans text-white">
      <main>
        <HeroApp
          conversations={conversations}
          activeConversationId={activeConversationId}
          messages={messages}
          isLoading={isLoading}
          error={error}
          onSendMessage={handleSendMessage}
          onNewChat={handleNewChat}
          onSelectConversation={handleSelectConversation}
        />

        <div ref={destinationSectionRef}>
          <DestinationCards onPlanTrip={handleSendMessage} />
        </div>

        <HowItWorks />
        <Reviews />
        <MobileAppPromo onTryPlanner={() => window.scrollTo({ top: 0, behavior: "smooth" })} />
      </main>
      <Footer />
    </div>
  );
}

export default App;
