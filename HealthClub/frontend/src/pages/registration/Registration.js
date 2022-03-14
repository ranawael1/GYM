import React from 'react';
import InputForm from './InputForm';
import { useState , useEffect} from "react";
import "./Registration.css"
import SelectForm from './SelectForm';
import axios from 'axios';
import { useHistory } from 'react-router-dom';
import Cookies from 'js-cookie';
import Form1 from './Form1';
import Form2 from './Form2';
import {faChevronLeft, faChevronRight}from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import "./../../components/styles/color.css";
function Registration(props) {
    let history = useHistory()
    let [next, setNext] = useState({
        next: false
    })
    const [password, setPassword] = useState({
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
        password: "",
        confirmPassword: "",
        username: ""
    })
    const [errResponse,setErrResponse] = useState({
        username: null,
        email: null,
        phone: null,
        branch: null,
        gender: null,
        age: null,
        password: null,
        membership_num: null
    })
    const emailRegex = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/
    const usernameRegex = /\s/g

    const changeForm =(check)=>{
        if (check === "next"){
            setNext({
                next: true
            })
        }
        else{
            setNext({
                next: false
            })
        }
       
    }
    useEffect(()=>{}, [next])
  
    const onChange = (e) => {
        if (e.target.id === "email") {
            setUser({
                ...newUser,
                email: e.target.value
            })
        }
        else if (e.target.id === "password") {
            setPassword({
                ...password,
                password: e.target.value
            })
            setUser({
                ...newUser,
                password: e.target.value
            })
            setErrors({
                ...errors,
                confirmPassword: e.target.value !== password.confirm ? "Unmatched password" : null,
            })
        }
        else if (e.target.id === "username") {
            setUser({
                ...newUser,
                username: e.target.value
            })
            setErrors({
                ...errors,
                username: e.target.value.length === 0 ? "User name is required!" : usernameRegex.test(e.target.value) ? "User name must have no spaces" : null,
            })
        }
        else if (e.target.id === "confirmPassword") {
            setPassword({
                ...password,
                confirm: e.target.value
            })
            setErrors({
                ...errors,
                confirmPassword: e.target.value !== password.password ? "Unmatched password" : null,
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
        if (!errors.confirmPassword && !errors.password && !errors.username) {
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.withCredentials = true
            console.log(newUser)
            axios.post('physio-slim/add-user/', newUser)
                .then((res) => {
                    console.log(res.data)
                    history.push({
                        pathname: '/verify',
                        state: { detail: res.data }
                    })
                })
                .catch((err) => { setErrResponse(err.response.data); 
                    console.log(err.response.data);
                })
        }

    }
    return (
        <>
            <form className=" loginForm col-10 col-md-5" onSubmit={(e) => onSubmit(e)}>
                <h1 className='gray-color'>Registration</h1>
                {
                    next.next !== true  
                    ?
                    <>
                    <Form1  
                    errors={errors}
                    onChange={(e) => onChange(e)}
                    data = {newUser}
                    confirm={password.confirm}
                    errorResponse = {errResponse}
                    />
                     <br></br>
                    <button type="button" className="btn btn-light float-end " name="button" onClick={()=>{changeForm('next')}}
                >Next <FontAwesomeIcon icon={faChevronRight}/></button>
                    </>
                    :
                    <>
                    <Form2
                    errors={errors}
                    onChange={(e) => onChange(e)}
                    data = {newUser}
                    errorResponse = {errResponse}
                    />
                    <br></br>
                    {errResponse.username ||errResponse.email || errResponse.phone || errResponse.password?
                     <button type="button" className="btn btn-light SignupButton text-danger" name="button" onClick={()=>{changeForm('back')}}
                > <FontAwesomeIcon icon={faChevronLeft}/>Back</button>
                :
                <button type="button" className="btn btn-light SignupButton" name="button" onClick={()=>{changeForm('back')}}
                > <FontAwesomeIcon icon={faChevronLeft}/>Back</button>
                }
                    <button type="submit" className="btn btn-success SignupButton float-end gray-background" name="button"
                disabled={
                 errors.password ||
                 errors.username ||
                 errors.confirmPassword
                 }
                //  disabled= {Object.values(newUser).map((ele, index)=>{
                //     return(ele===null||ele==="")
                    
                //  })&& (true)}
                >Register</button></>
                    
                }
                

              
               
                <br></br>
                
            </form>
        </>
    );
}

export default Registration;