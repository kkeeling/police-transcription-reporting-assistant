import React from 'react'
import Header from './components/Header'
import Footer from './components/Footer'
import PoliceReportGenerator from './components/PoliceReportGenerator'

const App: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen bg-black text-white">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-8">
        <PoliceReportGenerator />
      </main>
      <Footer />
    </div>
  )
}

export default App
