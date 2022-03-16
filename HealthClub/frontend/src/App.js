import './App.css';
import {BrowserRouter, Route, Switch} from 'react-router-dom'
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
    </Switch>
    </div>
  </BrowserRouter>
  </>
  );
}

export default App;
