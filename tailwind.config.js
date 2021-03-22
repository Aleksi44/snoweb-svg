const colors = require('tailwindcss/colors');

module.exports = {
  purge: [
    './app/**/*.html',
  ],
  darkMode: 'class',
  theme: {
    fill: {
      current: 'currentColor',
    },
    colors: {
      white: colors.white,
      red: colors.red,
      green: colors.green,
      orange: colors.orange,
      light: {
        0: '#FFFFFF',
        50: '#F9FAFB',
        100: '#F3F4F6',
        200: '#E5E7EB',
        300: '#D1D5DB',
        400: '#9CA3AF',
        500: '#6B7280',
        600: '#4B5563',
        700: '#374151',
        800: '#1F2937',
        900: '#111827',
      },
      dark: {
        0: '#010917',
        50: '#030E1F',
        100: '#020D21',
        200: '#293340',
        300: '#434E5D',
        400: '#5E6774',
        500: '#78818E',
        600: '#9199A7',
        700: '#A7AFBC',
        800: '#B3BAC6',
        900: '#C9CED8',
      },
      primary: {
        50: '#EAF2FA',
        100: '#C4DFFA',
        200: '#9DCBF7',
        300: '#75B4F0',
        400: '#4C95DB',
        500: '#32679B',
        600: '#144B82',
        700: '#0C3157',
        800: '#08233E',
        900: '#041322',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
};
