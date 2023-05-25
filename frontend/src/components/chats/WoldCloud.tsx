import React from 'react';
import WordCloud from 'react-d3-cloud';
import {HiLanguage} from "react-icons/hi2";
import {BsMastodon} from "react-icons/bs";
// import {getMastodonLangCount} from "../../api/api";


export const RWordCloud = (props: { data: { text: string, value: number }[] }) => {
  return (
    <div
      className='rounded-sm border border-stroke bg-white pt-5 px-6 shadow-default dark:border-strokedark dark:bg-boxdark'
    >
      {/*<div className=' flex space-x-2 items-center pb-5'>*/}
      {/*  <HiLanguage className='text-xl'/>*/}
      {/*  <div className='text-2xl font-medium text-black-2 dark:text-white '>Localization</div>*/}
      {/*</div>*/}
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
        data={props.data}
        width={500}
        height={500}
        fontSize={(word) => Math.log2(word.value) * 20}
        spiral="rectangular"
      />
    </div>
  );
};

export default RWordCloud;