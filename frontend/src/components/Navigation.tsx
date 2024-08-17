import React from 'react'
import { Link } from 'react-router-dom'

const Navigation: React.FC = () => {
  return (
    <nav className="bg-gray-200 p-4">
      <ul className="flex space-x-4">
        <li><Link to="/" className="text-blue-600 hover:underline">Home</Link></li>
        <li><Link to="/transcription" className="text-blue-600 hover:underline">Transcription</Link></li>
        <li><Link to="/report-generation" className="text-blue-600 hover:underline">Report Generation</Link></li>
      </ul>
    </nav>
  )
}

export default Navigation
