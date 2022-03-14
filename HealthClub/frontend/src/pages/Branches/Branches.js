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
            // .get('../api-branches/?format=json')
            .get(`https://fakestoreapi.com/products/`)

            .then((res) => {
                result = res.data
                setResult(result)
                console.log(res.data)
                console.log(result)

            }
            )


            .catch((err) => console.log(err))
    }, []
    )
    // const onSubmit = (e) => {
    //     e.preventDefault()
    //     axios.defaults.xsrfHeaderName = "X-CSRFToken";
    //     axios.defaults.xsrfCookieName = 'csrftoken';
    //     axios.defaults.withCredentials = true
    //     axios.post('physio-slim/add-user/', newUser)
    //         .then((res) => {
    //             console.log(res.data)
    //             history.push({
    //                 pathname: '/data/classes',
    //                 state: { detail: res.data }
    //             })
    //         })
    //         .catch((err) => { setErrResponse(err.response.data); 
    //             console.log(err.response.data);
    //         })


    // }
    return (
        <div className='text-center'>
            <h1 className='yellow-color'> test</h1>

            {result &&
                <div className='row'>
                    {result.map((branch,index) =>  (
                        <div className='col-4' key={index}>
                            <Link to={`/data/classes/${branch.id}`} > <p>{branch.id}</p></Link> 
                         </div>
       
                        )
                    )}
                </div>
            }

        </div>
    );
}

export default Branches;