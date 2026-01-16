# Dockerfile拥有

1.Matlab-2025b
2.CUDA 12.9
3.Miniconda
4.PaddlePaddle
5.PyTorch
6.LangChain
7.Ollama
等环境

# ==============================================================================
# MATLAB 在线许可证认证配置
# ==============================================================================
# 方式 A: 网络许可证服务器 (取消注释并填写您的服务器地址)
# ENV MLM_LICENSE_FILE=27000@your-license-server.example.com

# 方式 B: MathWorks 账户在线认证 (交互式，启动时通过浏览器登录)
# 使用 -browser 模式启动时会自动提示登录 MathWorks 账户

# 方式 C: Batch Licensing Token (非交互式/CI-CD 场景)
# ENV MLM_LICENSE_TOKEN="your-email@example.com::your-encoded-token"

# 方式 D: 挂载许可证文件
# 运行时使用: -v /path/to/license.lic:/licenses/license.lic
# ENV MLM_LICENSE_FILE=/licenses/license.lic
# ==============================================================================
# ==============================================================================
