# 1. 指定 MATLAB R2025b 官方镜像
FROM mathworks/matlab:r2025b

# 2. 切换到 root 账户进行环境配置
USER root

# 3. 设置 CUDA 12.9 核心环境变量
# 确保容器内的程序能找到 CUDA 库路径
ENV CUDA_VERSION=12.9
ENV PATH=/usr/local/cuda-12.9/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda-12.9/lib64:${LD_LIBRARY_PATH}

# 4. 安装必要的系统依赖（用于 Paddle 和 Conda）
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    libgomp1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 5. 安装 Miniconda
ENV CONDA_DIR=/opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p $CONDA_DIR && \
    rm ~/miniconda.sh
ENV PATH=$CONDA_DIR/bin:$PATH

# 6. 安装 PaddlePaddle GPU 版 (针对 CUDA 12 系列)
# 使用 3.0.0-beta 版本以获得最佳的 CUDA 12.x 支持
RUN pip install --no-cache-dir --upgrade pip && \
    pip install paddlepaddle-gpu==3.0.0b2 -i https://www.paddlepaddle.org.cn/packages/stable/cu123/

ENV ANTHROPIC_BASE_URL="https://api.jiekou.ai/anthropic"
ENV ANTHROPIC_AUTH_TOKEN="YOUR_API_KEY_HERE"

ENV ANTHROPIC_MODEL_OPUS="claude-opus-4-5-20251101"
ENV ANTHROPIC_MODEL_SONNET="claude-sonnet-4-5-20250929"
ENV ANTHROPIC_MODEL_HAIKU="claude-haiku-4-5-20251001"

ENV ANTHROPIC_MODEL="claude-sonnet-4-5-20250929"
ENV ANTHROPIC_SMALL_FAST_MODEL="claude-sonnet-4-5-20250929"

# 8. 权限管理：允许 matlab 用户操作 conda
RUN chown -R matlab:matlab $CONDA_DIR
USER matlab
WORKDIR /home/matlab

# 初始化 Shell
RUN conda init bash