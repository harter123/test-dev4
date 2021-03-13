<template>
  <div style="height: 100%">
    <div :style="backgroundDiv" class="homeMain">
      <div style="margin: 120px 0 0 50px">
        <div style="
        color: white;
        font-size: 1rem;
        font-weight: 400;
        line-height: 1.7;"
        >JOIN THE CHANGE</div>
        <div style="font-size: 3.5rem;font-weight: 400;
    line-height: 1.2; color: white;">
          <div>Space service</div>
          <div>that moves</div>
          <div>work forward</div>
        </div>
      </div>
      <div class="loginForm">
<h2>
  itest platform
</h2>
        <div>
          <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="5px" class="demo-ruleForm">
            <el-form-item label="" prop="name">
              <el-input v-model="ruleForm.name" placeholder="Enter your username"></el-input>
            </el-form-item>
            <el-form-item label="" prop="psw">
              <el-input show-password v-model="ruleForm.psw" placeholder="Enter your password"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="success" style="width: 100%">Get Stared</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
    <div class="homeFoot">
      <div class="homeFootText">
        All rights reserved. ©重定向科技. 2021 itest.info
      </div>
    </div>
  </div>

</template>

<script>
// @ is an alias to /src
export default {
  name: 'Home',
  data(){
    return {
      classTest: 'test',
      backgroundDiv: {
        backgroundImage: 'url(' + require('../assets/img4.jpg') + ')',
      },
      ruleForm: {
        name: '',
        psw: '',
      },
      rules: {
        name: [
          { required: true, message: 'Enter your username', trigger: 'blur' },
        ],
        psw: [
          { required: true, message: 'Enter your password', trigger: 'blur' },
        ],
      }
    }
  },
  components: {
  }
}
</script>

<style>

.homeMain {
  width: 100%;
  height: 85%;
  background-size: 100% auto;
  display: flex;
  justify-content: space-between;
}

.homeMain .el-input__inner{
  height: 50px;
}
.homeMain button{
  padding: 15px 20px;
}
.homeFoot{
  height: 15%;
  background: #151b26;
  display: flex;
  align-items: center;
  justify-content: center;
}

.homeFootText {
  color: #8c98a4 !important;
}

.loginForm {
  width: 300px;
  background: white;
  border-radius: 5px;
  height: 270px;
  margin: 70px 60px 0 0;
  padding: 20px 30px;
}
</style>