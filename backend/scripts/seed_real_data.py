"""
ShamGP 商城真实数据种子脚本
生成300个商品、15个分类、100+SKU、100用户 + 地址数据
"""
import asyncio
import sys
import os
import random
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models import (
    User, Role, ProductCategory, Product, ProductSpu,
    ProductSku, ProductImage, Address,
    CartItem, Order, OrderItem
)
from app.models.recommend import Floor, FloorProduct

# ============================================================
# 15个商品分类
# ============================================================
CATEGORIES = [
    {"name": "手机数码", "code": "phone_digital", "sort": 1},
    {"name": "家电家居", "code": "home_appliance", "sort": 2},
    {"name": "服装鞋帽", "code": "clothing_shoes", "sort": 3},
    {"name": "美妆护肤", "code": "beauty_skincare", "sort": 4},
    {"name": "食品生鲜", "code": "fresh_food", "sort": 5},
    {"name": "母婴用品", "code": "mother_baby", "sort": 6},
    {"name": "图书文具", "code": "books_stationery", "sort": 7},
    {"name": "运动户外", "code": "sports_outdoor", "sort": 8},
    {"name": "汽车用品", "code": "auto_supplies", "sort": 9},
    {"name": "珠宝饰品", "code": "jewelry_accessories", "sort": 10},
    {"name": "厨具餐具", "code": "kitchenware", "sort": 11},
    {"name": "家纺床品", "code": "home_textile", "sort": 12},
    {"name": "钟表眼镜", "code": "watches_glasses", "sort": 13},
    {"name": "宠物用品", "code": "pet_supplies", "sort": 14},
    {"name": "虚拟商品", "code": "virtual_goods", "sort": 15},
]

# ============================================================
# 商品模板（每个分类2-5个模板，每个模板会生成多个变体）
# ============================================================
PRODUCT_TEMPLATES = [
    # 手机数码
    {"cat_idx": 0, "name_tpl": "iPhone 15 Pro Max {storage} {color}", "price_range": (7999, 11999), "brief": "苹果旗舰手机，A17 Pro芯片", "cover_seed": 101, "variants": [
        {"storage": "256G", "color": "深空黑", "price_offset": 0},
        {"storage": "256G", "color": "原色钛金属", "price_offset": 0},
        {"storage": "512G", "color": "深空黑", "price_offset": 1000},
        {"storage": "512G", "color": "白色钛金属", "price_offset": 1000},
        {"storage": "1TB", "color": "原色钛金属", "price_offset": 2000},
    ]},
    {"cat_idx": 0, "name_tpl": "iPhone 15 {storage} {color}", "price_range": (5999, 7999), "brief": "苹果性价比旗舰", "cover_seed": 102, "variants": [
        {"storage": "128G", "color": "蓝色", "price_offset": 0},
        {"storage": "128G", "color": "粉色", "price_offset": 0},
        {"storage": "256G", "color": "黑色", "price_offset": 900},
        {"storage": "256G", "color": "绿色", "price_offset": 900},
    ]},
    {"cat_idx": 0, "name_tpl": "小米14 Ultra {storage} {color}", "price_range": (5999, 7999), "brief": "小米徕卡影像旗舰", "cover_seed": 103, "variants": [
        {"storage": "256G", "color": "黑色", "price_offset": 0},
        {"storage": "256G", "color": "白色", "price_offset": 0},
        {"storage": "512G", "color": "钛灰", "price_offset": 1000},
    ]},
    {"cat_idx": 0, "name_tpl": "华为Mate 60 Pro+ {storage} {color}", "price_range": (6999, 9999), "brief": "华为麒麟芯片旗舰", "cover_seed": 104, "variants": [
        {"storage": "256G", "color": "宣白", "price_offset": 0},
        {"storage": "512G", "color": "砚黑", "price_offset": 1000},
        {"storage": "512G", "color": "宣白", "price_offset": 1000},
    ]},
    {"cat_idx": 0, "name_tpl": "AirPods Pro (第三代)", "price_range": (1799, 2299), "brief": "主动降噪无线耳机", "cover_seed": 105, "variants": [
        {"storage": "标准版", "color": "白色", "price_offset": 0},
    ]},
    {"cat_idx": 0, "name_tpl": "Sony WH-1000XM5 头戴式耳机", "price_range": (2199, 2799), "brief": "业界顶级降噪耳机", "cover_seed": 106, "variants": [
        {"storage": "标准版", "color": "黑色", "price_offset": 0},
        {"storage": "标准版", "color": "铂金银", "price_offset": 0},
    ]},
    {"cat_idx": 0, "name_tpl": "Apple Watch Series 9 {size}mm", "price_range": (2999, 3999), "brief": "苹果智能手表", "cover_seed": 107, "variants": [
        {"storage": "41mm", "color": "午夜色铝合金", "price_offset": 0},
        {"storage": "45mm", "color": "星光色铝合金", "price_offset": 200},
        {"storage": "45mm", "color": "银色不锈钢", "price_offset": 800},
    ]},
    {"cat_idx": 0, "name_tpl": "小米手环8 Pro", "price_range": (299, 399), "brief": "大屏健康手环", "cover_seed": 108, "variants": [
        {"storage": "标准版", "color": "黑色", "price_offset": 0},
        {"storage": "标准版", "color": "银色", "price_offset": 0},
    ]},
    # 家电家居
    {"cat_idx": 1, "name_tpl": "小米电视 ES65 {version}", "price_range": (2999, 3999), "brief": "4K超高清智能电视", "cover_seed": 201, "variants": [
        {"storage": "标准版", "color": "黑色", "price_offset": 0},
        {"storage": "Pro版", "color": "黑色", "price_offset": 500},
    ]},
    {"cat_idx": 1, "name_tpl": "戴森V15 Detect Fluffy吸尘器", "price_range": (4999, 5999), "brief": "智能无绳吸尘器", "cover_seed": 202, "variants": [
        {"storage": "标准版", "color": "铜金色", "price_offset": 0},
    ]},
    {"cat_idx": 1, "name_tpl": "石头扫地机器人 G20S", "price_range": (3999, 4999), "brief": "扫拖一体智能机器人", "cover_seed": 203, "variants": [
        {"storage": "标准版", "color": "黑色", "price_offset": 0},
    ]},
    {"cat_idx": 1, "name_tpl": "美的变频空调 {size} 匹", "price_range": (2299, 4299), "brief": "变频冷暖空调", "cover_seed": 204, "variants": [
        {"storage": "1.5匹", "color": "白色", "price_offset": 0},
        {"storage": "2匹", "color": "白色", "price_offset": 800},
        {"storage": "3匹", "color": "白色", "price_offset": 1600},
    ]},
    {"cat_idx": 1, "name_tpl": "海尔双开门冰箱 {size}L", "price_range": (2999, 5999), "brief": "对开门变频冰箱", "cover_seed": 205, "variants": [
        {"storage": "500L", "color": "银灰色", "price_offset": 0},
        {"storage": "600L", "color": "银灰色", "price_offset": 1000},
    ]},
    {"cat_idx": 1, "name_tpl": "小熊电饭煲 {size}", "price_range": (199, 399), "brief": "智能电饭煲", "cover_seed": 206, "variants": [
        {"storage": "3L", "color": "白色", "price_offset": 0},
        {"storage": "5L", "color": "白色", "price_offset": 100},
    ]},
    {"cat_idx": 1, "name_tpl": "苏泊尔电磁炉", "price_range": (199, 399), "brief": "家用电磁灶", "cover_seed": 207, "variants": [
        {"storage": "标准版", "color": "黑色", "price_offset": 0},
    ]},
    {"cat_idx": 1, "name_tpl": "九阳破壁机 Y1", "price_range": (499, 799), "brief": "多功能破壁料理机", "cover_seed": 208, "variants": [
        {"storage": "标准版", "color": "红色", "price_offset": 0},
        {"storage": "升级版", "color": "银色", "price_offset": 200},
    ]},
    # 服装鞋帽
    {"cat_idx": 2, "name_tpl": "Nike Air Jordan 1 Retro High OG", "price_range": (1299, 1699), "brief": "经典复古篮球鞋", "cover_seed": 301, "variants": [
        {"storage": "标准版", "color": "黑红配色", "price_offset": 0},
        {"storage": "标准版", "color": "芝加哥", "price_offset": 300},
    ]},
    {"cat_idx": 2, "name_tpl": "Adidas Ultraboost 22", "price_range": (899, 1299), "brief": "跑步旗舰跑鞋", "cover_seed": 302, "variants": [
        {"storage": "标准版", "color": "黑色", "price_offset": 0},
        {"storage": "标准版", "color": "白色", "price_offset": 0},
    ]},
    {"cat_idx": 2, "name_tpl": "北面1996经典羽绒服 {size}", "price_range": (1999, 2999), "brief": "户外工装羽绒服", "cover_seed": 303, "variants": [
        {"storage": "S", "color": "黑色", "price_offset": 0},
        {"storage": "M", "color": "黑色", "price_offset": 0},
        {"storage": "L", "color": "灰色", "price_offset": 0},
        {"storage": "XL", "color": "绿色", "price_offset": 0},
    ]},
    {"cat_idx": 2, "name_tpl": "LEVI'S 501经典牛仔裤 {size}", "price_range": (399, 699), "brief": "直筒版型牛仔裤", "cover_seed": 304, "variants": [
        {"storage": "30", "color": "石洗蓝", "price_offset": 0},
        {"storage": "32", "color": "石洗蓝", "price_offset": 0},
        {"storage": "34", "color": "深蓝", "price_offset": 0},
    ]},
    {"cat_idx": 2, "name_tpl": "UNIQLO U系列圆领T恤 {size}", "price_range": (79, 149), "brief": "纯棉基本款T恤", "cover_seed": 305, "variants": [
        {"storage": "S", "color": "白色", "price_offset": 0},
        {"storage": "M", "color": "黑色", "price_offset": 0},
        {"storage": "L", "color": "浅灰", "price_offset": 0},
    ]},
    {"cat_idx": 2, "name_tpl": "波司登极寒系列羽绒服 {size}", "price_range": (799, 1599), "brief": "御寒保暖羽绒服", "cover_seed": 306, "variants": [
        {"storage": "160/S", "color": "黑色", "price_offset": 0},
        {"storage": "170/M", "color": "深蓝", "price_offset": 0},
        {"storage": "180/L", "color": "红色", "price_offset": 0},
    ]},
    {"cat_idx": 2, "name_tpl": "斯凯奇熊猫鞋", "price_range": (499, 699), "brief": "经典复古运动鞋", "cover_seed": 307, "variants": [
        {"storage": "标准版", "color": "黑白配色", "price_offset": 0},
        {"storage": "标准版", "color": "粉白配色", "price_offset": 0},
    ]},
    {"cat_idx": 2, "name_tpl": "耐克Air Force 1 '07", "price_range": (699, 899), "brief": "经典板鞋", "cover_seed": 308, "variants": [
        {"storage": "标准版", "color": "全白", "price_offset": 0},
        {"storage": "标准版", "color": "黑白", "price_offset": 50},
    ]},
    # 美妆护肤
    {"cat_idx": 3, "name_tpl": "兰蔻小黑瓶精华50ml", "price_range": (760, 920), "brief": "护肤肌底精华液", "cover_seed": 401, "variants": [
        {"storage": "50ml", "color": "标准版", "price_offset": 0},
    ]},
    {"cat_idx": 3, "name_tpl": "雅诗兰黛小棕瓶眼霜15ml", "price_range": (499, 599), "brief": "眼部修护精华霜", "cover_seed": 402, "variants": [
        {"storage": "15ml", "color": "标准版", "price_offset": 0},
    ]},
    {"cat_idx": 3, "name_tpl": "SK-II神仙水230ml", "price_range": (1199, 1540), "brief": "护肤精华水", "cover_seed": 403, "variants": [
        {"storage": "230ml", "color": "标准版", "price_offset": 0},
        {"storage": "330ml", "color": "标准版", "price_offset": 600},
    ]},
    {"cat_idx": 3, "name_tpl": "YSL圣罗兰口红 #{shade}", "price_range": (335, 395), "brief": "缎光镜面口红", "cover_seed": 404, "variants": [
        {"storage": "标准版", "color": "#196 焦糖橘棕", "price_offset": 0},
        {"storage": "标准版", "color": "#302 赤裸豆沙", "price_offset": 0},
        {"storage": "标准版", "color": "#416 经典红", "price_offset": 0},
    ]},
    {"cat_idx": 3, "name_tpl": "La Mer海蓝之谜面霜60ml", "price_range": (2180, 2790), "brief": "经典精华面霜", "cover_seed": 405, "variants": [
        {"storage": "60ml", "color": "标准版", "price_offset": 0},
    ]},
    {"cat_idx": 3, "name_tpl": "OLAY玉兰油小白瓶精华", "price_range": (229, 299), "brief": "烟酰胺美白精华", "cover_seed": 406, "variants": [
        {"storage": "30ml", "color": "标准版", "price_offset": 0},
        {"storage": "50ml", "color": "标准版", "price_offset": 100},
    ]},
    {"cat_idx": 3, "name_tpl": "娇韵诗双萃精华50ml", "price_range": (760, 890), "brief": "黄金双瓶精华液", "cover_seed": 407, "variants": [
        {"storage": "50ml", "color": "标准版", "price_offset": 0},
    ]},
    {"cat_idx": 3, "name_tpl": "迪奥999经典口红", "price_range": (350, 400), "brief": "烈艳蓝金唇膏", "cover_seed": 408, "variants": [
        {"storage": "标准版", "color": "哑光版", "price_offset": 0},
        {"storage": "标准版", "color": "缎光版", "price_offset": 0},
    ]},
    # 食品生鲜
    {"cat_idx": 4, "name_tpl": "三只松鼠坚果礼盒1525g", "price_range": (98, 138), "brief": "坚果零食大礼包", "cover_seed": 501, "variants": [
        {"storage": "标准版", "color": "红色礼盒", "price_offset": 0},
    ]},
    {"cat_idx": 4, "name_tpl": "阳澄湖大闸蟹礼券 {size}型", "price_range": (288, 888), "brief": "鲜活大闸蟹礼券", "cover_seed": 502, "variants": [
        {"storage": "888型", "color": "标准版", "price_offset": 0},
        {"storage": "1288型", "color": "标准版", "price_offset": 400},
    ]},
    {"cat_idx": 4, "name_tpl": "伊利金典纯牛奶250ml*24盒", "price_range": (65, 79), "brief": "有机纯牛奶", "cover_seed": 503, "variants": [
        {"storage": "24盒装", "color": "标准版", "price_offset": 0},
    ]},
    {"cat_idx": 4, "name_tpl": "飞天茅台53度500ml", "price_range": (1499, 2999), "brief": "酱香型白酒", "cover_seed": 504, "variants": [
        {"storage": "500ml", "color": "标准版", "price_offset": 0},
    ]},
    {"cat_idx": 4, "name_tpl": "农夫山泉17.5°橙4.5斤", "price_range": (45, 65), "brief": "新鲜脐橙", "cover_seed": 505, "variants": [
        {"storage": "4.5斤装", "color": "标准版", "price_offset": 0},
    ]},
    {"cat_idx": 4, "name_tpl": "海底捞自热火锅 {flavor}", "price_range": (35, 55), "brief": "方便自热火锅", "cover_seed": 506, "variants": [
        {"storage": "标准版", "color": "番茄牛肉", "price_offset": 0},
        {"storage": "标准版", "color": "麻辣牛肉", "price_offset": 0},
    ]},
    {"cat_idx": 4, "name_tpl": "荷兰进口有机奶粉4段", "price_range": (168, 258), "brief": "婴幼儿配方奶粉", "cover_seed": 507, "variants": [
        {"storage": "800g", "color": "标准版", "price_offset": 0},
    ]},
    {"cat_idx": 4, "name_tpl": "星巴克浓缩咖啡豆454g", "price_range": (78, 98), "brief": "进口咖啡豆", "cover_seed": 508, "variants": [
        {"storage": "454g", "color": "中度烘焙", "price_offset": 0},
        {"storage": "454g", "color": "深度烘焙", "price_offset": 0},
    ]},
    # 母婴用品
    {"cat_idx": 5, "name_tpl": "贝亲宽口径奶瓶160ml", "price_range": (108, 148), "brief": "婴儿硅胶奶瓶", "cover_seed": 601, "variants": [
        {"storage": "160ml", "color": "透明色", "price_offset": 0},
        {"storage": "240ml", "color": "透明色", "price_offset": 30},
    ]},
    {"cat_idx": 5, "name_tpl": "花王妙而舒纸尿裤M号64片", "price_range": (115, 145), "brief": "婴儿纸尿裤", "cover_seed": 602, "variants": [
        {"storage": "M64片", "color": "标准版", "price_offset": 0},
        {"storage": "L54片", "color": "标准版", "price_offset": 20},
    ]},
    {"cat_idx": 5, "name_tpl": "美德乐电动吸奶器", "price_range": (899, 1399), "brief": "双边电动吸乳器", "cover_seed": 603, "variants": [
        {"storage": "标准版", "color": "粉色", "price_offset": 0},
    ]},
    {"cat_idx": 5, "name_tpl": "好孩子婴儿推车D619", "price_range": (699, 1099), "brief": "轻便折叠婴儿车", "cover_seed": 604, "variants": [
        {"storage": "标准版", "color": "深蓝色", "price_offset": 0},
        {"storage": "标准版", "color": "红色", "price_offset": 0},
    ]},
    {"cat_idx": 5, "name_tpl": "启初婴儿面霜80g", "price_range": (68, 88), "brief": "宝宝保湿护肤霜", "cover_seed": 605, "variants": [
        {"storage": "80g", "color": "标准版", "price_offset": 0},
    ]},
    {"cat_idx": 5, "name_tpl": "儿童安全座椅0-12岁", "price_range": (699, 1299), "brief": "ISOFIX接口安全座椅", "cover_seed": 606, "variants": [
        {"storage": "标准版", "color": "黑色", "price_offset": 0},
    ]},
    {"cat_idx": 5, "name_tpl": "gb好孩子儿童餐具套装", "price_range": (89, 129), "brief": "不锈钢儿童餐具", "cover_seed": 607, "variants": [
        {"storage": "标准版", "color": "蓝色", "price_offset": 0},
        {"storage": "标准版", "color": "粉色", "price_offset": 0},
    ]},
    {"cat_idx": 5, "name_tpl": "费雪牌婴儿健身架", "price_range": (299, 399), "brief": "多功能婴儿健身器", "cover_seed": 608, "variants": [
        {"storage": "标准版", "color": "彩色", "price_offset": 0},
    ]},
    # 图书文具
    {"cat_idx": 6, "name_tpl": "人类简史三部曲套装", "price_range": (134, 168), "brief": "尤瓦尔·赫拉利作品集", "cover_seed": 701, "variants": [
        {"storage": "套装3册", "color": "标准版", "price_offset": 0},
    ]},
    {"cat_idx": 6, "name_tpl": "华为MatePad 11平板", "price_range": (2499, 2999), "brief": "鸿蒙OS平板电脑", "cover_seed": 702, "variants": [
        {"storage": "6+64G", "color": "海岛蓝", "price_offset": 0},
        {"storage": "6+128G", "color": "曜石灰", "price_offset": 300},
    ]},
    {"cat_idx": 6, "name_tpl": "Kindle Paperwhite 5电子书", "price_range": (1299, 1499), "brief": "6.8英寸护眼电纸书", "cover_seed": 703, "variants": [
        {"storage": "8G", "color": "黑色", "price_offset": 0},
        {"storage": "32G", "color": "黑色", "price_offset": 200},
    ]},
    {"cat_idx": 6, "name_tpl": "得力金属笔筒", "price_range": (29, 49), "brief": "桌面收纳笔筒", "cover_seed": 704, "variants": [
        {"storage": "标准版", "color": "银色", "price_offset": 0},
    ]},
    {"cat_idx": 6, "name_tpl": "MUJI无印良品中性笔6支装", "price_range": (35, 45), "brief": "按动中性笔", "cover_seed": 705, "variants": [
        {"storage": "6支装", "color": "黑色", "price_offset": 0},
    ]},
    {"cat_idx": 6, "name_tpl": "LAMY狩猎者钢笔", "price_range": (149, 199), "brief": "德国精钢笔尖", "cover_seed": 706, "variants": [
        {"storage": "标准版", "color": "白色", "price_offset": 0},
        {"storage": "标准版", "color": "绿色", "price_offset": 0},
    ]},
    {"cat_idx": 6, "name_tpl": "晨光软皮笔记本A5", "price_range": (15, 25), "brief": "加厚线圈笔记本", "cover_seed": 707, "variants": [
        {"storage": "A5", "color": "粉色", "price_offset": 0},
        {"storage": "B5", "color": "蓝色", "price_offset": 5},
    ]},
    {"cat_idx": 6, "name_tpl": "小米平板6 MAX 14", "price_range": (3499, 4499), "brief": "大屏旗舰平板", "cover_seed": 708, "variants": [
        {"storage": "8+256G", "color": "黑色", "price_offset": 0},
        {"storage": "12+512G", "color": "黑色", "price_offset": 800},
    ]},
    # 运动户外
    {"cat_idx": 7, "name_tpl": "迪卡侬山地自行车 {size}", "price_range": (899, 1999), "brief": "成人变速山地车", "cover_seed": 801, "variants": [
        {"storage": "26寸", "color": "黑色", "price_offset": 0},
        {"storage": "27.5寸", "color": "蓝色", "price_offset": 500},
    ]},
    {"cat_idx": 7, "name_tpl": "骆驼户外帐篷 {size}", "price_range": (299, 599), "brief": "全自动户外帐篷", "cover_seed": 802, "variants": [
        {"storage": "2-3人", "color": "绿色", "price_offset": 0},
        {"storage": "4-5人", "color": "蓝色", "price_offset": 200},
    ]},
    {"cat_idx": 7, "name_tpl": "李宁羽毛球拍超轻突击", "price_range": (199, 399), "brief": "碳纤维球拍", "cover_seed": 803, "variants": [
        {"storage": "标准版", "color": "红色", "price_offset": 0},
        {"storage": "专业版", "color": "黑色", "price_offset": 150},
    ]},
    {"cat_idx": 7, "name_tpl": "耐克篮球鞋 Giannis Immortality 3", "price_range": (499, 699), "brief": "男子实战篮球鞋", "cover_seed": 804, "variants": [
        {"storage": "标准版", "color": "黑色/白色", "price_offset": 0},
    ]},
    {"cat_idx": 7, "name_tpl": "小米手环8 {version}", "price_range": (249, 299), "brief": "运动健康手环", "cover_seed": 805, "variants": [
        {"storage": "标准版", "color": "黑色", "price_offset": 0},
        {"storage": "NFC版", "color": "黑色", "price_offset": 80},
    ]},
    {"cat_idx": 7, "name_tpl": "哥伦比亚户外徒步鞋", "price_range": (499, 799), "brief": "防滑透气登山鞋", "cover_seed": 806, "variants": [
        {"storage": "标准版", "color": "棕色", "price_offset": 0},
        {"storage": "标准版", "color": "黑色", "price_offset": 0},
    ]},
    {"cat_idx": 7, "name_tpl": "锐步瑜伽垫10mm", "price_range": (89, 149), "brief": "加厚防滑瑜伽垫", "cover_seed": 807, "variants": [
        {"storage": "183*61cm", "color": "紫色", "price_offset": 0},
        {"storage": "183*80cm", "color": "粉色", "price_offset": 40},
    ]},
    {"cat_idx": 7, "name_tpl": "威尔胜专业篮球", "price_range": (129, 199), "brief": "室内外通用篮球", "cover_seed": 808, "variants": [
        {"storage": "标准版", "color": "棕色", "price_offset": 0},
    ]},
    # 汽车用品
    {"cat_idx": 8, "name_tpl": "米其林轮胎 215/55R17", "price_range": (499, 699), "brief": "静音舒适轮胎", "cover_seed": 901, "variants": [
        {"storage": "单条", "color": "黑色", "price_offset": 0},
        {"storage": "四条装", "color": "黑色", "price_offset": 1800},
    ]},
    {"cat_idx": 8, "name_tpl": "倍思车载充电器100W", "price_range": (59, 89), "brief": "双口快充车载充电", "cover_seed": 902, "variants": [
        {"storage": "标准版", "color": "黑色", "price_offset": 0},
    ]},
    {"cat_idx": 8, "name_tpl": "3M汽车贴膜 {size}", "price_range": (899, 1999), "brief": "车窗防紫外线隔热膜", "cover_seed": 903, "variants": [
        {"storage": "前挡风", "color": "浅色", "price_offset": 0},
        {"storage": "全车套装", "color": "浅色", "price_offset": 1200},
    ]},
    {"cat_idx": 8, "name_tpl": "固特异汽车脚垫 {model}", "price_range": (199, 399), "brief": "专用立体脚垫", "cover_seed": 904, "variants": [
        {"storage": "通用型", "color": "黑色", "price_offset": 0},
        {"storage": "专车专用", "color": "棕色", "price_offset": 150},
    ]},
    {"cat_idx": 8, "name_tpl": "70迈行车记录仪A500S", "price_range": (349, 449), "brief": "前后双录高清记录仪", "cover_seed": 905, "variants": [
        {"storage": "单镜头", "color": "黑色", "price_offset": 0},
        {"storage": "双镜头", "color": "黑色", "price_offset": 150},
    ]},
    {"cat_idx": 8, "name_tpl": "铁将军胎压监测器", "price_range": (199, 299), "brief": "太阳能外置胎压监测", "cover_seed": 906, "variants": [
        {"storage": "4胎", "color": "黑色", "price_offset": 0},
    ]},
    {"cat_idx": 8, "name_tpl": "车载冰箱 12L", "price_range": (199, 349), "brief": "压缩机制冷车用冰箱", "cover_seed": 907, "variants": [
        {"storage": "12L", "color": "银色", "price_offset": 0},
        {"storage": "20L", "color": "银色", "price_offset": 150},
    ]},
    {"cat_idx": 8, "name_tpl": "香百年车载香水 {fragrance}", "price_range": (49, 99), "brief": "固体香薰除异味", "cover_seed": 908, "variants": [
        {"storage": "标准版", "color": "古龙香", "price_offset": 0},
        {"storage": "标准版", "color": "海洋香", "price_offset": 0},
    ]},
    # 珠宝饰品
    {"cat_idx": 9, "name_tpl": "周大福传承系列金手镯 {weight}", "price_range": (3999, 12999), "brief": "古法黄金手镯", "cover_seed": 1001, "variants": [
        {"storage": "30g", "color": "黄金色", "price_offset": 0},
        {"storage": "50g", "color": "黄金色", "price_offset": 6000},
    ]},
    {"cat_idx": 9, "name_tpl": "施华洛世奇跳动的心项链", "price_range": (399, 499), "brief": "水晶项链", "cover_seed": 1002, "variants": [
        {"storage": "标准版", "color": "银色", "price_offset": 0},
        {"storage": "标准版", "color": "金色", "price_offset": 50},
    ]},
    {"cat_idx": 9, "name_tpl": "潘多拉 Moments 手链", "price_range": (298, 398), "brief": "镀金珠手链", "cover_seed": 1003, "variants": [
        {"storage": "标准版", "color": "银色", "price_offset": 0},
    ]},
    {"cat_idx": 9, "name_tpl": "APM Monaco六芒星项链", "price_range": (698, 798), "brief": "银质镶钻项链", "cover_seed": 1004, "variants": [
        {"storage": "标准版", "color": "银色", "price_offset": 0},
    ]},
    {"cat_idx": 9, "name_tpl": "卡西欧 G-SHOCK 腕表 GA-110", "price_range": (1299, 1599), "brief": "防磁防震电子表", "cover_seed": 1005, "variants": [
        {"storage": "标准版", "color": "黑色", "price_offset": 0},
        {"storage": "标准版", "color": "白色", "price_offset": 0},
    ]},
    {"cat_idx": 9, "name_tpl": "Tissot 天梭力洛克机械表", "price_range": (3999, 4599), "brief": "瑞士自动机械表", "cover_seed": 1006, "variants": [
        {"storage": "标准版", "color": "银色", "price_offset": 0},
        {"storage": "皮带版", "color": "银色", "price_offset": 0},
    ]},
    {"cat_idx": 9, "name_tpl": "周六福黄金吊坠", "price_range": (899, 1999), "brief": "足金吊坠", "cover_seed": 1007, "variants": [
        {"storage": "标准版", "color": "黄金色", "price_offset": 0},
    ]},
    {"cat_idx": 9, "name_tpl": "潮宏基时尚耳钉", "price_range": (299, 499), "brief": "18K金耳饰", "cover_seed": 1008, "variants": [
        {"storage": "标准版", "color": "玫瑰金", "price_offset": 0},
        {"storage": "标准版", "color": "银色", "price_offset": -50},
    ]},
    # 厨具餐具
    {"cat_idx": 10, "name_tpl": "WMF德国福腾宝刀具套装", "price_range": (299, 499), "brief": "不锈钢厨刀套装", "cover_seed": 1101, "variants": [
        {"storage": "3件套", "color": "银色", "price_offset": 0},
        {"storage": "5件套", "color": "银色", "price_offset": 200},
    ]},
    {"cat_idx": 10, "name_tpl": "双立人ZWILLING 炒锅28cm", "price_range": (399, 599), "brief": "不粘锅炒锅", "cover_seed": 1102, "variants": [
        {"storage": "28cm", "color": "黑色", "price_offset": 0},
        {"storage": "30cm", "color": "黑色", "price_offset": 100},
    ]},
    {"cat_idx": 10, "name_tpl": "日本进口骨瓷餐具套装", "price_range": (199, 399), "brief": "釉下彩陶瓷餐具", "cover_seed": 1103, "variants": [
        {"storage": "20件套", "color": "白色", "price_offset": 0},
        {"storage": "46件套", "color": "蓝色", "price_offset": 200},
    ]},
    {"cat_idx": 10, "name_tpl": "炊大皇不粘炒锅30cm", "price_range": (99, 179), "brief": "电磁炉通用不粘锅", "cover_seed": 1104, "variants": [
        {"storage": "30cm", "color": "黑色", "price_offset": 0},
    ]},
    {"cat_idx": 10, "name_tpl": "LOCK&LOCK乐扣乐扣保温杯", "price_range": (89, 149), "brief": "不锈钢真空保温杯", "cover_seed": 1105, "variants": [
        {"storage": "350ml", "color": "黑色", "price_offset": 0},
        {"storage": "500ml", "color": "银色", "price_offset": 30},
    ]},
    {"cat_idx": 10, "name_tpl": "德国双立人刀具 {set}", "price_range": (399, 899), "brief": "专业厨房刀具套装", "cover_seed": 1106, "variants": [
        {"storage": "三件套", "color": "银色", "price_offset": 0},
        {"storage": "七件套", "color": "银色", "price_offset": 400},
    ]},
    {"cat_idx": 10, "name_tpl": "美的电压力锅5L", "price_range": (299, 449), "brief": "智能电压力锅", "cover_seed": 1107, "variants": [
        {"storage": "5L", "color": "银色", "price_offset": 0},
    ]},
    {"cat_idx": 10, "name_tpl": "小熊电烤箱 {size}", "price_range": (139, 199), "brief": "多功能家用电烤箱", "cover_seed": 1108, "variants": [
        {"storage": "10L", "color": "白色", "price_offset": 0},
        {"storage": "20L", "color": "白色", "price_offset": 60},
    ]},
    # 家纺床品
    {"cat_idx": 11, "name_tpl": "水星家纺60支纯棉四件套 {size}", "price_range": (299, 499), "brief": "高支高密纯棉套件", "cover_seed": 1201, "variants": [
        {"storage": "1.5m床", "color": "蓝色", "price_offset": 0},
        {"storage": "1.8m床", "color": "灰色", "price_offset": 80},
    ]},
    {"cat_idx": 11, "name_tpl": "富安娜羊毛被 {size}", "price_range": (299, 599), "brief": "澳洲羊毛被子", "cover_seed": 1202, "variants": [
        {"storage": "150*200cm", "color": "白色", "price_offset": 0},
        {"storage": "200*230cm", "color": "白色", "price_offset": 150},
    ]},
    {"cat_idx": 11, "name_tpl": "梦洁泰国乳胶枕", "price_range": (199, 399), "brief": "天然乳胶护颈枕", "cover_seed": 1203, "variants": [
        {"storage": "标准版", "color": "白色", "price_offset": 0},
    ]},
    {"cat_idx": 11, "name_tpl": "罗莱全棉毛巾两条装", "price_range": (49, 79), "brief": "柔软吸水毛巾", "cover_seed": 1204, "variants": [
        {"storage": "两条装", "color": "白色", "price_offset": 0},
        {"storage": "四条装", "color": "蓝色", "price_offset": 40},
    ]},
    {"cat_idx": 11, "name_tpl": "晚安家居护脊床垫 {size}", "price_range": (999, 2999), "brief": "弹簧护脊床垫", "cover_seed": 1205, "variants": [
        {"storage": "120*190cm", "color": "灰色", "price_offset": 0},
        {"storage": "150*200cm", "color": "灰色", "price_offset": 500},
    ]},
    {"cat_idx": 11, "name_tpl": "无印良品天竺棉床单", "price_range": (199, 299), "brief": "简约纯棉床单", "cover_seed": 1206, "variants": [
        {"storage": "标准版", "color": "浅灰", "price_offset": 0},
    ]},
    {"cat_idx": 11, "name_tpl": "紫罗兰抗菌防螨枕芯", "price_range": (59, 99), "brief": "立体护颈枕芯", "cover_seed": 1207, "variants": [
        {"storage": "标准版", "color": "白色", "price_offset": 0},
    ]},
    {"cat_idx": 11, "name_tpl": "艾美特珊瑚绒毯子", "price_range": (89, 149), "brief": "加厚保暖毯", "cover_seed": 1208, "variants": [
        {"storage": "150*200cm", "color": "米色", "price_offset": 0},
        {"storage": "180*220cm", "color": "灰色", "price_offset": 50},
    ]},
    # 钟表眼镜
    {"cat_idx": 12, "name_tpl": "暴龙眼镜 BJ6089", "price_range": (299, 499), "brief": "光学镜框近视眼镜", "cover_seed": 1301, "variants": [
        {"storage": "标准版", "color": "黑色", "price_offset": 0},
        {"storage": "标准版", "color": "金色", "price_offset": 50},
    ]},
    {"cat_idx": 12, "name_tpl": "海伦凯勒眼镜 H8055", "price_range": (399, 599), "brief": "偏光太阳镜", "cover_seed": 1302, "variants": [
        {"storage": "标准版", "color": "黑色", "price_offset": 0},
        {"storage": "标准版", "color": "渐变灰", "price_offset": 50},
    ]},
    {"cat_idx": 12, "name_tpl": "精工SEIKO 5号自动机械表", "price_range": (1199, 1699), "brief": "日本自动机械表", "cover_seed": 1303, "variants": [
        {"storage": "标准版", "color": "黑色表盘", "price_offset": 0},
        {"storage": "标准版", "color": "蓝色表盘", "price_offset": 100},
    ]},
    {"cat_idx": 12, "name_tpl": "浪琴名匠系列机械表", "price_range": (9999, 14999), "brief": "瑞士名表自动机械", "cover_seed": 1304, "variants": [
        {"storage": "标准版", "color": "银色", "price_offset": 0},
    ]},
    {"cat_idx": 12, "name_tpl": "海鸥表国民系列 816.13.6080", "price_range": (599, 899), "brief": "国产自动机械表", "cover_seed": 1305, "variants": [
        {"storage": "标准版", "color": "银色", "price_offset": 0},
    ]},
    {"cat_idx": 12, "name_tpl": "蔡司镜片近视眼镜片 {度数}", "price_range": (298, 698), "brief": "防蓝光非球面镜片", "cover_seed": 1306, "variants": [
        {"storage": "1.56非球面", "color": "标准版", "price_offset": 0},
        {"storage": "1.67非球面", "color": "标准版", "price_offset": 300},
    ]},
    {"cat_idx": 12, "name_tpl": "雷朋Ray-Ban RB3025太阳镜", "price_range": (698, 898), "brief": "经典款飞行员太阳镜", "cover_seed": 1307, "variants": [
        {"storage": "标准版", "color": "金色/绿色", "price_offset": 0},
    ]},
    {"cat_idx": 12, "name_tpl": "依视路钻晶A3镜片 {规格}", "price_range": (398, 898), "brief": "防污防刮眼镜片", "cover_seed": 1308, "variants": [
        {"storage": "1.552", "color": "标准版", "price_offset": 0},
        {"storage": "1.601", "color": "标准版", "price_offset": 300},
    ]},
    # 宠物用品
    {"cat_idx": 13, "name_tpl": "皇家Royal Canin猫粮 {age}", "price_range": (198, 398), "brief": "全价猫粮成猫粮", "cover_seed": 1401, "variants": [
        {"storage": "2kg", "color": "标准版", "price_offset": 0},
        {"storage": "4kg", "color": "标准版", "price_offset": 180},
    ]},
    {"cat_idx": 13, "name_tpl": "疯狂小狗狗粮 {flavor}", "price_range": (68, 138), "brief": "全价犬粮牛肉味", "cover_seed": 1402, "variants": [
        {"storage": "2kg", "color": "牛肉味", "price_offset": 0},
        {"storage": "5kg", "color": "鸡肉味", "price_offset": 100},
    ]},
    {"cat_idx": 13, "name_tpl": "霍曼Homerun智能猫砂盆", "price_range": (699, 899), "brief": "自动除臭猫砂盆", "cover_seed": 1403, "variants": [
        {"storage": "标准版", "color": "白色", "price_offset": 0},
    ]},
    {"cat_idx": 13, "name_tpl": "PIDAN混合猫砂6L", "price_range": (49, 69), "brief": "豆腐膨润土混合砂", "cover_seed": 1404, "variants": [
        {"storage": "6L", "color": "灰色", "price_offset": 0},
        {"storage": "12L", "color": "灰色", "price_offset": 40},
    ]},
    {"cat_idx": 13, "name_tpl": "小佩PETKIT宠物饮水机", "price_range": (139, 199), "brief": "循环过滤饮水机", "cover_seed": 1405, "variants": [
        {"storage": "标准版", "color": "白色", "price_offset": 0},
    ]},
    {"cat_idx": 13, "name_tpl": "派特灵宠物驱虫滴剂", "price_range": (49, 99), "brief": "猫咪体外驱虫药", "cover_seed": 1406, "variants": [
        {"storage": "3支装", "color": "标准版", "price_offset": 0},
    ]},
    {"cat_idx": 13, "name_tpl": "哈根纽翠斯猫罐头85g*12罐", "price_range": (149, 189), "brief": "进口猫主食罐", "cover_seed": 1407, "variants": [
        {"storage": "12罐装", "color": "鸡肉味", "price_offset": 0},
        {"storage": "12罐装", "color": "三文鱼味", "price_offset": 0},
    ]},
    {"cat_idx": 13, "name_tpl": "宠物外出便携背包", "price_range": (59, 119), "brief": "猫咪狗狗外出背包", "cover_seed": 1408, "variants": [
        {"storage": "小号", "color": "灰色", "price_offset": 0},
        {"storage": "大号", "color": "蓝色", "price_offset": 40},
    ]},
    # 虚拟商品
    {"cat_idx": 14, "name_tpl": "腾讯视频VIP会员 {period}", "price_range": (25, 268), "brief": "视频网站会员月卡/年卡", "cover_seed": 1501, "variants": [
        {"storage": "月卡", "color": "标准版", "price_offset": 0},
        {"storage": "季卡", "color": "标准版", "price_offset": 60},
        {"storage": "年卡", "color": "标准版", "price_offset": 220},
    ]},
    {"cat_idx": 14, "name_tpl": "爱奇艺VIP黄金会员 {period}", "price_range": (25, 248), "brief": "视频会员月卡/年卡", "cover_seed": 1502, "variants": [
        {"storage": "月卡", "color": "标准版", "price_offset": 0},
        {"storage": "年卡", "color": "标准版", "price_offset": 200},
    ]},
    {"cat_idx": 14, "name_tpl": "网易云音乐黑胶VIP {period}", "price_range": (18, 218), "brief": "音乐平台会员", "cover_seed": 1503, "variants": [
        {"storage": "月卡", "color": "标准版", "price_offset": 0},
        {"storage": "年卡", "color": "标准版", "price_offset": 180},
    ]},
    {"cat_idx": 14, "name_tpl": "QQ音乐绿钻豪华版 {period}", "price_range": (18, 198), "brief": "音乐平台会员", "cover_seed": 1504, "variants": [
        {"storage": "月卡", "color": "标准版", "price_offset": 0},
        {"storage": "年卡", "color": "标准版", "price_offset": 160},
    ]},
    {"cat_idx": 14, "name_tpl": "饿了么超级吃货卡 {period}", "price_range": (15, 180), "brief": "外卖平台会员", "cover_seed": 1505, "variants": [
        {"storage": "季卡", "color": "标准版", "price_offset": 0},
        {"storage": "年卡", "color": "标准版", "price_offset": 150},
    ]},
    {"cat_idx": 14, "name_tpl": "美团外卖会员 {period}", "price_range": (15, 180), "brief": "外卖红包会员", "cover_seed": 1506, "variants": [
        {"storage": "季卡", "color": "标准版", "price_offset": 0},
        {"storage": "年卡", "color": "标准版", "price_offset": 150},
    ]},
    {"cat_idx": 14, "name_tpl": "京东PLUS会员 {period}", "price_range": (69, 699), "brief": "电商平台会员", "cover_seed": 1507, "variants": [
        {"storage": "季卡", "color": "标准版", "price_offset": 0},
        {"storage": "年卡", "color": "标准版", "price_offset": 580},
    ]},
    {"cat_idx": 14, "name_tpl": "百度网盘超级会员 {period}", "price_range": (25, 298), "brief": "云存储会员", "cover_seed": 1508, "variants": [
        {"storage": "月卡", "color": "标准版", "price_offset": 0},
        {"storage": "年卡", "color": "标准版", "price_offset": 250},
    ]},
]

# 每个分类至少2个模板，不够时随机扩展
def expand_templates():
    """确保每个分类至少有2个模板"""
    by_cat = {}
    for t in PRODUCT_TEMPLATES:
        by_cat.setdefault(t["cat_idx"], []).append(t)
    
    expanded = []
    for cat_idx in range(15):
        cats = by_cat.get(cat_idx, [])
        if len(cats) < 2:
            # 复制现有模板作为补充
            existing = cats[0] if cats else PRODUCT_TEMPLATES[0]
            while len(cats) < 2:
                cats.append(existing)
        expanded.extend(cats)
    return expanded


def make_product_code(cat_idx: int, seq: int) -> str:
    """生成商品编码"""
    prefixes = ["PHN", "HOM", "CLT", "BTY", "FOD", "MBB", "BKS", "SPT", "AUT", "JWL", 
                "KTN", "TXL", "WTG", "PET", "VTG"]
    return f"{prefixes[cat_idx]}{seq:04d}"


def make_picsum_url(seed: int, idx: int = 0, width: int = 500, height: int = 500) -> str:
    """生成picsum.photos图片URL"""
    return f"https://picsum.photos/seed/{seed + idx}/{width}/{height}"


def rnd_price(low: float, high: float) -> float:
    import random as _rnd
    return round(_rnd.uniform(low, high), 2)


def rnd_int(low: int, high: int) -> int:
    import random as _rnd
    return _rnd.randint(low, high)


def rnd_bool(p: float = 0.2) -> bool:
    import random as _rnd
    return _rnd.random() < p


async def seed_real_data():
    """执行真实数据种子"""
    async with AsyncSessionLocal() as session:
        print("=" * 60)
        print("开始生成真实数据...")
        print("=" * 60)

        # =============================================
        # 1. 创建管理员角色
        # =============================================
        from sqlalchemy import select
        result = await session.execute(select(Role).where(Role.code == "admin"))
        admin_role = result.scalar_one_or_none()
        if not admin_role:
            admin_role = Role(name="管理员", code="admin", description="系统管理员", sort=1)
            session.add(admin_role)
            await session.flush()
            print("[OK] Created admin role")

        # =============================================
        # 2. 创建15个商品分类
        # =============================================
        categories = []
        for cat_data in CATEGORIES:
            cat = ProductCategory(
                name=cat_data["name"],
                code=cat_data["code"],
                sort=cat_data["sort"],
                level=1,
                status=1
            )
            session.add(cat)
            categories.append(cat)
        await session.flush()
        print(f"[OK] Created {len(categories)} categories")

        # =============================================
        # 3. 创建100个用户 + 地址
        # =============================================
        usernames = [
            "xiaoming", "xiaohong", "xiaozhang", "xiaoli", "xiaowang",
            "lao_wang", "sisi_123", "hunter99", "ocean_view", "star_rain",
            "cloud_nine", "moon_light", "sun_flower", "grass_roots", "wind_bell",
            "snow_flake", "rain_bow", "thunder_bolt", "leaf_green", "rose_red",
            "jacket_man", "book_worm", "music_fan", "game_king", "code_ninja",
            "data_pro", "cloud_dev", "ai_master", "web_wizard", "app_builder",
            "happy_life", "lucky_day", "peace_world", "love_forever", "dream_home",
            "sweet_home", "green_earth", "blue_sky", "clean_water", "fresh_air",
            "tech_guru", "fashion_lady", "sport_king", "food_lover", "travel_fan",
            "photo_pro", "video_pro", "design_master", "art_lover", "read_more",
            "study_hard", "work_smart", "play_hard", "rest_well", "eat_healthy",
            "run_fast", "jump_high", "swim_long", "bike_ride", "hike_mountain",
            "coffee_addict", "tea_lover", "wine_taster", "beer_fan", "cake_lover",
            "fruit_fan", "veggie_lover", "meat_eater", "fish_fan", "noodle_lover",
            "rice_bowl", "pizza_hut", "burger_king", "kfc_fan", "mc_fan",
            "online_shopper", "store_shopper", "mall_lover", "street_shopper", "market_fan",
            "super_market", "convenient_store", "warehouse_club", "outlet_fan", "duty_free",
            "beauty_fan", "skincare_lover", "makeup_pro", "perfume_fan", "jewelry_lover",
            "watch_collector", "bag_lover", "shoe_fan", "hat_collector", "scarf_lover",
        ]
        users = []
        for i, username in enumerate(usernames[:100]):
            user = User(
                username=username,
                password=get_password_hash("user123"),
                nickname=username.title().replace("_", " "),
                email=f"{username}@shamgp.com",
                phone=f"138{rnd_int(10000000, 99999999)}",
                status=1,
                user_type=2
            )
            session.add(user)
            users.append(user)
        await session.flush()
        print(f"[OK] 创建 {len(users)} 个用户")

        # 创建地址
        provinces = ["北京", "上海", "广东", "浙江", "江苏", "四川", "湖北", "湖南", "河南", "山东"]
        cities = {
            "北京": ["北京"], "上海": ["上海"], "广东": ["广州", "深圳", "东莞", "佛山"],
            "浙江": ["杭州", "宁波", "温州"], "江苏": ["南京", "苏州", "无锡"],
            "四川": ["成都", "绵阳"], "湖北": ["武汉", "宜昌"], "湖南": ["长沙"],
            "河南": ["郑州", "洛阳"], "山东": ["济南", "青岛"]
        }
        districts = ["朝阳区", "海淀区", "浦东新区", "黄浦区", "天河区", "西湖区", "江干区", "锦江区", "武侯区"]
        streets = ["中关村大街", "建国路", "南京路", "人民路", "建设路", "解放路", "文化路", "体育路"]

        for user in users[:100]:
            prov = provinces[rnd_int(0, len(provinces)-1)]
            city_list = cities.get(prov, ["上海"])
            city = city_list[rnd_int(0, len(city_list)-1)]
            district = districts[rnd_int(0, len(districts)-1)]
            street = streets[rnd_int(0, len(streets)-1)]
            addr = Address(
                user_id=user.id,
                consignee_name=user.nickname or user.username,
                consignee_phone=user.phone,
                province=prov,
                city=city,
                district=district,
                detail_address=f"{street}{rnd_int(1,999)}号{rnd_int(1,50)}楼{rnd_int(101,2999)}室",
                is_default=(rnd_int(0, 9) < 3)
            )
            session.add(addr)
        print(f"[OK] 创建地址数据")

        # =============================================
        # 4. 创建商品 + SPU + SKU + 图片
        # =============================================
        all_products = []
        all_spus = []
        all_skus = []
        all_images = []

        templates = PRODUCT_TEMPLATES  # 使用原始模板
        product_seq = 1
        spu_seq = 1
        sku_seq = 1
        img_seq = 1

        for cat_idx, cat in enumerate(categories):
            # 该分类下的所有模板
            cat_templates = [t for t in templates if t["cat_idx"] == cat_idx]
            if not cat_templates:
                # 如果没有模板，从第0个分类复制
                cat_templates = [t for t in templates if t["cat_idx"] == 0][:2]

            seq_in_cat = 0
            for tpl in cat_templates:
                base_price = rnd_price(tpl["price_range"][0], tpl["price_range"][1])
                # 每个模板生成多个商品（每2个variant生成1个商品主记录）
                num_products = max(1, (len(tpl["variants"]) + 1) // 2)

                for p_seq in range(num_products):
                    variant_start = p_seq * 2
                    variant_end = min(variant_start + 2, len(tpl["variants"]))
                    variants = tpl["variants"][variant_start:variant_end]
                    if not variants:
                        variants = tpl["variants"][:1]

                    price = base_price
                    name = tpl["name_tpl"]
                    # 用第一个variant生成基本信息
                    v0 = variants[0]
                    if "{storage}" in name:
                        name = name.replace("{storage}", v0.get("storage", ""))
                    if "{color}" in name:
                        name = name.replace("{color}", v0.get("color", ""))
                    if "{size}" in name:
                        name = name.replace("{size}", v0.get("storage", "标准"))
                    if "{weight}" in name:
                        name = name.replace("{weight}", v0.get("storage", "30g"))
                    if "{flavor}" in name:
                        name = name.replace("{flavor}", v0.get("storage", ""))
                    if "{age}" in name:
                        name = name.replace("{age}", "成猫")
                    if "{度数}" in name:
                        name = name.replace("{度数}", "1.56")
                    if "{period}" in name:
                        name = name.replace("{period}", v0.get("storage", ""))
                    if "{model}" in name:
                        name = name.replace("{model}", v0.get("storage", ""))
                    if "{version}" in name:
                        name = name.replace("{version}", v0.get("storage", ""))
                    if "{fragrance}" in name:
                        name = name.replace("{fragrance}", v0.get("storage", ""))
                    if "{set}" in name:
                        name = name.replace("{set}", v0.get("storage", ""))
                    if "{model}" in name:
                        name = name.replace("{model}", "")

                    price = base_price + v0.get("price_offset", 0)
                    original_price = round(price * rnd_price(1.1, 1.5), 2)
                    sales = rnd_int(0, 10000)
                    views = rnd_int(int(sales * 5), int(sales * 20)) if sales > 0 else rnd_int(10, 500)
                    stock = rnd_int(50, 500)
                    cover_seed = tpl["cover_seed"] + p_seq

                    product_code = make_product_code(cat_idx, product_seq)
                    product_seq += 1
                    seq_in_cat += 1

                    # ---- Product (legacy) ----
                    product = Product(
                        category_id=cat.id,
                        name=name[:200],
                        code=product_code,
                        brief=tpl.get("brief", ""),
                        cover_image=make_picsum_url(cover_seed, 0),
                        images=json.dumps([make_picsum_url(cover_seed, i) for i in range(1, 4)]),
                        price=price,
                        original_price=original_price,
                        stock=stock,
                        sales=sales,
                        views=views,
                        is_hot=rnd_bool(0.15),
                        is_new=rnd_bool(0.2),
                        is_recommend=rnd_bool(0.1),
                        status=1,
                        sort=seq_in_cat
                    )
                    session.add(product)
                    all_products.append(product)

                    # ---- ProductSpu ----
                    spu = ProductSpu(
                        id=spu_seq,
                        name=name[:200],
                        subtitle=tpl.get("brief", ""),
                        category_id=cat.id,
                        main_image=make_picsum_url(cover_seed, 0),
                        description=f"商品描述：{name}",
                        status=1,
                        sort=seq_in_cat,
                        sales_count=sales,
                        view_count=views
                    )
                    spu_seq += 1
                    session.add(spu)
                    all_spus.append(spu)

                    await session.flush()

                    # ---- ProductImage ----
                    for img_idx in range(3):
                        img = ProductImage(
                            id=img_seq,
                            spu_id=spu.id,
                            image_url=make_picsum_url(cover_seed, img_idx + 1),
                            image_type=0 if img_idx == 0 else 1,
                            sort=img_idx
                        )
                        img_seq += 1
                        session.add(img)
                        all_images.append(img)

                    # ---- ProductSku (每个商品2-4个SKU) ----
                    for v_idx, v in enumerate(variants):
                        sku_name = name
                        # 尝试替换variant信息
                        if len(variants) > 1:
                            if "{storage}" in tpl["name_tpl"]:
                                sku_name = name.replace(v0.get("storage", ""), v.get("storage", ""), 1)
                            elif "{color}" in tpl["name_tpl"]:
                                sku_name = name.replace(v0.get("color", ""), v.get("color", ""), 1)

                        sku_price = price + v.get("price_offset", 0)
                        sku_original = round(sku_price * rnd_price(1.1, 1.3), 2)
                        sku = ProductSku(
                            id=sku_seq,
                            spu_id=spu.id,
                            sku_code=f"{product_code}S{v_idx+1:02d}",
                            name=sku_name[:200] if sku_name else name[:200],
                            specs=json.dumps({"颜色": v.get("color", ""), "规格": v.get("storage", "")}, ensure_ascii=False),
                            image=make_picsum_url(cover_seed, v_idx),
                            price=sku_price,
                            original_price=sku_original,
                            cost_price=round(sku_price * 0.6, 2),
                            status=1,
                            sort=v_idx
                        )
                        sku_seq += 1
                        session.add(sku)
                        all_skus.append(sku)

        await session.flush()
        print(f"[OK] 创建 {len(all_products)} 个商品 (Product)")
        print(f"[OK] 创建 {len(all_spus)} 个商品SPU (ProductSpu)")
        print(f"[OK] 创建 {len(all_skus)} 个SKU (ProductSku)")
        print(f"[OK] 创建 {len(all_images)} 张商品图片 (ProductImage)")

        # =============================================
        # 5. 创建首页楼层数据
        # =============================================
        floor_defs = [
            {"name": "热销推荐", "code": "floor_hot", "title": "[HOT] 热销爆款", "subtitle": "精选畅销好物", "style": 1},
            {"name": "新品上市", "code": "floor_new", "title": "[NEW] 新品速递", "subtitle": "发现最新好物", "style": 2},
            {"name": "精品推荐", "code": "floor_recommend", "title": "[REC] 精选推荐", "subtitle": "编辑推荐好物", "style": 1},
            {"name": "手机数码", "code": "floor_phone", "title": "[PHONE] 手机数码", "subtitle": "科技生活", "style": 3},
            {"name": "家电家居", "code": "floor_home", "title": "[HOME] 家电家居", "subtitle": "品质生活", "style": 2},
            {"name": "美妆护肤", "code": "floor_beauty", "title": "[BEAUTY] 美妆护肤", "subtitle": "焕新肌肤", "style": 1},
        ]

        # 取出各分类前8个商品
        hot_products = [p for p in all_products if p.is_hot][:10]
        new_products = [p for p in all_products if p.is_new][:10]
        rec_products = [p for p in all_products if p.is_recommend][:10]
        phone_products = [p for p in all_products if p.category_id == categories[0].id][:10]
        home_products = [p for p in all_products if p.category_id == categories[1].id][:10]
        beauty_products = [p for p in all_products if p.category_id == categories[3].id][:10]

        product_pools = {
            "floor_hot": hot_products or all_products[:10],
            "floor_new": new_products or all_products[10:20],
            "floor_recommend": rec_products or all_products[20:30],
            "floor_phone": phone_products or all_products[30:40],
            "floor_home": home_products or all_products[40:50],
            "floor_beauty": beauty_products or all_products[50:60],
        }

        for f_def in floor_defs:
            floor = Floor(
                name=f_def["name"],
                code=f_def["code"],
                title=f_def["title"],
                subtitle=f_def["subtitle"],
                style=f_def["style"],
                sort=floor_defs.index(f_def) + 1,
                status=1
            )
            session.add(floor)
            await session.flush()

            pool = product_pools.get(f_def["code"], [])
            for sort_idx, prod in enumerate(pool[:8]):
                fp = FloorProduct(
                    floor_id=floor.id,
                    product_id=prod.id,
                    sort=sort_idx,
                    created_at=datetime.now()
                )
                session.add(fp)
        print(f"[OK] 创建 {len(floor_defs)} 个首页楼层")

        # =============================================
        # 6. 提交
        # =============================================
        await session.commit()
        print("=" * 60)
        print("[OK] 所有数据已提交!")
        print("=" * 60)

        # 打印统计
        print("\n[STAT] 数据统计:")
        print(f"  - 商品分类: {len(categories)} 条")
        print(f"  - 商品(products): {len(all_products)} 条")
        print(f"  - 商品SPU: {len(all_spus)} 条")
        print(f"  - 商品SKU: {len(all_skus)} 条")
        print(f"  - 商品图片: {len(all_images)} 条")
        print(f"  - 用户: {len(users)} 条")
        print(f"  - 首页楼层: {len(floor_defs)} 条")
        print("\n[OK] seed_real_data.py 执行完成!")


if __name__ == "__main__":
    asyncio.run(seed_real_data())
