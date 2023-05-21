import CardFour from '../../components/CardFour';
import CardOne from '../../components/CardOne';
import CardThree from '../../components/CardThree';
import CardTwo from '../../components/CardTwo';
import ChartOne from '../../components/ChartOne';
import ChartThree from '../../components/ChartThree';
import ChartTwo from '../../components/ChartTwo';
import ChatCard from '../../components/ChatCard';
// import MapOne from '../../components/MapOne';
import TableOne from '../../components/TableOne';
import DefaultLayout from '../../layout/DefaultLayout';
// import MapTest from "../../components/maps/mapTest";
import MapHover from "../../components/maps/mapHover";

const ECommerce = () => {
  return (
    <DefaultLayout>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-5 2xl:gap-7.5">
        {/* # Homeless topics */}
        <CardOne/>
        <CardOne/>
        {/* # Homeless topics */}
        <CardTwo/>
        <CardThree/>
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
        <ChatCard/>
      </div>
    </DefaultLayout>
  );
};

export default ECommerce;
