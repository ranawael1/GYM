import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
function BranchClasses(props) {
    const params = useParams();
    const [classes, setClasses] = useState([])
    useEffect(() => {
        axios
            .get(`/physio-slim/branch-classes/${params.id}?format=json`)
            .then((res) => setClasses(res.data))
            .catch((err) => console.log(err))
    }, [params.id])


    return (
            <div >
                <h1>Classes</h1>
                {/* classe because class is a reserved word */}
                {classes.map(classe => {
                    return (
                        <>
                            <ul>
                                {/* Class here starts with a capital letter  */}
                                <li>{classe.Class}</li>
                                <li>{classe.description}</li>
                                <li> <img src={classe.photo}/> </li>
                                {classe.photo && (<li> <img src={classe.photo}/> </li>)}
                            </ul>
                        </>
                    )
                })}
            </div>
    );
}

export default BranchClasses;