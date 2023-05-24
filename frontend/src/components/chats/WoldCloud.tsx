import React, {useEffect, useState} from 'react';
import WordCloud from 'react-d3-cloud';
import {getMastodonLangCount} from "../../api/api";


// const data = [
//   {text: 'Hey', value: 1000},
//   {text: 'lol', value: 200},
//   {text: 'first impression', value: 800},
//   {text: 'very cool', value: 1000000},
//   {text: 'duck', value: 10},
// ];
export const RWordCloud = (props: { data: { text: string, value: number }[] }) => {
  return (
    <div
      className='rounded-sm border border-stroke bg-white pt-5 px-6 shadow-default dark:border-strokedark dark:bg-boxdark'
    >
      <div className='text-2xl font-medium text-black-2 dark:text-white pb-5'>Localization Cloud</div>
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