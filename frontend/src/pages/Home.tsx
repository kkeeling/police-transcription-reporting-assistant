import React from 'react'
import PoliceReportGenerator from '../components/PoliceReportGenerator'

const Home: React.FC = () => {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Welcome to Police Transcription & Report Generation</h2>
      <PoliceReportGenerator />
    </div>
  )
}

export default Home
