import {ApexOptions} from 'apexcharts';
import React, {useEffect, useState} from 'react';
import ReactApexChart from 'react-apexcharts';
import {getMastodonAbuseLang} from "../api/api";
import {HiLanguage} from "react-icons/hi2";
import {FaBug} from "react-icons/fa";

const initOptions: ApexOptions = {
  colors: ['#3C50E0', '#80CAEE'],
  chart: {
    fontFamily: 'Satoshi, sans-serif',
    type: 'bar',
    height: '50px',
    stacked: true,
    toolbar: {
      show: false,
    },
    zoom: {
      enabled: false,
    },
  },
  responsive: [
    {
      breakpoint: 1,
      options: {
        plotOptions: {
          bar: {
            borderRadius: 0,
            columnWidth: '35%',
          },
        },
      },
    },
  ],
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 0,
      columnWidth: '25%',
      borderRadiusApplication: 'end',
      borderRadiusWhenStacked: 'last',
    },
  },
  dataLabels: {
    enabled: false,
  },

  xaxis: {
    categories: [],
  },
  legend: {
    position: 'top',
    horizontalAlign: 'left',
    fontFamily: 'Satoshi',
    fontWeight: 500,
    fontSize: '14px',
    markers: {
      radius: 99,
    },
  },
  fill: {
    opacity: 1,
  },
};

interface ChartTwoState {
  series: {
    name: string;
    data: number[];
  }[];
}

const ChartTwo: React.FC = () => {
  const [options, setOptions] = useState<ApexOptions>(initOptions);
  const [state, setState] = useState<ChartTwoState>({
    series: [],
  });
  useEffect(() => {
    const fetchData = async () => {
      const res = await getMastodonAbuseLang();
      // console.log(res);
      const xAxis = Object.keys(res)
      const newOptions = JSON.parse(JSON.stringify(options))
      newOptions.xaxis!.categories = xAxis
      setOptions(newOptions)
      setState({
        series: [
          {
            name: 'Vulgar Words Ratio Rank',
            // @ts-ignore
            data: Object.values(res).map((d) => d.toFixed(2)) as number[],
          }
        ]
      })
    }
    fetchData()

    const interval = setInterval(() => {
      fetchData()
    }, 3000)

    return () => clearInterval(interval)
  }, []);

  return (
    <div
      className="col-span-12 rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark xl:col-span-12">
      <div className='flex items-center space-x-4'>
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4 ">
          {/*<BsMastodon className="text-xl fill-primary dark:fill-white"/>*/}
          <FaBug className='text-xl fill-primary dark:fill-white'/>
        </div>
        <div className='text-2xl font-medium text-black-2 dark:text-white'>
          Vulgar Words Ratio Rank
        </div>
      </div>

      <div>
        <div id="chartTwo" className="-ml-5 -mb-9">
          <ReactApexChart
            options={options}
            series={state.series}
            type="bar"
            height={310}
          />
        </div>
      </div>
    </div>
  );
};

export default ChartTwo;
