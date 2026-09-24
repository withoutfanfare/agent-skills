// Tailwind CSS v3 only. Projects on v4 use assets/theme.css instead.
// Replace the primary scale with the project's real brand colour, keep the
// token names generic, and extend rather than replace `theme` wholesale.
import type { Config } from 'tailwindcss'
import forms from '@tailwindcss/forms'

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
        // 50 and 700 pair for light mode, 900 and 200 for dark.
        success: { 50: '#ecfdf3', 200: '#a7e8c0', 700: '#15703d', 900: '#0b3d22' },
        warning: { 50: '#fff7e6', 200: '#fcd79a', 700: '#8a4b00', 900: '#4a2800' },
        danger: { 50: '#fef1f0', 200: '#fbc4bf', 700: '#b42318', 900: '#5c1410' },
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
    forms,
  ],
} satisfies Config
