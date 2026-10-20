# motedb.github.io

MoteDB 官网源码 · GitHub Pages 直出静态站，无构建框架。

## 文件

| 路径 | 说明 |
|---|---|
| `index.html` | **唯一事实源**（中文，`lang="zh-CN"`）。样式、脚本、双语字典全部内联 |
| `en/index.html` | **构建产物**，由 `build_en.py` 生成，不要手改 |
| `build_en.py` | 从 `index.html` 派生英文页：静态替换全部 `data-i18n` 节点 + 语言相关 `<head>` 字段 |
| `sitemap.xml` | 两个 URL 各带 hreflang 互指（zh-CN / en / x-default） |
| `404.html` | 双语品牌 404（GitHub Pages 自动识别），`noindex` |
| `og-card.html` → `og-zh.png` / `og-en.png` | 分享卡片模板与产物（1200×630）。改模板后在浏览器以 1200×630 视口分别打开 `og-card.html` 和 `og-card.html?lang=en` 截图覆盖 |
| `robots.txt` | 全放行 + 显式欢迎主流 AI 爬虫 |
| `llms.txt` / `llms-full.txt` | [llmstxt.org](https://llmstxt.org) 标准，供 LLM/AI 搜索读取 |

## 改页面

```bash
# 1. 只改 index.html（文案改字典 I18N 的 zh/en 两份，结构改 HTML）
# 2. 重新生成英文页
python3 build_en.py
# 3. 两份一起提交
git add index.html en/index.html && git commit && git push
```

`build_en.py` 内置断言：任一 `<head>` 替换命中数不为 1、或替换的 i18n 节点数与源文件 `data-i18n` 总数不等，即中止并报错——防止源页改动后英文页静默漂移。

## 语言路由

- `/` 中文、`/en/` 英文，由 URL 决定爬虫看到的语言；两页互相声明 hreflang。
- 导航栏语言按钮在两个 URL 之间跳转并记住偏好（localStorage `motedb-lang`）。
- 根路径上无偏好且浏览器非中文时，仅做**页内**翻译，不自动跳转（Google 不建议按 UA 语言重定向）。

## 访问统计

GoatCounter（免 cookie），后台 https://motedb.goatcounter.com 。排除自己的访问：浏览器打开一次 `https://motedb.github.io/#toggle-goatcounter`。
