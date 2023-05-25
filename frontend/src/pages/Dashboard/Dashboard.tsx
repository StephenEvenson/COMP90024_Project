import DefaultLayout from '../../components/layout/DefaultLayout';
import CardTotalTweets from '../../components/CardTotalTweets';
import ChartOne from '../../components/ChartOne';
import ChartThree from '../../components/ChartThree';
import MapDashboard from "../../components/maps/mapHover";
import MessageBox from "../../components/MessageBox/MessageBox";
import CardTotalMastodon from "../../components/CardTotalMastodon";


const HomelessPage = () => {
  // const [{data, isLoading, isError}, setUrl] = useData('https://jsonplaceholder.typicode.com/users', []);
  // console.log({data, isLoading, isError});
  return (
    <DefaultLayout>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5">
        <CardTotalMastodon/>
        <CardTotalTweets/>
        <div className='col-span-2'>
          <MessageBox max_num={10} server={'.au'} interval={10000} key={'.au'}/>
        </div>
        <div className='col-span-2'>
          <MessageBox max_num={10} server={'.tictoc'} interval={10000} key={'.tictoc'}/>
        </div>
        <div className='col-span-2'>
          <MessageBox max_num={10} server={'.social'} interval={10000} key={'.social'}/>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-12 gap-4 md:mt-6 md:gap-6 2xl:mt-7.5 2xl:gap-7.5">
        <MapDashboard />
        {/*<ChartTwo/>*/}
        <ChartThree/>
        <ChartOne/>
      </div>
    </DefaultLayout>
  );
};

export default HomelessPage;
