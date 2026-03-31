-- ========================================
-- RBAC 权限初始化脚本
-- shamgp RBAC 迁移
-- ========================================

-- 角色表（已存在，此处补充初始数据）
INSERT INTO role (name, code, description, sort, is_deleted, created_at, updated_at)
SELECT '超级管理员', 'superadmin', '系统超级管理员，拥有所有权限', 1, FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM role WHERE code = 'superadmin');

INSERT INTO role (name, code, description, sort, is_deleted, created_at, updated_at)
SELECT '运营管理员', 'admin', '运营管理员，可管理商品/订单/用户', 2, FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM role WHERE code = 'admin');

INSERT INTO role (name, code, description, sort, is_deleted, created_at, updated_at)
SELECT '客服', 'customer_service', '客服人员，仅查看和处理工单', 3, FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM role WHERE code = 'customer_service');

INSERT INTO role (name, code, description, sort, is_deleted, created_at, updated_at)
SELECT '普通用户', 'user', '普通注册用户', 4, FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM role WHERE code = 'user');

-- 权限表（已存在，此处补充初始数据）
-- API 权限
INSERT INTO permission (name, code, type, path, method, parent_id, sort, description, is_deleted, created_at, updated_at)
SELECT '查看权限', 'permission:read', 'api', '/api/v1/roles/permissions', 'GET', 0, 1, '查看权限列表', FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'permission:read');

INSERT INTO permission (name, code, type, path, method, parent_id, sort, description, is_deleted, created_at, updated_at)
SELECT '创建权限', 'permission:create', 'api', '/api/v1/roles/permissions', 'POST', 0, 2, '创建新权限', FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'permission:create');

INSERT INTO permission (name, code, type, path, method, parent_id, sort, description, is_deleted, created_at, updated_at)
SELECT '更新权限', 'permission:update', 'api', '/api/v1/roles/permissions/{id}', 'PUT', 0, 3, '更新权限', FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'permission:update');

INSERT INTO permission (name, code, type, path, method, parent_id, sort, description, is_deleted, created_at, updated_at)
SELECT '删除权限', 'permission:delete', 'api', '/api/v1/roles/permissions/{id}', 'DELETE', 0, 4, '删除权限', FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'permission:delete');

-- 角色权限
INSERT INTO permission (name, code, type, path, method, parent_id, sort, description, is_deleted, created_at, updated_at)
SELECT '查看角色', 'role:read', 'api', '/api/v1/roles/roles', 'GET', 0, 10, '查看角色列表', FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role:read');

INSERT INTO permission (name, code, type, path, method, parent_id, sort, description, is_deleted, created_at, updated_at)
SELECT '创建角色', 'role:create', 'api', '/api/v1/roles/roles', 'POST', 0, 11, '创建新角色', FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role:create');

INSERT INTO permission (name, code, type, path, method, parent_id, sort, description, is_deleted, created_at, updated_at)
SELECT '更新角色', 'role:update', 'api', '/api/v1/roles/roles/{id}', 'PUT', 0, 12, '更新角色', FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role:update');

INSERT INTO permission (name, code, type, path, method, parent_id, sort, description, is_deleted, created_at, updated_at)
SELECT '删除角色', 'role:delete', 'api', '/api/v1/roles/roles/{id}', 'DELETE', 0, 13, '删除角色', FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role:delete');

INSERT INTO permission (name, code, type, path, method, parent_id, sort, description, is_deleted, created_at, updated_at)
SELECT '分配角色', 'role:assign', 'api', '/api/v1/roles/users/{id}/roles', 'POST', 0, 14, '为用户分配角色', FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role:assign');

-- 订单权限
INSERT INTO permission (name, code, type, path, method, parent_id, sort, description, is_deleted, created_at, updated_at)
SELECT '查看订单', 'order:read', 'api', '/api/v1/orders', 'GET', 0, 20, '查看订单', FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'order:read');

INSERT INTO permission (name, code, type, path, method, parent_id, sort, description, is_deleted, created_at, updated_at)
SELECT '管理订单', 'order:manage', 'api', '/api/v1/orders/{id}/status', 'PUT', 0, 21, '更新订单状态/发货/取消', FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'order:manage');

-- 商品权限
INSERT INTO permission (name, code, type, path, method, parent_id, sort, description, is_deleted, created_at, updated_at)
SELECT '查看商品', 'product:read', 'api', '/api/v1/products', 'GET', 0, 30, '查看商品列表', FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'product:read');

INSERT INTO permission (name, code, type, path, method, parent_id, sort, description, is_deleted, created_at, updated_at)
SELECT '管理商品', 'product:manage', 'api', '/api/v1/products', 'POST', 0, 31, '创建/编辑/删除商品', FALSE, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'product:manage');

-- 超级管理员赋所有权限
INSERT INTO role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM role r, permission p
WHERE r.code = 'superadmin'
AND NOT EXISTS (
    SELECT 1 FROM role_permission rp
    WHERE rp.role_id = r.id AND rp.permission_id = p.id
);

-- 运营管理员赋订单+商品权限
INSERT INTO role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM role r, permission p
WHERE r.code = 'admin'
AND p.code IN ('order:read', 'order:manage', 'product:read', 'product:manage')
AND NOT EXISTS (
    SELECT 1 FROM role_permission rp
    WHERE rp.role_id = r.id AND rp.permission_id = p.id
);

-- 客服仅查看订单
INSERT INTO role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM role r, permission p
WHERE r.code = 'customer_service'
AND p.code IN ('order:read')
AND NOT EXISTS (
    SELECT 1 FROM role_permission rp
    WHERE rp.role_id = r.id AND rp.permission_id = p.id
);
