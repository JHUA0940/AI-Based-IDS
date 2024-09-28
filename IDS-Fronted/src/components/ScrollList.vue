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
          <span>vulnerability{{index}}</span>
          <span>port: 808{{index}}</span>
          <span>source IP:  23424{{index}}</span>
          <span>Time: 2024.09.{{index}}</span>
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
    msg: String,
  },
  data() {
    return {
      items: [
        '11111111',
        '2222222',
        '3333333',
        '44444444',
      ],
      loading: false,
      autoScrollInterval: null,
    };
  },
  mounted() {
    this.loadMore();
    this.startAutoScroll();
  },
  methods: {
    loadMore() {
      if (this.loading) return;

      this.loading = true;
      setTimeout(() => {
        const newItems = [`Item ${this.items.length + 1}`];
        this.items = [...this.items, ...newItems];
        this.loading = false;
      }, 500);
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
