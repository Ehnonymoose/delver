var webpack = require('webpack');
var UglifyJsPlugin = webpack.optimize.UglifyJsPlugin;
var env = process.env.WEBPACK_ENV;

var appName = 'app';
var host = '0.0.0.0';
var port = '9000';

var plugins = [], outputFile;

if (env === 'prod') {
  plugins.push(new UglifyJsPlugin({ minimize: true }));
  outputFile = appName + '.min.js';
} else {
  outputFile = appName + '.js';
}

var config = {
  entry: './src/app.jsx',
  devtool: 'source-map',
  resolve: {
    root: __dirname + '/src',
    extensions: ['', '.js', '.jsx']
  },
  output: {
    path: __dirname + '/../server/public/js',
    filename: outputFile,
    publicPath: __dirname + '/../server/public'
  },
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        loaders: ['babel?cacheDirectory'],
        exclude: 'node_modules'
      }
    ]
  },
  plugins: plugins
};

module.exports = config;
