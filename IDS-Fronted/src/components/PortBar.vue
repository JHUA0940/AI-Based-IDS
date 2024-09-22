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
  mounted() {
    this.initializeChart();
    this.updateData();
    setInterval(() => {
      this.updateData();
    }, 3000);
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
            data: ['80', '82', '83']
          },
          series: [
            {
              name: 'X',
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
        // Generate random data
        const newData = [];
        for (let i = 0; i < 5; ++i) {
          newData.push(Math.round(Math.random() * 200));
        }
        this.data = newData;

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
