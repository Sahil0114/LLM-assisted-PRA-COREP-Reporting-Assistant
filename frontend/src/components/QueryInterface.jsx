import { useState } from 'react'

function QueryInterface({ onSubmit, loading }) {
    const [question, setQuestion] = useState('')
    const [scenario, setScenario] = useState('')

    const handleSubmit = (e) => {
        e.preventDefault()
        if (question.trim()) {
            onSubmit(question, scenario)
        }
    }

    // Sample questions for quick testing
    const sampleQuestions = [
        {
            question: "What are the CET1 capital requirements for this bank?",
            scenario: "A UK bank with £1B in ordinary share capital, £200M retained earnings, £50M AT1 instruments, and £100M Tier 2 subordinated debt."
        },
        {
            question: "Calculate the total own funds for this institution",
            scenario: "The bank has £500M CET1 instruments (ordinary shares), £150M share premium, £300M retained earnings, £75M Additional Tier 1 capital, and £125M Tier 2 instruments."
        }
    ]

    const loadSample = (sample) => {
        setQuestion(sample.question)
        setScenario(sample.scenario)
    }

    return (
        <form className="query-interface" onSubmit={handleSubmit}>
            <div className="form-group">
                <label className="form-label" htmlFor="question">
                    Question
                </label>
                <textarea
                    id="question"
                    className="form-textarea"
                    placeholder="Enter your question about COREP own funds reporting..."
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    rows={3}
                />
            </div>

            <div className="form-group">
                <label className="form-label" htmlFor="scenario">
                    Scenario Description
                </label>
                <textarea
                    id="scenario"
                    className="form-textarea"
                    placeholder="Describe the bank's capital position, e.g., 'A bank with £1B in ordinary shares, £200M retained earnings...'"
                    value={scenario}
                    onChange={(e) => setScenario(e.target.value)}
                    rows={4}
                />
            </div>

            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginRight: '0.5rem' }}>Quick examples:</span>
                {sampleQuestions.map((sample, idx) => (
                    <button
                        key={idx}
                        type="button"
                        onClick={() => loadSample(sample)}
                        style={{
                            padding: '0.25rem 0.75rem',
                            fontSize: '0.75rem',
                            background: 'var(--bg-tertiary)',
                            border: '1px solid var(--border-color)',
                            borderRadius: '4px',
                            color: 'var(--text-secondary)',
                            cursor: 'pointer',
                            transition: 'all 150ms ease'
                        }}
                        onMouseOver={(e) => {
                            e.target.style.borderColor = 'var(--accent-blue)'
                            e.target.style.color = 'var(--accent-blue)'
                        }}
                        onMouseOut={(e) => {
                            e.target.style.borderColor = 'var(--border-color)'
                            e.target.style.color = 'var(--text-secondary)'
                        }}
                    >
                        Example {idx + 1}
                    </button>
                ))}
            </div>

            <button
                type="submit"
                className="btn btn-primary"
                disabled={loading || !question.trim()}
            >
                {loading ? (
                    <>
                        <span className="loading-spinner" />
                        Processing...
                    </>
                ) : (
                    <>
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        Generate Template
                    </>
                )}
            </button>
        </form>
    )
}

export default QueryInterface
