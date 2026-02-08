function formatCurrency(value, currency = 'GBP') {
    if (value === null || value === undefined) return '—'

    return new Intl.NumberFormat('en-GB', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value)
}

function AuditTrail({ entries }) {
    if (!entries || entries.length === 0) {
        return (
            <div className="empty-state" style={{ padding: '2rem' }}>
                <svg className="empty-state-icon" style={{ width: '48px', height: '48px' }} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
                </svg>
                <h3 className="empty-state-title">No Audit Trail</h3>
                <p className="empty-state-description">
                    Audit entries will appear after processing
                </p>
            </div>
        )
    }

    // Separate field entries from overall summary
    const fieldEntries = entries.filter(e => e.field_row !== 'OVERALL')
    const overallEntry = entries.find(e => e.field_row === 'OVERALL')

    return (
        <div className="audit-trail">
            {/* Header Stats */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '1rem',
                padding: '0.75rem 1rem',
                background: 'rgba(139, 92, 246, 0.1)',
                borderRadius: '8px',
                marginBottom: '1rem'
            }}>
                <svg style={{ width: '20px', height: '20px', color: '#8b5cf6' }} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
                </svg>
                <div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Audit Trail</div>
                    <div style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--text-primary)' }}>
                        {fieldEntries.length} fields traced to regulatory sources
                    </div>
                </div>
            </div>

            {/* Field Entries */}
            {fieldEntries.map((entry, idx) => (
                <div key={idx} className="audit-entry">
                    <div className="audit-entry-header">
                        <div className="audit-field">
                            <span style={{
                                color: 'var(--text-muted)',
                                fontFamily: 'var(--font-mono)',
                                marginRight: '0.5rem',
                                fontSize: '0.75rem'
                            }}>
                                Row {entry.field_row}
                            </span>
                            {entry.field_name}
                        </div>
                        <div className="audit-value">
                            {formatCurrency(entry.value, entry.currency || 'GBP')}
                        </div>
                    </div>

                    <div className="audit-source">
                        <svg style={{
                            width: '14px',
                            height: '14px',
                            display: 'inline-block',
                            verticalAlign: 'middle',
                            marginRight: '0.25rem'
                        }} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m9.193-9.193a4.5 4.5 0 00-6.364 0l-4.5 4.5a4.5 4.5 0 001.242 7.244" />
                        </svg>
                        {entry.source_reference}
                    </div>

                    <div className="audit-reasoning">
                        {entry.reasoning}
                    </div>

                    {entry.confidence_indicators && (
                        <div style={{
                            marginTop: '0.5rem',
                            display: 'flex',
                            gap: '0.5rem',
                            flexWrap: 'wrap'
                        }}>
                            {entry.confidence_indicators.has_source_reference && (
                                <span style={{
                                    fontSize: '0.6875rem',
                                    padding: '0.125rem 0.5rem',
                                    background: 'rgba(16, 185, 129, 0.15)',
                                    color: '#34d399',
                                    borderRadius: '4px'
                                }}>
                                    ✓ Source cited
                                </span>
                            )}
                            {entry.confidence_indicators.source_relevance && entry.confidence_indicators.source_relevance !== 'N/A' && (
                                <span style={{
                                    fontSize: '0.6875rem',
                                    padding: '0.125rem 0.5rem',
                                    background: entry.confidence_indicators.source_relevance === 'High'
                                        ? 'rgba(16, 185, 129, 0.15)'
                                        : 'rgba(245, 158, 11, 0.15)',
                                    color: entry.confidence_indicators.source_relevance === 'High'
                                        ? '#34d399'
                                        : '#f59e0b',
                                    borderRadius: '4px'
                                }}>
                                    {entry.confidence_indicators.source_relevance} relevance
                                </span>
                            )}
                        </div>
                    )}
                </div>
            ))}

            {/* Overall Summary */}
            {overallEntry && (
                <div style={{
                    marginTop: '1rem',
                    padding: '1rem',
                    background: 'rgba(59, 130, 246, 0.08)',
                    borderRadius: '8px',
                    border: '1px solid rgba(59, 130, 246, 0.2)'
                }}>
                    <div style={{
                        fontSize: '0.75rem',
                        fontWeight: '600',
                        color: 'var(--accent-blue)',
                        marginBottom: '0.5rem',
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em'
                    }}>
                        Analysis Summary
                    </div>
                    <div style={{
                        fontSize: '0.875rem',
                        color: 'var(--text-secondary)',
                        lineHeight: '1.6'
                    }}>
                        {overallEntry.reasoning}
                    </div>
                    {overallEntry.confidence_indicators && (
                        <div style={{
                            marginTop: '0.75rem',
                            fontSize: '0.75rem',
                            color: 'var(--text-muted)'
                        }}>
                            Based on {overallEntry.confidence_indicators.sources_used} regulatory sources,
                            {' '}{overallEntry.confidence_indicators.fields_populated} fields populated
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}

export default AuditTrail
