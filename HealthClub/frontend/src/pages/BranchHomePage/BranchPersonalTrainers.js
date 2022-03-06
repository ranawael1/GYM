import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function BranchPersonalTrainers(props) {
    const params = useParams();

    const [personalTrainers, setPersonalTrainers] = useState([])
    
    console.log(params)
    useEffect(() => {
        axios.get(`/physio-slim/branch-trainers/${params.id}?format=json`)
            .then((res) => setPersonalTrainers(res.data))
            .catch((err) => console.log(err))
    }, [params.id])
    return (
        <div>
            <h1>Personal Trainers</h1>
            {personalTrainers.map(personalTrainer => {
                return (
                    <>
                        <ul>
                            <li>{personalTrainer.name}</li>
                            <li>{personalTrainer.bio}</li>
                            <li>{personalTrainer.position}</li>
                            <li>{personalTrainer.years_of_experience}</li>
                        </ul>
                    </>
                )
            })}
        </div>
    );
}

export default BranchPersonalTrainers;