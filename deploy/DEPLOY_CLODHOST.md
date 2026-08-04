# 元晟传媒工作台 · ClodHost 部署手册

与 `Windows-Copilot-API-master/jobnext/zhuanchang-platform` 中 **转场罗盘** 共用同一台 ClodHost 服务器。

## 服务器现状（来自仓库配置）

| 项目 | 值 |
| --- | --- |
| 公网 IP | `78.47.174.254` |
| 域名 | `clodhost.com` |
| Web 服务 | Apache（HTTPS 自签证书 `/etc/ssl/hermes/`） |
| FreeLLMAPI | `127.0.0.1:3001` |
| 转场罗盘 API | `127.0.0.1:3002` → `compass.clodhost.com` |
| **本工作台** | `127.0.0.1:8025` → `gensight.clodhost.com`（待配置） |

参考文档：`Windows-Copilot-API-master/jobnext/zhuanchang-platform/DEPLOY_CN_LOW_COST.md` 附录「ClodHost 同机部署」。

## 1. DNS

在 `clodhost.com` 添加 A 记录：

```
gensight → 78.47.174.254
```

## 2. SSH 登录

本机已有密钥 `~/.ssh/id_clodhost`（`known_hosts` 中已有该 IP 记录）。若登录失败，需在服务器控制台重新授权公钥：

```bash
# 本机查看公钥
cat ~/.ssh/id_clodhost.pub
```

建议在 `~/.ssh/config` 增加：

```
Host clodhost
    HostName 78.47.174.254
    User root
    IdentityFile ~/.ssh/id_clodhost
    StrictHostKeyChecking accept-new
```

测试：`ssh clodhost "hostname"`

## 3. 首次服务器初始化（仅需一次）

```bash
ssh clodhost

sudo mkdir -p /srv/gensight/current
sudo chown -R $USER:$USER /srv/gensight

# systemd 服务
sudo cp /srv/gensight/current/deploy/systemd/gensight.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gensight

# Apache 虚拟主机
sudo cp /srv/gensight/current/deploy/apache/gensight.conf /etc/apache2/sites-available/
sudo a2ensite gensight.conf
sudo apache2ctl configtest && sudo systemctl reload apache2
```

## 4. 本机同步代码

```bash
cd /Users/apple/Desktop/Gensight
chmod +x deploy/sync-to-server.sh
./deploy/sync-to-server.sh
```

或手动 rsync：

```bash
rsync -avz --delete \
  -e "ssh -i ~/.ssh/id_clodhost" \
  /Users/apple/Desktop/Gensight/ \
  root@78.47.174.254:/srv/gensight/current/
```

## 5. 启动与验证

```bash
ssh clodhost "sudo systemctl restart gensight && sudo systemctl status gensight --no-pager"
ssh clodhost "curl -s http://127.0.0.1:8025/api/data | head -c 120"
```

浏览器访问：`https://gensight.clodhost.com`（自签证书需在浏览器中信任一次）。

侧边栏显示「双人协同已开启」表示 `/api/data` 正常。

## 6. 日常更新

```bash
./deploy/sync-to-server.sh
ssh clodhost "sudo systemctl restart gensight"
```

`data.json` 在服务器上持久保存；同步时**不要**用 `--delete` 覆盖服务器上已积累的协同数据——若需保留服务器数据，去掉 rsync 的 `--delete`，或先 `scp` 备份 `data.json`。

## 7. 安全提示

当前工作台无登录鉴权，部署到公网后Howard、Brian以外的人也可能访问。**建议**：

- 在 Apache 对该 VirtualHost 加 HTTP Basic Auth；或
- 仅允许固定 IP（办公室 / 家庭宽带）；或
- 使用 VPN / Tailscale 内网访问。

内部运营数据（渠道价、询盘）请勿长期暴露在无保护公网。

## 端口对照（同机共存）

```
3001  FreeLLMAPI
3002  compass-api（转场罗盘）
8025  gensight（元晟传媒工作台）← 本部署
```
