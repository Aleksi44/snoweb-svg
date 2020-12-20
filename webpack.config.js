const path = require('path');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const BrowserSyncPlugin = require('browser-sync-webpack-plugin');
const { version } = require('./package.json');

module.exports = ({ mode = 'development' } = {}) => {
  const isProductionBuild = mode === 'production';
  const defaultPlugins = [];
  const productionPlugins = [
    new CleanWebpackPlugin(['build']),
  ];
  const devPlugins = [
    new BrowserSyncPlugin({
      proxy: '127.0.0.1:4243',
      port: 3009,
      files: [
        'snowebsvg/static/snowebsvg/src/scss/**/*.scss',
        'snowebsvg/static/dist/js/**/*.js',
      ],
      reloadDelay: 0,
      notify: false,
      open: false,
    }),
  ];

  return {
    entry: {
      app: path.resolve(__dirname, 'snowebsvg/static/snowebsvg/src/js/app.js'),
      styles: path.resolve(__dirname, 'snowebsvg/static/snowebsvg/src/scss/styles.scss'),
    },
    output: {
      filename: `static/snowebsvg/dist/js/[name]${version}.js`,
      chunkFilename: `static/snowebsvg/dist/js/[name]${version}.js`,
      path: path.resolve(__dirname, 'snowebsvg'),
      publicPath: '/',
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          use: {
            loader: 'babel-loader',
          },
        },
        {
          test: /\.html$/,
          use: {
            loader: 'html-loader',
          },
        },
        {
          test: /\.(png|svg|jpg|gif)$/,
          use: {
            loader: 'file-loader',
          },
        },
        {
          test: /\.(eot|svg|ttf|woff|woff2|otf)$/,
          loader: 'file-loader',
        },
        {
          test: /\.css$/i,
          use: ['style-loader', 'css-loader'],
        },
        {
          test: /\.s[ac]ss$/i,
          use: [
            {
              loader: 'file-loader',
              options: {
                name: `static/snowebsvg/dist/css/[name]${version}.css`,
              },
            },
            {
              loader: 'extract-loader',
            },
            {
              loader: 'css-loader?-url',
            },
            {
              loader: 'postcss-loader',
            },
            {
              loader: 'sass-loader',
            },
          ],
        },
      ],
    },
    plugins: [
      ...defaultPlugins,
      ...isProductionBuild ? productionPlugins : devPlugins,
    ],
    devtool: isProductionBuild ? 'source-map' : false,
    devServer: {
      open: true,
      disableHostCheck: true,
      proxy: {
        '/': {
          target: 'http://127.0.0.1:4243',
        },
      },
    },
  };
};
