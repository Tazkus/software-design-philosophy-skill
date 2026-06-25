# Software Design Philosophy for Codex

一个可安装的 Codex 插件，内含 `software-design-philosophy` Skill。它把 John Ousterhout 在 *A Philosophy of Software Design* 中强调的复杂度管理思想，整理成可执行的软件设计、评审和重构流程。

本项目不是书籍内容的复制，也不隶属于作者或出版社；Skill 中的文字、模板和示例均为面向工程实践的原创转述。

## 它解决什么问题

Skill 会让 Codex 在设计或修改代码时优先关注：

- 变更放大、认知负担和隐藏依赖；
- 深模块与简单接口；
- 信息隐藏和单一知识所有权；
- 适度通用而非过度抽象；
- 将复杂度下沉到模块内部；
- 从语义上减少错误和特殊情况；
- 对重要设计至少比较两个方案；
- 精确命名、接口注释和可发现的约束。

它不会机械地要求“方法越短越好”或“类越小越好”，也不会把纯格式化任务升级成架构重构。

## 项目结构

```text
.
├── .agents/plugins/marketplace.json
├── .codex-plugin/plugin.json
├── .github/workflows/validate.yml
├── skills/software-design-philosophy/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   │   ├── principles.md
│   │   ├── review-rubric.md
│   │   └── examples.md
│   └── assets/design-review-template.md
├── evals/
│   ├── prompts.csv
│   └── rubric.md
├── scripts/validate.py
├── CHANGELOG.md
└── LICENSE
```

## 安装

将本仓库添加为 Codex marketplace：

```bash
codex plugin marketplace add Tazkus/software-design-philosophy-skill
```

然后启动 Codex，运行 `/plugins`，在 **Software Design Philosophy** marketplace 中安装同名插件。

也可以克隆仓库后从本地路径安装，便于开发和测试：

```bash
git clone https://github.com/Tazkus/software-design-philosophy-skill.git
codex plugin marketplace add ./software-design-philosophy-skill
```

## 调用示例

显式调用：

```text
使用 $software-design-philosophy 评审这个缓存模块，给出两个接口方案并推荐一个。
```

```text
Use $software-design-philosophy to refactor this parser so format knowledge has one owner.
```

适合隐式触发的请求：

```text
这个改动每次都要修改六个文件。请分析变更放大并重构模块边界。
```

```text
Compare these API designs for cognitive load, information leakage, and error semantics.
```

不应触发的请求：

```text
把这个文件格式化，并升级依赖版本。
```

## 输出方式

对于重要设计，Skill 默认输出：

1. 上下文与约束；
2. 有代码证据的复杂度诊断；
3. 两个结构上不同的方案；
4. 明确选择和理由；
5. 修改计划或实现摘要；
6. 验证结果；
7. 剩余风险与权衡。

## 验证

项目只依赖 Python 标准库：

```bash
python3 scripts/validate.py
```

验证器会检查：

- 插件 manifest；
- marketplace 条目；
- Skill front matter 与必需章节；
- `agents/openai.yaml` UI metadata；
- 参考文件和模板；
- eval prompt 集中的正例与负例。

## Evals

`evals/prompts.csv` 提供触发与非触发样例，`evals/rubric.md` 定义行为评分标准。可以使用 `codex exec --json` 运行实际回归测试，再按 rubric 评分。

建议从这些场景开始：

- 架构或 API 评审；
- 模块边界和信息泄漏诊断；
- 重构计划与实现；
- 异常、配置和调用顺序简化；
- 命名与注释的抽象层次评审。

## 设计边界

- 正确性、安全性、可靠性和兼容性约束优先于简化。
- 不以减少代码行数为目标，而以降低全系统维护成本为目标。
- 不在缺少证据时建议重写整个系统。
- 不将书中的原则当作僵化规则；每个建议都应说明具体收益与代价。

## License

MIT。参见 `LICENSE`。
