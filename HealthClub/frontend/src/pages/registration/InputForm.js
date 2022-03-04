import { useEffect, useState } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons'
import "./../../components/styles/color.css"

export default function InputForm(props) {
    const [eye, setEye] = useState({
        value: faEyeSlash,
        type: "password",
        // hide: "hidden"
    })
    let [data, setData]= useState()

    const showPassword = (e) => {
        if (eye.value === faEyeSlash) {
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
                
                        <label htmlFor="exampleInputEmail1" className="col-form-label gray-color">{props.label}</label>
                
                        <div className="parent">
                            <input type={props.type === "password" ? eye.type : props.type}
                                // className={`form-control input-field ${(props.errors == null || props.errors == "") ? "" : "border-danger"}`}
                                className={`form-control input-field ${props.errors || props.errorResponse&& ("border-danger")}`}
                                id={props.id}
                                aria-describedby="emailHelp"
                                onChange={(e) => {props.handleChange(e)}}
                                name={props.type}
                                value = {props.value!= null?props.value: ""}
                            />
                            {props.eye && <span onClick={(e) => showPassword(e)}
                                className="eye"><FontAwesomeIcon icon={eye.value} />
                            </span>}
                        </div>
                    </div>
             
            <small id="emailHelp" className="form-text text-danger" >
                {props.errors && (props.errors)}
                {props.errorResponse && (props.errorResponse)}
            </small>
        </>
    )
}