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
        100: '#F2F5F7',
        200: '#DBE2EA',
        300: '#B8C7D8',
        400: '#111A92',
        500: '#0F1780',
        600: '#0D146D',
        700: '#0B105B',
        800: '#090D49',
        900: '#070A36',
      },
      dark: {
        0: '#060B37',
        50: '#090d49',
        100: '#0D146D',
        200: '#0D146D',
        300: '#6B7280',
        400: '#9CA3AF',
        500: '#D1D5DB',
        600: '#E5E7EB',
        700: '#F3F4F6',
        800: '#F9FAFB',
        900: '#FFFFFF',
      },
      primary: {
        50: '#F2FCF9',
        100: '#E0F5EF',
        200: '#C1EBDF',
        300: '#E0F5EF',
        400: '#81D6BD',
        500: '#65CDAE',
        600: '#46C39E',
        700: '#37A987',
        800: '#2D8B6F',
        900: '#236C56',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
};
