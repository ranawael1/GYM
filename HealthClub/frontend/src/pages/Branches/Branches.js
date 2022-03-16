import React from 'react';
import { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';
import {Link} from 'react-router-dom'
import './../../components/styles/main.css'
import './../../components/styles/color.css'

function Branches(props) {
    let [result, setResult] = useState(null)

    useEffect(() => {
        axios
            .get('../api-branches/?format=json')
            // .get(`https://fakestoreapi.com/products/`)

            .then((res) => {
                result = res.data
                setResult(result)
            }
            )
            .catch((err) => {
                console.log(err)
                window.location.href='http://127.0.0.1:8000'
            })
    }, []
    )
    return (
        <div className='text-center'>
            <h1 className='yellow-color'> Branches</h1>

            {result &&
                <div className='row'>
                    {result.map((branch,index) =>  (
                        <div className='col-4' key={index}>
                            <Link to={`/data/classes/${branch.id}`} className='text-light'> <p>{branch.name}</p></Link> 
                         </div>
       
                        )
                    )}
                </div>
            }
            <div>
            <Link to={`/data/classes/${branch.id}`} className='text-light'> <p> Back to Classes</p></Link> 
            <Link to={`/data/classes/${branch.id}`} className='text-light'> <p> Back to Branches</p></Link> 

            </div>

        </div>
    );
}

export default Branches;