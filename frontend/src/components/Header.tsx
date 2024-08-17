import React from 'react'

const Header: React.FC = () => {
  return (
    <header className="text-white p-4">
      <h1 className="text-3xl font-bold">Police Report Generator</h1>
      <p className="text-lg">Upload an audio file or dictate your report and let the AI handle the formatting.</p>
    </header>
  )
}

export default Header
