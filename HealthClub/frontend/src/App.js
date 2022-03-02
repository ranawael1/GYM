import './App.css';
import {BrowserRouter, Route, Switch} from 'react-router-dom'
import Registration from './pages/registration/Registration'
import Login from './pages/login/Login';
function App() {
  return (
  <>
  <BrowserRouter>
    <Switch>
      <Route exact path={'/registration'} component={Registration}/>
      <Route exact path={'/login'} component={Login}/>
    </Switch>
  </BrowserRouter>
  </>
  );
}

export default App;
