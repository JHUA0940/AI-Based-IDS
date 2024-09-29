<template>
  <div class="scrollList-wrap">
    <div class="scrollList-con">
      <ul 
        class="infinite-list"
        v-infinite-scroll="loadMore"
        infinite-scroll-disabled="loading"
        infinite-scroll-distance="10"
        @mouseover="pauseScroll"
        @mouseleave="resumeScroll"
      >
        <li v-for="(item, index) in items" :key="index" class="infinite-list-item">
          <span>source IP:  {{item.src_ip}}</span>
          <span>port: {{item.port}}</span>
          <span>protocol: {{item.protocol}}</span>
          <span>Time: {{item.timestamp}}</span>
        </li>
      </ul>
    </div>
    <div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ScrollList',
  props: {
    dataList: Array
  },
  data() {
    return {
      items: [],
      loading: false,
      autoScrollInterval: null,
    };
  },
  mounted() {
    this.loadMore();
    this.startAutoScroll();
  },
  watch: {
    dataList: {
      handler(newDataList) {
        // 当 dataList 发生变化时，更新 items
          this.items = [...this.items, ...newDataList]
      },
      deep: true, // 如果 dataList 是一个复杂对象，建议使用深度监听
      immediate: true // 立即执行处理函数以处理初始数据
    }
  },
  methods: {
    loadMore() {
      if (this.loading) return;
      this.loading = true;
    },
    startAutoScroll() {
      this.autoScrollInterval = setInterval(() => {
        const list = document.querySelector('.infinite-list');
        if (list) {
          list.scrollTop += 1;
          if (list.scrollTop >= list.scrollHeight - list.clientHeight) {
            list.scrollTop = 0;
          }
        }
      }, 20);
    },
    pauseScroll() {
      if (this.autoScrollInterval) {
        clearInterval(this.autoScrollInterval);
      }
    },
    resumeScroll() {
      this.startAutoScroll();
    }
  },
  beforeUnmount() {
    if (this.autoScrollInterval) {
      clearInterval(this.autoScrollInterval);
    }
  }
};
</script>

<style scoped>
.scrollList-con {
  padding: 40px;
  background: #424243;
}

.infinite-list {
  height: 300px;
  overflow-y: scroll; /* Ensure that scrolling is enabled */
  padding: 0;
  margin: 0;
  list-style: none;
  scrollbar-width: none; /* Firefox */
}

.infinite-list::-webkit-scrollbar {
  display: none; /* Chrome, Safari, and Opera */
}

.infinite-list .infinite-list-item {
  display: flex;
  align-items: center;
  justify-content: space-around;
  height: 50px;
  background: #636466;
  margin: 10px;
  color: var(--el-color-primary);
}
</style>
