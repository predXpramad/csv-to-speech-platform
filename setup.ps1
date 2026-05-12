$baseDir = "d:\02 Projects\TTS ML Model"
if (!(Test-Path $baseDir)) {
    New-Item -ItemType Directory -Force -Path $baseDir | Out-Null
}
cd $baseDir

$dirs = @(
    "frontend/public",
    "frontend/src/components/ui",
    "frontend/src/components/features/tts",
    "frontend/src/hooks",
    "frontend/src/services",
    "frontend/src/pages",
    "frontend/src/store",
    "frontend/src/types",
    "frontend/src/lib",
    "frontend/src/styles",
    "backend/app/api/v1/endpoints",
    "backend/app/services",
    "backend/app/models",
    "backend/app/schemas",
    "backend/app/core",
    "backend/app/utils",
    "backend/app/websocket",
    "backend/app/storage",
    "backend/app/middleware",
    "nginx/conf.d",
    "storage/uploads",
    "storage/temp_audio",
    "storage/zip_exports",
    "storage/metadata"
)

foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
}

$files = @(
    "frontend/src/main.tsx",
    "frontend/src/App.tsx",
    "frontend/src/styles/globals.css",
    "frontend/src/lib/utils.ts",
    "frontend/src/services/api.ts",
    "frontend/src/services/websocket.ts",
    "frontend/src/store/ttsStore.ts",
    "frontend/src/types/index.ts",
    "frontend/package.json",
    "frontend/vite.config.ts",
    "frontend/tailwind.config.js",
    "frontend/tsconfig.json",
    "backend/app/main.py",
    "backend/app/core/config.py",
    "backend/app/api/v1/api.py",
    "backend/app/api/v1/endpoints/tts.py",
    "backend/app/api/v1/endpoints/ws.py",
    "backend/app/services/edge_tts_service.py",
    "backend/app/services/csv_service.py",
    "backend/app/websocket/manager.py",
    "backend/app/models/domain.py",
    "backend/app/schemas/requests.py",
    "backend/app/utils/zip_manager.py",
    "backend/app/storage/file_manager.py",
    "backend/requirements.txt",
    "backend/Dockerfile",
    "frontend/Dockerfile",
    "docker-compose.yml",
    "nginx/nginx.conf",
    "nginx/conf.d/default.conf",
    ".env.example",
    "README.md",
    ".gitignore"
)

foreach ($file in $files) {
    if (!(Test-Path $file)) {
        New-Item -ItemType File -Force -Path $file | Out-Null
    }
}
Write-Output "Setup complete."
