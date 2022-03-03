import { useEffect, useState } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons'

export default function InputForm(props) {
    const [eye, setEye] = useState({
        value: faEyeSlash,
        type: "password",
        // hide: "hidden"
    })
    const showPassword = (e) => {
        if (eye.value == faEyeSlash) {
            setEye({
                ...eye,
                value: faEye,
                type: "text",

            })
        }
        else {
            setEye({
                ...eye,
                value: faEyeSlash,
                type: "password",
            })
        }
    }
    return (
        <>
            <div className="form-group input-div my-2">
                <div className="row g-2 d-flex justify-content-between">
                    <div className="col-3 ">
                        <label htmlFor="exampleInputEmail1" className="col-form-label">{props.label}</label>
                    </div>
                    <div className="col-9">
                        <div className="parent">
                            <input type={props.type == "password" ? eye.type : props.type}
                                // className={`form-control input-field ${(props.errors == null || props.errors == "") ? "" : "border-danger"}`}
                                className={`form-control input-field ${props.errors && ("border-danger")}`}
                                id={props.id}
                                aria-describedby="emailHelp"
                                onChange={(e) => props.handleChange(e)}
                                name={props.type}
                            />
                            {props.eye && <span onClick={(e) => showPassword(e)}
                                className="eye"><FontAwesomeIcon icon={eye.value} />
                            </span>}
                        </div>
                    </div>
                </div>



            </div>
            <small id="emailHelp" className="form-text text-danger" >
                {props.errors && (props.errors)}
            </small>
        </>
    )
}