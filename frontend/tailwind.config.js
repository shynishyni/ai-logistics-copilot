/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          950: '#0b0f19',
          900: '#0f172a',
          850: '#161f30',
          800: '#1e293b',
          700: '#334155',
        },
        brand: {
          cyan: '#06b6d4',
          blue: '#3b82f6',
          purple: '#8b5cf6',
          emerald: '#10b981',
        }
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
        'glow-blue': '0 0 20px rgba(59, 130, 246, 0.35)',
        'glow-cyan': '0 0 20px rgba(6, 182, 212, 0.35)',
      },
      backdropBlur: {
        'xs': '2px',
        'glass': '16px',
      },
      animation: {
        'pulse-subtle': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.3s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(6px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    },
  },
  plugins: [],
}
