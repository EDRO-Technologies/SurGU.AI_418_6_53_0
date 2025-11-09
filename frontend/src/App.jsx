import { Routes, Route } from 'react-router-dom'
import LoginPage from './LoginPage'
import DashboardPage from './DashboardPage'
import DocumentsPage from './DocumentsPage'
import StatisticsPage from './StatisticsPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/documents" element={<DocumentsPage />} />
      <Route path="/statistics" element={<StatisticsPage />} />
    </Routes>
  )
}

export default App
