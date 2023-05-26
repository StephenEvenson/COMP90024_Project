import DefaultLayout from '../../components/layout/DefaultLayout';
import CardTotalTweets from '../../components/CardTotalTweets';
import ChartThree from '../../components/ChartThree';
import MessageBox from "../../components/MessageBox/MessageBox";
import CardTotalMastodon from "../../components/CardTotalMastodon";
import MapHomeless from "../../components/maps/mapHomeless";
import HomelessLineChart from "../../components/HomelessLineChart";


const HomelessPage = () => {
  // const [{data, isLoading, isError}, setUrl] = useData('https://jsonplaceholder.typicode.com/users', []);
  // console.log({data, isLoading, isError});
  return (
    <DefaultLayout>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5">
        <div className='col-span-2'>
          <MessageBox max_num={30} server={'.au'} homeless={true} sentiment={false} interval={5000}/>
        </div>
        {/*<CardTwo/>*/}
        <CardTotalMastodon/>
        <CardTotalTweets/>
      </div>

      <div className="mt-4 grid grid-cols-12 gap-4 md:mt-6 md:gap-6 2xl:mt-7.5 2xl:gap-7.5">
        <MapHomeless/>
        <ChartThree/>
        <HomelessLineChart/>
      </div>
    </DefaultLayout>
  );
};

export default HomelessPage;
