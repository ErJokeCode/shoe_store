import './App.css';
import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom';

import Auth from '../src/pages/auth/auth'
import Navigate from './pages/admin_panel/admin_panel';
import Error from './pages/not_found/not_found';

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="admin_panel" element={<Navigate/>}/>
          <Route path="sing_in_admin" element={<Auth/>}/>
          <Route path="*" element={<Error/>}/>
        </Routes>
      </BrowserRouter>
    </div>
    
  );
}

export default App;