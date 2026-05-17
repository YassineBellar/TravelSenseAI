import {
  Bell,
  Building2,
  CircleHelp,
  Heart,
  MessageCircle,
  Search,
} from "lucide-react";
import { useEffect, useState } from "react";

import ChatHistory from "./ChatHistory";
import ChatPanel from "./ChatPanel";

const navItems = [
  { label: "AI Chat", icon: MessageCircle, active: true },
  { label: "Trips", icon: Building2 },
  { label: "Explore", icon: Search },
  { label: "Saved", icon: Heart },
  { label: "Help", icon: CircleHelp },
];

const heroImages = [
  {
    src: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1900&q=80",
    alt: "Scenic coast at sunset",
  },
  {
    src: "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1900&q=80",
    alt: "Paris skyline",
  },
  {
    src: "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1900&q=80",
    alt: "Istanbul skyline",
  },
  {
    src: "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1900&q=80",
    alt: "Bali terraces",
  },
];

const suggestions = [
  "Plan a 5-day cultural trip",
  "Compare Lisbon and Rome",
  "Travel on a low budget",
  "Find a family-friendly trip",
  "Help me choose a destination",
];

function HeroApp({
  conversations,
  activeConversationId,
  messages,
  isLoading,
  error,
  onSendMessage,
  onNewChat,
  onSelectConversation,
}) {
  const [activeImage, setActiveImage] = useState(0);
  const hasStartedChat = messages.length > 0;
  const hasSavedChats = conversations.some((conversation) => conversation.messages.length > 0);

  useEffect(() => {
    const interval = window.setInterval(() => {
      setActiveImage((current) => (current + 1) % heroImages.length);
    }, 5600);

    return () => window.clearInterval(interval);
  }, []);

  return (
    <section className="relative isolate h-screen overflow-hidden bg-navy px-4 py-4 text-white sm:px-6 sm:py-6">
      <div className="absolute inset-0 -z-20">
        {heroImages.map((image, index) => (
          <img
            className={`absolute inset-0 h-full w-full scale-[1.02] object-cover transition-opacity duration-1000 ${
              index === activeImage ? "opacity-70" : "opacity-0"
            }`}
            src={image.src}
            alt={image.alt}
            key={image.src}
          />
        ))}
        <div className="absolute inset-0 bg-gradient-to-b from-navy/58 via-navy/48 to-navy/72" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(179,207,229,0.12),transparent_30%),radial-gradient(circle_at_82%_76%,rgba(74,127,167,0.14),transparent_32%)]" />
      </div>

      <div className="mx-auto flex h-full w-full max-w-[1240px] flex-col">
        <header className="flex flex-shrink-0 flex-wrap items-center justify-between gap-4 rounded-full border border-white/[0.12] bg-navy/[0.28] px-5 py-3 shadow-[0_18px_60px_rgba(0,0,0,0.16)] backdrop-blur-md md:px-6">
          <button className="text-xl font-extrabold tracking-normal text-white" type="button">
            TravelSense <span className="text-mist">AI</span>
          </button>

          <nav className="order-3 flex w-full gap-2 overflow-x-auto md:order-none md:w-auto">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  className={`inline-flex min-h-10 flex-none items-center gap-2 rounded-full px-4 text-sm font-bold transition duration-200 ${
                    item.active
                      ? "bg-mist text-navy shadow-[0_10px_26px_rgba(179,207,229,0.18)]"
                      : "border border-white/[0.10] bg-white/[0.06] text-white/[0.78] hover:bg-white/[0.12]"
                  }`}
                  key={item.label}
                  type="button"
                >
                  <Icon size={15} />
                  {item.label}
                </button>
              );
            })}
          </nav>

          <div className="flex items-center gap-3">
            <button
              className="inline-flex min-h-10 items-center rounded-full bg-mist px-3 text-xs font-extrabold text-navy transition hover:-translate-y-0.5 hover:bg-snow sm:px-4 sm:text-sm"
              type="button"
              onClick={onNewChat}
              disabled={isLoading}
            >
              New Chat
            </button>
            <button
              className="grid h-10 w-10 place-items-center rounded-full border border-white/[0.10] bg-white/[0.06] text-white transition hover:bg-white/[0.12]"
              type="button"
              aria-label="Notifications"
            >
              <Bell size={17} />
            </button>
            <div className="grid h-10 w-10 place-items-center rounded-full border border-white/20 bg-mist text-sm font-extrabold text-navy">
              YA
            </div>
          </div>
        </header>

        <div className="min-h-0 flex-1 pt-4 md:pt-5">
          {hasStartedChat ? (
            <div className="grid h-full min-h-0 grid-rows-[auto_minmax(0,1fr)] gap-3 lg:grid-cols-[248px_minmax(0,1fr)] lg:grid-rows-1">
              <details className="rounded-2xl border border-white/[0.08] bg-navy/[0.24] px-3 py-2 text-left backdrop-blur-xl lg:hidden">
                <summary className="cursor-pointer text-xs font-extrabold uppercase tracking-normal text-mist">
                  Saved chats
                </summary>
                <div className="mt-2 max-h-64 overflow-hidden">
                  <ChatHistory
                    conversations={conversations}
                    activeConversationId={activeConversationId}
                    onSelectConversation={onSelectConversation}
                    onNewChat={onNewChat}
                    disabled={isLoading}
                    variant="mobile"
                  />
                </div>
              </details>
              <div className="hidden min-h-0 lg:block">
                <ChatHistory
                  conversations={conversations}
                  activeConversationId={activeConversationId}
                  onSelectConversation={onSelectConversation}
                  onNewChat={onNewChat}
                  disabled={isLoading}
                />
              </div>
              <ChatPanel
                messages={messages}
                isLoading={isLoading}
                error={error}
                onSendMessage={onSendMessage}
                hasStartedChat={hasStartedChat}
              />
            </div>
          ) : (
            <div className="flex h-full min-h-0 items-start justify-center pt-8 pb-5 md:pt-11">
              <div className="mx-auto flex w-full max-w-5xl flex-col items-center text-center">
                <div className="transition-all duration-500 animate-fade-up">
                  <h1 className="text-4xl font-extrabold leading-tight tracking-normal text-white md:text-[3.35rem]">
                    Hello! I’m your AI travel companion.
                  </h1>
                  <p className="mx-auto mt-3 max-w-2xl text-base leading-7 text-white/[0.76] md:text-lg">
                    Tell me your budget, mood, destination idea or travel style, and I’ll help you
                    plan your next trip.
                  </p>
                </div>

                <div className="mt-7 flex max-w-3xl flex-wrap justify-center gap-2 animate-fade-up-delay">
                  {suggestions.map((suggestion) => (
                    <button
                      className="rounded-full border border-white/[0.12] bg-white/[0.06] px-4 py-2.5 text-sm font-bold text-white/[0.84] backdrop-blur-md transition duration-200 hover:-translate-y-0.5 hover:bg-mist hover:text-navy disabled:opacity-60"
                      disabled={isLoading}
                      key={suggestion}
                      onClick={() => onSendMessage(suggestion)}
                      type="button"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>

                <div className="mt-7 w-full animate-fade-up-late">
                  <ChatPanel
                    messages={messages}
                    isLoading={isLoading}
                    error={error}
                    onSendMessage={onSendMessage}
                    hasStartedChat={hasStartedChat}
                  />
                </div>

                {hasSavedChats ? (
                  <div className="mt-4 w-full animate-fade-up-late">
                    <ChatHistory
                      conversations={conversations}
                      activeConversationId={activeConversationId}
                      onSelectConversation={onSelectConversation}
                      onNewChat={onNewChat}
                      disabled={isLoading}
                      variant="home"
                    />
                  </div>
                ) : null}
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

export default HeroApp;
