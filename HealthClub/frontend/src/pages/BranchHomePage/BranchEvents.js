import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function BranchEvents(props) {
    const params = useParams();
    const [events, setEvent] = useState([])
    useEffect(() => {
        axios
            .get(`/physio-slim/branch-events/${params.id}?format=json`)
            .then((res) => setEvent(res.data))
            .catch((err) => console.log(err))
    }, [params.id])


    return (
            <div>
                <h1>Events</h1>
                {events.map(event => {
                    return (
                        <>
                            <ul>
                                <li>{event.event}</li>
                                <li>{event.description}</li>
                                {event.photo && (<li>{event.photo}</li>)}
                            </ul>
                        </>
                    )
                })}
            </div>
    );
}

export default BranchEvents;