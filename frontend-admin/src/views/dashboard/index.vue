<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <el-statistic title="用户数" :value="1234" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <el-statistic title="订单数" :value="5678" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <el-statistic title="商品数" :value="901" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <el-statistic title="销售额" prefix="¥" :value="123456" />
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>欢迎使用 SHAMGP 管理后台</span>
            </div>
          </template>
          <div class="welcome-content">
            <p>您已成功登录，这是一个功能完整的 RBAC 权限系统</p>
            <p>主要功能包括：</p>
            <ul>
              <li>用户管理</li>
              <li>角色管理</li>
              <li>菜单管理</li>
              <li>动态路由</li>
            </ul>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.dashboard-container {
  padding: 0;
}

.stat-card {
  text-align: center;
}

.card-header {
  font-weight: bold;
}

.welcome-content {
  font-size: 14px;
  color: #606266;
}

.welcome-content ul {
  margin-left: 20px;
}
</style>
