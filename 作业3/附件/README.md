# 第三次作业（作业3）

题目来源：`第三次作业.doc`（文档内公式/插图若为 OLE 占位，请以课堂讲义为准）。

## 目录说明

| 路径 | 说明 |
|------|------|
| `run_all.py` | 一键运行数值实验，写入 `output/*.json` 与 `figures/*.png` |
| `src/q1_one_model.py` | **题1**：任选一类模型构造网络并统计属性（默认 BA，N=15,m=3） |
| `src/q2_four_models.py` | **题2**：四类模型构造 + 参数扫描表与对比图 |
| `src/q3_er_giant.py` | **题3**：ER 巨片占比随 p 变化仿真 + 平均场示意曲线 |
| `src/q5_search.py` | **题5**：BFS / 最大度贪心 / 随机游走搜索（默认示例拓扑见脚本） |
| `src/models.py` / `metrics.py` | 模型构造与指标计算封装 |
| `equation_images.py` | Matplotlib 渲染公式为 PNG |

书面作答 **题3 证明**、**题4 Milgram/WS/Kleinberg**、**BA 幂律证明与鲁棒性** 等在 **`第三次作业解答.docx`** 中汇总。

## 运行

```bash
cd 作业3
python3 -m pip install -r requirements.txt
python3 run_all.py
```

### Word 中的公式

`build_docx.py` 将用到的表达式交给 **`equation_images.py`**，用 Matplotlib mathtext 生成 **`figures/equations_doc/*.png`** 并居中插入文档；**正文里不再直接粘贴 LaTeX 源码**，避免 Word 显示 `_`、`{}`、`^` 等裸符号串。



### 生成老式 `.doc`（可选）

`python-docx` 只能直接写出 `.docx`。要得到 **`.doc`（Word 97–2003）**：

1. **推荐**：安装 LibreOffice 后执行：
   ```bash
   brew install --cask libreoffice   # 若未安装
   bash make_doc.sh
   ```
   或在安装 LibreOffice 后再次执行 `python3 build_docx.py`（脚本会自动尝试 headless 转换为 `.doc`）。
2. **或用 Microsoft Word**：打开 `第三次作业解答.docx` →「另存为」→ 选择 **Word 97-2003 文档（*.doc）**。


