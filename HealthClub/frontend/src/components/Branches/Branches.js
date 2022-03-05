import React from 'react';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { Link } from "react-router-dom";
function Branches(props) {
    const [branches, setBranches] = useState([])
    useEffect(() => {
        axios.get('/physio-slim/branch-all/?format=json')
            .then((res) => setBranches(res.data))
            .catch((err) => console.log(err))
    }, []
    )

    return (
        <>
            {/* looping over the branches */}
            {branches.map(branch => {
                return (
                  <li className="nav-item">
                        <Link key={branch.id} className="nav-link" to={`/branch/${branch.id}`}>{branch.name}</Link>
                  </li>
                )
              })}
            {/* ends here */}

        </>
    );
}

export default Branches;