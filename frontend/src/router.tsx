import React from "react";
import {createBrowserRouter} from "react-router-dom";

import ErrorPage from "./error-page";
import Homeless from "./pages/Dashboard/Homeless";
import Language from "./pages/Dashboard/Language";
import Sentiment from "./pages/Dashboard/Sentiment";
import Team from "./pages/Team";

export default createBrowserRouter([
  {
    path: "/",
    element: <Homeless/>,
    errorElement: <ErrorPage/>,
    children: [{
      path: "/dashboard",
      element: <Homeless/>,
      children: [
        {
          path: "homeless",
          element: <Homeless/>,
        },
        {
          path: "sentiment",
          element: <Sentiment/>,
        }, {
          path: "language",
          element: <Language/>,
        }
      ]
    }, {
      path: "team",
      element: <Team/>
    }]
  },
]);