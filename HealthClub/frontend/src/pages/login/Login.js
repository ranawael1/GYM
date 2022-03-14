import React from 'react';
import { useLocation } from 'react-router-dom';

function Login(props) {
    const location = useLocation()
    let success
    if (location.state!= null) {
        success = location.state.detail.message
    }
    else {
        success = null
    }
    return (
        <div>
            <h1>Login page check</h1>
            <p>{success}</p>
        </div>
    );
}

export default Login;