var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

var config = require('./webpack.base.config.js')

config.output.path = require('path').resolve('./assets/dist')

config.plugins = config.plugins.concat([
  new BundleTracker({
    filename: './webpack-stats-prod.json',
    indent: '  ',
  }),

  // removes a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': JSON.stringify('production')
    }}),

  // ignore unused momentjs locales to reduce output file size
  new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
  // minify code
  new webpack.optimize.UglifyJsPlugin({
    compressor: {
      warnings: false
    },
    output: {
      comments: false,
    },
  })
])

// Add a loader for JSX files
config.module.loaders.push({
  test: /\.jsx?$/,
  exclude: /node_modules/,
  loader: 'babel-loader',
  query: {
    presets: ['es2015', 'react']
  }
})

module.exports = config
