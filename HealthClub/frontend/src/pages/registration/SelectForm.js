import React from 'react';

function SelectForm(props) {
    let options = props.options
    return (
        <>
            <div className="form-group input-div my-2">
            <div className="row g-2 d-flex justify-content-between">
            <div className="col-3 ">
                <label htmlFor="exampleInputEmail1" className="col-form-label">{props.label}</label>
            </div>
            <div className="col-9 ">
                <div className="parent">
                <select className={`form-control form-select ${props.errors &&("border-danger")}`} 
                aria-label="Default select example" id={props.id}
                onChange={(e) => props.handleChange(e)}
                name={props.type}
                >
                    {options.map((select,index)=>(
                        <option value={select.value} key={index} >{select.option} </option>
                    ))}
                </select>
                </div>
                </div>
            </div> 
            </div>
            <small id="emailHelp" className="form-text text-danger" >     
                {props.errors && (props.errors)}
            </small>
   
        </>
    );
}

export default SelectForm;