// Field metadata for display
const FIELD_META = {
    row_010: { label: 'Capital instruments eligible as CET1', category: 'CET1', isTotal: false },
    row_020: { label: 'Share premium (CET1)', category: 'CET1', isTotal: false },
    row_030: { label: 'Retained earnings', category: 'CET1', isTotal: false },
    row_040: { label: 'Accumulated OCI', category: 'CET1', isTotal: false },
    row_050: { label: 'Other reserves', category: 'CET1', isTotal: false },
    row_060: { label: 'Minority interests', category: 'CET1', isTotal: false },
    row_070: { label: 'Interim/year-end profits', category: 'CET1', isTotal: false },
    row_080: { label: '(-) Goodwill & intangibles', category: 'CET1 Deductions', isTotal: false },
    row_090: { label: '(-) Deferred tax assets', category: 'CET1 Deductions', isTotal: false },
    row_095: { label: '(-) Provisions shortfall', category: 'CET1 Deductions', isTotal: false },
    row_100: { label: 'CET1 capital before adjustments', category: 'CET1', isTotal: true },
    row_200: { label: 'CET1 Capital', category: 'CET1', isTotal: true },
    row_300: { label: 'AT1 instruments', category: 'AT1', isTotal: false },
    row_310: { label: 'Share premium (AT1)', category: 'AT1', isTotal: false },
    row_320: { label: '(-) AT1 deductions', category: 'AT1', isTotal: false },
    row_400: { label: 'Tier 1 Capital', category: 'Tier 1', isTotal: true },
    row_500: { label: 'Tier 2 instruments', category: 'Tier 2', isTotal: false },
    row_510: { label: 'Share premium (T2)', category: 'Tier 2', isTotal: false },
    row_520: { label: '(-) Tier 2 deductions', category: 'Tier 2', isTotal: false },
    row_600: { label: 'Tier 2 Capital', category: 'Tier 2', isTotal: true },
    row_700: { label: 'TOTAL OWN FUNDS', category: 'Total', isTotal: true }
}

// Category colors
const CATEGORY_COLORS = {
    'CET1': '#3b82f6',
    'CET1 Deductions': '#ef4444',
    'AT1': '#8b5cf6',
    'Tier 1': '#10b981',
    'Tier 2': '#f59e0b',
    'Total': '#10b981'
}

function formatCurrency(value, currency = 'GBP') {
    if (value === null || value === undefined) return '—'

    const absValue = Math.abs(value)
    const isNegative = value < 0

    // Format with thousands separators
    const formatted = new Intl.NumberFormat('en-GB', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(absValue)

    return isNegative ? `(${formatted})` : formatted
}

function TemplateViewer({ data }) {
    if (!data) return null

    const currency = data.currency || 'GBP'

    // Filter to only show rows that have values
    const displayRows = Object.entries(FIELD_META)
        .filter(([key]) => data[key] !== null && data[key] !== undefined)
        .sort((a, b) => {
            const numA = parseInt(a[0].replace('row_', ''))
            const numB = parseInt(b[0].replace('row_', ''))
            return numA - numB
        })

    return (
        <div className="template-viewer">
            <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '1rem',
                padding: '0.75rem 1rem',
                background: 'rgba(59, 130, 246, 0.1)',
                borderRadius: '8px',
                border: '1px solid rgba(59, 130, 246, 0.2)'
            }}>
                <div>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Template</span>
                    <h3 style={{ fontSize: '1rem', fontWeight: '600', color: 'var(--text-primary)' }}>
                        C01.00 - Own Funds
                    </h3>
                </div>
                <span style={{
                    fontSize: '0.875rem',
                    fontWeight: '500',
                    color: 'var(--accent-blue)',
                    fontFamily: 'var(--font-mono)'
                }}>
                    {currency}
                </span>
            </div>

            <table className="template-table">
                <thead>
                    <tr>
                        <th style={{ width: '80px' }}>Row</th>
                        <th>Description</th>
                        <th style={{ width: '60px' }}>Category</th>
                        <th style={{ width: '150px', textAlign: 'right' }}>Amount</th>
                    </tr>
                </thead>
                <tbody>
                    {displayRows.map(([key, meta]) => {
                        const value = data[key]
                        const rowNum = key.replace('row_', '')
                        const isNegative = value < 0

                        return (
                            <tr
                                key={key}
                                className={meta.isTotal ? 'row-total' : ''}
                            >
                                <td>
                                    <span style={{
                                        fontFamily: 'var(--font-mono)',
                                        fontSize: '0.8125rem',
                                        color: 'var(--text-muted)'
                                    }}>
                                        {rowNum}
                                    </span>
                                </td>
                                <td className="row-label">
                                    {meta.isTotal && (
                                        <span style={{
                                            color: CATEGORY_COLORS[meta.category],
                                            marginRight: '0.5rem'
                                        }}>■</span>
                                    )}
                                    {meta.label}
                                </td>
                                <td>
                                    <span style={{
                                        fontSize: '0.6875rem',
                                        padding: '0.125rem 0.375rem',
                                        borderRadius: '4px',
                                        background: `${CATEGORY_COLORS[meta.category]}20`,
                                        color: CATEGORY_COLORS[meta.category],
                                        fontWeight: '500'
                                    }}>
                                        {meta.category}
                                    </span>
                                </td>
                                <td className={`row-value ${isNegative ? 'negative' : 'positive'}`}>
                                    {formatCurrency(value, currency)}
                                </td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>

            {displayRows.length === 0 && (
                <div style={{
                    textAlign: 'center',
                    padding: '2rem',
                    color: 'var(--text-muted)'
                }}>
                    No data populated in template
                </div>
            )}
        </div>
    )
}

export default TemplateViewer
