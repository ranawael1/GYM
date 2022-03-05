import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function BranchOffers(props) {
    const params = useParams();
    const [offers, setOffers] = useState([])
    useEffect(() => {
        axios
            .get(`/physio-slim/branch-offers/${params.id}?format=json`)
            .then((res) => setOffers(res.data))
            .catch((err) => console.log(err))
    }, [params.id])


    return (
            <div>
                <h1>Offers</h1>
                {offers.map(offer => {
                    return (
                        <>
                            <ul>
                                <li>offer:{offer.name}</li>
                                <li>classes:{offer.num_of_class}</li>
                                <li>discount:{offer.discount}</li>
                            </ul>
                        </>
                    )
                })}
            </div>
    );
}

export default BranchOffers;