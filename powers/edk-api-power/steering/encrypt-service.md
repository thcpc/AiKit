# 加密服务工作流

## 概述

本工作流启动本地加密服务 `scripts/encrypt-server.js`，为 Admin Auth 等需要密码加密的接口提供 RSA 加密支持。

---

## 加密服务说明

- 脚本路径：`scripts/encrypt-server.js`（位于 Power 目录下）
- 监听地址：`http://localhost:9876`
- 接口：`POST /encrypt`
- 请求体：`{ "password": "明文密码" }`
- 响应体：`{ "encrypted": "Base64编码的RSA加密密码" }`
- 加密方式：RSA PKCS1 公钥加密，密码与时间戳组合后加密

## 步骤 1：启动加密服务

使用 `controlPwshProcess` 工具以后台进程方式启动加密服务：

```
command: node scripts/encrypt-server.js
cwd: {power目录路径}
```

启动后确认输出包含 `Encrypt server running on http://localhost:9876`。

## 步骤 2：在 Admin Auth Request 中添加 Pre-request Script

**不要**将加密密码写死在请求体中。应通过 Postman 的 pre-request script 动态加密。

创建 Admin Auth Request 时，请求体保留明文密码，同时通过 `events` 参数添加 pre-request script：

```javascript
const password = pm.request.body ? JSON.parse(pm.request.body.raw).password : '';
pm.sendRequest({
    url: 'http://localhost:9876/encrypt',
    method: 'POST',
    header: { 'Content-Type': 'application/json' },
    body: { mode: 'raw', raw: JSON.stringify({ password: password }) }
}, function (err, res) {
    if (!err && res.code === 200) {
        const encrypted = res.json().encrypted;
        const body = JSON.parse(pm.request.body.raw);
        body.password = encrypted;
        pm.request.body.raw = JSON.stringify(body);
    }
});
```

在调用 `createCollectionRequest` 时，通过 `events` 参数传入：

```json
[{
    "listen": "prerequest",
    "script": {
        "type": "text/javascript",
        "exec": [
            "const password = pm.request.body ? JSON.parse(pm.request.body.raw).password : '';",
            "pm.sendRequest({",
            "    url: 'http://localhost:9876/encrypt',",
            "    method: 'POST',",
            "    header: { 'Content-Type': 'application/json' },",
            "    body: { mode: 'raw', raw: JSON.stringify({ password: password }) }",
            "}, function (err, res) {",
            "    if (!err && res.code === 200) {",
            "        const encrypted = res.json().encrypted;",
            "        const body = JSON.parse(pm.request.body.raw);",
            "        body.password = encrypted;",
            "        pm.request.body.raw = JSON.stringify(body);",
            "    }",
            "});"
        ]
    }
}]
```

## 步骤 3：使用加密密码

密码加密在 Postman 运行时自动完成：
1. Postman 执行 Admin Auth 请求前，pre-request script 自动运行
2. 脚本调用本地加密服务 `http://localhost:9876/encrypt`
3. 获取加密后的密码并替换请求体中的明文密码
4. 然后发送带加密密码的请求

## 何时需要加密

- 当 API Sequence 中包含 `admin/auth` 或 `administrator/auth` 端点时
- 当 User Input Data 中包含 `password` 字段时
- 加密服务必须在调用 Auth 接口之前启动

## 停止加密服务

使用完毕后，可通过 `controlPwshProcess` 的 stop action 停止加密服务进程。

## 故障排查

### 加密服务启动失败

**问题：** `node scripts/encrypt-server.js` 报错
**解决方案：**
1. 确认 Node.js 已安装
2. 确认脚本路径正确
3. 确认端口 9876 未被占用：`netstat -ano | findstr 9876`

### 加密接口返回 500

**问题：** 加密请求返回服务器错误
**解决方案：**
1. 确认请求体格式正确：`{ "password": "xxx" }`
2. 确认 Content-Type 为 `application/json`
3. 查看加密服务控制台输出的错误信息
