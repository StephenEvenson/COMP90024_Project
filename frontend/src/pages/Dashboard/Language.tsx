import CardFour from '../../components/CardFour';
import CardOne from '../../components/CardOne';
import CardTotalTweets from '../../components/CardTotalTweets';
import CardTwo from '../../components/CardTwo';
import ChartOne from '../../components/ChartOne';
import ChartThree from '../../components/ChartThree';
import ChartTwo from '../../components/ChartTwo';
import TeamCard from '../../components/TeamCard';
import TableOne from '../../components/TableOne';
import DefaultLayout from '../../components/layout/DefaultLayout';
import MapHover from "../../components/maps/mapHover";
import RWordCloud from "../../components/chats/WoldCloud";
import MessageBox from "../../components/MessageBox/MessageBox";
import CardTotalMastodon from "../../components/CardTotalMastodon";
import React, {useEffect, useState} from "react";
import {getMastodonLangCount} from "../../api/api";
import CardLanMastodon from "../../components/CardLanMastodon";

const LanguagePage = () => {
  const intervalTimeMs = 5000;
  const [data, setData] = useState([]) as any[];
  useEffect(() => {
    async function fetch_data() {
      const mess = await getMastodonLangCount(500);
      // map key to text and value
      const data = Object.keys(mess).map((key) => ({text: key, value: mess[key]}));
      setData(data);
    }

    const interval = setInterval(() => {
      fetch_data()
    }, intervalTimeMs);
    fetch_data()
    return () => clearInterval(interval);
  }, []);


  return (
    <DefaultLayout>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5">
        <div className='col-span-2'>
          <MessageBox max_num={30} server={'.au'} className='h-75 xl:h-75' interval={intervalTimeMs}/>
        </div>
        <RWordCloud data={data}/>
        <CardLanMastodon data={data} className='h-94 xl:h-94'/>
      </div>

      {/*<div className="mt-4 grid grid-cols-12 gap-4 md:mt-6 md:gap-6 2xl:mt-7.5 2xl:gap-7.5">*/}
      {/*  <MapHover/>*/}
      {/*  <ChartTwo/>*/}
      {/*  <ChartThree/>*/}
      {/*  <ChartOne/>*/}

      {/*  /!*<MapOne />*!/*/}
      {/*  /!*<div className="col-span-12 xl:col-span-8">*!/*/}
      {/*  /!*  <TableOne/>*!/*/}
      {/*  /!*</div>*!/*/}
      {/*  /!*<TeamCard/>*!/*/}
      {/*</div>*/}


    </DefaultLayout>
  );
};

export default LanguagePage;
