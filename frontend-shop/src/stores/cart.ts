import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface CartItem {
  id: number
  productId: number
  name: string
  price: number
  quantity: number
  image?: string
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])

  const totalPrice = computed(() => {
    return items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
  })

  const totalCount = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantity, 0)
  })

  function addItem(product: { id: number; name: string; price: number; image?: string }, quantity: number = 1) {
    const existingItem = items.value.find(item => item.productId === product.id)
    if (existingItem) {
      existingItem.quantity += quantity
    } else {
      items.value.push({
        id: Date.now(),
        productId: product.id,
        name: product.name,
        price: product.price,
        quantity,
        image: product.image
      })
    }
    saveToStorage()
  }

  function updateQuantity(productId: number, quantity: number) {
    const item = items.value.find(item => item.productId === productId)
    if (item) {
      if (quantity <= 0) {
        removeItem(productId)
      } else {
        item.quantity = quantity
        saveToStorage()
      }
    }
  }

  function removeItem(productId: number) {
    const index = items.value.findIndex(item => item.productId === productId)
    if (index > -1) {
      items.value.splice(index, 1)
      saveToStorage()
    }
  }

  function clearCart() {
    items.value = []
    saveToStorage()
  }

  function saveToStorage() {
    localStorage.setItem('cart', JSON.stringify(items.value))
  }

  function loadFromStorage() {
    const saved = localStorage.getItem('cart')
    if (saved) {
      try {
        items.value = JSON.parse(saved)
      } catch (e) {
        console.error('Failed to parse cart from storage:', e)
      }
    }
  }

  return {
    items,
    totalPrice,
    totalCount,
    addItem,
    updateQuantity,
    removeItem,
    clearCart,
    loadFromStorage
  }
})
