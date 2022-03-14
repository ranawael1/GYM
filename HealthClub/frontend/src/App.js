import './App.css';
import {BrowserRouter, Route, Switch} from 'react-router-dom'
import Registration from './pages/registration/Registration'
import Verify from './pages/verify/Verify';
import Login from './pages/login/Login';
import Classes from './pages/Classes/Classes';
import Branches from './pages/Branches/Branches';
import Users from './pages/Users/Users';
function App() {
  // let admin = window.location.host+'/admin'
  return (
  <>
  <BrowserRouter>
  <div className='container my-5 d-flex justify-content-center' >
    <Switch>
      <Route exact path={'/data/branches'} component={Branches}/>
      <Route exact path={'/data/classes/:id'} component={Classes}/>
      <Route exact path={'/data/class/:id'} component={Users}/>

      <Route exact path={'/registration'} component={Registration}/>
      <Route exact path={'/verify'} component={Verify}/>
      <Route exact path={'/login'} component={Login}/>
      {/* <Route  exact path={'/users'} component={Users}/>
      <Route  exact path={'/branches'} component={Branches}/>
      <Route  exact path={'/branch/:id?'} component={BranchHomePage}/> */}
    </Switch>
    </div>
  </BrowserRouter>
  </>
  );
}

export default App;
