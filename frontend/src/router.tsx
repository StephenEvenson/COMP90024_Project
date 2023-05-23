import React from "react";
import {createBrowserRouter} from "react-router-dom";

import Homeless from "./pages/Dashboard/Homeless";
import Language from "./pages/Dashboard/Language";
import Sentiment from "./pages/Dashboard/Sentiment";
import Team from "./pages/Team";
import ErrorPage from "./error-page";


export default createBrowserRouter([
  {
    path: "/",
    errorElement: <ErrorPage/>,
    element: <Homeless/>,
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