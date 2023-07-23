import { Navigate } from "react-router-dom";
export const PrivateRoute = ({children}) => {
  const currentUser = true;
  if(!currentUser)
  {
    return <Navigate to="/" replace={true} />
  }
  return children;
}