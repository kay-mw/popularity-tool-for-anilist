/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,js,svelte,ts}"],
  theme: {},
  daisyui: {
    themes: [
      {
        mytheme: {
          primary: "#00bbbc",
          secondary: "#00c79c",
          accent: "#c45a00",
          neutral: "#171717",
          "base-100": "#141414",
          info: "#ffffff",
          success: "#00ff81",
          warning: "#f43f5e",
          error: "#ff84a5",
        },
      },
    ],
  },
  plugins: [require("daisyui")],
};
