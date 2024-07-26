/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./refactor_app/**/*.{html,js}"],
  theme: {
    extend: {
      transitionProperty: {
        'width': 'width',
      },
    },
  },
  plugins: [],
};
