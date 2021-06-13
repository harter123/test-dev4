<template>
  <div>
    <div>
      <div class="interface-params-dec">
        名称
      </div>
      <el-input v-model="testCase.name" placeholder="name"></el-input>
    </div>
    <div class="interface-params-in-line">
      <el-select v-model="testCase.method" placeholder="请选择">
        <el-option
            label="Get"
            :value="getMethod">
        </el-option>
        <el-option
            label="Post"
            :value="postMethod">
        </el-option>
      </el-select>

      <el-input v-model="testCase.url" placeholder="http://xxx.com"></el-input>
      <el-button type="primary" plain @click="debug">发送</el-button>
    </div>
    <div class="interface-params-in-line">
      <el-radio v-model="testCase.request_type" :label="formType">form-data</el-radio>
      <el-radio v-model="testCase.request_type" :label="jsonType">json</el-radio>
    </div>
    <div class="interface-params-in-line">
      <Editor v-model="testCase.request_body" @init="editorInit" lang="json" theme="chrome"
              height="200"></Editor>
    </div>
    <div>
      <div class="interface-params-dec">
        断言
      </div>
      <Editor v-model="testCase.response_assert" @init="editorInit" lang="json" theme="chrome"
              height="200"></Editor>
    </div>
    <div>
      <div class="interface-params-dec">
        响应
      </div>
      <el-input
          type="textarea"
          :rows="6"
          placeholder="请输入内容"
          v-model="testCase.response">
      </el-input>
    </div>
    <div class="interface-params-save">
      <el-button type="danger" plain @click="editInterface">保存</el-button>
      <el-button type="info" plain @click="cancel">取消</el-button>
    </div>
  </div>
</template>

<script>
import Editor from 'vue2-ace-editor'
import {debugTestCase, updateTestCase} from "@/request/testCase";

export default {
  props: {
    needEditData: {
      type: Object,
    },
    serviceId: {
      type: Number,
    }
  },
  name: "newAndEditInterface",
  components: {
    Editor
  },
  data() {
    return {
      getMethod: 1,
      postMethod: 2,
      formType: 1,
      jsonType: 2,

      testCase: {
        id: 0,
        service_id: 0,
        method: 1,
        url: "",
        name: "",
        request_type: 1,
        request_body: "{}",
        response_assert: "{}",
        response: ""
      }
    }
  },
  methods: {
    editorInit: function () {
      require('brace/ext/language_tools') //language extension prerequsite...
      require('brace/mode/json')
      require('brace/mode/javascript')    //language  这里改为sjon
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') //snippet
    },
    cancel() {
      this.$emit("editInterfaceCancel")
    },
    editInterface() {
      if (undefined === this.serviceId || null === this.serviceId) {
        this.$message.error('请选择模块');
        return
      }
      if ("" === this.testCase.name) {
        this.$message.error('请输入名称');
        return
      }
      if ("" === this.testCase.url) {
        this.$message.error('请输入URL');
        return
      }

      let req = JSON.parse(JSON.stringify(this.testCase)) //复制一个新对象
      req.request_body = JSON.parse(req.request_body)
      req.response_assert = JSON.parse(req.response_assert)
      req.service_id = this.serviceId
      req.id = undefined
      updateTestCase(this.testCase.id, req).then(rsp => {
        let success = rsp.data.success;
        if (true === success) {
          this.$emit("editInterfaceSuccess")
        }
      }).catch(() => {
      })
    },
    debug(){
      if ("" === this.testCase.url) {
        this.$message.error('请输入URL');
        return
      }

      let newCase = JSON.parse(JSON.stringify(this.testCase)) //复制一个新对象
      let req = {}
      req.request_body = JSON.parse(newCase.request_body)
      req.method = newCase.method
      req.url = newCase.url
      req.request_type = newCase.request_type

      debugTestCase(req).then(rsp => {
        let success = rsp.data.success;
        if (true === success) {
          this.testCase.response = rsp.data.data
        }
      }).catch(() => {
      })
    }
  },
  created() {
    this.testCase.id = this.needEditData.id
    this.testCase.service_id = this.needEditData.service_id
    this.testCase.method = this.needEditData.method
    this.testCase.url = this.needEditData.url
    this.testCase.name = this.needEditData.name
    this.testCase.request_type = this.needEditData.request_type
    this.testCase.response_assert = JSON.stringify(this.needEditData.response_assert)
    this.testCase.response = this.needEditData.response
    this.testCase.request_body = JSON.stringify(this.needEditData.request_body)
  }
}
</script>

<style scoped>
.interface-params-dec {
  font-weight: bolder;
  margin-top: 15px;
  margin-bottom: 5px;
}

.interface-params-in-line {
  display: flex;
  margin-top: 10px;
}

.interface-params-save {
  margin-top: 10px;
  margin-bottom: 10px;
  text-align: right;
}
</style>