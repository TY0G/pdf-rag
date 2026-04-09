# PDF 文档扫描 / 智能问答项目

一个基于 **Vue 3 + FastAPI + PostgreSQL(pgvector) + Docker Compose** 的 PDF 文档扫描 / 解析 / 检索问答项目。  
特点：

- 浅色风格前端界面
- 后端分层清晰，避免单一大文件
- 支持邮箱验证码注册、JWT 登录
- 支持 PDF 上传、解析、切分、索引
- 支持单文档与多文档问答
- 支持答案引用页码与原文片段
- 默认无需外接大模型即可运行演示
- 预留 OpenAI / Ollama 兼容接口

## 1. 一键启动

```bash
docker compose up -d --build
```

启动后访问：

- 前端：`http://localhost:8080`
- 后端 API：`http://localhost:8000/docs`

## 2. 默认账号

系统首次启动会自动创建管理员账号：

- 邮箱：`admin@example.com`
- 密码：`Admin123!`

## 3. 主要技术栈

### 前端
- Vue 3
- Vite
- Element Plus
- Pinia
- Vue Router
- Axios

### 后端
- FastAPI
- SQLAlchemy 2
- PostgreSQL
- pgvector
- PyMuPDF
- scikit-learn HashingVectorizer
- JWT

## 4. 目录结构

```text
pdf_doc_scan_project/
├─ docker-compose.yml
├─ .env.example
├─ README.md
├─ backend/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  ├─ scripts/
│  │  └─ entrypoint.sh
│  └─ app/
│     ├─ main.py
│     ├─ core/
│     ├─ db/
│     ├─ models/
│     ├─ repositories/
│     ├─ schemas/
│     ├─ services/
│     ├─ utils/
│     └─ api/
└─ frontend/
   ├─ Dockerfile
   ├─ nginx.conf
   ├─ package.json
   ├─ vite.config.ts
   └─ src/
```

## 5. Docker 启动说明

`docker compose up -d --build` 会启动 3 个服务：

1. `postgres`：数据库 + pgvector 扩展
2. `backend`：FastAPI 服务
3. `frontend`：Nginx 托管前端静态页面，并代理 `/api`

## 6. 环境变量说明

如需接入真正大模型，在根目录创建 `.env`，参考 `.env.example`：

```env
OPENAI_BASE_URL=http://host.docker.internal:11434/v1
OPENAI_API_KEY=ollama
OPENAI_MODEL=qwen2.5:7b
```

### Ollama 接入说明
如果你本机已有 Ollama，可将模型接口暴露为 OpenAI 兼容格式，然后设置：

- `OPENAI_BASE_URL=http://host.docker.internal:11434/v1`
- `OPENAI_API_KEY=ollama`
- `OPENAI_MODEL=你的模型名`

未配置时，系统自动使用**检索式回答**回退逻辑，依然可完整演示主流程。

## 7. 业务流程

1. 注册 / 登录
2. 上传 PDF
3. 后端后台解析 PDF
4. 提取文本、清洗、切分
5. 生成固定维度向量并写入 pgvector
6. 用户提问
7. 检索相关 chunk
8. 生成回答并附带证据引用

## 8. 当前默认能力边界

默认版本聚焦于“可运行 + 可演示 + 层次清晰”的工程版本，因此：

- 对**文本型 PDF**支持最好
- 对纯扫描图片 PDF 预留 OCR 扩展接口，但未默认启用重量级 OCR 依赖
- 默认 Embedding 使用本地轻量 HashingVectorizer，避免首次启动下载大模型
- 若接入 OpenAI / Ollama，可获得更自然的生成式回答

## 9. 后续增强建议

- 增加 OCR（PaddleOCR / Tesseract）
- 增加重排模型
- 增加后台管理界面
- 增加异步任务队列（Celery / RQ）
- 增加文档权限与标签管理

## 10. 开发时本地运行

### 后端
```bash
cd backend
pip install -r requirements.txt
export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/pdf_scan
uvicorn app.main:app --reload
```

### 前端
```bash
cd frontend
npm install
npm run dev
```
