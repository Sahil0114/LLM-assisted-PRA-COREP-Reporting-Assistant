import { useState } from 'react'
import QueryInterface from './components/QueryInterface'
import TemplateViewer from './components/TemplateViewer'
import ValidationPanel from './components/ValidationPanel'
import AuditTrail from './components/AuditTrail'

function App() {
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)
    const [activeTab, setActiveTab] = useState('template')

    const handleQuery = async (question, scenario) => {
        setLoading(true)
        setError(null)

        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question,
                    scenario,
                    template_type: 'C01'
                }),
            })

            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`)
            }

            const data = await response.json()
            setResult(data)
            setActiveTab('template')
        } catch (err) {
            setError(err.message)
            console.error('Query failed:', err)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="app-container">
            <header className="header">
                <div className="header-title">
                    <svg className="card-title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <h1>COREP Reporting Assistant</h1>
                    <span className="header-badge">Prototype</span>
                </div>
                <div className="header-badge" style={{ background: 'rgba(16, 185, 129, 0.2)', color: '#10b981', borderColor: 'rgba(16, 185, 129, 0.4)' }}>
                    C01 - Own Funds
                </div>
            </header>

            <main className="main-grid">
                <div className="left-column">
                    <div className="card">
                        <div className="card-header">
                            <h2 className="card-title">
                                <svg className="card-title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                Regulatory Query
                            </h2>
                        </div>
                        <div className="card-content">
                            <QueryInterface onSubmit={handleQuery} loading={loading} />
                        </div>
                    </div>

                    {error && (
                        <div className="card" style={{ marginTop: '1.5rem', borderColor: 'rgba(239, 68, 68, 0.5)' }}>
                            <div className="card-content">
                                <div className="validation-item error">
                                    <svg className="validation-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <div className="validation-content">
                                        <div className="validation-rule">Error</div>
                                        <div className="validation-message">{error}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                <div className="right-column">
                    <div className="card">
                        <div className="card-header">
                            <h2 className="card-title">
                                <svg className="card-title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                                Results
                            </h2>
                        </div>
                        <div className="card-content">
                            {!result ? (
                                <div className="empty-state">
                                    <svg className="empty-state-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                                        <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                                    </svg>
                                    <h3 className="empty-state-title">No Results Yet</h3>
                                    <p className="empty-state-description">
                                        Enter a question about own funds requirements and a scenario to populate the COREP template.
                                    </p>
                                </div>
                            ) : (
                                <>
                                    <div className="tabs">
                                        <button
                                            className={`tab-btn ${activeTab === 'template' ? 'active' : ''}`}
                                            onClick={() => setActiveTab('template')}
                                        >
                                            Template
                                        </button>
                                        <button
                                            className={`tab-btn ${activeTab === 'validation' ? 'active' : ''}`}
                                            onClick={() => setActiveTab('validation')}
                                        >
                                            Validation
                                        </button>
                                        <button
                                            className={`tab-btn ${activeTab === 'audit' ? 'active' : ''}`}
                                            onClick={() => setActiveTab('audit')}
                                        >
                                            Audit Trail
                                        </button>
                                    </div>

                                    {activeTab === 'template' && (
                                        <TemplateViewer data={result.template_data} />
                                    )}

                                    {activeTab === 'validation' && (
                                        <ValidationPanel results={result.validation_results} />
                                    )}

                                    {activeTab === 'audit' && (
                                        <AuditTrail entries={result.audit_trail} />
                                    )}
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </main>
        </div>
    )
}

export default App
