/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        "dm-sans": ["DM Sans", "sans-serif"],
      },
    },
  },
  daisyui: {
    themes: [
      {
        mytheme: {
          primary: "#00bbbc",

          secondary: "#00c79c",

          accent: "#c45a00",

          neutral: "#1c1917",

          "base-100": "#141414",

          info: "#111827",

          success: "#00ff81",

          warning: "#ffd100",

          error: "#ff84a5",
        },
      },
    ],
  },
  plugins: [require("daisyui")],
};
