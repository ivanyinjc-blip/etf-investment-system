# gzh-article-pipeline

> 微信公众号文章全流程生产流水线 — 从选题矩阵到草稿箱，全链路自动化。

## 一句话简介

**一条命令，从HTML到草稿箱，全程无人值守。** 自动上传配图、自动清理重复元素、自动替换占位符、自动推送草稿箱。

## 标签

`公众号` `微信` `自动化` `内容创作` `草稿箱` `封面图` `GPT-Image2` `Python` `AI写作` `工作流`

---

## 核心优势

| 维度 | 传统方式 | 本Skill |
|------|---------|---------|
| 选题 | 凭感觉 | 跨领域交叉选题矩阵 |
| 封面图 | 手动找图/裁剪 | GPT-Image2字体美学提示词模板 |
| 排版 | 复制到编辑器调格式 | _wx.html保留格式直接推送 |
| 配图 | 手动逐张上传 | 占位符自动匹配→上传→替换 |
| 推送 | 手动粘贴+调整 | 一条命令 `python3 wx_push_article.py` |

---

## 流水线全景

```
选题矩阵 → MD撰写 → HTML排版(_wx.html) → 封面图(GPT-Image2) → 配图准备
                                                    ↓
                                              推送草稿箱(wx_push_article.py)
                                                    ↓
                                              公众号后台 → 预览 → 发布
```

---

## 文件结构

```
skills/gzh-article-pipeline/
├── SKILL.md                              ← 完整技能文档（排版规范/操作流程）
├── README.md                             ← 本文件
├── references/
│   ├── cover-prompt-template.txt         ← 封面图提示词模板（复制到ChatGPT）
│   └── topic-matrix.md                   ← 跨领域交叉选题矩阵
│
scripts/
├── wx_push_article.py                    ← 通用图文推送脚本
└── wx_draft_image.py                     ← 单图片消息推送脚本
```

---

## 快速开始

### 环境要求

- Python 3.8+（仅标准库，零依赖）
- 微信公众号已认证（需API权限）
- ChatGPT（GPT-4o）用于生成封面图

### 配置

```bash
export WX_APP_ID="你的AppID"
export WX_APP_SECRET="你的AppSecret"
```

### 推送一篇文章

```bash
# 文章文件夹结构
公众号/B02_T型人才/
├── B02_T型人才_wx.html    # 微信适配版HTML
├── B02_封面.png           # 公众号封面图
└── B02_产品卡片.png       # 正文配图（可选）

# 一键推送
python3 scripts/wx_push_article.py "公众号/B02_T型人才" --author "阿超AI"
```

### 生成封面图

1. 分析标题深层隐喻 → 写视觉方向分析
2. 复制 `references/cover-prompt-template.txt` 到ChatGPT
3. 下载生成的封面图到文章文件夹
4. 命名规则：`封面图.png` 或 `{编号}_封面.png`

---

## B系列文章（AI思维方法论）

| 编号 | 标题 | 交叉领域 |
|------|------|---------|
| B02 | AI时代最危险的人：只懂一个领域的专家 | AI × 职业发展 |
| B03 | 收藏夹里存了三年，打开不超过三次 | AI × 信息管理 |
| B04 | AI时代最蠢的工作方式：走一步看一步 | AI × 效率思维 |

---

## 依赖

- Python 3.8+（仅标准库）
- 微信公众号已认证
- ChatGPT（封面图生成）

## 作者

阿超 AI — 专注AI工具实战与跨领域思维

## License

MIT
