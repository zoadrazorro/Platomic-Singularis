import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Architecture from './pages/Architecture'
import InfinityEngine from './pages/InfinityEngine'
import Philosophy from './pages/Philosophy'
import GettingStarted from './pages/GettingStarted'
import API from './pages/API'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/architecture" element={<Architecture />} />
        <Route path="/infinity-engine" element={<InfinityEngine />} />
        <Route path="/philosophy" element={<Philosophy />} />
        <Route path="/getting-started" element={<GettingStarted />} />
        <Route path="/api" element={<API />} />
      </Routes>
    </Layout>
  )
}

export default App
