import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import { useUserStore } from '@/stores/user'
import { getToken } from '@/utils/auth'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(ElementPlus)

// 路由守卫
const whiteList = ['/login']
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  const hasToken = getToken()
  
  if (hasToken) {
    if (to.path === '/login') {
      next({ path: '/' })
    } else {
      if (!userStore.name) {
        try {
          await userStore.getInfo()
        } catch (error) {
          await userStore.resetUser()
          next(`/login?redirect=${to.path}`)
          return
        }
      }
      next()
    }
  } else {
    if (whiteList.indexOf(to.path) !== -1) {
      next()
    } else {
      next(`/login?redirect=${to.path}`)
    }
  }
})

app.mount('#app')
