// import React from "react";
import {
  createBrowserRouter,
  RouterProvider,
  type RouteObject,
} from "react-router-dom";
import IdePage from "./pages/app/IdePage";
import DocsPage from "./pages/documentation/DocsPage";

const App = () => {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <IdePage />,
      errorElement: <div>error</div>,
    },
    {
      path: "/docs",
      element: <DocsPage />,
    },
  ] as RouteObject[]);
  return <RouterProvider router={router} />;
};

export default App;
