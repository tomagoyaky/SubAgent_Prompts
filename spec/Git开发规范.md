# Git开发规范

## 1. 分支管理策略

### 1.1 分支命名规范

| 分支类型 | 命名格式 | 说明 |
|---------|---------|------|
| 主分支 | `main` | 生产环境代码，始终保持稳定 |
| 开发分支 | `develop` | 开发主分支，功能集成分支 |
| 特性分支 | `feature/*` | 新功能开发分支 |
| 发布分支 | `release/*` | 准备发布版本 |
| 热修复分支 | `hotfix/*` | 紧急修复生产问题 |

### 1.2 分支命名示例

```bash
# 特性分支示例
feature/user-authentication
feature/order-management-module
feature/requirement-list-view

# 发布分支示例
release/v1.0.0
release/v1.1.0

# 热修复分支示例
hotfix/fix-login-bug
hotfix/critical-security-patch
```

### 1.3 分支生命周期

1. **创建分支**：从`develop`创建特性分支
2. **开发执行**：在特性分支上进行开发
3. **同步更新**：定期同步`develop`分支的更新
4. **提交合并**：完成开发后合并回`develop`分支
5. **清理分支**：合并后删除特性分支

## 2. 提交规范

### 2.1 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 2.2 Type 类型说明

| Type | 说明 |
|------|------|
| `feat` | 新功能开发 |
| `fix` | Bug修复 |
| `docs` | 文档更新 |
| `style` | 代码格式调整（不影响功能） |
| `refactor` | 代码重构 |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 构建配置、辅助工具更新 |
| `ci` | CI/CD配置变更 |

### 2.3 Scope 影响范围

- 模块名称：`user`, `order`, `requirement`, `api`等
- 通用变更：`common`, `config`, `utils`等

### 2.4 提交信息示例

```bash
# 功能开发
feat(requirement): 新增需求列表搜索功能

fix(user): 修复用户登录验证bug

docs(readme): 更新项目README文档

refactor(api): 重构用户认证接口

perf(list): 优化需求列表查询性能

chore(deps): 更新项目依赖版本
```

### 2.5 提交信息模板

```bash
# 简洁模式（推荐）
feat(auth): 实现JWT Token认证

# 详细模式
feat(auth): 实现JWT Token认证

- 添加Token生成和验证逻辑
- 集成到所有需要认证的接口
- 添加Token过期处理

Closes #123
```

## 3. Pull Request 规范

### 3.1 PR创建流程

1. **完成开发**：确保代码完整、功能可用
2. **同步更新**：拉取最新`develop`分支并合并
3. **解决冲突**：解决可能的代码冲突
4. **创建PR**：创建Pull Request
5. **填写模板**：按照PR模板填写信息
6. **请求Review**：指定Reviewer

### 3.2 PR模板

```markdown
## 功能描述

<!-- 描述本次PR解决的问题和功能 -->

## 改动说明

<!-- 详细说明改动内容 -->

## 改动类型

- [ ] 新功能 (feat)
- [ ] Bug修复 (fix)
- [ ] 文档更新 (docs)
- [ ] 代码重构 (refactor)
- [ ] 其他

## 测试情况

- [ ] 已完成单元测试
- [ ] 已完成集成测试
- [ ] 手动测试通过
- [ ] 无需测试

## 检查清单

- [ ] 代码符合编码规范
- [ ] 无Console报错
- [ ] 已更新相关文档
- [ ] 提交信息符合规范

## 截图/演示

<!-- 如有UI改动，添加截图 -->

## 相关Issue

<!-- 关联的Issue编号 -->
```

### 3.3 PR描述示例

```markdown
## 功能描述

实现需求管理系统的用户认证模块，包括登录、注册和Token管理功能。

## 改动说明

- 新增用户登录接口 `/api/auth/login`
- 新增用户注册接口 `/api/auth/register`
- 实现JWT Token生成和验证
- 添加Token刷新机制
- 更新用户模型增加认证相关字段

## 改动类型

- [x] 新功能 (feat)

## 测试情况

- [x] 已完成单元测试
- [x] 手动测试通过

## 检查清单

- [x] 代码符合编码规范
- [x] 无Console报错
- [x] 已更新API文档
- [x] 提交信息符合规范

## 相关Issue

Closes #45
```

### 3.4 PR合并时机

- 所有Reviewer批准
- 所有CI检查通过
- 无未解决的冲突
- 测试全部通过

## 4. Code Review 规范

### 4.1 Reviewer职责

- 24小时内完成Review
- 重点关注：逻辑正确性、代码质量、安全性
- 提供建设性反馈
- 区分必须修改和建议改进

### 4.2 Review检查项

```markdown
### 功能正确性
- [ ] 代码逻辑是否正确
- [ ] 是否覆盖边界情况
- [ ] 异常处理是否完善

### 代码质量
- [ ] 命名是否清晰
- [ ] 是否有重复代码
- [ ] 是否有不必要的复杂度
- [ ] 是否有硬编码

### 安全性
- [ ] 是否有SQL注入风险
- [ ] 是否有XSS风险
- [ ] 敏感信息是否泄露
- [ ] 权限校验是否完善

### 性能
- [ ] 是否有明显的性能问题
- [ ] 是否有不必要的数据库查询
- [ ] 是否有内存泄漏风险
```

### 4.3 Review反馈格式

```markdown
## 阻塞性问题（必须修改）

1. [文件名:行号] 问题描述
   ```
   问题代码
   ```
   建议修改方案

## 建议改进（可选修改）

1. [文件名:行号] 建议内容
   原因说明
```

## 5. 合并冲突处理

### 5.1 冲突预防

- 定期同步主分支
- 小批量提交
- 及时创建PR

### 5.2 冲突解决步骤

```bash
# 1. 更新本地develop分支
git checkout develop
git pull origin develop

# 2. 切换到特性分支
git checkout feature/xxx

# 3. 合并develop分支
git merge develop

# 4. 解决冲突后
git add <resolved-files>
git commit -m "chore: resolve merge conflicts"

# 5. 推送到远程
git push origin feature/xxx
```

### 5.3 冲突解决原则

- 优先保留功能逻辑完整性
- 与相关开发者沟通确认
- 避免简单粗暴的覆盖

## 6. 版本发布规范

### 6.1 版本号规则

采用语义化版本：`主版本.次版本.修订号`

- **主版本 (Major)**：不兼容的API变更
- **次版本 (Minor)**：新增功能（向后兼容）
- **修订号 (Patch)**：Bug修复（向后兼容）

### 6.2 发布流程

```bash
# 1. 创建发布分支
git checkout develop
git checkout -b release/v1.0.0

# 2. 更新版本号
# 修改package.json或版本配置文件

# 3. 提交版本更新
git add .
git commit -m "chore: bump version to v1.0.0"

# 4. 合并到main分支
git checkout main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags

# 5. 合并回develop分支
git checkout develop
git merge release/v1.0.0

# 6. 清理发布分支
git branch -d release/v1.0.0
```

### 6.3 Changelog生成

```markdown
# Changelog v1.0.0 (2024-01-15)

## 新功能
- 实现用户认证模块 (#45)
- 添加需求列表管理功能 (#42)
- 支持需求状态筛选 (#38)

## Bug修复
- 修复登录验证问题 (#50)
- 解决列表分页异常 (#47)

## 改进优化
- 提升列表查询性能 (#48)
- 优化用户界面交互 (#44)

## 文档更新
- 更新API接口文档 (#46)
- 补充快速开始指南 (#43)
```

## 7. 常用Git命令速查

### 7.1 日常开发命令

```bash
# 创建特性分支
git checkout -b feature/xxx develop

# 提交更改
git add .
git commit -m "feat(scope): description"

# 推送远程
git push origin feature/xxx

# 更新本地develop分支
git checkout develop
git pull origin develop

# 合并更新到特性分支
git checkout feature/xxx
git merge develop

# 查看提交历史
git log --oneline --graph --decorate
```

### 7.2 撤销操作

```bash
# 撤销工作区修改
git checkout -- <file>

# 撤销暂存区
git reset HEAD <file>

# 修改最后一次提交
git commit --amend

# 回退版本
git reset --hard <commit-hash>
git reset --soft <commit-hash>
```

## 8. 提交检查清单

在提交代码前，请确认：

- [ ] 提交信息符合规范格式
- [ ] 代码编译/运行正常
- [ ] 无Console错误或警告
- [ ] 单元测试全部通过
- [ ] 无敏感信息泄露
- [ ] 已更新相关文档
- [ ] 已同步最新主分支代码
- [ ] 已解决所有代码冲突
