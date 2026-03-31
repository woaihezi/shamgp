# JWT Auth Fix Summary

## `app/api/v1/orders.py`

**Status:** No changes needed — already uses `current_user: User = Depends(get_current_active_user)` on all non-admin endpoints.

Functions that were already correct (no `user_id: int = 1` found):
- `get_addresses` ✅
- `get_default_address` ✅
- `create_address` ✅
- `update_address` ✅
- `delete_address` ✅
- `create_order` ✅
- `get_orders` ✅
- `get_order` ✅
- `update_order_status` ✅
- `cancel_order` ✅
- `create_refund` ✅
- `get_refunds` ✅
- `get_refund` ✅

Admin endpoints (no auth, as expected):
- `admin_get_orders` — public (admin only)
- `admin_get_order` — public (admin only)
- `admin_update_order_status` — public (admin only)

---

## `app/api/v1/carts.py`

**Status:** All 6 endpoints updated from `user_id: int = 1` to `current_user: User = Depends(get_current_active_user)`.

| Function | Change |
|---|---|
| `get_cart_summary` | `user_id: int = 1` → `current_user: User = Depends(get_current_active_user)`; `user_id` → `current_user.id` in body |
| `get_cart_items` | `user_id: int = 1` → `current_user: User = Depends(get_current_active_user)`; `user_id` → `current_user.id` in body |
| `add_cart_item` | `user_id: int = 1` → `current_user: User = Depends(get_current_active_user)`; `user_id` → `current_user.id` in body |
| `update_cart_item` | `user_id: int = 1` → `current_user: User = Depends(get_current_active_user)`; `user_id` → `current_user.id` in body |
| `remove_cart_item` | `user_id: int = 1` → `current_user: User = Depends(get_current_active_user)`; `user_id` → `current_user.id` in body |
| `clear_cart` | `user_id: int = 1` → `current_user: User = Depends(get_current_active_user)`; `user_id` → `current_user.id` in body |

**Imports added to carts.py:**
```python
from ...api.deps import get_current_active_user
from ...models.user import User
```

**Syntax verification:** `py -m py_compile` passes for both files.
