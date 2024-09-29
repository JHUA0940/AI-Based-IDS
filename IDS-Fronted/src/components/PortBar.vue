<template>
  <div class="bar-container" ref="barChart"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'PortBar',
  data() {
    return {
      chart: null,
      data: []
    };
  },
  props: {
    dataList: Array
  },
  mounted() {
    this.initializeChart();
    this.updateData();
  },
  watch: {
    dataList: {
      handler() {
        this.updateData();
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    initializeChart() {
      try {
        const chartElement = this.$refs.barChart;
        if (!chartElement) {
          console.error('Chart container element is not found.');
          return;
        }

        this.chart = echarts.init(chartElement);

        const option = {
          xAxis: {
            type: 'value', // 设置为数值类型
            max: 'dataMax',
          },
          yAxis: {
            type: 'category', // 设置为类别类型
            data: [], // 初始为空，稍后更新
          },
          series: [
            {
              name: 'Count', // 可选：更新系列名称
              type: 'bar', // 仍然使用柱状图
              data: this.data,
              label: {
                show: true,
                position: 'top', // 标签显示在柱子顶部
                valueAnimation: true
              }
            }
          ],
          legend: {
            show: false
          },
          animationDuration: 0,
          animationDurationUpdate: 3000,
          animationEasing: 'linear',
          animationEasingUpdate: 'linear'
        };

        this.chart.setOption(option);
      } catch (error) {
        console.error('Error initializing chart:', error);
      }
    },
    updateData() {
      try {
        // 统计端口出现次数
        const portCounts = {};

        this.dataList.forEach(item => {
          const port = item.port; // 假设每个 item 中有一个 port 属性
          if (port) {
            portCounts[port] = (portCounts[port] || 0) + 1; // 增加端口计数
          }
        });

        // 将端口计数转为数组并排序
        const sortedPorts = Object.entries(portCounts)
          .sort((a, b) => b[1] - a[1]) // 按计数降序排序
          .slice(0, 5); // 取前三个

        // 提取端口和计数
        const topPorts = sortedPorts.map(([port]) => port);
        const topCounts = sortedPorts.map(([, count]) => count);

        this.data = topCounts; // 更新数据为前三个端口的计数

        // console.log('Top Ports:', topPorts); // 打印出前三个端口
        // console.log('Top Counts:', topCounts); // 打印出对应的计数
        console.log(this.dataList,topPorts,topCounts)

        if (this.chart) {
          this.chart.setOption({
            yAxis: {
              data: topPorts // 更新 x 轴为 topPorts
            },
            series: [
              {
                type: 'bar',
                data: topCounts // 更新系列数据
              }
            ]
          });
        }
      } catch (error) {
        console.error('Error updating data:', error);
      }
    }
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.dispose();
    }
  }
};
</script>

<style scoped>
.bar-container {
  width: 100%;
  height: 300px; /* Adjust as needed */
}
</style>
