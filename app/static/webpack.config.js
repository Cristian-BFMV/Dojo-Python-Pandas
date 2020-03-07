const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCSSExtractPlugin = require('mini-css-extract-plugin');
// Webpack uses this to work with directories
const path = require('path');
const extractTextPlugin = require('extract-text-webpack-plugin');
// This is main configuration object.
// Here you write different options and tell Webpack what to do
module.exports = {

  // Path to your entry point. From this file Webpack will begin his work
  entry: {
        'app': './js/index.js',
        'styles-custom': './css/index.js'
    },

  // Path and filename of your result bundle.
  // Webpack will bundle all JavaScript into this file
  output: {
    //path: path.resolve(__dirname, ''),
    //filename: 'bundle.js'
    path: path.resolve(__dirname, 'dist'), //directory for output files
    filename: '[name].js' //using [name] will create a bundle with same file name as source
  },
  module: {
    rules: [
         {
                  test: /\.js$/,
                  loader: 'ify-loader'
         },
        {
          test: /\.js$/,
          exclude: /(node_modules)/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-env']
            }
          }
        },
        {
            // Exposes jQuery for use outside Webpack build
            test: require.resolve('jquery'),
            use: [{
                loader: 'expose-loader',
                options: 'jQuery'
            }, {
                loader: 'expose-loader',
                options: '$'
            }]
        },
        {
            test: /\.css$/,
            loader: [
              MiniCSSExtractPlugin.loader,
              "css-loader"
            ]
          }
    ]
  },
    plugins: [
        new MiniCSSExtractPlugin({
          filename: "./custom-styles.css",
        })
      ],
  mode: 'development'
};
