import React from "react";


export default function Input(props) {
  return (
    <div className="mb-3">
      <label htmlFor={props.id} className="form-label">
        {props.label}
      </label>
      <input
        type={props.type}
        className={`form-control ${props.errors ? "border-danger" : ""}`}
        id={props.id}
        placeholder={props.placeHolder}
        aria-describedby={props.name}
        value={props.value}
        onChange={(e) => props.onChange(e)}
        name={props.name}
      />
      <div id={props.id} className="form-text text-danger">
        {props.errors}
      </div>
    </div>
  );
}