// 本地加密服务 - 供 Postman pre-request 脚本调用
// 启动: node encrypt-server.js
const http = require('http');
const crypto = require('crypto');

const RSA_PUB_KEY = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCTYnHdPs3A6JDZanoNumpZqoTam3B4yMiRblbaSmxGs8tW5AUEGfdevRZJn3zg/g0KETIptFXJ7oFbhYdmeo5Q8XEQnrXU1Q9GKyVZBpfJujGD7y3MaMYw29TwUdAuWDm0aWAqiwlqR2B9IWPkVBysIp2BypwfMrpe5IutObo3jQIDAQAB\n-----END PUBLIC KEY-----';

const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/encrypt') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const { password } = JSON.parse(body);
        const dto = JSON.stringify({ password, time: Date.now() });
        const encrypted = crypto.publicEncrypt(
          { key: RSA_PUB_KEY, padding: crypto.constants.RSA_PKCS1_PADDING },
          Buffer.from(dto, 'utf8')
        );
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ encrypted: encrypted.toString('base64') }));
      } catch (e) {
        res.writeHead(500);
        res.end(JSON.stringify({ error: e.message }));
      }
    });
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

server.listen(9876, () => console.log('Encrypt server running on http://localhost:9876'));
