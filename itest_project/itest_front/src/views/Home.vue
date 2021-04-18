<template>
  <div style="height: 100%" class="home-main">
    <div class="home-main-left">
      <div>
        <img :src="itestPng" class="home-main-left-image"/>
      </div>
      <div>
        <div class="home-color home-main-left-menu-type">
          测试接口
        </div>
        <div id="home-main-menu">
          <el-menu
              default-active="1"
              background-color="#354052"
              text-color="#fff"
              class="el-menu-vertical-demo">
            <el-menu-item index="1">
              <i class="el-icon-menu"></i>
              <span slot="title">模块管理</span>
            </el-menu-item>
            <el-menu-item index="2">
              <i class="el-icon-document"></i>
              <span slot="title">用例管理</span>
            </el-menu-item>
            <el-menu-item index="3">
              <i class="el-icon-setting"></i>
              <span slot="title">任务管理</span>
            </el-menu-item>
          </el-menu>
        </div>
      </div>

      <div>
        <div class="home-color home-main-left-menu-type">
          测试工具
        </div>
      </div>
    </div>

    <div class="home-main-right">
      <div class="home-main-right-menu">
        <div class="home-main-right-menu-title">
          模块
        </div>
        <div class="home-main-right-menu-user">
          <el-dropdown trigger="click">
            <span class="el-dropdown-link" style="font-size: 18px">
              {{ user.name }}<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item icon="el-icon-user">Logout</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </div>
      <div class="home-main-right-context">
context
      </div>
      <div class="home-main-right-foot">
        2021 © 重定向科技 - itest.info
      </div>
    </div>
  </div>

</template>

<script>
// @ is an alias to /src
import {getLoginUserInfo} from "../request/user";
import itest from "../assets/itest.png"

export default {
  name: 'Home',
  data(){
    return {
      itestPng: itest,
      user: {}
    }
  },
  components: {
  },
  methods:{
    getUserInfo(){
      getLoginUserInfo().then(rsp=>{
        let success = rsp.data.success;
        this.user = rsp.data.data;
        if(false===success){
          this.$router.push('/login');
        }
      }).catch(()=>{
        this.$router.push('/login');
      })
    }
  },
  created() {
    this.getUserInfo()
  }
}
</script>

<style>
.home-main{
  display: flex;
  justify-content: normal;
}

/*这里代表固定宽度260px,宽度不会自动延伸，但是高度自动延伸*/
.home-main-left {
  flex: 0 1 260px;
  background: #354052
}
/*这里代表自动宽度，宽度自动延伸，高度自动延伸*/
.home-main-right {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
}

.home-main-left-image {
  width: 85px;
  margin: 20px auto;
}

.home-color {
  color: #cedce4;
}

.home-main-left-menu-type {
  font-size: 12px;
  text-align: left;
  margin-left: 30px;
}

#home-main-menu .el-menu-item {
  text-align: left;
}

#home-main-menu i {
  margin-left: 10px;
}

.home-main-right-menu {
  display: flex;
  height: 50px;
  width: 100%;
}

.home-main-right-menu-title {
  flex: 1 1 auto;
  text-align: left;
}
.home-main-right-menu-user {
  flex: 0 1 100px;
  padding: 10px 5px 5px 5px;
  background-color: #fafbfd;
}

.home-main-right-foot {
  height: 35px;
  text-align: left;
  padding-left: 40px;
  color: #98a6ad;
  padding-top: 15px;
  border-top: 1px solid rgba(152,166,173,.2);
}
.home-main-right-context {
  width: 100%;
  flex: 1 1 auto;
}
</style>