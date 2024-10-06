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
  </div>
</template>

<script>
export default {
  name: 'ScrollList',
  props: {
    dataList: Array,
    paused: {
      type: Boolean,
      default: false // 默认值为 false
    }
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
    if (!this.paused) {
      this.startAutoScroll();
    }
  },
  watch: {
    dataList: {
      handler(newDataList) {
        // 当 dataList 发生变化时，更新 items
        this.items = [...this.items, ...newDataList];
      },
      deep: true,
      immediate: true
    },
    paused: {
      handler(newVal) {
        if (newVal) {
          this.pauseScroll();
        } else {
          this.resumeScroll();
        }
      },
      immediate: true
    }
  },
  methods: {
    loadMore() {
      if (this.loading) return;
      this.loading = true;
      // 模拟数据加载，添加你的数据获取逻辑
      setTimeout(() => {
        this.loading = false; // 数据加载完成
      }, 1000);
    },
    startAutoScroll() {
      if (this.autoScrollInterval) return; // 确保只启动一个定时器
      this.autoScrollInterval = setInterval(() => {
        const list = this.$el.querySelector('.infinite-list');
        if (list) {
          list.scrollTop += 1;
          // 如果到达底部，重新开始滚动
          if (list.scrollTop >= list.scrollHeight - list.clientHeight) {
            list.scrollTop = 0;
          }
        }
      }, 20);
    },
    pauseScroll() {
      if (this.autoScrollInterval) {
        clearInterval(this.autoScrollInterval);
        this.autoScrollInterval = null; // 清空定时器
      }
    },
    resumeScroll() {
      if (!this.autoScrollInterval) {
        this.startAutoScroll();
      }
    }
  },
  beforeUnmount() {
    this.pauseScroll(); // 清理定时器
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
