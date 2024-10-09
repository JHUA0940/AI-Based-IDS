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
      default: false 
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
        // Update items when the dataList changes
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
      // Simulate data loading and add your data acquisition logic
      setTimeout(() => {
        this.loading = false; // Data loading complete
      }, 1000);
    },
    startAutoScroll() {
      if (this.autoScrollInterval) return; // Make sure to start only one timer
      this.autoScrollInterval = setInterval(() => {
        const list = this.$el.querySelector('.infinite-list');
        if (list) {
          list.scrollTop += 1;
          // If reach the bottom, start rolling again
          if (list.scrollTop >= list.scrollHeight - list.clientHeight) {
            list.scrollTop = 0;
          }
        }
      }, 20);
    },
    pauseScroll() {
      if (this.autoScrollInterval) {
        clearInterval(this.autoScrollInterval);
        this.autoScrollInterval = null; // clearInterval
      }
    },
    resumeScroll() {
      if (!this.autoScrollInterval) {
        this.startAutoScroll();
      }
    }
  },
  beforeUnmount() {
    this.pauseScroll(); // Clearing timer
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
