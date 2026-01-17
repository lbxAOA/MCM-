# ==============================================================================
# MCM 2026 建模环境镜像 
# ==============================================================================

FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu22.04

# ------------------------------------------------------------------------------
# 1. 模型准备 (Model Preparation)
# 职责：系统底层依赖，增加编译工具以支持 PyTorch 扩展库
# ------------------------------------------------------------------------------
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# libspatialindex-dev (Geopandas依赖), graphviz (绘图依赖), ffmpeg (视频生成)
RUN sed -i 's@http://archive.ubuntu.com@http://mirrors.aliyun.com@g' /etc/apt/sources.list && \
    sed -i 's@http://security.ubuntu.com@http://mirrors.aliyun.com@g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    wget curl git build-essential ca-certificates \
    libgomp1 libgl1-mesa-glx libibverbs-dev \
    glpk-utils coinor-libcbc-dev \
    libspatialindex-dev graphviz ffmpeg graphviz-dev \
    && rm -rf /var/lib/apt/lists/*

# Miniconda 安装
ENV CONDA_DIR=/opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && /bin/bash ~/miniconda.sh -b -p ${CONDA_DIR} \
    && rm ~/miniconda.sh
ENV PATH=${CONDA_DIR}/bin:${PATH}

# ------------------------------------------------------------------------------
# 2. 模型假设 (Model Assumptions)
# 职责：基础 Python 环境与计算底座
# ------------------------------------------------------------------------------
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ && \
    conda config --set show_channel_urls yes && \
    conda install -y python=3.10 && \
    conda clean -afy

# 设置 PyPI 清华源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# ------------------------------------------------------------------------------
# 3. 模型建立 (Model Formulation) - 核心 PyTorch 层
# 职责：安装 PyTorch 核心及其视觉/音频组件
# ------------------------------------------------------------------------------
# 注意：指定 extra-index-url 以获取 CUDA 12.4 兼容版本 (兼容 12.6 容器)
RUN pip install --no-cache-dir \
    torch torchvision torchaudio \
    --extra-index-url https://download.pytorch.org/whl/cu124

# ------------------------------------------------------------------------------
# 4. 模型求解 (Model Solving) - PyTorch 生态系统 & 运筹优化
# 职责：安装用于解决具体数学问题的 PyTorch 扩展库及优化工具包
# ------------------------------------------------------------------------------
# [新增] cvxpy (凸优化), mesa (多智能体仿真), geopandas/osmnx (地理空间B题核心)
RUN pip install --no-cache-dir \
    numpy pandas scipy \
    lightning \
    neuralprophet \
    torch_geometric pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.4.0+cu124.html \
    optuna \
    ortools pulp cvxpy \
    scikit-opt \
    networkx \
    mesa \
    geopandas osmnx shapely folium \
    sympy

# ------------------------------------------------------------------------------
# 5. 结果分析 (Results Analysis) - 训练过程可视化
# 职责：监控 Loss 曲线，分析模型训练效果
# ------------------------------------------------------------------------------
# [新增] pygraphviz (复杂网络绘图), plotly (交互式图表)
RUN pip install --no-cache-dir \
    matplotlib seaborn \
    tensorboard \
    torchviz \
    scienceplots \
    pygraphviz \
    plotly

# ------------------------------------------------------------------------------
# 6. 模型检验 (Model Validation) - 评估指标
# 职责：计算准确率、F1 Score、MAPE 等数学指标
# ------------------------------------------------------------------------------
# [新增] statsmodels (传统统计学检验，针对B题非常重要)
RUN pip install --no-cache-dir \
    torchmetrics \
    scikit-learn \
    statsmodels

# ------------------------------------------------------------------------------
# 7. 模型应用 (Model Application) - 部署与展示
# 职责：将模型导出为 ONNX 格式，或快速生成 Demo 界面
# ------------------------------------------------------------------------------
# [新增] jupyterlab (交互式编程), openpyxl (读取竞赛提供的Excel数据)
RUN pip install --no-cache-dir \
    onnx \
    netron \
    gradio \
    jupyterlab \
    openpyxl xlrd

# 设置工作目录
WORKDIR /workspace
CMD ["/bin/bash"]