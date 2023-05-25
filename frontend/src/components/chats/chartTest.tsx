import React, {useEffect} from 'react';
import ReactECharts from 'echarts-for-react';
import {getMastodonAbuseLang} from "../../api/api";

const EChartsExample = () => {
  useEffect(() => {
    const interval = setInterval(run, 3000);
    return () => clearInterval(interval);
  }, []);

  const run = async () => {

    getMastodonAbuseLang().then((res) => {
      console.log(res);

    })


    const newData: any[] = [];


    // @ts-ignore
    // const newData = data.map(value => {
    //   if (Math.random() > 0.9) {
    //     return value + Math.round(Math.random() * 2000);
    //   } else {
    //     return value + Math.round(Math.random() * 200);
    //   }
    // });
    // @ts-ignore
    myChart.setOption({
      series: [
        {
          type: 'bar',
          data: newData,
        },
      ],
    });
  };
  // @ts-ignore
  const data = [];
  for (let i = 0; i < 5; ++i) {
    data.push(Math.round(Math.random() * 200));
  }

  const option = {
    xAxis: {
      max: 'dataMax',
    },
    yAxis: {
      type: 'category',
      data: ['A', 'B', 'C', 'D', 'E'],
      inverse: true,
      animationDuration: 300,
      animationDurationUpdate: 300,
      max: 2, // only the largest 3 bars will be displayed
    },
    series: [
      {
        realtimeSort: true,
        name: 'X',
        type: 'bar',
        data: data,
        label: {
          show: true,
          position: 'right',
          valueAnimation: true,
        },
      },
    ],
    legend: {
      show: true,
    },
    animationDuration: 0,
    animationDurationUpdate: 3000,
    animationEasing: 'linear',
    animationEasingUpdate: 'linear',
  };
  // @ts-ignore
  let myChart;

  // @ts-ignore
  const onChartReady = chart => {
    myChart = chart;
    run();
  };

  return (
    <div
      className="rounded-sm border border-stroke bg-white py-6 px-6 shadow-default dark:border-strokedark dark:bg-boxdark overflow-hiddens">
      <ReactECharts option={option} onChartReady={onChartReady}/>
    </div>
  )
};

export default EChartsExample;