<template>
  <div class="bar-container" ref="barChart"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'AttackNumBar',
  data() {
    return {
      chart: null,
      data: [],
      
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
        // 当 dataList 发生变化时，更新 items
        this.updateData();
      },
      deep: true, // 如果 dataList 是一个复杂对象，建议使用深度监听
      immediate: true // 立即执行处理函数以处理初始数据
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
            type: 'value',
            max: 'dataMax',
          },
          yAxis: {
            type: 'category',
            data: ['TCP', 'UDP', 'ICMP']
          },
          series: [
            {
              name: 'Y',
              type: 'bar',
              data: this.data,
              label: {
                show: true,
                position: 'right',
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
        this.data = [0, 0, 0]; // Initialize data array to hold counts for TCP, UDP, ICMP

        // Loop through newDataList and count protocol occurrences
        this.dataList.forEach(item => {
          if (item.protocol === 'tcp') {
            this.data[0] += 1; // Increase TCP count
          } else if (item.protocol === 'udp') {
            this.data[1] += 1; // Increase UDP count
          } else if (item.protocol === 'icmp') {
            this.data[2] += 1; // Increase ICMP count
          }
        });
        console.log(this.data, 'Updated data counts'); 
        if (this.chart) {
          this.chart.setOption({
            series: [
              {
                type: 'bar',
                data: this.data
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
