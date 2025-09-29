import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)

  // ✅ Charger la valeur initiale depuis FastAPI
  useEffect(() => {
    const fetchCount = async () => {
      try {
        const response = await fetch('http://localhost:8000/count')
        if (!response.ok) throw new Error('Failed to fetch count')
        const data = await response.json()
        setCount(data.count)
      } catch (error) {
        console.error('Erreur lors du fetch count:', error)
      }
    }
    fetchCount()
  }, [])

  // ✅ Incrémenter le count via FastAPI
  const incrementCount = async () => {
    if (loading) return
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/count/increment', {
        method: 'POST'
      })
      if (!response.ok) throw new Error('Failed to increment')
      const data = await response.json()
      setCount(data.count)
    } catch (error) {
      console.error('Erreur increment:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <h1>REACT Counter & FastAPI</h1>
      <div className="card">
        <button onClick={incrementCount} disabled={loading || count === null}>
          {loading
            ? 'Loading...'
            : `count is ${count !== null ? count : '...'}`}
        </button>
      </div>
    </>
  )
}

export default App
