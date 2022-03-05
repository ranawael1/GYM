import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function BranchDetails(props) {
    const params = useParams();
    const [branch, setBranch] = useState([])
    useEffect(() => {
        axios
            .get(`/physio-slim/branch-one/${params.id}?format=json`)
            .then((res) => setBranch(res.data))
            .catch((err) => console.log(err))
    }, [params.id])


    return (
            <div>
                <h1>Branch Details</h1>
                        <>
                            <ul>
                                <li>{branch.name}</li>
                                <li>{branch.address}</li>
                                <li>{branch.phone}</li>
                            </ul>
                        </>
            </div>
    );
}

export default BranchDetails;