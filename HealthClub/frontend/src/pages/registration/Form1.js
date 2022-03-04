import React, { useState } from 'react';
import InputForm from './InputForm';
function Form1(props) {
    let errors = props.errors
    let data = props.data
    let onChange = props.onChange

    return (
        <>
            <InputForm errors={errors.username}
                type={"text"}
                label={"Username"}
                id={"username"}
                handleChange={(e) => {onChange(e); }}
                value = {data.username}
                errorResponse = {props.errorResponse.username}

            />
            <InputForm errors={errors.email}
                type={"email"}
                label={"Email"}
                id={"email"}
                handleChange={(e) => onChange(e)
                }
                value = {data.email}
                errorResponse = {props.errorResponse.email}

            />

            <InputForm 
                type={"text"}
                label={"Phone"}
                id={"phone"}
                handleChange={(e) => onChange(e)}
                value = {data.phone}
                errorResponse = {props.errorResponse.phone}

            />
            <InputForm errors={errors.password}
                type={"password"}
                label={"Password "}
                id={"password"}
                handleChange={(e) => onChange(e)}
                hide={errors.hide}
                eye={true}
                value = {data.password}
                errorResponse = {props.errorResponse.password}
            />
            <InputForm errors={errors.confirmPassword}
                type={"password"}
                label={"Confirm Password "}
                id={"confirmPassword"}
                handleChange={(e) => onChange(e)}
                hide={errors.hide}
                value = {props.confirm}
                
            />
        </>
    );
}

export default Form1;