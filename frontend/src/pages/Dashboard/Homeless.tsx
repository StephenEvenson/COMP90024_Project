import DefaultLayout from '../../components/layout/DefaultLayout';
import CardFour from '../../components/CardFour';
import CardOne from '../../components/CardOne';
import CardTotalTweets from '../../components/CardTotalTweets';
import CardTwo from '../../components/CardTwo';
import ChartOne from '../../components/ChartOne';
import ChartThree from '../../components/ChartThree';
import ChartTwo from '../../components/ChartTwo';
import TeamCard from '../../components/TeamCard';
import TableOne from '../../components/TableOne';
import MapHover from "../../components/maps/mapHover";
// import useData from "../../hooks/useData";
import MessageBox from "../../components/MessageBox/MessageBox";


const HomelessPage = () => {
  // const [{data, isLoading, isError}, setUrl] = useData('https://jsonplaceholder.typicode.com/users', []);
  // console.log({data, isLoading, isError});
  return (
    <DefaultLayout>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5">
        {/* # Homeless topics */}
        {/*<CardOne/>*/}
        {/* # Homeless topics */}
        <div className='col-span-2'>
          <MessageBox max_num={30} server={'.au'}  />
        </div>
        {/*<CardTwo/>*/}
        <CardTotalTweets/>
        <CardFour/>
      </div>

      <div className="mt-4 grid grid-cols-12 gap-4 md:mt-6 md:gap-6 2xl:mt-7.5 2xl:gap-7.5">
        <MapHover/>
        <ChartTwo/>
        <ChartThree/>
        <ChartOne/>

        {/*<MapOne />*/}
        <div className="col-span-12 xl:col-span-8">
          <TableOne/>
        </div>
        <TeamCard/>
      </div>
    </DefaultLayout>
  );
};

export default HomelessPage;
