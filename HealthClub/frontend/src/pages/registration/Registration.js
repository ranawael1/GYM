import React from 'react';
import InputForm from './InputForm';
import { useState } from "react";
import "./Registration.css"
import SelectForm from './SelectForm';
import axios from 'axios';
import { useHistory } from 'react-router-dom';
import Cookies from 'js-cookie';


function Registration(props) {

    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.xsrfCookieName = 'csrftoken';

    axios.defaults.withCredentials = true
    let history = useHistory()
    const [userData, setUserData] = useState({
        email: null,
        password: null,
        confirm: null,

    })
    const [newUser, setUser] = useState({
        username: null,
        email: null,
        phone: null,
        branch: null,
        gender: null,
        age: null,
        password: null,
        membership_num: null


    })

    const [errors, setErrors] = useState({
        email: "",
        password: "",
        confirmPassword: "",
        name: "",
        username: "",
        check: true,
        hide: "none"
        // init: true

    })
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
    const emailRegex = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/
    const usernameRegex = /\s/g
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])/
    const onChange = (e) => {

        if (e.target.id === "email") {
            setUserData({
                ...userData,
                email: e.target.value
            })
            setUser({
                ...newUser,
                email: e.target.value
            })
            setErrors({
                ...errors,
                email: e.target.value.length === 0 ? "Email is required!" : !emailRegex.test(e.target.value) ? "Email address is invalid!" : null,
                check: (e.target.value.length > 0 && emailRegex.test(e.target.value) && errors.password === null && errors.name === null) ? false : true,
                hide: errors.email !== null ? "none" : "hidden"
            })


        }
        else if (e.target.id === "password") {
            setUserData({
                ...userData,
                password: e.target.value
            })
            setUser({
                ...newUser,
                password: e.target.value
            })
            setErrors({
                ...errors,
                password: e.target.value.length === 0 ? "Password is required!" :
                    e.target.value.length < 8 ? "Password must be 8 or more characters." :
                        !passwordRegex.test(e.target.value) ? "Password must contain at least one uppercase letter, one lowercase letter, one number and one special character" : null,
                confirmPassword: e.target.value !== userData.confirm ? "Unmatched password" : null,
                check: (errors.email === null && e.target.value.length > 0 && e.target.value.length >= 8 && errors.name === null) ? false : true,
                hide: errors.password !== null ? "none" : "hidden"

            })
        }
        else if (e.target.id === "username") {
            setUserData({
                ...userData,
                username: e.target.value
            })
            setUser({
                ...newUser,
                username: e.target.value
            })
            setErrors({
                ...errors,
                username: e.target.value.length === 0 ? "User name is required!" : usernameRegex.test(e.target.value) ? "User name must have no spaces" : null,
                check: (errors.email === null && errors.password === null && e.target.value.length > 0) ? false : true,
                hide: errors.name !== null ? "none" : "hidden"
            })
        }
        else if (e.target.id === "confirmPassword") {
            setUserData({
                ...userData,
                confirm: e.target.value
            })

            setErrors({
                ...errors,
                confirmPassword: e.target.value !== userData.password ? "Unmatched password" : null,
                check: (errors.email == null && e.target.value.length > 0 && e.target.value.length >= 8 && errors.name == null) ? false : true,
                hide: errors.password !== null ? "none" : "hidden"
            })
        }
        else if ((e.target.id === "gender")) {
            setUser({
                ...newUser,
                gender: e.target.value
            })
        }
        else if ((e.target.id === "age")) {
            setUser({
                ...newUser,
                age: e.target.value
            })
        }
        else if ((e.target.id === "branch")) {
            setUser({
                ...newUser,
                branch: e.target.value
            })
        }
        else if ((e.target.id === "membership_num")) {
            setUser({
                ...newUser,
                membership_num: e.target.value
            })
        }
        else if ((e.target.id === "phone")) {
            setUser({
                ...newUser,
                phone: e.target.value
            })
        }

    }
    const onSubmit = (e) => {
        e.preventDefault()
        if (!errors.email && !errors.password) {
            console.log(newUser)
            axios.post('physio-slim/add-user/', newUser)
                .then((res) => {
                    console.log(res.data)
                    history.push({
                        pathname: '/verify',
                        state: { detail: res.data }
                    })
                })
                .catch((err) => { console.log(err) })


        }

    }
    return (
        <>
            <form className=" loginForm col-10 col-md-5" onSubmit={(e) => onSubmit(e)}>
                <h1>Registration</h1>
                <InputForm errors={errors.username}
                    type={"text"}
                    label={"Username"}
                    id={"username"}
                    handleChange={(e) => onChange(e)}
                />
                <InputForm errors={errors.email}
                    type={"email"}
                    label={"Email"}
                    id={"email"}
                    handleChange={(e) => onChange(e)
                    }
                />
                <SelectForm
                    label={"Branch "}
                    id={"branch"}
                    handleChange={(e) => onChange(e)}
                    hide={errors.hide}
                    options={branch}
                />
                <SelectForm
                    label={"Gender "}
                    id={"gender"}
                    handleChange={(e) => onChange(e)}
                    hide={errors.hide}
                    options={gender}
                />
                <InputForm errors={errors.username}
                    type={"number"}
                    label={"Age"}
                    id={"age"}
                    handleChange={(e) => onChange(e)}
                />
                <InputForm errors={errors.username}
                    type={"text"}
                    label={"Phone"}
                    id={"phone"}
                    handleChange={(e) => onChange(e)}
                />
                <InputForm errors={errors.password}
                    type={"password"}
                    label={"Password "}
                    id={"password"}
                    handleChange={(e) => onChange(e)}
                    hide={errors.hide}
                    eye={true}
                />
                <InputForm errors={errors.confirmPassword}
                    type={"password"}
                    label={"Confirm Password "}
                    id={"confirmPassword"}
                    handleChange={(e) => onChange(e)}
                    hide={errors.hide}
                />
                <InputForm errors={errors.username}
                    type={"text"}
                    label={"Membership No. (if you have)"}
                    id={"membership_num"}
                    handleChange={(e) => onChange(e)}
                />
                <br></br>
                <button type="submit" className="btn btn-success SignupButton" name="button"
                // disabled={errors.check ||
                //  errors.email || 
                //  errors.password ||
                //  errors.name ||
                //  errors.username ||
                //  errors.confirmPassword
                //  }
                >Register</button>
            </form>
        </>
    );
}

export default Registration;