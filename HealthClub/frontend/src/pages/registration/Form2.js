import React from 'react';
import InputForm from './InputForm';
import SelectForm from './SelectForm';
function Form2(props) {
    let errors = props.errors
    let onChange = props.onChange
    let data = props.data
    const gender = [
        { option: "Choose your gender", value: null },
        { option: "Male", value: "male" },
        { option: "Female", value: "female" },
    ]
    const branch = [
        { option: "Choose your branch", value: null },
        { option: "Branch 1", value: "branch1" },
        { option: "Branch 2", value: "branch2" },
        { option: "Branch 3", value: "branch3" },
    ]
    return (
        <>
            <SelectForm
                label={"Branch "}
                id={"branch"}
                handleChange={(e) => onChange(e)}
                hide={errors.hide}
                options={branch}
                value = {data.branch}
                errorResponse = {props.errorResponse.branch}

            />
            <SelectForm
                label={"Gender "}
                id={"gender"}
                handleChange={(e) => onChange(e)}
                hide={errors.hide}
                options={gender}
                value = {data.gender}
                errorResponse = {props.errorResponse.gender}

            />

            <InputForm 
                type={"number"}
                label={"Age"}
                id={"age"}
                handleChange={(e) => onChange(e)}
                value = {data.age}
                errorResponse = {props.errorResponse.age}

            />

            <InputForm
                type={"text"}
                label={"Membership No. (if you have)"}
                id={"membership_num"}
                handleChange={(e) => onChange(e)}
                value = {data.membership_num}
                errorResponse = {props.errorResponse.membership_num}

            />
           
        </>
    );
}

export default Form2;