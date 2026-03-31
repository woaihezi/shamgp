import sqlite3
import datetime

with sqlite3.connect('shop_db.db') as conn:
    # 插入角色
    roles = [
        ('超级管理员', 'superadmin', '系统超级管理员，拥有所有权限', 1),
        ('运营管理员', 'admin', '运营管理员，可管理商品/订单/用户', 2),
        ('客服', 'customer_service', '客服人员，仅查看和处理工单', 3),
        ('普通用户', 'user', '普通注册用户', 4),
    ]
    for name, code, desc, sort in roles:
        conn.execute(
            "INSERT OR IGNORE INTO role (name, code, description, sort, is_deleted, created_at, updated_at) VALUES (?, ?, ?, ?, 0, ?, ?)",
            (name, code, desc, sort, datetime.datetime.now(), datetime.datetime.now())
        )

    # 插入权限
    perms = [
        ('查看权限', 'permission:read', 'api', 1),
        ('创建权限', 'permission:create', 'api', 2),
        ('更新权限', 'permission:update', 'api', 3),
        ('删除权限', 'permission:delete', 'api', 4),
        ('查看角色', 'role:read', 'api', 10),
        ('创建角色', 'role:create', 'api', 11),
        ('更新角色', 'role:update', 'api', 12),
        ('删除角色', 'role:delete', 'api', 13),
        ('分配角色', 'role:assign', 'api', 14),
        ('查看订单', 'order:read', 'api', 20),
        ('管理订单', 'order:manage', 'api', 21),
        ('查看商品', 'product:read', 'api', 30),
        ('管理商品', 'product:manage', 'api', 31),
    ]
    for name, code, typ, sort in perms:
        conn.execute(
            "INSERT OR IGNORE INTO permission (name, code, type, sort, is_deleted, created_at, updated_at) VALUES (?, ?, ?, ?, 0, ?, ?)",
            (name, code, typ, sort, datetime.datetime.now(), datetime.datetime.now())
        )

    # 超级管理员赋所有权限
    cursor = conn.execute("SELECT id FROM role WHERE code='superadmin'")
    superadmin = cursor.fetchone()
    if superadmin:
        superadmin_id = superadmin[0]
        cursor = conn.execute("SELECT id FROM permission")
        perm_ids = [r[0] for r in cursor.fetchall()]
        for pid in perm_ids:
            conn.execute(
                "INSERT OR IGNORE INTO role_permission (role_id, permission_id) VALUES (?, ?)",
                (superadmin_id, pid)
            )

    # 运营管理员赋订单+商品权限
    cursor = conn.execute("SELECT id FROM role WHERE code='admin'")
    admin = cursor.fetchone()
    if admin:
        admin_id = admin[0]
        cursor = conn.execute("SELECT id FROM permission WHERE code IN ('order:read','order:manage','product:read','product:manage')")
        perm_ids = [r[0] for r in cursor.fetchall()]
        for pid in perm_ids:
            conn.execute(
                "INSERT OR IGNORE INTO role_permission (role_id, permission_id) VALUES (?, ?)",
                (admin_id, pid)
            )

    conn.commit()
    print("Seed completed")

    # 验证
    cursor = conn.execute("SELECT COUNT(*) FROM role")
    print(f"Roles: {cursor.fetchone()[0]}")
    cursor = conn.execute("SELECT COUNT(*) FROM permission")
    print(f"Permissions: {cursor.fetchone()[0]}")
    cursor = conn.execute("SELECT COUNT(*) FROM role_permission")
    print(f"Role-Permission mappings: {cursor.fetchone()[0]}")
