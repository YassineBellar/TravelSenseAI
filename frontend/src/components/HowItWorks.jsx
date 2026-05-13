import { Compass, GitCompare, Map } from "lucide-react";

const steps = [
  {
    icon: Compass,
    title: "Tell us your travel situation",
    text: "Share your dates, budget, mood and what kind of trip you want.",
  },
  {
    icon: GitCompare,
    title: "Compare personalized ideas",
    text: "Review destination ideas with clear reasons, tradeoffs and fit.",
  },
  {
    icon: Map,
    title: "Leave with a clear plan",
    text: "Turn scattered ideas into a simple itinerary and next steps.",
  },
];

function HowItWorks() {
  return (
    <section className="bg-[#eef6fb] px-5 py-24" id="how-it-works">
      <div className="mx-auto w-full max-w-7xl reveal-up">
        <div className="max-w-3xl">
          <p className="text-sm font-extrabold uppercase tracking-normal text-ocean">
            How it works
          </p>
          <h2 className="mt-3 text-4xl font-extrabold tracking-normal text-navy md:text-5xl">
            From vague idea to confident first plan
          </h2>
        </div>

        <div className="mt-10 grid gap-5 md:grid-cols-3">
          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <article
                className="rounded-[2rem] border border-navy/10 bg-white p-6 shadow-card transition duration-300 hover:-translate-y-1 hover:shadow-soft"
                key={step.title}
              >
                <div className="flex items-center justify-between">
                  <span className="grid h-12 w-12 place-items-center rounded-2xl bg-navy text-white">
                    <Icon size={22} />
                  </span>
                  <span className="text-sm font-extrabold text-ocean/50">0{index + 1}</span>
                </div>
                <h3 className="mt-8 text-2xl font-extrabold text-navy">{step.title}</h3>
                <p className="mt-3 leading-7 text-slate-600">{step.text}</p>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}

export default HowItWorks;
