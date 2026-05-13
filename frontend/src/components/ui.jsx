import { forwardRef } from "react";

export function Button({ variant = "primary", className = "", ...props }) {
  const variants = {
    primary:
      "bg-navy text-white shadow-card hover:-translate-y-0.5 hover:bg-royal",
    secondary:
      "border border-white/60 bg-white/20 text-white backdrop-blur-md hover:bg-white/30",
    ghost:
      "border border-navy/10 bg-white text-navy shadow-card hover:-translate-y-0.5 hover:border-ocean/30",
    sand:
      "bg-sand text-navy shadow-card hover:-translate-y-0.5 hover:brightness-105",
  };

  return (
    <button
      className={`inline-flex min-h-12 items-center justify-center rounded-full px-6 text-sm font-bold transition duration-200 disabled:pointer-events-none disabled:opacity-60 ${variants[variant]} ${className}`}
      {...props}
    />
  );
}

export function Card({ className = "", ...props }) {
  return (
    <div
      className={`rounded-product border border-navy/10 bg-white shadow-card ${className}`}
      {...props}
    />
  );
}

export function Badge({ className = "", ...props }) {
  return (
    <span
      className={`inline-flex w-fit items-center rounded-full border border-white/50 bg-white/20 px-3 py-1.5 text-xs font-extrabold uppercase tracking-normal text-white backdrop-blur-md ${className}`}
      {...props}
    />
  );
}

export const Textarea = forwardRef(function Textarea({ className = "", ...props }, ref) {
  return (
    <textarea
      ref={ref}
      className={`min-h-28 w-full resize-none rounded-3xl border border-navy/10 bg-white px-5 py-4 text-base text-navy outline-none transition placeholder:text-slate-400 focus:border-ocean focus:ring-4 focus:ring-ocean/[0.15] ${className}`}
      {...props}
    />
  );
});

export const Input = forwardRef(function Input({ className = "", ...props }, ref) {
  return (
    <input
      ref={ref}
      className={`h-12 w-full rounded-full border border-navy/10 bg-white px-4 text-navy outline-none transition placeholder:text-slate-400 focus:border-ocean focus:ring-4 focus:ring-ocean/[0.15] ${className}`}
      {...props}
    />
  );
});

export function Separator({ className = "" }) {
  return <div className={`h-px w-full bg-navy/10 ${className}`} />;
}

export function Avatar({ initials, className = "" }) {
  return (
    <div
      className={`grid h-10 w-10 place-items-center rounded-full bg-royal text-sm font-extrabold text-white ${className}`}
    >
      {initials}
    </div>
  );
}

export function Tabs({ children, className = "" }) {
  return <div className={`rounded-full bg-snow p-1 ${className}`}>{children}</div>;
}

export function Accordion({ children, className = "" }) {
  return <div className={`divide-y divide-navy/10 ${className}`}>{children}</div>;
}

