const path = require("path");
const basePath = path.join(__dirname, "/webserver/static/js");
const ManifestPlugin = require("webpack-manifest-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const ForkTsCheckerWebpackPlugin = require("fork-ts-checker-webpack-plugin");

module.exports = function (env) {
  const isProd = env === "production";
  const plugins = [
    new CleanWebpackPlugin(),
    new ManifestPlugin(),
    new ForkTsCheckerWebpackPlugin({
      typescript: {
        diagnosticOptions: {
          semantic: true,
          syntactic: true,
        },
        mode: "write-references",
      },
      eslint: {
        files: "**/js/src/**/*.{ts,tsx,js,jsx}",
        options: { fix: !isProd },
      },
    }),
  ];
  return {
    mode: isProd ? "production" : "development",
    entry: {
      main: path.join(basePath, "src/RecentListens.tsx")
    },
    output: {
      filename: "[name].js",
      path: path.join(basePath, "dist")
    },
    devtool: isProd ? false : "inline-source-map",
    module: {
      rules: [
        {
          test: /\.(js|jsx|ts|tsx)$/,
          exclude: /node_modules/,
          use: ['babel-loader']
        }
      ]
    },
    watch: !isProd
  };
};
