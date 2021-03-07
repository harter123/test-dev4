<template>
  <div class="red-color">
    这是一个子组件：
    海贼，这节课迟到啦， 原因：{{reason}}  {{a}}

    <el-button @click="tEvent">bt</el-button>
  </div>
</template>

<script>
export default {
  name: "aboutChild",
  props: {
    reason: {
      type: String,
      required: true
    }
  },
  data(){
    return {
      a: "ccc"
    }
  },
  methods: {
    funB(){
      alert('aboutchild funb')
    },
    tEvent(){
      //alert(this.$parent.a)
      let params = "回调参数"
      this.$emit('callback', params);
    }
  }
}
</script>

<style scoped>
.red-color{
  color: red;
}
</style>