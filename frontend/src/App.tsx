import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import AppRouter from './routers/AppRouter';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRouter />
        <div className="bg-blue-500 text-white p-4">Hello</div>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;