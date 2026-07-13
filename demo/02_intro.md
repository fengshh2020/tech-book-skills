# 导论：为什么是 Zenoh

Zenoh 是一个超低开销的 pub/sub + 查询协议，线上 wire overhead 只有 4-6 字节。本章先用一个最小数据流建立直觉。

> **[性能提示]** Zenoh 的线上开销仅 4-6 字节，适合带宽受限的边缘场景。

## 最小数据流

从输入到 worker，数据流动如下（证据见 `example.py:1-3`）：

```mermaid
flowchart LR
  Input -->|passes data| Worker
```

图：最小数据流（example.py:1-3）

## 发布一条消息

用 `put` 即可发布一次消息：

```python caption="Listing 2-1: 一次性发布"
from zenoh import Zenoh

with Zenoh.open({}) as session:
    session.put("demo/key", "Hello")
```

## 关键术语

| 概念 | 含义 |
|------|------|
| Session | Zenoh 的核心组件，管理所有网络连接 |
| KeyExpr | 键表达式，Zenoh 的地址空间，支持通配符 |
| put | 一次性发布的快捷方法 |
