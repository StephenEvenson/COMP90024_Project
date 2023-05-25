import {useEffect, useState} from "react";
import {getTwitterCount} from "../api/api";
import {GrTwitter} from "react-icons/gr";
import {TwitterCount} from "../types";

const CardTotalTweets = () => {
  const [data, setData] = useState<TwitterCount>({
    all: 0,
    homeless: 0,
  });
  useEffect(() => {
    const getData = async () => {
      const number = await getTwitterCount('all')
      setData(number)
    }
    getData()
  }, []);
  return (
    <div
      className="rounded-sm border border-stroke bg-white py-6 px-6 shadow-default dark:border-strokedark dark:bg-boxdark">
      <div className='flex items-center space-x-4'>
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <GrTwitter className="text-xl fill-primary dark:fill-white"/>
        </div>
        <div className='text-2xl font-medium text-black-2 dark:text-white'>Tweets</div>
      </div>

      <div className="mt-4 flex items-end justify-between">
        <div className='flex flex-col w-full'>
          <div className="flex justify-between  text-title-md font-bold text-black dark:text-white w-full pb-2">
            <div>
              {data!.all}
            </div>
            <div className="flex items-center gap-1 text-md font-medium dark:text-meta-2">
              Total
            </div>
          </div>
          <div className="flex justify-between text-title-sm font-bold text-black dark:text-white w-full">
            <div>
              {data!.homeless}
            </div>
            <div className="flex items-center gap-1 text-sm font-medium text-meta-3">
              Homeless
            </div>
          </div>
          {/*<div className="flex justify-between text-title-sm font-bold text-black dark:text-white w-full">*/}
          {/*  <div>*/}
          {/*    {data!.language}*/}
          {/*  </div>*/}
          {/*  <div className="flex items-center gap-1 text-sm font-medium text-secondary">*/}
          {/*    Language*/}
          {/*  </div>*/}
          {/*</div>*/}
          {/*<div className="flex justify-between text-title-sm font-bold text-black dark:text-white w-full">*/}
          {/*  <div>*/}
          {/*    {data!.abuse}*/}
          {/*  </div>*/}
          {/*  <div className="flex items-center gap-1 text-sm font-medium text-secondary">*/}
          {/*    Vulgar words*/}
          {/*  </div>*/}
          {/*</div>*/}
        </div>
      </div>
    </div>
  );
};

export default CardTotalTweets;
