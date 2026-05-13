import { ArrowUpRight } from "lucide-react";

const destinations = [
  {
    name: "Istanbul",
    description: "Culture & food",
    tags: ["culture", "food", "budget"],
    image:
      "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=900&q=80",
    prompt: "Help me plan a 5-day cultural trip to Istanbul with a medium budget.",
  },
  {
    name: "Lisbon",
    description: "Relaxed city escape",
    tags: ["city", "food", "budget"],
    image:
      "https://images.unsplash.com/photo-1548707309-dcebeab9ea9b?auto=format&fit=crop&w=900&q=80",
    prompt: "Help me plan a relaxed city escape to Lisbon with a medium budget.",
  },
  {
    name: "Rome",
    description: "History & monuments",
    tags: ["history", "culture", "family"],
    image:
      "https://images.unsplash.com/photo-1529260830199-42c24126f198?auto=format&fit=crop&w=900&q=80",
    prompt: "Help me plan a history-focused trip to Rome with monuments and local food.",
  },
  {
    name: "Bali",
    description: "Nature & wellness",
    tags: ["nature", "wellness", "relax"],
    image:
      "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=900&q=80",
    prompt: "Help me plan a nature and wellness trip to Bali.",
  },
  {
    name: "Tokyo",
    description: "City discovery",
    tags: ["city", "food", "culture"],
    image:
      "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=900&q=80",
    prompt: "Help me plan a city discovery trip to Tokyo with cultural highlights.",
  },
  {
    name: "Tunis",
    description: "Mediterranean culture",
    tags: ["culture", "food", "budget"],
    image:
      "https://images.unsplash.com/photo-1549144511-f099e773c147?auto=format&fit=crop&w=900&q=80",
    prompt: "Help me plan a Mediterranean culture trip to Tunis with a medium budget.",
  },
];

function DestinationCards({ onPlanTrip }) {
  return (
    <section className="bg-snow px-5 py-24" id="destinations">
      <div className="mx-auto w-full max-w-7xl reveal-up">
        <div className="max-w-3xl">
          <p className="text-sm font-extrabold uppercase tracking-normal text-ocean">
            Destinations
          </p>
          <h2 className="mt-3 text-4xl font-extrabold tracking-normal text-navy md:text-5xl">
            Explore trips that match your style
          </h2>
        </div>

        <div className="mt-10 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {destinations.map((destination) => (
            <article
              className="group overflow-hidden rounded-[2rem] border border-navy/10 bg-white shadow-card transition duration-300 hover:-translate-y-1 hover:shadow-soft"
              key={destination.name}
            >
              <div className="relative h-72 overflow-hidden">
                <img
                  className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
                  src={destination.image}
                  alt={`${destination.name} travel inspiration`}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-navy/[0.72] via-navy/[0.06] to-transparent" />
                <div className="absolute bottom-5 left-5 right-5 text-white">
                  <h3 className="text-3xl font-extrabold">{destination.name}</h3>
                  <p className="mt-1 font-semibold text-white/[0.82]">
                    {destination.description}
                  </p>
                </div>
              </div>

              <div className="p-5">
                <div className="flex flex-wrap gap-2">
                  {destination.tags.map((tag) => (
                    <span
                      className="rounded-full bg-mist/35 px-3 py-1 text-xs font-extrabold uppercase tracking-normal text-royal"
                      key={tag}
                    >
                      {tag}
                    </span>
                  ))}
                </div>
                <button
                  className="mt-5 inline-flex min-h-12 w-full items-center justify-between rounded-full bg-navy px-5 text-sm font-extrabold text-white transition hover:-translate-y-0.5 hover:bg-royal"
                  type="button"
                  onClick={() => onPlanTrip(destination.prompt)}
                >
                  Plan this trip
                  <ArrowUpRight size={18} />
                </button>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

export default DestinationCards;
