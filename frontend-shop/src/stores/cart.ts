import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { cartApi, type CartItem as ApiCartItem } from "../api/cart";

export interface CartItem {
  id: number;
  productId: number;
  name: string;
  price: number;
  quantity: number;
  image?: string;
}

export const useCartStore = defineStore("cart", () => {
  const items = ref<CartItem[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const totalPrice = computed(() => {
    return items.value.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0,
    );
  });

  const totalCount = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantity, 0);
  });

  async function loadCart() {
    loading.value = true;
    error.value = null;
    try {
      const response = await cartApi.getItems();
      items.value = response.data.map((item: ApiCartItem) => ({
        id: item.id,
        productId: item.product_id,
        name: item.product_name || "",
        price: item.product_price || 0,
        quantity: item.quantity,
        image: item.product_image,
      }));
    } catch (err) {
      console.error("Failed to load cart:", err);
      error.value = "Failed to load cart";
    } finally {
      loading.value = false;
    }
  }

  async function addItem(
    product: { id: number; name: string; price: number; image?: string },
    quantity: number = 1,
  ) {
    loading.value = true;
    error.value = null;
    try {
      await cartApi.addItem({
        product_id: product.id,
        quantity,
      });
      await loadCart();
    } catch (err) {
      console.error("Failed to add item to cart:", err);
      error.value = "Failed to add item to cart";
    } finally {
      loading.value = false;
    }
  }

  async function updateQuantity(productId: number, quantity: number) {
    loading.value = true;
    error.value = null;
    try {
      const cartItem = items.value.find((item) => item.productId === productId);
      if (cartItem) {
        if (quantity <= 0) {
          await removeItem(productId);
        } else {
          await cartApi.updateItem(cartItem.id, {
            quantity,
          });
          await loadCart();
        }
      }
    } catch (err) {
      console.error("Failed to update item quantity:", err);
      error.value = "Failed to update item quantity";
    } finally {
      loading.value = false;
    }
  }

  async function removeItem(productId: number) {
    loading.value = true;
    error.value = null;
    try {
      const cartItem = items.value.find((item) => item.productId === productId);
      if (cartItem) {
        await cartApi.removeItem(cartItem.id);
        await loadCart();
      }
    } catch (err) {
      console.error("Failed to remove item from cart:", err);
      error.value = "Failed to remove item from cart";
    } finally {
      loading.value = false;
    }
  }

  async function clearCart() {
    loading.value = true;
    error.value = null;
    try {
      await cartApi.clearCart();
      items.value = [];
    } catch (err) {
      console.error("Failed to clear cart:", err);
      error.value = "Failed to clear cart";
    } finally {
      loading.value = false;
    }
  }

  return {
    items,
    totalPrice,
    totalCount,
    loading,
    error,
    loadCart,
    addItem,
    updateQuantity,
    removeItem,
    clearCart,
  };
});
