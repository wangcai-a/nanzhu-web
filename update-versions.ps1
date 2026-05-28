# 更新HTML文件中的版本号参数
# 每次修改CSS/JS文件后运行此脚本，或在修改HTML后运行

$frontendDir = "d:\code\web\frontend\public"
$htmlFiles = @("index.html", "admin.html", "product.html", "contact.html")

$newVersion = Get-Date -Format "yyyyMMddHHmmss"

Write-Host "正在更新版本号: v$newVersion" -ForegroundColor Cyan

foreach ($file in $htmlFiles) {
    $filePath = Join-Path $frontendDir $file
    if (Test-Path $filePath) {
        $content = Get-Content $filePath -Raw

        $updatedContent = $content -replace '\?v=\d+', "?v=$newVersion"

        if ($content -ne $updatedContent) {
            Set-Content -Path $filePath -Value $updatedContent -NoNewline
            Write-Host "✓ 已更新 $file" -ForegroundColor Green
        } else {
            Write-Host "○ $file 版本号已是最新" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✗ 找不到 $file" -ForegroundColor Red
    }
}

Write-Host "`n版本号更新完成！请刷新浏览器页面。" -ForegroundColor Cyan
