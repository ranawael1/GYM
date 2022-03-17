import React from 'react';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { useParams, useHistory, useLocation } from 'react-router-dom';
import './../../components/styles/main.css'
import './../../components/styles/color.css'
function Users(props) {
    let history = useHistory()
    
    let location = useLocation()
    console.log(window.location.host)
    const params = useParams();
    let [result, setResult] = useState(null)
    let [result2, setResult2] = useState(null)

    useEffect(() => {
        let req1 = axios.get(`../../api-class-subscribers/${params.id}?format=json`)
        let req2 = axios.get(`../../api-class/${params.id}?format=json`)
        axios
            .all([req1, req2])
            //.get(`https://fakestoreapi.com/products/`)

            .then(axios.spread((res1, res2) => {
                result = res1.data
                result2 = res2.data["Class"]
                setResult(result)
                setResult2(result2)
                console.log(result)
                console.log(res2.data['Class'])

            }))
            .catch((err) => {
                console.log(err)
                window.location.href='http://127.0.0.1:8000'
            }
            
            )
    }, [params.id]
    )

    return (
        <div className='text-center container-fluid'>
            <h1 className=' text-capitalize text-light mb-5'> {result2}</h1>
            {result &&
                    <table className="table table-hover " style={{width: '100%'}}>
                        <thead>
                            <tr className='yellow-background'>
                                <th>ID</th>
                                <th>Username</th>
                                <th>Phone</th>
                                <th>Email</th>
                                <th>Gender</th>
                                <th>Age</th>
                            </tr>
                        </thead>  
                        <tbody className='black-background'>
                            {result.map((user, index) => (
                                <tr className='text-light background-gray'>
                                    <td>{user.id}</td>
                                    <td>{user.username}</td>
                                    <td>{user.phone}</td>
                                    <td>{user.email}</td>
                                    <td>{user.gender}</td>
                                    <td>{user.age}</td>
                                </tr>
                                )
                            )}
                        </tbody>
                    </table>

                
            }

        </div>
    );
}

export default Users;