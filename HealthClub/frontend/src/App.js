import './App.css';
import {BrowserRouter, Route, Switch} from 'react-router-dom'
import Registration from './pages/registration/Registration'
import Verify from './pages/verify/Verify';
import Login from './pages/login/Login';
import Navbar from './components/Navbar/Navbar';
import Users from './pages/Users';
function App() {
  let admin = window.location.host+'/admin'
  return (
  <>
  <BrowserRouter>
  <Navbar/>
  <div className='container my-5 d-flex justify-content-center' >
    <Switch>
      <Route exact path={'/registration'} component={Registration}/>
      <Route exact path={'/verify'} component={Verify}/>
      <Route exact path={'/login'} component={Login}/>
      <Route  exact path={'/users'} component={Users}/>
    </Switch>
    </div>
  </BrowserRouter>
  </>
  );
}

export default App;
