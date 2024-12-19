import './App.css';
import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom';

import Auth from './pages/auth'
import Navigate from './pages/admin_panel';
import Error from './pages/not_found';
import Catalog from './pages/catalog/catalog'

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Catalog/>}/>
          <Route path="admin_panel" element={<Navigate/>}/>
          <Route path="sing_in_admin" element={<Auth/>}/>
          <Route path="*" element={<Error/>}/>
        </Routes>
      </BrowserRouter>
  );
}

export default App;