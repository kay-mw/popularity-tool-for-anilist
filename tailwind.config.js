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

          neutral: "#171717",

          "base-100": "#141414",

          info: "#262626",

          success: "#00ff81",

          warning: "#ffd100",

          error: "#ff84a5",
        },
      },
    ],
  },
  plugins: [require("daisyui")],
};
