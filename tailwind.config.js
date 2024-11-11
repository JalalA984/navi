/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./flask_app/templates/**/*.{html,js,jsx,ts,tsx,vue,astro,svelte}"],
  theme: {
    extend: {
      fontFamily: {
        mono: ['"Fira Mono"', 'monospace'],
      },
      keyframes: {
        glitch: {
          '2%, 64%': { transform: 'translate(2px, 0) skew(0deg)' },
          '4%, 60%': { transform: 'translate(-2px, 0) skew(0deg)' },
          '62%': { transform: 'translate(0, 0) skew(5deg)' },
        },
        glitchTop: {
          '2%, 64%': { transform: 'translate(2px, -2px)' },
          '4%, 60%': { transform: 'translate(-2px, 2px)' },
          '62%': { transform: 'translate(13px, -1px) skew(-13deg)' },
        },
        glitchBottom: {
          '2%, 64%': { transform: 'translate(-2px, 0)' },
          '4%, 60%': { transform: 'translate(-2px, 0)' },
          '62%': { transform: 'translate(-22px, 5px) skew(21deg)' },
        },
      },
      animation: {
        glitch: 'glitch 1s linear infinite',
        glitchTop: 'glitchTop 1s linear infinite',
        glitchBottom: 'glitchBottom 1.5s linear infinite',
      },
    },
  },
  plugins: [],
}

