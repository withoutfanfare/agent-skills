// Starting point for a token-driven Tailwind config.
// Replace the primary scale with the project's real brand colour, keep the
// token names generic, and extend rather than replace `theme` wholesale.
import type { Config } from 'tailwindcss'

export default {
  content: [
    './src/**/*.{html,js,ts,jsx,tsx,vue}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eef4ff',
          100: '#d9e6ff',
          300: '#93b8ff',
          500: '#3d7bff',
          600: '#2a5fe0',
          700: '#1f47ad',
          900: '#142b66',
        },
        surface: {
          light: '#ffffff',
          dark: '#101418',
        },
        success: '#1f9d55',
        warning: '#d97a06',
        danger: '#d9342b',
      },
      spacing: {
        // 4px base unit; extend only where the default scale skips a value
        // the project actually uses.
        18: '4.5rem',
      },
      fontSize: {
        // [size, { lineHeight }] so type and leading move together.
        sm: ['0.875rem', { lineHeight: '1.35rem' }],
        base: ['1rem', { lineHeight: '1.5rem' }],
        lg: ['1.125rem', { lineHeight: '1.75rem' }],
        xl: ['1.375rem', { lineHeight: '1.85rem' }],
      },
      borderRadius: {
        card: '0.75rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
} satisfies Config
