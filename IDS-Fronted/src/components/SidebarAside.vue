<template>
  <div class="radar-container">
    <div class="radar">
        <!-- Radar line -->
        <ul class="radar_line">
            <li></li>
            <li></li>
            <li></li>
            <li></li>
        </ul>
        <!-- Radar circle range -->
        <ul class="radar_circle">
            <li></li>
            <li></li>
            <li></li>
        </ul>
        <!-- radar scan -->
        <div class="scanning"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RadarScan',
  data() {
    return {
      blips: this.generateBlips(),
    };
  },
  methods: {
    generateBlips() {
      const blips = [];
      for (let i = 0; i < 10; i++) {
        blips.push({
          x: Math.random() * 280 - 140,
          y: Math.random() * 280 - 140,
        });
      }
      return blips;
    },
  },
};
</script>

<style scoped>
.radar-container {
  width: 100%;
  height: 450px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #000;
}
/* radar box */
.radar {
    position: relative;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    border: 10px solid #fff;
    background: #000;
    overflow: hidden;
}
/* 雷达线 */
.radar_line li {
    position: absolute;
    top: 0;
    left: 50%;
    background: #409eff;
    width: 1px;
    height: 100%;
}
.radar_line>li:nth-child(1) {
    transform: rotate(45deg);
}
.radar_line>li:nth-child(2) {
    transform: rotate(90deg);
}
.radar_line>li:nth-child(3) {
    transform: rotate(135deg);
}
/* radar cricle */
.radar_circle li {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    border: 1px solid #409eff;
    border-radius: 50%;
}
.radar_circle>li:nth-child(1) {
    width: 100px;
    height: 100px;
}
.radar_circle>li:nth-child(2) {
    width: 200px;
    height: 200px;
}
.radar_circle>li:nth-child(3) {
    width: 300px;
    height: 300px;
}
/* scanning */
.scanning {
    position: absolute;
    top: 50%;
    left: 50%;
    width:200px;
    height: 200px;
    background: linear-gradient(45deg, #409eff 0%, transparent 50%);
    animation: investigation  2s infinite linear;
    transform-origin: left top;
}
@keyframes investigation  {
  from {
      transform: rotate(0deg);
  }
  to {
      transform: rotate(360deg);
  }
}
</style>
