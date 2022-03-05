import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function BranchClinics(props) {
    const params = useParams();
    const [clinics, setClinic] = useState([])
    useEffect(() => {
        axios
            .get(`/physio-slim/branch-clinics/${params.id}?format=json`)
            .then((res) => setClinic(res.data))
            .catch((err) => console.log(err))
    }, [params.id])

    return (
            <div>
                <h1>Clinics</h1>
                {clinics.map(clinic => {
                    return (
                        <>
                            <ul>
                                <li>{clinic.clinic}</li>
                                <li>{clinic.description}</li>
                                {clinic.photo && (<li>{clinic.photo}</li>)}
                            </ul>
                        </>
                    )
                })}
            </div>
    );
}

export default BranchClinics;