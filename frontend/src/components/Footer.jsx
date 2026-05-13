function Footer() {
  return (
    <footer className="border-t border-white/10 bg-navy px-5 py-10 text-white">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-xl font-extrabold">TravelSense AI</p>
          <p className="mt-2 text-white/[0.55]">Smarter travel planning through conversation.</p>
        </div>
        <nav className="flex flex-wrap gap-5 text-sm font-bold text-white/[0.58]">
          <a className="hover:text-white" href="#destinations">Destinations</a>
          <a className="hover:text-white" href="#how-it-works">How it works</a>
          <a className="hover:text-white" href="#reviews">Reviews</a>
          <a className="hover:text-white" href="#app">App</a>
        </nav>
      </div>
    </footer>
  );
}

export default Footer;

