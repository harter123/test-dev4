<template>
  <div class="about">
    <h1>This is an about page</h1>
    <h1>{{a}}</h1>
    <div v-html="b"></div>

    <div v-if="flag" :id="divId" :class="newClass" ssss="sdjsjkdsj">
      ddddd
    </div>
    <div v-else>
      eeeeeee
    </div>

    <div v-show="flag">
      fffff
    </div>

    <div v-for="item,index in myList" :key="item">
        {{index}} - {{item}}
    </div>

    等同于写4个div
    <div >
      0 - a
    </div>
    <div >
      1 - b
    </div>
    ....

    <el-button @click="buttonEvent">vue button</el-button>
    <el-input v-model="input" placeholder="请输入内容" @focus="focusEvent"></el-input>

    <el-input v-model="modelInput" placeholder="请输入内容"></el-input>

    <el-select v-model="modelSelect" placeholder="请选择">
      <el-option
              label="选项1"
              value="选项1的值">
      </el-option>
      <el-option
              label="选项2"
              value="选项2的值">
      </el-option>
    </el-select>

    <div>
      <el-radio v-model="modelRadio" label="1">备选项1</el-radio>
      <el-radio v-model="modelRadio" label="2">备选项2</el-radio>
    </div>

    <div>
      <el-checkbox-group v-model="modelCheckList">
        <el-checkbox label="复选框 A"></el-checkbox>
        <el-checkbox label="复选框 B"></el-checkbox>
        <el-checkbox label="复选框 C"></el-checkbox>
      </el-checkbox-group>
    </div>

    <aboutChildComponent :reason="reasonOfLate" ref="aboutChildV1"
                         @callback="callbackfunc"></aboutChildComponent>
  </div>
</template>

<script>
    import aboutChild from "@/views/aboutChild";
    export default {
        name: 'about',
        props: {
            msg: String
        },
        components: {
          aboutChildComponent: aboutChild //key: value
        },
        data(){
            return{
                a: "海贼很帅",
                b: "<h2>虫师也很帅</h2>",
                divId: "xxxx",
                newClass: "my-css",
                flag: false,

                myList: ["a","b","c", "d"],
                input: "dddd",

                modelInput: "dkdkdkdkd",
                modelSelect: "选项1的值",
                modelRadio: "1",
                modelCheckList: ['复选框 A', '复选框 C'],

                reasonOfLate: "webstorm出问题了啊",
            }
        },
        methods:{
            m1(){

            },
            callbackfunc(p){
              alert('callback' + p)
            },
            buttonEvent(){
                alert(this.modelInput + "-" + this.modelSelect+ "-" + this.modelRadio +'-' +this.modelCheckList)
              this.reasonOfLate = "haizei睡晚啦"

              alert(this.$refs.aboutChildV1.a)

            },
            focusEvent(){
                alert('focus input')
            }
        },
        create(){

        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h3 {
    margin: 40px 0 0;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: inline-block;
    margin: 0 10px;
  }
  a {
    color: #42b983;
  }
  .my-css {
    color: #42b983;
  }
</style>
