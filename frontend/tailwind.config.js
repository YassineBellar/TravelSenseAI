/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        navy: "#0A1931",
        mist: "#B3CFE5",
        ocean: "#4A7FA7",
        royal: "#1A3D63",
        snow: "#F6FAFD",
        sand: "#E9C46A",
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', "Inter", "system-ui", "sans-serif"],
      },
      boxShadow: {
        soft: "0 24px 70px rgba(10, 25, 49, 0.14)",
        card: "0 18px 45px rgba(10, 25, 49, 0.10)",
      },
      borderRadius: {
        product: "2rem",
      },
    },
  },
  plugins: [],
};
