import React from "react";
import { Navigate } from "react-router-dom";
import useUserActions from "../hooks/user.actions.js";


function ProtectedRoute({ children }) {
    const { getUser } = useUserActions();
    const user = getUser();
    return user ? <>{children}</> : <Navigate to="/login/" />;
}

export default ProtectedRoute;
