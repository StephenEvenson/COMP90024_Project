import React from 'react';
import MapTest from './components/maps/mapTest';
import ChartTest from './components/chats/chartTest';


function App() {
  return (
    <div className="w-screen h-screen">
      <div className="font-bold text-2xl text-center">CCC Template</div>
      <ChartTest/>
      <MapTest/>
    </div>
  );
}


export default App;
