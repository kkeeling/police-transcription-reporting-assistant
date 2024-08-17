import React from 'react'

const Navigation: React.FC = () => {
  return (
    <nav className="bg-gray-200 p-4">
      <ul className="flex space-x-4">
        <li><a href="#" className="text-blue-600 hover:underline">Home</a></li>
        <li><a href="#" className="text-blue-600 hover:underline">Transcription</a></li>
        <li><a href="#" className="text-blue-600 hover:underline">Report Generation</a></li>
      </ul>
    </nav>
  )
}

export default Navigation
