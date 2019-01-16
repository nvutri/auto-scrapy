var path = require("path")
var webpack = require('webpack')

module.exports = {
  context: __dirname,
  entry: ['babel-polyfill', './assets/js/index'],

  output: {
    path: path.resolve('./assets/bundles/'),
    filename: "[name]-[hash].js"
  },

  plugins: [],

  module: {
    loaders: [],
  },

  resolve: {
    modules: ['node_modules', 'bower_components'],
    extensions: ['.js', '.jsx']
  },
}
