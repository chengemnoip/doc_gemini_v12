# Gemini CLI 配置範例

本文件包含從 Gemini CLI 官方文件中提取的配置範例，並附有繁體中文註釋。

## `settings.json` 檔案範例

### 錯誤指令(bugCommand)

```json
"bugCommand": { "urlTemplate": "https://bug.example.com/new?title={title}&info={info}" }
```

**註釋:** 此設定允許您自訂 `/bug` 指令的行為，將錯誤報告指向您自己的錯誤追蹤系統，而不是預設的 GitHub issues 頁面。

### 檔案過濾(fileFiltering)

```json
"fileFiltering": { "respectGitIgnore": true, "enableRecursiveFileSearch": false }
```

**註釋:** 這個設定可以控制檔案搜尋的行為。`respectGitIgnore` 設為 `true` 會讓 CLI 在搜尋檔案時遵循 `.gitignore` 的規則，而 `enableRecursiveFileSearch` 設為 `false` 則會停用在 `@` 提及檔案時的遞迴搜尋。

### 核心工具(coreTools)

```json
"coreTools": ["ReadFileTool", "GlobTool", "SearchText"]
```

**註釋:** 這個設定可以讓您明確指定要提供給模型的內建工具。這對於限制模型可用的功能很有用。

### 排除工具(excludeTools)

```json
"excludeTools": ["run_shell_command", "findFiles"]
```

**註釋:** 這個設定可以讓您從模型可用的工具中排除特定的工具。

### 自動接受(autoAccept)

```json
"autoAccept": true
```

**註釋:** 當設定為 `true` 時，CLI 會自動執行被認為是安全的工具呼叫（例如唯讀操作），而不需要使用者確認。

### 主題(theme)

```json
"theme": "GitHub"
```

**註釋:** 這個設定可以讓您更改 CLI 的視覺主題。

### 沙箱(sandbox)

```json
"sandbox": "docker"
```

**註釋:** 這個設定可以啟用沙箱模式來執行工具，以增強安全性。`docker` 表示使用 Docker 作為沙箱環境。

### 工具發現指令(toolDiscoveryCommand)

```json
"toolDiscoveryCommand": "bin/get_tools"
```

**註釋:** 這個設定允許您定義一個自訂的 shell 指令，用來發現專案中的可用工具。

### 工具呼叫指令(toolCallCommand)

```json
"toolCallCommand": "bin/call_tool"
```

**註釋:** 這個設定允許您定義一個自訂的 shell 指令，用來呼叫由 `toolDiscoveryCommand` 發現的工具。

### MCP 伺服器(mcpServers)

```json
"mcpServers": {
  "myPythonServer": {
    "command": "python",
    "args": ["mcp_server.py", "--port", "8080"],
    "cwd": "./mcp_tools/python",
    "timeout": 5000
  },
  "myNodeServer": {
    "command": "node",
    "args": ["mcp_server.js"],
    "cwd": "./mcp_tools/node"
  },
  "myDockerServer": {
    "command": "docker",
    "args": ["run", "i", "--rm", "-e", "API_KEY", "ghcr.io/foo/bar"],
    "env": {
      "API_KEY": "$MY_API_TOKEN"
    }
  }
}
```

**註釋:** 這個設定允許您配置一個或多個模型上下文協定（MCP）伺服器的連線，以發現和使用自訂工具。

### 檢查點(checkpointing)

```json
"checkpointing": {
  "enabled": false
}
```

**註釋:** 這個設定可以啟用或停用對話和檔案狀態的儲存和恢復功能。

### 偏好編輯器(preferredEditor)

```json
"preferredEditor": "vscode"
```

**註釋:** 這個設定可以指定您偏好的編輯器，用來檢視差異。

### 遙測(telemetry)

```json
"telemetry": {
  "enabled": true,
  "target": "local",
  "otlpEndpoint": "http://localhost:16686",
  "logPrompts": false
}
```

**註釋:** 這個設定可以配置 Gemini CLI 的日誌記錄和指標收集。

### 停用使用統計(usageStatisticsEnabled)

```json
"usageStatisticsEnabled": false
```

**註釋:** 這個設定可以停用匿名使用統計資料的收集。

### 完整的 `settings.json` 範例

```json
{
  "theme": "GitHub",
  "sandbox": "docker",
  "toolDiscoveryCommand": "bin/get_tools",
  "toolCallCommand": "bin/call_tool",
  "mcpServers": {
    "mainServer": {
      "command": "bin/mcp_server.py"
    },
    "anotherServer": {
      "command": "node",
      "args": ["mcp_server.js", "--verbose"]
    }
  },
  "telemetry": {
    "enabled": true,
    "target": "local",
    "otlpEndpoint": "http://localhost:4317",
    "logPrompts": true
  },
  "usageStatisticsEnabled": true
}
```

**註釋:** 這是一個完整的 `settings.json` 檔案範例，展示了多個設定的組合。

## 環境變數範例

### 設定 Gemini 模型

```bash
export GEMINI_MODEL="gemini-2.5-flash"
```

**註釋:** 這個環境變數可以讓您指定要使用的預設 Gemini 模型。

### 設定 Google Cloud API 金鑰

```bash
export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
```

**註釋:** 在使用 Vertex AI 時，需要設定您的 Google Cloud API 金鑰。

### 設定 Google Cloud 專案

```bash
export GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
```

**註釋:** 在使用 Code Assist 或 Vertex AI 時，需要設定您的 Google Cloud 專案 ID。

### 設定 Google 應用程式憑證

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
```

**註釋:** 這個環境變數可以讓您指定您的 Google 應用程式憑證 JSON 檔案的路徑。

### 設定 OTLP Google Cloud 專案

```bash
export OTLP_GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
```

**註釋:** 這個環境變數可以讓您指定您在 Google Cloud 中用於遙測的 Google Cloud 專案 ID。

### 設定 Google Cloud 位置

```bash
export GOOGLE_CLOUD_LOCATION="YOUR_PROJECT_LOCATION"
```

**註釋:** 在非快速模式下使用 Vertex AI 時，需要設定您的 Google Cloud 專案位置。

## 命令列參數範例

### 指定模型

```bash
npm start -- --model gemini-1.5-pro-latest
```

**註釋:** 這個參數可以讓您在本次會話中指定要使用的 Gemini 模型。

## `GEMINI.md` 內容範例

```markdown
# 專案：我的出色 TypeScript 函式庫

## 一般指令：
- 產生新的 TypeScript 程式碼時，請遵循現有的編碼風格。
- 確保所有新函式和類別都有 JSDoc 註解。
- 在適當的地方優先使用函式式程式設計範式。
- 所有程式碼應與 TypeScript 5.0 和 Node.js 18+ 相容。

## 編碼風格：
- 使用 2 個空格進行縮排。
- 介面名稱應以 `I` 為前置（例如，`IUserService`）。
- 私有類別成員應以下劃線（`_`）為前置。
- 始終使用嚴格相等（`===` 和 `!==`）。

## 特定元件：`src/api/client.ts`
- 此檔案處理所有對外的 API 請求。
- 新增新的 API 呼叫函式時，確保它們包含健全的錯誤處理和日誌記錄。
- 對所有 GET 請求使用現有的 `fetchWithRetry` 實用程式。

## 關於依賴項：
- 除非絕對必要，否則避免引入新的外部依賴項。
- 如果需要新的依賴項，請說明原因。
```

**註釋:** `GEMINI.md` 檔案允許您向 AI 提供專案特定的指令、編碼風格指南或任何相關的背景資訊，使其回應更加客製化和準確。

## 沙箱 Dockerfile 範例

```dockerfile
FROM gemini-cli-sandbox

# 在此處新增您的自訂依賴項或設定
# 例如：
# RUN apt-get update && apt-get install -y some-package
# COPY ./my-config /app/my-config
```

**註釋:** 這個 Dockerfile 範例展示了如何基於基礎的沙箱映像檔來建立自訂的沙箱環境。

### 建立自訂沙箱映像檔

```bash
BUILD_SANDBOX=1 gemini -s
```

**註釋:** 當 `.gemini/sandbox.Dockerfile` 存在時，您可以使用 `BUILD_SANDBOX` 環境變數來自動建立自訂的沙箱映像檔。
