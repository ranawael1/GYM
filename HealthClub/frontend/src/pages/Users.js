import React from 'react';
import axios from 'axios';
import { useEffect } from 'react';
function Users(props) {
    useEffect(() => {
        axios.get('physio-slim/users/?format=json')
        .then((res) => console.log(res.data))
        .catch((err) => console.log(err))
    }, []
    )
    return (
        <div>

        </div>
    );
}

export default Users;