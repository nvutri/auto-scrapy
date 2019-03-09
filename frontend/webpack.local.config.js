var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

var config = require('./webpack.base.config.js')

const webpackDevServerPort = 3000;

config.entry = [
  `webpack-dev-server/client?http://localhost:${webpackDevServerPort}`,
  'webpack/hot/only-dev-server',
  './js/index'
]

config.output.publicPath = `http://localhost:${webpackDevServerPort}/assets/bundles/`;

config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoEmitOnErrorsPlugin(), // don't reload if there is an error
  new BundleTracker({filename: './webpack-stats.json', indent: '  '}),
])

config.devServer = {
  hot: true,
  inline: true,
  port: webpackDevServerPort,
  headers: {
    'Access-Control-Allow-Origin': '*'
  }
}

config.module.loaders.push({
  test: /\.jsx?$/,
  exclude: /node_modules/,
  loader: 'babel-loader',
  query: {
    presets: ['es2015', 'react']
  }
})

module.exports = config
