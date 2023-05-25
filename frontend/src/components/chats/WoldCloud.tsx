import React from 'react';
import WordCloud from 'react-d3-cloud';
import {HiLanguage} from "react-icons/hi2";
import {code2lan} from "../CardLanMastodon";


export const RWordCloud = (props: { data: { text: string, value: number }[] }) => {
  const data = props.data.map((item) => ({text: code2lan[item.text], value: item.value}));
  return (
    <div
      className='rounded-sm border border-stroke bg-white pt-5 px-6 shadow-default dark:border-strokedark dark:bg-boxdark h-94 xl:h-94'
    >
      <div className='flex items-center space-x-4'>
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4 ">
          {/*<BsMastodon className="text-xl fill-primary dark:fill-white"/>*/}
          <HiLanguage className='text-xl fill-primary dark:fill-white'/>
        </div>
        <div className='text-2xl font-medium text-black-2 dark:text-white'>
          Word Cloud
        </div>
      </div>
      <WordCloud
        // @ts-ignore
        data={data}
        width={500}
        height={500}
        fontSize={(word) => Math.log2(word.value) * 10}
        spiral="rectangular"
      />
    </div>
  );
};

export default RWordCloud;