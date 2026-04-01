# ShamGP 商城最小验证脚本 (PowerShell)
# 用于验证登录→商品→购物车→地址→创建订单的完整链路

Write-Host "=== ShamGP 最小验证脚本 ===" -ForegroundColor Cyan
Write-Host ""

$BASE_URL = "http://localhost:8000/api/v1"
$token = $null
$address_id = $null
$cart_item_ids = @()

Write-Host "[1/6] 测试健康检查..." -ForegroundColor Yellow
try {
    $health = Invoke-WebRequest -Uri "$BASE_URL/health" -UseBasicParsing
    Write-Host "✅ 健康检查通过: $($health.Content)" -ForegroundColor Green
} catch {
    Write-Host "❌ 健康检查失败" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "[2/6] 测试登录..." -ForegroundColor Yellow
try {
    $body = @{username="testuser";password="user123"} | ConvertTo-Json
    $login = Invoke-WebRequest -Uri "$BASE_URL/auth/login" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
    $login_data = $login.Content | ConvertFrom-Json
    $token = $login_data.data.access_token
    Write-Host "✅ 登录成功" -ForegroundColor Green
    Write-Host "   Token: $($token.Substring(0, 50))..." -ForegroundColor Gray
} catch {
    Write-Host "❌ 登录失败" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "[3/6] 测试商品列表..." -ForegroundColor Yellow
try {
    $headers = @{"Authorization"="Bearer $token"}
    $products = Invoke-WebRequest -Uri "$BASE_URL/products/simple" -Headers $headers -UseBasicParsing
    $products_data = $products.Content | ConvertFrom-Json
    Write-Host "✅ 商品列表获取成功，共 $($products_data.total) 个商品" -ForegroundColor Green
} catch {
    Write-Host "❌ 商品列表获取失败" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "[4/6] 测试加购物车..." -ForegroundColor Yellow
try {
    $headers = @{"Authorization"="Bearer $token"}
    $body = @{product_id=1;quantity=1} | ConvertTo-Json
    $cart = Invoke-WebRequest -Uri "$BASE_URL/carts/items" -Method POST -Headers $headers -Body $body -ContentType "application/json" -UseBasicParsing
    $cart_data = $cart.Content | ConvertFrom-Json
    $cart_item_ids += $cart_data.data.id
    Write-Host "✅ 加购物车成功，Cart Item ID: $($cart_data.data.id)" -ForegroundColor Green
} catch {
    Write-Host "❌ 加购物车失败" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "[5/6] 测试获取地址并创建地址..." -ForegroundColor Yellow
try {
    $headers = @{"Authorization"="Bearer $token"}
    $addresses = Invoke-WebRequest -Uri "$BASE_URL/orders/addresses" -Headers $headers -UseBasicParsing
    $addresses_data = $addresses.Content | ConvertFrom-Json
    
    if ($addresses_data.data.Count -eq 0) {
        Write-Host "   暂无地址，创建一个..." -ForegroundColor Gray
        $body = @{
            consignee_name="测试用户"
            consignee_phone="13800138000"
            province="广东省"
            city="深圳市"
            district="南山区"
            detail_address="科技园路123号"
            zip_code="518000"
            is_default=$true
        } | ConvertTo-Json
        $new_address = Invoke-WebRequest -Uri "$BASE_URL/orders/addresses" -Method POST -Headers $headers -Body $body -ContentType "application/json" -UseBasicParsing
        $new_address_data = $new_address.Content | ConvertFrom-Json
        $address_id = $new_address_data.data.id
    } else {
        $address_id = $addresses_data.data[0].id
    }
    Write-Host "✅ 地址获取/创建成功，Address ID: $address_id" -ForegroundColor Green
} catch {
    Write-Host "❌ 地址获取/创建失败" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "[6/6] 测试创建订单..." -ForegroundColor Yellow
try {
    $headers = @{"Authorization"="Bearer $token"}
    $body = @{
        address_id=$address_id
        cart_item_ids=$cart_item_ids
        remark="验证订单"
    } | ConvertTo-Json -Depth 10
    $order = Invoke-WebRequest -Uri "$BASE_URL/orders/" -Method POST -Headers $headers -Body $body -ContentType "application/json" -UseBasicParsing
    $order_data = $order.Content | ConvertFrom-Json
    Write-Host "✅ 订单创建成功，订单号: $($order_data.data.order_no)" -ForegroundColor Green
    Write-Host "   总金额: $($order_data.data.total_amount)" -ForegroundColor Gray
} catch {
    Write-Host "❌ 订单创建失败" -ForegroundColor Red
    Write-Host "   错误: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "=== 所有验证通过！最小下单闭环已通 ===" -ForegroundColor Green
