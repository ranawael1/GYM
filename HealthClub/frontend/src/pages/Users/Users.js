import React from 'react';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom'
import './../../components/styles/main.css'
import './../../components/styles/color.css'
function Users(props) {
    const params = useParams();
    let [result, setResult] = useState(null)

    useEffect(() => {
        axios
            // .get(`../../api-class-subscribers/${params.id}?format=json`)
            .get(`https://fakestoreapi.com/products/`)

            .then((res) => {
                result = res.data
                setResult(result)
                console.log(result)
            })
            .catch((err) => console.log(err))
    }, [params.id]
    )

    return (
        <div className='text-center'>
            <h1> Class</h1>
            {result &&
                <div className='row'>
                    <table class="table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Username</th>
                                <th>Phone</th>
                                <th>Email</th>
                                <th>Gender</th>
                                <th>Age</th>
                            </tr>
                        </thead>  <tbody>
                            {result.map((user, index) => (
                                <tr>
                                    <td>{user.id}</td>
                                    <td>{user.username}</td>
                                    <td>{user.phone}</td>
                                    <td>{user.email}</td>
                                    <td>{user.gender}</td>
                                    <td>{user.age}</td>
                                </tr>
                            )
                            )}</tbody>
                    </table>

                </div>
            }

        </div>
    );
}

export default Users;