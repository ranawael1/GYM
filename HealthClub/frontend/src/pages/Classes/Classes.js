import React from 'react';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {Link} from 'react-router-dom'
import './../../components/styles/main.css'
import './../../components/styles/color.css'

function Classes(props) {
    const params = useParams();    
    let [result, setResult] = useState(null)

    useEffect(() => {
        axios
        // .get(`../../api-classes/${params.id}?format=json`)
        .get(`https://fakestoreapi.com/products/`)

        .then((res) =>{
            console.log(res.data)

            result = res.data
            setResult(result)
            console.log(result)
        })
        .catch((err) => console.log(err))
    }, [params.id]
    )

    return (
        <div className='text-center'>
            <h1 className='yellow-color'> Classes</h1>

            {result &&
                <div className='row'>
                    {result.map((cla,index) =>  (
                        <div className='col-4' key={index}>
                            <Link to={`/data/class/${cla.id}`} > <p>{cla.id}</p></Link> 
                         </div>
       
                        )
                    )}
                </div>
            }

        </div>
    );
}

export default Classes;