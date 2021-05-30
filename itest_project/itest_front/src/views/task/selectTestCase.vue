<template>
  <div>
    <div class="filterStyle">
      <div>
        <el-select v-model="currentServiceId" placeholder="请选择服务" @change="getAllTestCases">
          <el-option
              v-for="item in serviceList"
              :key="item.id"
              :label="item.name"
              :value="item.id">
          </el-option>
        </el-select>
      </div>
    </div>
    <div>
      <el-table
          :data="testCaseList"
          :header-cell-style="{'color': '#555555'}"
          stripe
          style="width: 100%"
          @selection-change="handleSelectionChange">
        <el-table-column
            type="selection"
            width="45">
        </el-table-column>

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
      </el-table>
      <div>
        <el-pagination
            :page-sizes="[20, 50, 100]"
            @size-change="changeSize"
            @current-change="changePage"
            layout="sizes, prev, pager, next"
            :total="testCaseCount">
        </el-pagination>
      </div>
    </div>
    <div style="text-align: right">
      <el-button type="danger" plain @click="success">确定</el-button>
      <el-button type="info" plain @click="cancel">取消</el-button>
    </div>

  </div>
</template>

<script>
import {getTestCaseList} from "@/request/testCase";
import {getServiceList} from "@/request/service";

export default {
  props: {
    projectId: {
      type: String
    }
  },
  name: "selectTestCase",
  data() {
    return {
      currentServiceId: undefined,
      page: 1,
      size: 20,
      serviceList: [],
      testCaseList: [],
      testCaseCount: 0,

      multipleSelection: [],
    }
  },
  methods: {
    getAllServices() {
      getServiceList(this.projectId).then(rsp => {
        let success = rsp.data.success;
        if (true === success) {
          this.serviceList = rsp.data.data;
        }
      }).catch(() => {
      })
    },
    getAllTestCases() {
      getTestCaseList(this.currentServiceId, this.size, this.page).then(rsp => {
        let success = rsp.data.success;
        if (true === success) {
          this.testCaseList = rsp.data.data.list;
          this.testCaseCount = rsp.data.data.total
        }
      }).catch(() => {
      })
    },
    changeSize(size) {
      this.size = size;
      this.getAllTestCases()
    },
    changePage(page) {
      this.page = page;
      this.getAllTestCases()
    },
    handleSelectionChange(val){
      this.multipleSelection = val;
    },
    success(){
      this.$emit("success", this.multipleSelection)
    },
    cancel(){
      this.$emit("cancel")
    }
  },
  created() {
    this.getAllServices()
  }
}
</script>

<style scoped>
.filterStyle {
  display: flex;
  justify-content: space-between;
}
</style>