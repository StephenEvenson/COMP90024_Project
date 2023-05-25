import {ApexOptions} from 'apexcharts';
import React, {useEffect, useState} from 'react';
import ReactApexChart from 'react-apexcharts';
import {getTwitterSentimentPeriod} from "../api/api";

const initOptions: ApexOptions = {
  legend: {
    show: false,
    position: 'top',
    horizontalAlign: 'left',
  },
  colors: ['#3056D3', '#80CAEE', '#eef43f'],
  chart: {
    fontFamily: 'Satoshi, sans-serif',
    height: 335,
    type: 'area',
    dropShadow: {
      enabled: true,
      color: '#623CEA14',
      top: 10,
      blur: 4,
      left: 0,
      opacity: 0.1,
    },

    toolbar: {
      show: false,
    },
  },
  responsive: [
    {
      breakpoint: 1024,
      options: {
        chart: {
          height: 300,
        },
      },
    },
    {
      breakpoint: 1366,
      options: {
        chart: {
          height: 350,
        },
      },
    },
  ],
  stroke: {
    width: [2, 2],
    curve: 'straight',
  },
  // labels: {
  //   show: false,
  //   position: "top",
  // },
  grid: {
    xaxis: {
      lines: {
        show: true,
      },
    },
    yaxis: {
      lines: {
        show: true,
      },
    },
  },
  dataLabels: {
    enabled: false,
  },
  markers: {
    size: 4,
    colors: '#fff',
    strokeColors: ['#3056D3', '#80CAEE', '#eef43f'],
    strokeWidth: 3,
    strokeOpacity: 0.9,
    strokeDashArray: 0,
    fillOpacity: 1,
    discrete: [],
    hover: {
      size: undefined,
      sizeOffset: 5,
    },
  },
  xaxis: {
    type: 'category',
    categories: ['0-2', '2-4', '4-6', '6-8', '8-10', '10-12', '12-14', '14-16', '16-18', '18-20', '20-22', '22-24'],
    axisBorder: {
      show: false,
    },
    axisTicks: {
      show: false,
    },
  },
  yaxis: {
    title: {
      style: {
        fontSize: '0px',
      },
    },
    min: 0,
    max: 20000,
  },
};

interface ChartOneState {
  series: {
    name: string;
    data: number[];
  }[];
}

const period_options = ['Day', 'Week', 'Month', 'Year'];
const ChartOne: React.FC = () => {
  const [state, setState] = useState<ChartOneState>({series: []});
  const [options, setOptions] = useState<ApexOptions>(initOptions);
  const [period, setPeriod] = useState<string>('Day');
  const [date, setDate] = useState<string[]>(['2021-05-01', '2021-05-31']);

  useEffect(() => {
    const fetchData = async () => {
      const {sentiment_counts: res, start_date, end_date} = await getTwitterSentimentPeriod(period.toLowerCase())
      setDate([start_date, end_date])
      const series = [
        {
          name: 'Neutral',
          data: Object.values(res).map((item: any) => item.neutral),
        },
        {
          name: 'Positive',
          data: Object.values(res).map((item: any) => item.positive),
        },
        {
          name: 'Negative',
          data: Object.values(res).map((item: any) => item.negative),
        }
      ]
      const maxY = Math.max(...series.map((item: any) => Math.max(...item.data)))
      const xaxis = Object.keys(res)
      const newOptions = JSON.parse(JSON.stringify(options))
      newOptions.xaxis!.categories = xaxis
      newOptions!.yaxis!.max = maxY * 1.2
      setOptions(newOptions)
      setState({series: series})
    }
    fetchData()
  }, [period])
  return (
    <div
      className="col-span-12 rounded-sm border border-stroke bg-white px-5 pt-7.5 pb-5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:col-span-8">
      <div className="flex flex-wrap items-start justify-between gap-3 sm:flex-nowrap">
        <div className='text-2xl font-medium text-black-2 dark:text-white'>Sentiment Distribution of Tweets</div>
        <div className="flex w-full max-w-45 justify-end">
          <div className="inline-flex items-center rounded-md bg-whiter p-1.5 dark:bg-meta-4">
            {period_options.map((item, index) =>
              item == period ?
                (
                  <button
                    className="rounded bg-white py-1 px-3 text-xs font-medium text-black shadow-card hover:bg-white hover:shadow-card dark:bg-boxdark dark:text-white dark:hover:bg-boxdark"
                    onClick={() => setPeriod(item)}
                    key={index + item}
                  >
                    {item}
                  </button>
                ) : (
                  <button
                    className="rounded py-1 px-3 text-xs font-medium text-black hover:bg-white hover:shadow-card dark:text-white dark:hover:bg-boxdark"
                    onClick={() => setPeriod(item)}
                    key={index + item}
                  >
                    {item}
                  </button>
                )
            )}
          </div>
        </div>
      </div>

      <div>
        <div id="chartOne" className="-ml-5">
          <ReactApexChart
            options={options}
            series={state.series}
            type="area"
            height={350}
          />
        </div>
      </div>
    </div>
  )
    ;
};

export default ChartOne;
