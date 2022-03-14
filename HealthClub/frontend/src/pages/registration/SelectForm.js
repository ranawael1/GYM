import React from 'react';
import "./../../components/styles/color.css";

function SelectForm(props) {
    let options = props.options
    return (
        <>
            <div className="form-group input-div my-2">
            
                <label htmlFor="exampleInputEmail1" className="col-form-label gray-color">{props.label}</label>
         
                <div className="parent">
                <select className={`form-control form-select ${props.errors &&("border-danger")}`} 
                aria-label="Default select example" id={props.id}
                onChange={(e) => props.handleChange(e)}
                name={props.type}
                defaultValue={props.value&&(props.value)}
                >
                    {options.map((select,index)=>(
                        <option value={select.value} key={index} >{select.option} </option>
                    ))}
                
                </select>
                </div>
                </div>
         
                <small id="emailHelp" className="form-text text-danger" >
                {props.errors && (props.errors)}
                {props.errorResponse && (props.errorResponse)}
            </small>
        </>
    );
}

export default SelectForm;