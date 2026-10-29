# nonebot-plugin-homo

把任意数字转换成「114514 风格」的恶臭数字论证表达式。

## 安装

使用 NB-CLI 安装（推荐）：

```bash
nb plugin install nonebot-plugin-homo
```

或用 pip：

```bash
pip install nonebot-plugin-homo
```

安装后在 `.env` 中确认已启用 OneBot V11 适配器：

```dotenv
DRIVER=~fastapi
COMMAND_START=["/"]
```

## 使用

```
/homo 400
```

返回：

```
400 = -114+514
```

别名：`/HOMO`。

更多例子：

| 输入 | 输出 |
| --- | --- |
| `/homo 0` | `0 = (1-1)*4514` |
| `/homo 114514` | `114514 = 114514` |
| `/homo 1000` | `1000 = 1+14*5*14+1+1+4*5+1-4` |
| `/homo -5` | `-5 = (11-4-5+1-4)*(11-4*5+14)` |
| `/homo 12345` | `12345 = 11451+4+11*4*5*1*4-11/4+51/4` |

输出的表达式只用 `1`、`4`、`5` 这些数字与四则运算拼成，可以自行验算。

## 配置

配置项均为可选，在 `.env` 中填写即可覆盖默认值：

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `HOMO_MAX_INPUT` | int | `1000000000000` | 允许输入的数字绝对值上限 |
| `HOMO_MAX_LENGTH` | int | `2000` | 生成表达式的最大字符数 |

示例：

```dotenv
HOMO_MAX_INPUT=100000
```

## 支持的适配器

仅支持 **OneBot V11**（使用了 `at_sender` 参数）。

## 开发

```bash
git clone https://github.com/Ltiiatn/nonebot-plugin-homo.git
cd nonebot-plugin-homo
pip install -e ".[dev]"
pytest
```

