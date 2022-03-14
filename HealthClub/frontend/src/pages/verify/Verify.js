import React from 'react';
import axios from 'axios';
import { useState } from 'react';
import { useHistory, useLocation } from 'react-router-dom';
function Verify(props) {
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.withCredentials = true
    let history = useHistory()
    const location = useLocation()
    const user = location.state.detail
    console.log(user)
    const [verify, setVerify] = useState({
        code: null
    })
    const [errResponse, setErrResponse] = useState()
    const onChange = (e) => {
        setVerify({
            code: e.target.value
        })

    }
    const onSubmit = (e) => {
        e.preventDefault()   
            axios.post(`physio-slim/api-verify/`,verify,{
                params: user
            })
            .then((res)=>{console.log(res.data)
                history.push({
                    pathname: '/login',
                    state: { detail: res.data}
                })
            })
            .catch((err) => { 
                if (err.response) {
                    setErrResponse(err.response.data); 
                    console.log(err.response.data);
                }
            })    
    }
    return (
        <>
            <form className=" loginForm col-10 col-md-5" onSubmit={(e) => onSubmit(e)}>
                <div className="form-group input-div my-2">
                  
                            <label className="col-form-label">Verify</label>
                     
                            <div className="parent">
                                <input type="text"
                                    className={`form-control input-field ${props.errors && ("border-danger")}`}
                                    id={props.id}
                                    onChange={(e) => onChange(e)}
                                    name={"verify"}
                                />
                            </div>
                        </div>
                        {errResponse&&
                        (<p className='text-danger'>{errResponse.error}</p>)
                        }
                <br></br>
                
                <button type="submit" className="btn btn-success " name="button"
                disabled={verify.code===null || verify.code===""? true: false}
                >Submit</button>
            </form>
        </>
    );
}

export default Verify;