function ValidationPanel({ results }) {
    if (!results || results.length === 0) {
        return (
            <div className="empty-state" style={{ padding: '2rem' }}>
                <svg className="empty-state-icon" style={{ width: '48px', height: '48px' }} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <h3 className="empty-state-title">No Validation Results</h3>
                <p className="empty-state-description">
                    Validation will run after template population
                </p>
            </div>
        )
    }

    const errors = results.filter(r => !r.passed && r.severity === 'ERROR')
    const warnings = results.filter(r => !r.passed && r.severity === 'WARNING')
    const passed = results.filter(r => r.passed)

    return (
        <div className="validation-panel">
            {/* Summary */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 1fr)',
                gap: '0.75rem',
                marginBottom: '1rem'
            }}>
                <div style={{
                    padding: '0.75rem',
                    background: errors.length > 0 ? 'rgba(239, 68, 68, 0.1)' : 'rgba(16, 185, 129, 0.1)',
                    borderRadius: '8px',
                    textAlign: 'center'
                }}>
                    <div style={{
                        fontSize: '1.5rem',
                        fontWeight: '700',
                        color: errors.length > 0 ? '#ef4444' : '#10b981'
                    }}>
                        {errors.length}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Errors</div>
                </div>
                <div style={{
                    padding: '0.75rem',
                    background: warnings.length > 0 ? 'rgba(245, 158, 11, 0.1)' : 'rgba(16, 185, 129, 0.1)',
                    borderRadius: '8px',
                    textAlign: 'center'
                }}>
                    <div style={{
                        fontSize: '1.5rem',
                        fontWeight: '700',
                        color: warnings.length > 0 ? '#f59e0b' : '#10b981'
                    }}>
                        {warnings.length}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Warnings</div>
                </div>
                <div style={{
                    padding: '0.75rem',
                    background: 'rgba(16, 185, 129, 0.1)',
                    borderRadius: '8px',
                    textAlign: 'center'
                }}>
                    <div style={{
                        fontSize: '1.5rem',
                        fontWeight: '700',
                        color: '#10b981'
                    }}>
                        {passed.length}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Passed</div>
                </div>
            </div>

            {/* Error Items */}
            {errors.length > 0 && (
                <div style={{ marginBottom: '1rem' }}>
                    <h4 style={{
                        fontSize: '0.75rem',
                        fontWeight: '600',
                        color: '#ef4444',
                        marginBottom: '0.5rem',
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em'
                    }}>
                        Blocking Errors
                    </h4>
                    {errors.map((result, idx) => (
                        <div key={idx} className="validation-item error">
                            <svg className="validation-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                            </svg>
                            <div className="validation-content">
                                <div className="validation-rule">{result.rule_id}: {result.rule_name}</div>
                                <div className="validation-message">{result.message}</div>
                                {result.affected_fields && result.affected_fields.length > 0 && (
                                    <div style={{
                                        marginTop: '0.25rem',
                                        fontSize: '0.75rem',
                                        color: 'var(--text-muted)'
                                    }}>
                                        Affected: {result.affected_fields.join(', ')}
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Warning Items */}
            {warnings.length > 0 && (
                <div style={{ marginBottom: '1rem' }}>
                    <h4 style={{
                        fontSize: '0.75rem',
                        fontWeight: '600',
                        color: '#f59e0b',
                        marginBottom: '0.5rem',
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em'
                    }}>
                        Warnings
                    </h4>
                    {warnings.map((result, idx) => (
                        <div key={idx} className="validation-item warning">
                            <svg className="validation-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <div className="validation-content">
                                <div className="validation-rule">{result.rule_id}: {result.rule_name}</div>
                                <div className="validation-message">{result.message}</div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Passed Rules (collapsed by default) */}
            {passed.length > 0 && (
                <details style={{ marginTop: '1rem' }}>
                    <summary style={{
                        cursor: 'pointer',
                        fontSize: '0.75rem',
                        fontWeight: '600',
                        color: '#10b981',
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em'
                    }}>
                        {passed.length} Rules Passed
                    </summary>
                    <div style={{ marginTop: '0.5rem' }}>
                        {passed.map((result, idx) => (
                            <div key={idx} className="validation-item success" style={{ padding: '0.5rem' }}>
                                <svg className="validation-icon" style={{ width: '16px', height: '16px' }} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                <div className="validation-content">
                                    <div className="validation-rule" style={{ fontSize: '0.75rem' }}>
                                        {result.rule_id}: {result.rule_name}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </details>
            )}
        </div>
    )
}

export default ValidationPanel
