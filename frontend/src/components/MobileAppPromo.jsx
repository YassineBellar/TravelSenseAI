import { Bell, MapPin, MessageCircle } from "lucide-react";

function MobileAppPromo({ onTryPlanner }) {
  return (
    <section className="bg-[#eef6fb] px-5 py-24" id="app">
      <div className="mx-auto grid max-w-7xl items-center gap-10 overflow-hidden rounded-[2.5rem] border border-navy/10 bg-white p-6 shadow-soft reveal-up md:grid-cols-[1fr_0.78fr] md:p-12">
        <div className="max-w-2xl">
          <p className="w-fit rounded-full bg-mist px-3 py-1.5 text-xs font-extrabold uppercase tracking-normal text-navy">
            Coming soon
          </p>
          <h2 className="mt-4 text-4xl font-extrabold tracking-normal text-navy md:text-5xl">
            TravelSense AI on mobile
          </h2>
          <p className="mt-5 text-lg leading-8 text-slate-600">
            Your travel companion, soon available on your phone.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <button
              className="min-h-12 rounded-full bg-navy px-6 text-sm font-extrabold text-white transition hover:-translate-y-0.5 hover:bg-royal"
              type="button"
            >
              Get early access
            </button>
            <button
              className="min-h-12 rounded-full border border-navy/10 bg-snow px-6 text-sm font-extrabold text-navy transition hover:-translate-y-0.5 hover:bg-mist/45"
              type="button"
              onClick={onTryPlanner}
            >
              Try the web planner
            </button>
          </div>
        </div>

        <div className="relative mx-auto w-full max-w-sm">
          <div className="absolute -left-8 top-20 hidden rounded-3xl border border-navy/10 bg-white p-4 text-navy shadow-card md:block">
            <div className="flex items-center gap-3">
              <span className="grid h-10 w-10 place-items-center rounded-full bg-mist text-navy">
                <Bell size={18} />
              </span>
              <div>
                <p className="text-sm font-extrabold">Trip reminder</p>
                <p className="text-xs text-slate-500">Sunset viewpoint saved</p>
              </div>
            </div>
          </div>

          <div className="mx-auto w-[280px] rounded-[2.5rem] border border-navy/10 bg-navy p-3 shadow-soft">
            <div className="overflow-hidden rounded-[2rem] bg-snow p-4 text-navy">
              <div className="mx-auto mb-4 h-1.5 w-16 rounded-full bg-navy/20" />
              <div className="flex items-center justify-between">
                <span className="font-extrabold">TravelSense AI</span>
                <span className="rounded-full bg-mist px-2 py-1 text-[0.65rem] font-extrabold uppercase">
                  Soon
                </span>
              </div>
              <div className="mt-5 overflow-hidden rounded-[1.5rem] bg-gradient-to-br from-mist to-ocean p-5 text-white">
                <MapPin size={22} />
                <p className="mt-16 text-2xl font-extrabold">Lisbon</p>
                <p className="text-sm font-semibold text-white/80">
                  Culture, food and slow mornings
                </p>
              </div>
              <div className="mt-4 rounded-3xl bg-white p-4 shadow-card">
                <div className="flex items-start gap-3">
                  <span className="grid h-10 w-10 flex-none place-items-center rounded-full bg-navy text-white">
                    <MessageCircle size={18} />
                  </span>
                  <p className="text-sm font-bold leading-5">
                    Your plan is saved. Want a quiet viewpoint for sunset?
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default MobileAppPromo;
