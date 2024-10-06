<template>
    <div class="common-layout">
        <el-container>
            <el-header style="text-align: center;">
                <h1>INTRUSION DETECTION SYSTEM</h1>
            </el-header>
            <el-container width="100%">
                <el-aside width="40%">
                    <SidebarAside />
                    <div class="slider-demo-block">
                        <span class="demonstration">Sensitiveness:</span>
                        <div class="flex flex-col items-start gap-4">
                            <el-segmented v-model="Sensitiveness" :options="options" @change="sensitiveness_change" />
                        </div>
                        <div class="sider-text-wrap">
                            <p>High sensitivity: false positive rate</p>
                            <p>Medium: recommended</p>
                            <p>Low sensitivity: false negative rate high</p>
                        </div>
                    </div>
                    <AttackNumBar :dataList="attackData" />
                </el-aside>
                <el-container width="60%" style="position:relative;">
                    <div class="loadding-main" ref="loadingMain" style="height: 200px;"></div>
                    <el-icon v-if="abnormalData.length" @click="drawer = true" style="position:absolute;top:10px;left:-30px;font-size:100px;cursor:pointer;">
                        <WarningFilled style="width:40px;height:40px;color:red;" />
                    </el-icon>
                    <el-drawer style="background:darkgray;" v-model="drawer" title="Abnormal Details" :with-header="true" direction="rtl" size="70%">
                        <AbnormalList :dataList="abnormalData" />
                    </el-drawer>
                    <el-main>
                        <Scroll :dataList="attackData" :paused="drawer" />
                        <PortBar :dataList="attackData" />
                    </el-main>
                </el-container>
            </el-container>
        </el-container>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts'; // Import ECharts
import Scroll from './components/ScrollList.vue';
import SidebarAside from './components/SidebarAside.vue';
import AttackNumBar from './components/AttackNumBar.vue';
import PortBar from './components/PortBar.vue';
import AbnormalList from './components/AbnormalList.vue'
import { ElMessage, ElMessageBox } from 'element-plus';
import io from 'socket.io-client';
import { WarningFilled } from '@element-plus/icons-vue';
import { postData } from './services/api.js'
export default {
    name: 'App',
    components: {
        Scroll,
        SidebarAside,
        AttackNumBar,
        PortBar,
        WarningFilled,
        AbnormalList
    },
    setup() {
        const Sensitiveness = ref(30);
        const previousSensitiveness = ref(Sensitiveness.value);
        const loadingMain = ref(null); // Ref for the loadding-main div
        const attackData = ref([]); // Ref for attack data
        const abnormalData = ref([])
        const drawer = ref(false); // Drawer state
        const options = [
            { label: 'low', value: 30 },
            { label: 'middle', value: 60 },
            { label: 'high', value: 100 },
        ];

        // ECharts setup
        const initECharts = () => {
            const myChart = echarts.init(loadingMain.value); // Initialize the chart in the loadding-main div
            const option = {
                graphic: {
                    elements: [{
                        type: 'group',
                        left: 'center',
                        top: 'center',
                        children: new Array(7).fill(0).map((val, i) => ({
                            type: 'rect',
                            x: i * 20,
                            shape: {
                                x: 0,
                                y: -40,
                                width: 10,
                                height: 80,
                            },
                            style: {
                                fill: '#5470c6',
                            },
                            keyframeAnimation: {
                                duration: 1000,
                                delay: i * 200,
                                loop: true,
                                keyframes: [{
                                        percent: 0.5,
                                        scaleY: 0.3,
                                        easing: 'cubicIn',
                                    },
                                    {
                                        percent: 1,
                                        scaleY: 1,
                                        easing: 'cubicOut',
                                    },
                                ],
                            },
                        })),
                    }, ],
                },
            };
            myChart.setOption(option); // Apply the chart options
        };

        // Method to handle the change in Sensitiveness
        const sensitiveness_change = (newValue) => {
            let messageInfo = newValue === 30 ? 'low' : (newValue === 60 ? 'middle' : 'high')
            ElMessageBox.confirm(
                    `Change sensitiveness to ${messageInfo}?`,
                    'Confirmation', {
                        confirmButtonText: 'OK',
                        cancelButtonText: 'Cancel',
                        type: 'warning',
                    }
                )
                .then(() => {
                    previousSensitiveness.value = newValue;
                    ElMessage.success('Sensitiveness updated successfully');
                    postData(newValue).then(response => {
                            console.log(postData, response.data);
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });
                })
                .catch(() => {
                    Sensitiveness.value = previousSensitiveness.value;
                    ElMessage({
                        type: 'info',
                        message: 'Sensitiveness update canceled',
                    });
                });
        };

        // Initialize Socket.IO connection
        const socket = io('http://localhost:4321'); // Replace with your Socket.IO server address

        // Listen for traffic_update event
        socket.on('traffic_update', (data) => {
            attackData.value.push(data); // Append data to attackData
            // Check if the data has 'abnormal' status and push it to abnormalData array
            if (data.status === 'abnormal') {
                abnormalData.value.push(data);
            }
        });

        // Initialize ECharts and fetch data on component mount
        onMounted(() => {
            initECharts();
        });

        return { Sensitiveness, options, sensitiveness_change, loadingMain, attackData, abnormalData, drawer };
    },
};
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #fff;
    background: #000;
    height: 100vh;
}

body {
    margin: 0px;
}

.el-aside {
    background: #000;
}

.el-main {
    background: #000;
    padding-top: 60px !important;
}

.slider-demo-block {
    max-width: 600px;
    display: flex;
    align-items: center;
    margin-top: 0px;
    position: relative;
}

.slider-demo-block .demonstration {
    font-size: 14px;
    color: #fff;
    font-weight: bold;
    line-height: 44px;
    white-space: nowrap;
    margin: 0px 10px 0px 0px;
}

.sider-text-wrap {
    position: absolute;
    left: 17%;
    top: 40px;
}

.sider-text-wrap p {
    margin: 0px;
    font-size: 12px;
    color: var(--el-text-color-secondary);
}

.loadding-main {
    width: 200px;
    position: absolute;
    right: 0px;
    top: -100px;
}

.el-segmented__item {
    width: 80px;
}

.el-drawer__title {
    color: red;
    font-weight: bold;
    font-size: 20px;
}

.el-drawer .el-drawer__close-btn:hover {
    color: red !important;
}
</style>
