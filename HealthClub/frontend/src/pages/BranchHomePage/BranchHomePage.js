
import React from 'react';
import BranchClasses from './BranchClasses';
import BranchClinics from './BranchClinics';
import BranchDetails from './BranchDetails';
import BranchEvents from './BranchEvents';
import BranchOffers from './BranchOffers';
import BranchPersonalTrainers from './BranchPersonalTrainers';

function BranchHomePage(props) {
    return (
       <div className='container'>
        <BranchEvents className='row' />
        <BranchClasses className='row' />
        <BranchClinics className='row' />
        <BranchOffers className='row' />
        <BranchDetails className='row' />
        <BranchPersonalTrainers  className='row' />
       </div>
    );
}

export default BranchHomePage;