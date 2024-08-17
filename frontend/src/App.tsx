import React from 'react'
import Header from './components/Header'
import Navigation from './components/Navigation'
import Footer from './components/Footer'
import SampleComponent from './components/SampleComponent'

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <Navigation />
      <main className="flex-grow container mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold mb-4">Welcome to the application</h2>
        <p className="mb-4">Development is in progress.</p>
        <SampleComponent />
      </main>
      <Footer />
    </div>
  )
}

export default App
