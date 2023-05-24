const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://101.188.82.212:58000',
      changeOrigin: true,
    })
  );
};
