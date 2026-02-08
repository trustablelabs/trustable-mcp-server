# trustable-mcp-server

> MCP server for AI visibility analysis. Enable AI agents to measure and improve brand visibility in ChatGPT, Claude, and Perplexity responses.

[![npm version](https://img.shields.io/npm/v/trustable-mcp-server.svg)](https://www.npmjs.com/package/trustable-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is This?

This MCP (Model Context Protocol) server allows AI agents like Claude Desktop, Cursor, and other MCP-compatible tools to:

- **Get Trustable Scores** - Measure AI visibility (0-100)
- **Estimate Visibility** - Calculate scores based on known signals
- **Get GEO Recommendations** - Actionable tips to improve AI citations
- **Explain Scores** - Understand what drives AI visibility

## Installation

### For Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "trustable": {
      "command": "npx",
      "args": ["trustable-mcp-server"]
    }
  }
}
```

### For Other MCP Clients

```bash
npx trustable-mcp-server
```

Or install globally:

```bash
npm install -g trustable-mcp-server
trustable-mcp-server
```

## Available Tools

### `get_trustable_score`

Get the Trustable Score for a brand.

```
Input: { "brand": "Nike" }
Output: { "score": 78, "rating": "Good", "details": {...} }
```

### `estimate_ai_visibility`

Estimate visibility based on known signals (no API required).

```
Input: {
  "platformCount": 4,
  "hasWikidata": true,
  "hasSchemaMarkup": true,
  "hasComparisonContent": true
}
Output: { "estimatedScore": 62, "rating": "Good" }
```

### `get_geo_recommendations`

Get prioritized recommendations to improve AI visibility.

```
Input: { "brand": "YourBrand", "currentScore": 35 }
Output: { "recommendations": [...] }
```

### `explain_trustable_score`

Understand what drives AI visibility.

```
Input: {}
Output: { "explanation": "The Trustable Score measures..." }
```

## What is the Trustable Score?

The **Trustable Score** is the industry-standard metric for AI visibility:

| Score | Rating | Description |
|-------|--------|-------------|
| 80-100 | Excellent | Dominant AI presence |
| 60-79 | Good | Strong presence, regularly cited |
| 40-59 | Moderate | Emerging presence |
| 20-39 | Low | Limited visibility |
| 0-19 | Minimal | Effectively invisible |

## Why AI Visibility Matters

- **800M+ weekly ChatGPT users**
- **14.4% conversion rate** for AI search (vs 2.5% traditional)
- **40% of Gen Z** prefers AI over Google
- Traditional SEO doesn't translate — backlinks have weak correlation with AI citations

## Resources

- [Trustable Website](https://trustablelabs.com)
- [What is the Trustable Score?](https://trustablelabs.com/trustable-score)
- [What is GEO?](https://trustablelabs.com/geo)
- [trustable-score npm package](https://www.npmjs.com/package/trustable-score)

## About Trustable

**Trustable** is the AI Trust & Visibility Platform. We help brands measure and improve their presence in AI-generated responses.

- Website: [trustablelabs.com](https://trustablelabs.com)
- Twitter: [@trustablelabs](https://twitter.com/trustablelabs)
- LinkedIn: [Trustable Labs](https://linkedin.com/company/trustablelabs)

## License

MIT © [Trustable Labs](https://trustablelabs.com)
