<template>
  <div class="abnormalList-wrap">
    <!-- Display the abnormal items -->
    <ul v-if="items.length > 0" class="infinite-list">
      <li v-for="(item, index) in items" :key="index" class="infinite-list-item">
        <span>source IP: {{ item.src_ip }}</span>
        <span>port: {{ item.port }}</span>
        <span>protocol: {{ item.protocol }}</span>
        <span>Time: {{ item.timestamp }}</span>
      </li>
    </ul>
    <!-- Fallback if no items are present -->
    <p v-else>No abnormal data available.</p>
  </div>
</template>

<script>
export default {
  name: 'AbnormalList',
  props: {
    dataList: {
      type: Array,
      default: () => [], // Ensure dataList is always an array
    },
  },
  data() {
    return {
      items: [],
    };
  },
  watch: {
    dataList: {
      handler(newDataList) {
        this.loadList(newDataList);
      },
      deep: true,
      immediate: true, // Handle initial data
    },
  },
  methods: {
    loadList(value) {
      if (Array.isArray(value)) {
        this.items = [...value]; // Replace with new data
      }
    },
  },
};
</script>

<style scoped>
.abnormalList-wrap {
  padding: 0px 20px;
  margin-top:-40px;
}
.infinite-list{
  margin:0px;
  padding:0px;
}
.infinite-list-item {
  display: flex;
  align-items: center;
  justify-content: space-around;
  height: 50px;
  background: #636466;
  margin: 10px;
  width:100%;
  color:red;
}
</style>
