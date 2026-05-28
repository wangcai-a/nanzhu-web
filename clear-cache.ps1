# 浏览器缓存清理脚本 - 专门针对 Trae 内嵌浏览器
# 解决修改代码后页面不更新的问题

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Trae 浏览器缓存清理工具" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$traePaths = @(
    "$env:APPDATA\TRAE SOLO CN",
    "$env:APPDATA\trae-webview"
)

$cachePatterns = @(
    "Cache",
    "GPUCache",
    "Code Cache",
    "CachedData",
    "CachedConfigurations",
    "Local Storage",
    "Session Storage",
    "blob_storage"
)

$totalCleaned = 0
$totalDirs = 0

foreach ($basePath in $traePaths) {
    if (Test-Path $basePath) {
        Write-Host "正在清理: $basePath" -ForegroundColor Yellow

        foreach ($pattern in $cachePatterns) {
            $cachePath = Join-Path $basePath $pattern

            if (Test-Path $cachePath) {
                try {
                    $sizeBefore = (Get-ChildItem $cachePath -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
                    if ($null -eq $sizeBefore) { $sizeBefore = 0 }

                    Remove-Item "$cachePath\*" -Recurse -Force -ErrorAction SilentlyContinue

                    $sizeAfter = (Get-ChildItem $cachePath -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
                    if ($null -eq $sizeAfter) { $sizeAfter = 0 }

                    $freed = $sizeBefore - $sizeAfter
                    if ($freed -gt 0) {
                        $totalCleaned += $freed
                        $totalDirs++
                        Write-Host "  ✓ 已清理: $pattern ($([math]::Round($freed/1MB, 2)) MB)" -ForegroundColor Green
                    }
                } catch {
                    Write-Host "  ⚠ 清理失败: $pattern" -ForegroundColor Red
                }
            }
        }

        # 清理 Partitions 目录
        $partitionsPath = Join-Path $basePath "Partitions"
        if (Test-Path $partitionsPath) {
            Get-ChildItem $partitionsPath -Directory | ForEach-Object {
                foreach ($pattern in $cachePatterns) {
                    $subCachePath = Join-Path $_.FullName $pattern
                    if (Test-Path $subCachePath) {
                        try {
                            Remove-Item "$subCachePath\*" -Recurse -Force -ErrorAction SilentlyContinue
                            $totalDirs++
                            Write-Host "  ✓ 已清理: $($_.Name)\$pattern" -ForegroundColor Green
                        } catch {}
                    }
                }
            }
        }
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
if ($totalDirs -gt 0) {
    Write-Host "清理完成！" -ForegroundColor Green
    Write-Host "清理了 $totalDirs 个缓存目录" -ForegroundColor Green
    Write-Host "释放空间: $([math]::Round($totalCleaned/1MB, 2)) MB" -ForegroundColor Green
} else {
    Write-Host "未找到浏览器缓存，或缓存已被清理" -ForegroundColor Yellow
}
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "提示：" -ForegroundColor Yellow
Write-Host "1. 现在请在 Trae 浏览器中刷新页面 (Ctrl+Shift+R)" -ForegroundColor White
Write-Host "2. 或关闭并重新打开浏览器" -ForegroundColor White
Write-Host "3. 服务器端已配置禁用缓存，无需手动清理即可获取最新版本" -ForegroundColor White
Write-Host "`n如仍有问题，请运行 update-versions.ps1 更新版本号" -ForegroundColor Cyan
