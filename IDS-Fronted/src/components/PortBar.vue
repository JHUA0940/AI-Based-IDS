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
            type: 'category', // Set as category type
            data: [], // Initially empty, will update later
          },
          yAxis: {
            type: 'value', // Set as value type
            max: 'dataMax',
            min: 1
          },
          series: [
            {
              name: 'X', // Optional: update series name
              type: 'bar', // Still using bar chart
              data: this.data,
              label: {
                show: true,
                position: 'top', // Labels displayed at the top of the bar
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
        // Count occurrences of ports
        const portCounts = {};

        this.dataList.forEach(item => {
          const port = item.port; // Assume each item has a port property
          if (port) {
            portCounts[port] = (portCounts[port] || 0) + 1; // Increment port count
          }
        });

        // Convert port counts to an array and sort
        const sortedPorts = Object.entries(portCounts)
          .sort((a, b) => b[1] - a[1]) // Sort by count in descending order
          .slice(0, 5); // Take the top 5

        // Extract ports and counts
        const topPorts = sortedPorts.map(([port]) => port);
        const topCounts = sortedPorts.map(([, count]) => count);

        this.data = topCounts; // Update data with counts of the top ports

        // console.log('Top Ports:', topPorts); // Print the top ports
        // console.log('Top Counts:', topCounts); // Print the corresponding counts
        // console.log(this.dataList,topPorts,topCounts)

        if (this.chart) {
          this.chart.setOption({
            xAxis: {
              data: topPorts // Update x-axis with topPorts
            },
            series: [
              {
                type: 'bar',
                data: topCounts // Update series data
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
  height: 400px; /* Adjust as needed */
}
</style>
