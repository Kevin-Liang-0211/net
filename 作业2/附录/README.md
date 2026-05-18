# 作业 2 — 文件说明（题目 · 代码 · 数据集）

本目录为第二次作业相关材料：`src/` 中为 Python 实现，`data/` 存放或缓存公开数据集，`figures/` 为运行实验得到的图像，`output/` 为数值汇总结果。书面论述与图表解读见 **`第二次作业解答.docx`**（与本 `README.md` 置于同一目录即可）。

---

## 目录结构（整理后）

| 路径 | 含义 |
|------|------|
| `README.md` | 本说明：各题与脚本、数据集的对应关系 |
| `requirements.txt` | Python 依赖 |
| `run_all.py` | 依次运行各题实验脚本，写入 `output/results_summary.json` |
| `build_docx.py` | 可选：排版辅助（插图、表格与公式引用） |
| `equation_images.py` | 可选：公式插图渲染 |
| `第二次作业解答.docx` | 作业解答正文 Word 文件（与 `README.md` 同目录即可） |
| `src/` | 各题核心代码 |
| `data/` | 数据集缓存目录（首次运行可从网络拉取，见下表） |
| `figures/` | 实验输出图像（含 `equations/` 公式图等） |
| `output/` | `results_summary.json`（各题关键指标的汇总） |

---

## 各题与代码、数据集对应

### 第 1 题 — 社团结构定义、评价准则与算法综述

- **代码**：无独立脚本（概念与算法梳理在 **`第二次作业解答.docx`** 正文）。
- **数据集**：无。

### 第 2 题 — 经典社团算法实现与可视化；（拓展）表征学习社团对比

| 脚本 | 作用 |
|------|------|
| `src/q2_louvain.py` | **Louvain** 社团划分，模块度与可视化 |
| `src/q2_deepwalk_compare.py` | **DeepWalk + KMeans** 社团划分（与 Louvain 对照） |
| `src/deepwalk_embed.py` | DeepWalk 随机游走 + Word2Vec 嵌入（供第 2、5、6 题复用） |
| `src/utils.py` | 路径、`figures/`/`data/` 目录与画图字体等公共配置 |

- **数据集**：**Zachary Karate Club**，由 `networkx.karate_club_graph()` 内置载入（无需额外文件）。

### 第 3 题 — 经典拓扑中心性指标与小规模网络计算

| 脚本 | 作用 |
|------|------|
| `src/q3_centrality.py` | 在代码内构造小规模无向图，计算度 / 介数 / 接近 / 特征向量中心性及排名 |

- **数据集**：无外部文件（示例拓扑由脚本内边表定义）。

### 第 4 题 — PageRank（有向加权公开网络）

| 脚本 | 作用 |
|------|------|
| `src/q4_pagerank.py` | 读入 SNAP **Bitcoin OTC** 信任网络，加权 **PageRank**、与加权入度相关性及可视化 |

- **数据集**：**SNAP soc-sign-bitcoinotc**（有向、加权）。首次运行从 SNAP 下载压缩包至 `data/soc-sign-bitcoinotc.csv.gz`，字段列为 `source, target, rating, time`（脚本按无表头解析）；边权取评分绝对值。

### 第 5 题 — （拓展）深度学习类节点影响力

| 脚本 | 作用 |
|------|------|
| `src/q5_embedding_influence.py` | 在 Bitcoin OTC **弱连通巨片的子图**上做 DeepWalk 嵌入，用嵌入 **L2 范数** 作为影响力分数，与 PageRank、度中心性、介数做 Spearman 对照 |
| `src/q4_pagerank.py`（复用） | `load_bitcoin_otc()` 载入同一 SNAP 数据 |
| `src/deepwalk_embed.py` | 嵌入计算 |

- **数据集**：与 **第 4 题** 相同（**SNAP Bitcoin OTC**）。

### 第 6 题 — 大规模网络统计与社团 / 影响力对比

| 脚本 | 作用 |
|------|------|
| `src/q6_analysis.py` | **Email-Eu-core** 网络基本统计、度分布图；巨连通分量上 Louvain vs DeepWalk+KMeans；度中心性、PageRank、嵌入范数及 Top 节点 |

- **数据集**：**SNAP Email-Eu-core**（有向边列表）。首次运行下载 **`data/email-Eu-core.txt.gz`**。若本地另有 **`data/email-Eu-core.txt`**，可作备份或对照明细；**默认程序读取的是 `.txt.gz` 官方格式**。

---

## 运行与环境

```bash
cd 作业2
python3 -m pip install -r requirements.txt
python3 run_all.py
```

运行成功后会产生或更新 **`output/results_summary.json`** 与 **`figures/`** 下各题图表。

可选脚本 **`build_docx.py`**、**`equation_images.py`** 为排版辅助用途，与上述实验流程相互独立；用法见各脚本开头注释。

---

## 数据集原始出处（便于引用）

- **Bitcoin OTC**：Stanford SNAP — *Bitcoin OTC trust weighted signed network*（`soc-sign-bitcoinotc.csv.gz`）。
- **Email-Eu-core**：Stanford SNAP — *EU email communication network*（`email-Eu-core.txt.gz`）。
- **Karate Club**：NetworkX 内置经典基准图。
