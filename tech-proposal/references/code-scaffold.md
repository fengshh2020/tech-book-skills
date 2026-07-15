# 代码骨架标准

tech-proposal 阶段⑤的深度参考。按需读，不常驻。

## 核心原则：接口优先

**Wave 0 定义所有共享类型，冻结后才写伪代码。** 接口是契约，伪代码是草图。

> "The moment your spec says 'use a Redis sorted set,' you have stopped specifying and started coding badly in English." — Spec-Driven Development

代码块是方案文档的一部分，给人读不给编译器跑。目标是**精确传达接口和逻辑流**，不是可执行代码。

## 两层代码块

### 第一层：接口定义（完整，无 stub）

- 类型、接口、函数签名全部写完
- 参数类型和返回类型完整标注
- 禁止 `any` / `unknown` / `object` / `interface{}` 等逃逸类型
- doc comment 写职责和关键约束

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

```rust
trait MotionController {
    /// 执行运动指令，返回执行状态
    fn execute(&mut self, cmd: MotionCommand) -> Result<ExecStatus, MotionError>;
    
    /// 紧急停机，不经过指令队列
    fn emergency_stop(&mut self) -> Result<(), SafetyError>;
    
    /// 当前关节状态
    fn joint_state(&self) -> JointState;
}
```

### 第二层：关键路径伪代码（逻辑骨架 + TODO）

- 核心逻辑流在（步骤 1→2→3）
- 实现细节留 `TODO(#N): 描述`
- 函数体用 `...` 或 `throw new Error('UNIMPLEMENTED')` 占位

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

**标准格式**：`TODO(#N): 描述`

| 格式 | 正确？ | 原因 |
|------|--------|------|
| `# TODO(#1): 实现 VAD 静音检测` | ✅ | 编号+描述 |
| `# TODO: fix later` | ❌ | 无编号、无描述、不可追踪 |
| `# TODO Auto-generated method stub` | ❌ | 无上下文 |
| `# TODO(#2): 处理 NLU 置信度低的情况` | ✅ | 编号+具体描述 |

**编号规则**：
- 方案文档内全局递增（#1, #2, #3…）
- 编号在自检时验证无遗漏
- 编号与方案文档"风险与待定"节交叉引用

**增强格式**（可选，复杂场景推荐）：

```python
# TODO(#4): 实现模型预热
# Why: 首次推理延迟 3-5s，需预热到 <200ms
# How: 启动时跑 3-5 次 dummy inference
```

## 代码块与架构图的一致性

**自检项**：

| 检查 | 方法 |
|------|------|
| 模块名一致 | C4 图中的 Container/Component 名 = 代码块中的类/模块名 |
| 接口名一致 | 模块职责表的"关键接口" = 代码块中的 trait/interface 名 |
| 调用关系一致 | 数据流图中的箭头 = 代码块中的调用 |
| 类型引用有定义 | 代码块中出现的类型在某个接口定义块中有定义 |

**可选工具**（不强制，agent 可能没装）：
- **baft**：Mermaid 图 → 代码 import 一致性验证
- **archspec**：YAML 架构契约 → CI 门

## 各技术栈约定

| 栈 | 接口定义方式 | 伪代码占位 | 类型检查器 |
|----|-------------|-----------|-----------|
| Python | `class` + `Protocol` + type hints | `...` (Ellipsis) | mypy / basedpyright |
| Rust | `trait` + `struct` + `enum` | `todo!()` | cargo check |
| Go | `interface` + `struct` | `panic("not implemented")` | go build |
| TypeScript | `interface` + `type` + `class` | `throw new Error('UNIMPLEMENTED')` | tsc --noEmit |
| C++ | 纯虚类 + `struct` | `= 0` / `// TODO(#N)` | cmake (头文件可编译) |
| Shell | 函数定义 + 注释 | `# TODO(#N): implement` | 无（降级为人工 review） |

**自适应验证**：有类型检查器的栈，接口定义应能 check 过（如果提取到文件）；没有的降级为人工 review。

## 反模式

| 反模式 | 问题 | 修正 |
|--------|------|------|
| 接口定义用 `any` | 逃逸类型=没定义 | 写出具体类型 |
| 伪代码写实现细节 | 方案不是实现 | 只留逻辑流+TODO |
| TODO 无编号 | 不可追踪 | `TODO(#N):` |
| 代码块与架构图模块名不一致 | 读者困惑 | 统一命名 |
| 同一接口定义两次且矛盾 | 自相矛盾 | 只定义一次，引用 |
