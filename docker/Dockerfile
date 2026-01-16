# ==============================================================================
# MATLAB R2025b + CUDA 12.9 + AI 开发环境 Docker 镜像
# 包含: MATLAB, CUDA 12.9, Miniconda, PaddlePaddle, PyTorch, LangChain, Ollama
# ==============================================================================

# 1. 指定 MATLAB R2025b 官方镜像
FROM mathworks/matlab:r2025b

# 2. 切换到 root 账户进行环境配置
USER root

# ==============================================================================
# 系统依赖安装
# ==============================================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    git \
    ca-certificates \
    gnupg \
    libgomp1 \
    lsb-release \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# ==============================================================================
# CUDA 12.9 Toolkit 安装 (仅安装运行时库，驱动由宿主机提供)
# 注意: MATLAB R2025b 基于 Ubuntu 22.04，使用 ubuntu2204 源
# ==============================================================================
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb \
    && dpkg -i cuda-keyring_1.1-1_all.deb \
    && rm cuda-keyring_1.1-1_all.deb \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        cuda-toolkit-12-6 \
    && rm -rf /var/lib/apt/lists/*

# CUDA 环境变量
ENV CUDA_VERSION=12.6
ENV CUDA_HOME=/usr/local/cuda-12.6
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64

# ==============================================================================
# Miniconda 安装
# ==============================================================================
ENV CONDA_DIR=/opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && /bin/bash ~/miniconda.sh -b -p ${CONDA_DIR} \
    && rm ~/miniconda.sh \
    && ${CONDA_DIR}/bin/conda clean -afy
ENV PATH=${CONDA_DIR}/bin:${PATH}

# ==============================================================================
# Python AI 框架安装
# ==============================================================================

# 升级 pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# PaddlePaddle GPU 版本 (CUDA 12.6)
RUN pip install --no-cache-dir \
    paddlepaddle-gpu==3.0.0 \
    -i https://www.paddlepaddle.org.cn/packages/stable/cu126/

# PyTorch GPU 版本 (使用 cu126 wheel)
RUN pip install --no-cache-dir \
    torch \
    torchvision \
    torchaudio \
    --index-url https://download.pytorch.org/whl/cu126

# LangChain 全套
RUN pip install --no-cache-dir \
    langchain \
    langchain-core \
    langchain-community \
    langchain-openai \
    langchain-anthropic \
    langgraph \
    langsmith

# ==============================================================================
# Ollama 安装 (用于运行 DeepSeek-R1:8b 模型)
# ==============================================================================
RUN curl -fsSL https://ollama.com/install.sh | sh

# 创建 Ollama 数据目录 (建议运行时挂载 volume 持久化模型)
RUN mkdir -p /root/.ollama

# 创建启动脚本：启动 Ollama 服务并下载 deepseek-r1:8b
RUN printf '#!/bin/bash\nollama serve &\nsleep 5\nollama pull deepseek-r1:8b\necho "DeepSeek-R1:8b 模型下载完成!"\n' > /usr/local/bin/setup-deepseek.sh \
    && chmod +x /usr/local/bin/setup-deepseek.sh

# ==============================================================================
# 权限管理
# ==============================================================================
RUN chown -R matlab:matlab ${CONDA_DIR}

# 切换回 matlab 用户
USER matlab
WORKDIR /home/matlab

# 初始化 conda
RUN conda init bash

# ==============================================================================
# 健康检查
# ==============================================================================
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD nvidia-smi || exit 1

# ==============================================================================
# 暴露端口
# ==============================================================================
EXPOSE 8888
EXPOSE 11434

# ==============================================================================
# 默认启动命令
# ==============================================================================
CMD ["matlab", "-browser"]