import { Quote } from "lucide-react";

import { Avatar } from "./ui";

const reviews = [
  {
    quote: "It helped me compare destinations without opening ten tabs.",
    name: "Lina",
    role: "Student traveler",
    initials: "LI",
  },
  {
    quote: "I liked that it explained why a destination fits my budget.",
    name: "Thomas",
    role: "Culture explorer",
    initials: "TH",
  },
  {
    quote: "It made planning feel less overwhelming.",
    name: "Sarah",
    role: "Family traveler",
    initials: "SA",
  },
];

function Reviews() {
  return (
    <section className="bg-snow px-5 py-24" id="reviews">
      <div className="mx-auto w-full max-w-7xl reveal-up">
        <div className="mx-auto max-w-3xl text-center">
          <p className="text-sm font-extrabold uppercase tracking-normal text-ocean">Reviews</p>
          <h2 className="mt-3 text-4xl font-extrabold tracking-normal text-navy md:text-5xl">
            Designed for travelers who want clarity
          </h2>
        </div>

        <div className="mt-10 grid gap-5 md:grid-cols-3">
          {reviews.map((review) => (
            <article
              className="rounded-[2rem] border border-navy/10 bg-white p-7 shadow-card transition duration-300 hover:-translate-y-1 hover:shadow-soft"
              key={review.name}
            >
              <Quote className="text-ocean" size={28} />
              <p className="mt-6 text-xl font-bold leading-8 text-navy">"{review.quote}"</p>
              <div className="mt-8 flex items-center gap-3">
                <Avatar initials={review.initials} />
                <div>
                  <p className="font-extrabold text-navy">{review.name}</p>
                  <p className="text-sm font-semibold text-slate-500">{review.role}</p>
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

export default Reviews;
