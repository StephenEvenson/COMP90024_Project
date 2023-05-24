import React from "react";
import {createBrowserRouter} from "react-router-dom";

import Homeless from "./pages/Dashboard/Homeless";
import Language from "./pages/Dashboard/Language";
import Sentiment from "./pages/Dashboard/Sentiment";
import Team from "./pages/Team";
import ErrorPage from "./error-page";
import Dashboard from "./pages/Dashboard/Dashboard";


export default createBrowserRouter([
  {
    path: "/",
    errorElement: <ErrorPage/>,
    element: <Dashboard/>,
  },
  {
    path: "/dashboard/homeless",
    element: <Homeless/>,
  },
  {
    path: "/dashboard/sentiment",
    element: <Sentiment/>,
  },
  {
    path: "/dashboard/language",
    element: <Language/>,
  },
  {
    path: "/team",
    element: <Team/>
  }
]);