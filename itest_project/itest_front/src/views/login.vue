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
          <el-form :model="ruleForm" :rules="rules" ref="ruleFormRef" label-width="5px" class="demo-ruleForm">
            <el-form-item label="" prop="name">
              <el-input v-model="ruleForm.name" placeholder="Enter your username"></el-input>
            </el-form-item>
            <el-form-item label="" prop="psw">
              <el-input show-password v-model="ruleForm.psw" placeholder="Enter your password"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="success" style="width: 100%" @click="submitForm">Get Started</el-button>
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
import {login} from "../request/user"
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
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        psw: [
          { required: true, message: 'Enter your password', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
      }
    }
  },
  components: {
  },
  methods:{
    submitForm() {
      this.$refs.ruleFormRef.validate((valid) => {
        if (valid) {
          login(this.ruleForm.name, this.ruleForm.psw).then(data=>{
            let success = data.data.success
            if(true === success){
              this.$router.push('/');
            }else{
              this.$message.error('登录失败：'+ data.data.error.message);
            }
          }).catch(()=>{
            this.$message.error('请求失败');
          })

        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
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