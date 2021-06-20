<template>
  <div>
    <el-button type="primary" plain @click="openAddTaskDialog">创建任务</el-button>
    <el-table
        :data="taskList"
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
          min-width="45%">
      </el-table-column>
      <el-table-column
          prop="ops"
          min-width="25%"
          label="操作">
        <template slot-scope="scope">
          <el-button @click="deleteTask(scope.row)" type="text" size="small">删除</el-button>
          <el-button @click="openEditTaskDialog(scope.row)" type="text" size="small">编辑</el-button>
          <el-button @click="openTaskTestCaseDialog(scope.row)" type="text" size="small">用例管理</el-button>
          <el-button @click="openTaskTestRunDialog(scope.row)" type="text" size="small">执行管理</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="创建任务" :visible.sync="addTaskDialogVisible">
      <el-form :model="addTaskForm" :rules="addTaskRule" ref="addTaskForm">
        <el-form-item label="名称" label-width="50px"  prop="name">
          <el-input v-model="addTaskForm.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="描述" label-width="50px" prop="description">
          <el-input type="textarea"
                    :rows="2"
                    v-model="addTaskForm.description" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addTaskDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addTaskConfirm">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog title="编辑任务" :visible.sync="editTaskDialogVisible">
      <el-form :model="editTaskForm" :rules="editTaskRule" ref="editTaskForm">
        <el-form-item label="名称" label-width="50px"  prop="name">
          <el-input v-model="editTaskForm.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="描述" label-width="50px" prop="description">
          <el-input type="textarea"
                    :rows="2"
                    v-model="editTaskForm.description" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="editTaskDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editTaskConfirm">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog title="用例管理" :visible.sync="taskTestCaseDialogVisible" width="80%" style="margin-top: -50px">
      <div style="height: 500px;overflow-y: auto">
        <el-button type="primary" plain @click="selectTaskTestCaseDialogVisible=true">添加用例</el-button>
        <el-table
            :data="testCaseList"
            :header-cell-style="{'color': '#555555'}"
            stripe
            style="width: 100%">
          <el-table-column
              prop="name"
              label="名称"
              min-width="20%">
          </el-table-column>
          <el-table-column
              prop="url"
              label="URL"
              min-width="35%">
          </el-table-column>
          <el-table-column
              prop="method"
              label="方法"
              min-width="10%">
            <template slot-scope="scope">
              <span>{{ 1 === scope.row.method ? "Get" : "Post" }}</span>
            </template>
          </el-table-column>
          <el-table-column
              prop="create_time"
              label="创建时间"
              min-width="20%">
          </el-table-column>
          <el-table-column
              prop="ops"
              min-width="10%"
              label="操作">
            <template slot-scope="scope">
              <el-button @click="removeTaskTestCase(scope.row)" type="text" size="small">移除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>

    <el-dialog title="选择用例" :visible.sync="selectTaskTestCaseDialogVisible" width="70%" style="margin-top: -50px">
     <div style="height: 500px;overflow-y: auto">
       <selectTestCase :project-id="projectId" @success="addTaskTestCaseFun" @cancel="selectTaskTestCaseDialogVisible=false"></selectTestCase>
     </div>
    </el-dialog>

    <el-dialog title="执行管理" :visible.sync="taskRunDialogVisible" width="50%" style="margin-top: -50px">
      <div style="height: 500px;overflow-y: auto">
        <el-button type="primary" plain @click="runTaskFun">单次执行</el-button>
        <el-button type="primary" plain @click="taskIntervalRunDialogVisible=true">循环执行</el-button>
        <el-button type="info" plain @click="stopIntervalRunTask">停止循环执行</el-button>
        <div v-if="taskIntervalRunDialogVisible" style="margin: 5px 0 5px 0">
          <span>天</span>
          <el-input-number size="mini"
                           :min="0"
                           v-model="currentTask.days"
                           style="margin-right: 15px"></el-input-number>
          <span>时</span>
          <el-input-number size="mini"
                           :min="0"
                           v-model="currentTask.hours"
                           style="margin-right: 15px"></el-input-number>
          <span>分</span>
          <el-input-number size="mini"
                           :min="0"
                           v-model="currentTask.minutes"></el-input-number>
          <el-date-picker
              style="margin: 5px 0"
              size="mini"
              v-model="currentTask.start_time"
              type="datetime"
              value-format="yyyy-MM-dd HH:mm:ss"
              placeholder="选择开始时间">
          </el-date-picker>
          <br/>
          <el-button size="small" type="danger" plain @click="openIntervalRun">保存</el-button>
          <el-button size="small" type="info" plain @click="taskIntervalRunDialogVisible=false">取消</el-button>
        </div>
        <div v-if="currentTask && currentTask.interval_switch">
          你已开启循环执行：天 {{currentTask.days}}  时 {{currentTask.hours}}  分 {{currentTask.minutes}}，开始时间： {{currentTask.start_time}}
        </div>
        <el-table
            :data="taskReportList"
            :header-cell-style="{'color': '#555555'}"
            stripe
            style="width: 100%">
          <el-table-column
              prop="name"
              label="名称"
              min-width="100%">
            <template slot-scope="scope">
              <a href="javascript:void(0)" @click="openReportDetail(scope.row)">{{scope.row.name}}</a>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { Loading } from 'element-ui';
import {
  addTaskTestCase,
  createTask,
  deleteTask,
  deleteTaskTestCase,
  getTaskList, getTaskReports,
  getTaskTestCaseList, runIntervalTask, runTask, stopIntervalTask,
  updateTask
} from "@/request/task";
import selectTestCase from "@/views/task/selectTestCase";
export default {
  props: {
    projectId: {
      type: String
    }
  },
  name: "index",
  data(){
    return {
      taskList: [],
      addTaskDialogVisible: false,
      addTaskForm: {
        name: "",
        description: ""
      },
      addTaskRule: {
        name: [
          { required: true, message: '请输入任务名称', trigger: 'blur' },
          { min: 1, max: 255, message: '长度在 1 到 255 个字符', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入任务描述', trigger: 'blur' },
        ],
      },
      editTaskDialogVisible: false,
      editTaskForm: {
        id: 0,
        name: "",
        description: "",
      },
      editTaskRule: {
        name: [
          { required: true, message: '请输入项目名称', trigger: 'blur' },
          { min: 1, max: 255, message: '长度在 1 到 255 个字符', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入项目描述', trigger: 'blur' },
        ],
      },
      taskTestCaseDialogVisible: false,
      testCaseList:[],
      currentTask: undefined,
      selectTaskTestCaseDialogVisible: false,
      taskRunDialogVisible: false,
      taskReportList: [],
      taskIntervalRunDialogVisible: false,
    }
  },
  components: {
    selectTestCase
  },
  methods:{
    getAllTasks(){
      getTaskList(this.projectId).then(rsp=>{
        let success = rsp.data.success;
        if(true===success){
          this.taskList = rsp.data.data;
        }
      }).catch(()=>{
      })
    },
    deleteTask(data){
      this.$confirm('此操作将永久删除该项目, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteTask(data.id).then(rsp=>{
          let success = rsp.data.success;
          if(true===success){
            this.getAllTasks()
          }
        }).catch(()=>{
        })
      }).catch(() => {
      });
    },
    openAddTaskDialog(){
      this.addTaskDialogVisible = true
      this.addTaskForm.name = ""
      this.addTaskForm.description = ""
    },
    addTaskConfirm(){
      this.$refs.addTaskForm.validate((valid) => {
        if (valid) {
          let req = {
            "name": this.addTaskForm.name,
            "description": this.addTaskForm.description,
            "project_id": Number(this.projectId),
          }
          createTask(req).then(rsp=>{
            let success = rsp.data.success;
            if(true===success){
              this.addTaskDialogVisible = false
              this.getAllTasks()
            }
          }).catch(()=>{
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    openEditTaskDialog(data){
      this.editTaskDialogVisible = true
      this.editTaskForm.id = data.id
      this.editTaskForm.name = data.name
      this.editTaskForm.description = data.description
    },
    editTaskConfirm(){
      this.$refs.editTaskForm.validate((valid) => {
        if (valid) {
          let req = {
            "name": this.editTaskForm.name,
            "description": this.editTaskForm.description,
            "project_id": Number(this.projectId),
          }
          updateTask(this.editTaskForm.id, req).then(rsp=>{
            let success = rsp.data.success;
            if(true===success){
              this.editTaskDialogVisible = false
              this.getAllTasks()
            }
          }).catch(()=>{
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    openTaskTestCaseDialog(task){
      this.currentTask = task;
      this.taskTestCaseDialogVisible = true;
      this.getTaskTestCaseListFun(task.id)
    },
    openTaskTestRunDialog(task){
      this.currentTask = task;
      this.taskRunDialogVisible = true;
      this.getTaskReportList(task.id)
    },
    getTaskTestCaseListFun(taskId){
      getTaskTestCaseList(taskId).then(rsp=>{
        let success = rsp.data.success;
        if(true===success){
          this.testCaseList = rsp.data.data
        }
      }).catch(()=>{
      })
    },
    removeTaskTestCase(data){
      console.log(data)
      deleteTaskTestCase(this.currentTask.id, data.task_test_case_id).then(rsp=>{
        let success = rsp.data.success;
        if(true===success){
          this.getTaskTestCaseListFun(this.currentTask.id)
        }
      }).catch(()=>{
      })
    },
    addTaskTestCaseFun(data){
      let testCaseIds = []
      for(let i=0;i<data.length;i++){
        testCaseIds.push(data[i].id)
      }
      if(0 === testCaseIds.length){
        return
      }

      addTaskTestCase(this.currentTask.id, {"test_case_ids": testCaseIds}).then(rsp=>{
        let success = rsp.data.success;
        if(true===success){
          this.getTaskTestCaseListFun(this.currentTask.id)
          this.selectTaskTestCaseDialogVisible = false
        }
      }).catch(()=>{
      })
    },
    runTaskFun(){
      let loadingInstance1 = Loading.service({ fullscreen: true });
      runTask(this.currentTask.id,).then(rsp=>{
        let success = rsp.data.success;
        if(true===success){
          this.getTaskReportList(this.currentTask.id)
        }
        loadingInstance1.close()
      }).catch(()=>{
      })
    },
    getTaskReportList(taskId){
      getTaskReports(taskId).then(rsp=>{
        let success = rsp.data.success;
        if(true===success){
          this.taskReportList = rsp.data.data
        }
      }).catch(()=>{
      })
    },
    openReportDetail(report){
      window.open(`http://localhost/backend/task/${this.currentTask.id}/report/${report.name}/`)
    },
    openIntervalRun(){
      if(""===this.currentTask.start_time||null===this.currentTask.start_time){
        this.$message.error('请输入开始时间');
        return
      }
      let req = {
        days: this.currentTask.days,
        hours: this.currentTask.hours,
        minutes: this.currentTask.minutes,
        start_time: this.currentTask.start_time
      }
      runIntervalTask(this.currentTask.id, req).then(rsp=>{
        let success = rsp.data.success;
        if(true===success){
          this.$message('开启循环执行成功');
          console.log("开启循环执行")
          this.currentTask.days = req.days;
          this.currentTask.hours = req.hours;
          this.currentTask.minutes = req.minutes;
          this.currentTask.start_time = req.start_time;
          this.currentTask.interval_switch = true;
        }
      }).catch(()=>{
      })
    },
    stopIntervalRunTask(){
      stopIntervalTask(this.currentTask.id).then(rsp=>{
        let success = rsp.data.success;
        if(true===success){
          this.$message('停止循环执行成功');
          console.log("停止循环执行")
          this.currentTask.days = 0;
          this.currentTask.hours = 0;
          this.currentTask.minutes = 0;
          this.currentTask.start_time = null;
          this.currentTask.interval_switch = false;
        }
      }).catch(()=>{
      })
    }
  },
  created() {
    this.getAllTasks()
  }
}
</script>

<style scoped>

</style>