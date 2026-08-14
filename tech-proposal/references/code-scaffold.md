# 代码骨架标准

tech-proposal 代码骨架阶段的深度参考。按需读，不常驻。

## 核心原则：接口优先

**先冻结所有共享类型和接口，再写伪代码。** 接口是契约，伪代码是草图。代码块是方案文档的一部分，给人读不给编译器跑——目标是**精确传达接口和逻辑流**，不是可执行代码。

## 两层代码块

### 第一层：接口定义（完整，无 stub）

类型、接口、函数签名全部写完；参数与返回类型完整标注；禁止 `any` / `unknown` / `object` / `interface{}` 等逃逸类型；doc comment 写职责和关键约束。占位用目标栈原生机制（`...` / `todo!()` / `throw` / Protocol / trait——agent 自知）：

```python
class VoicePipeline:
    """语音→指令 pipeline：ASR → NLU → Command"""

    def __init__(self, asr: ASREngine, nlu: NLUAgent) -> None:
        self._asr = asr
        self._nlu = nlu

    async def process(self, audio: AudioStream) -> Command:
        """音频流 → 结构化指令。抛 AudioError / NLUError。"""
        ...
```

### 第二层：关键路径伪代码（逻辑骨架 + TODO）

核心逻辑流在（步骤 1→2→3），实现细节留 `TODO(#N): 描述`：

```python
async def handle_voice_command(pipeline: VoicePipeline, robot: Robot) -> None:
    # 1. 采集音频
    audio = await capture_audio()  # TODO(#1): 实现 VAD 静音检测
    # 2. 语音→指令
    cmd = await pipeline.process(audio)  # TODO(#2): 处理 NLU 置信度低的情况
    # 3. 安全检查
    if not safety_check(cmd, robot.joint_state()):  # TODO(#3): 定义安全规则
        return
    # 4. 执行
    await robot.execute(cmd)
```

## TODO(#N) 格式

标准格式 `TODO(#N): 描述`——编号在方案文档内全局递增、与「风险与待定」节交叉引用。复杂场景用增强格式：

```python
# TODO(#4): 实现模型预热
# Why: 首次推理延迟 3-5s，需预热到 <200ms
# How: 启动时跑 3-5 次 dummy inference
```

## 一致性

C4 图的 Container/Component 名 = 代码块的类/模块名；模块职责表的接口名 = trait/interface 名；数据流图的箭头 = 代码调用；代码块出现的每个类型在某处有定义。有类型检查器的栈，接口定义应能 check 过；没有则人工 review。（SKILL.md 自检清单是验收门。）
