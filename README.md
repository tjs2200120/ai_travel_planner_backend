# AI 旅行规划师 (AI Travel Planner)

一个智能的旅行规划 Web 应用，通过 AI 技术为用户提供个性化的旅行路线和建议。

## 功能特点

### 1. 智能行程规划
- 🎤 支持语音和文字输入旅行需求
- 🤖 AI 自动生成个性化旅行路线
- 📍 包含交通、住宿、景点、餐厅等详细信息
- 🎯 根据预算、人数、偏好智能推荐

### 2. 费用预算与管理
- 💰 AI 智能预算分析
- 📊 实时记录和追踪旅行开销
- 🎙️ 支持语音记录消费

### 3. 用户管理与云端同步
- 👤 用户注册登录系统
- ☁️ 多设备云端同步
- 📱 保存和管理多份旅行计划

## 技术栈

### 前端
- Vue 3 + TypeScript
- Vite
- Element Plus UI
- Pinia 状态管理
- Axios HTTP 客户端
- Web Speech API (语音识别)

### 后端
- Python 3.10+
- FastAPI
- SQLAlchemy ORM
- MySQL 数据库
- JWT 认证
- 通义千问 AI API

### 部署
- Docker & Docker Compose
- Nginx

## 项目结构

```
AI-Travel-Planner/
├── frontend/              # Vue 3 前端应用
│   ├── src/
│   │   ├── api/          # API 请求
│   │   ├── components/   # Vue 组件
│   │   ├── views/        # 页面视图
│   │   ├── stores/       # Pinia 状态管理
│   │   ├── router/       # 路由配置
│   │   └── utils/        # 工具函数
│   └── package.json
├── backend/              # FastAPI 后端应用
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── models/      # 数据模型
│   │   ├── schemas/     # Pydantic 模式
│   │   ├── services/    # 业务逻辑
│   │   ├── core/        # 核心配置
│   │   └── main.py      # 应用入口
│   └── requirements.txt
├── docker-compose.yml    # Docker 编排配置
└── README.md

```

## 快速开始

### 环境要求
- Node.js 18+
- Python 3.10+
- MySQL 8.0+
- Docker & Docker Compose (可选)

### 1. 克隆项目
```bash
git clone <repository-url>
cd AI-Travel-Planner
```

### 2. 后端设置

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入必要的配置

# 运行数据库迁移
python -m alembic upgrade head

# 启动后端服务
uvicorn app.main:app --reload
```

后端服务将运行在 http://localhost:8000

### 3. 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将运行在 http://localhost:5173

### 4. 使用 Docker (推荐)

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 配置说明

### 后端环境变量 (.env)

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/travel_planner

# JWT 配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 通义千问 API
DASHSCOPE_API_KEY=your-dashscope-api-key

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 获取通义千问 API Key

1. 访问 [阿里云 DashScope](https://dashscope.aliyun.com/)
2. 注册/登录账号
3. 创建 API Key
4. 将 API Key 填入 `.env` 文件

## API 文档

启动后端服务后，访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 开发路线图

- [x] 项目初始化
- [ ] 用户认证系统
- [ ] AI 行程规划核心功能
- [ ] 语音输入集成
- [ ] 费用管理模块
- [ ] 云端数据同步
- [ ] 移动端适配
- [ ] 性能优化

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交 Issue。
