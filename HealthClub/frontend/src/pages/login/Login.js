import React from 'react';
import { useLocation } from 'react-router-dom';

function Login(props) {
    const location = useLocation()
    const success = location.state.detail
    return (
        <div>
            <h1>Login page check</h1>
            <p>{success.message}</p>
        </div>
    );
}

export default Login;