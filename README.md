# Architecture AI Analyzer

一个基于 DeepSeek API 的建筑案例分析小工具。

## 功能

输入一个或多个建筑名称，程序会调用 DeepSeek API，
并将建筑信息整理为结构化 JSON 数据。

目前输出字段包括：

- name
- location
- architect
- type
- features
- strategies

## 已实现

- 多建筑批量输入
- 支持中英文逗号
- JSON 结构化输出
- API 异常处理
- 请求超时处理
- 自动创建 outputs 文件夹
- API Key 使用环境变量保存

## 运行

需要提前设置环境变量：

DEEPSEEK_API_KEY

然后运行：

python main.py