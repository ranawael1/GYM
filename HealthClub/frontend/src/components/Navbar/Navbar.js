import React from 'react';
import {Link} from "react-router-dom";

function Navbar(props) {

    // let admin = window.location.host+'/admin'
    // console.log(admin)
    return (
        <>
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
  <div className="container-fluid">
   <Link className="navbar-brand" to={'/'}>Navbar</Link>
    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span className="navbar-toggler-icon"></span>
    </button>
    <div className="collapse navbar-collapse" id="navbarNav">
      <ul className="navbar-nav">
        <li className="nav-item">
         <Link className="nav-link active" aria-current="page" to={'/registration'}>Register</Link>
        </li>
        <li className="nav-item">
         <Link className="nav-link" to={"/login"}>Login</Link>
        </li>
        <li className="nav-item">
         <a className="nav-link"  href={'/'} target="_blank" rel="noopener noreferrer">Admin</a>
        </li>
        <li className="nav-item">
         <Link className="nav-link disabled" to={'/'} tabIndex="-1" aria-disabled="true">Disabled</Link>
        </li>
      </ul>
    </div>
  </div>
</nav>
        </>
    );
}

export default Navbar;