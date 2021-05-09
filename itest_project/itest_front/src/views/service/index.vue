<template>
  <div>
    <el-button type="primary" plain @click="openAddServiceDialog">创建模块</el-button>
    <el-table
        :data="serviceList"
        :header-cell-style="{'color': '#555555'}"
        stripe
        style="width: 100%">
      <el-table-column
          prop="name"
          label="名称"
          min-width="30%">
      </el-table-column>
      <el-table-column
          prop="description"
          label="描述"
          min-width="50%">
      </el-table-column>
      <el-table-column
          prop="ops"
          min-width="20%"
          label="操作">
        <template slot-scope="scope">
          <el-button @click="deleteService(scope.row)" type="text" size="small">删除</el-button>
          <el-button @click="openEditServiceDialog(scope.row)" type="text" size="small">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="创建模块" :visible.sync="addServiceDialogVisible">
      <el-form :model="addServiceForm" :rules="addServiceRule" ref="addServiceForm">
        <el-form-item label="名称" label-width="50px"  prop="name">
          <el-input v-model="addServiceForm.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="描述" label-width="50px" prop="description">
          <el-input type="textarea"
                    :rows="2"
                    v-model="addServiceForm.description" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addServiceDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addServiceConfirm">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog title="编辑模块" :visible.sync="editServiceDialogVisible">
      <el-form :model="editServiceForm" :rules="editServiceRule" ref="editServiceForm">
        <el-form-item label="名称" label-width="50px"  prop="name">
          <el-input v-model="editServiceForm.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="描述" label-width="50px" prop="description">
          <el-input type="textarea"
                    :rows="2"
                    v-model="editServiceForm.description" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="editServiceDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editServiceConfirm">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {createService, deleteService, getServiceList, updateService} from "@/request/service";

export default {
  props: {
    projectId: {
      type: String
    }
  },
  name: "index",
  data(){
    return {
      serviceList: [],
      addServiceDialogVisible: false,
      addServiceForm: {
        name: "",
        description: ""
      },
      addServiceRule: {
        name: [
          { required: true, message: '请输入模块名称', trigger: 'blur' },
          { min: 1, max: 255, message: '长度在 1 到 255 个字符', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入模块描述', trigger: 'blur' },
        ],
      },
      editServiceDialogVisible: false,
      editServiceForm: {
        id: 0,
        name: "",
        description: "",
      },
      editServiceRule: {
        name: [
          { required: true, message: '请输入项目名称', trigger: 'blur' },
          { min: 1, max: 255, message: '长度在 1 到 255 个字符', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入项目描述', trigger: 'blur' },
        ],
      }
    }
  },
  components: {
  },
  methods:{
    getAllServices(){
      getServiceList(this.projectId).then(rsp=>{
        let success = rsp.data.success;
        if(true===success){
          this.serviceList = rsp.data.data;
        }
      }).catch(()=>{
      })
    },
    deleteService(data){
      this.$confirm('此操作将永久删除该项目, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteService(data.id).then(rsp=>{
          let success = rsp.data.success;
          if(true===success){
            this.getAllServices()
          }
        }).catch(()=>{
        })
      }).catch(() => {
      });
    },
    openAddServiceDialog(){
      this.addServiceDialogVisible = true
      this.addServiceForm.name = ""
      this.addServiceForm.description = ""
    },
    addServiceConfirm(){
      this.$refs.addServiceForm.validate((valid) => {
        if (valid) {
          let req = {
            "name": this.addServiceForm.name,
            "description": this.addServiceForm.description,
            "project_id": Number(this.projectId),
          }
          createService(req).then(rsp=>{
            let success = rsp.data.success;
            if(true===success){
              this.addServiceDialogVisible = false
              this.getAllServices()
            }
          }).catch(()=>{
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    openEditServiceDialog(data){
      this.editServiceDialogVisible = true
      this.editServiceForm.id = data.id
      this.editServiceForm.name = data.name
      this.editServiceForm.description = data.description
    },
    editServiceConfirm(){
      this.$refs.editServiceForm.validate((valid) => {
        if (valid) {
          let req = {
            "name": this.editServiceForm.name,
            "description": this.editServiceForm.description,
            "project_id": Number(this.projectId),
          }
          updateService(this.editServiceForm.id, req).then(rsp=>{
            let success = rsp.data.success;
            if(true===success){
              this.editServiceDialogVisible = false
              this.getAllServices()
            }
          }).catch(()=>{
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    }
  },
  created() {
    this.getAllServices()
  }
}
</script>

<style scoped>

</style>