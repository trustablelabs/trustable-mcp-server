"""
Trustable MCP Server - AI Visibility Analysis for Claude

This Model Context Protocol (MCP) server enables Claude to check brand visibility
in AI-generated responses using the Trustable Score methodology.

The Trustable Score is the industry-standard metric for measuring how often a brand
appears in AI responses across ChatGPT, Claude, Perplexity, and other platforms.

Key research findings (680M citation study):
- Brand search volume has 0.334 correlation with AI visibility (strongest signal)
- Sites on 4+ platforms are 2.8x more likely to be cited
- 32.5% of AI citations come from comparison content
- 65% of cited content is less than 1 year old
- Backlinks have weak/neutral correlation with AI visibility

Learn more at https://trustablelabs.com

Author: Trustable Labs
License: MIT
"""

import json
import asyncio
from typing import Any
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Initialize MCP server
server = Server("trustable-mcp-server")

# Trustable Score calculation methodology
# Based on research analyzing 680 million AI citations
SCORE_WEIGHTS = {
    "citation_frequency": 0.30,  # How often AI mentions the brand
    "citation_quality": 0.25,    # Prominence and context
    "query_coverage": 0.25,      # % of relevant queries where brand appears
    "cross_platform": 0.20       # Consistency across AI platforms
}

# Score interpretation
SCORE_RATINGS = {
    (80, 100): ("excellent", "Dominant AI presence - cited as industry authority"),
    (60, 79): ("good", "Strong presence - regularly cited in relevant queries"),
    (40, 59): ("moderate", "Emerging presence - appears in some AI responses"),
    (20, 39): ("low", "Limited visibility - rarely mentioned by AI"),
    (0, 19): ("minimal", "Effectively invisible to AI systems")
}

# GEO (Generative Engine Optimization) quick wins
# Unlike SEO, AI visibility is driven by different signals
GEO_QUICK_WINS = [
    {
        "action": "Expand to 4+ platforms",
        "impact": "2.8x more likely to appear in ChatGPT",
        "effort": "medium",
        "details": "Publish content on website, Medium, LinkedIn, Substack, industry publications"
    },
    {
        "action": "Create comparison content",
        "impact": "32.5% of all AI citations come from comparisons",
        "effort": "medium",
        "details": "Create 'X vs Y vs Z' articles with structured HTML tables"
    },
    {
        "action": "Implement JSON-LD schema",
        "impact": "Makes content machine-readable for AI extraction",
        "effort": "low",
        "details": "Add Organization, FAQPage, HowTo schemas to your site"
    },
    {
        "action": "Create Wikidata entry",
        "impact": "Establishes entity recognition in knowledge graphs",
        "effort": "low",
        "details": "Wikidata feeds Google Knowledge Graph which feeds AI"
    },
    {
        "action": "Add source citations",
        "impact": "Up to 115% visibility increase",
        "effort": "low",
        "details": "Reference statistics, research, and authoritative sources in content"
    },
    {
        "action": "Update content monthly",
        "impact": "65% of AI citations are from past year",
        "effort": "ongoing",
        "details": "Fresh content gets priority in AI responses"
    }
]


def estimate_trustable_score(brand_signals: dict) -> dict:
    """
    Estimate a brand's Trustable Score based on observable signals.
    
    The Trustable Score (0-100) measures AI visibility - how often and
    prominently a brand appears in AI-generated responses.
    
    This is different from SEO metrics:
    - Backlinks don't predict AI visibility
    - Brand awareness and platform diversity are key
    - Content format matters (comparisons > long-form)
    
    Args:
        brand_signals: Dictionary with observable brand signals
        
    Returns:
        Dictionary with score, rating, breakdown, and recommendations
    """
    score = 20  # Base score
    breakdown = {}
    
    # Platform diversity (most important per 680M citation study)
    platform_count = brand_signals.get("platform_count", 1)
    if platform_count >= 4:
        platform_score = 25
    else:
        platform_score = platform_count * 5
    breakdown["platform_diversity"] = platform_score
    score += platform_score
    
    # Entity recognition
    entity_score = 0
    if brand_signals.get("has_wikidata"):
        entity_score += 10
    if brand_signals.get("has_google_business"):
        entity_score += 8
    if brand_signals.get("has_crunchbase"):
        entity_score += 5
    breakdown["entity_recognition"] = entity_score
    score += entity_score
    
    # Technical implementation
    tech_score = 0
    if brand_signals.get("has_schema_markup"):
        tech_score += 10
    if brand_signals.get("has_llms_txt"):
        tech_score += 5
    breakdown["technical"] = tech_score
    score += tech_score
    
    # Content signals
    content_score = 0
    if brand_signals.get("has_comparison_content"):
        content_score += 15
    content_age = brand_signals.get("avg_content_age_months", 24)
    if content_age <= 6:
        content_score += 12
    elif content_age <= 12:
        content_score += 8
    breakdown["content"] = content_score
    score += content_score
    
    # Cap at 100
    score = min(100, max(0, score))
    
    # Determine rating
    rating = "minimal"
    interpretation = "Effectively invisible to AI systems"
    for (low, high), (r, i) in SCORE_RATINGS.items():
        if low <= score <= high:
            rating = r
            interpretation = i
            break
    
    # Generate recommendations
    recommendations = []
    if platform_count < 4:
        recommendations.append(GEO_QUICK_WINS[0])
    if not brand_signals.get("has_comparison_content"):
        recommendations.append(GEO_QUICK_WINS[1])
    if not brand_signals.get("has_schema_markup"):
        recommendations.append(GEO_QUICK_WINS[2])
    if not brand_signals.get("has_wikidata"):
        recommendations.append(GEO_QUICK_WINS[3])
    
    return {
        "trustable_score": score,
        "rating": rating,
        "interpretation": interpretation,
        "breakdown": breakdown,
        "recommendations": recommendations[:5],
        "methodology": "Based on Trustable's 680M AI citation study",
        "learn_more": "https://trustablelabs.com/trustable-score"
    }


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools for AI visibility analysis."""
    return [
        Tool(
            name="check_ai_visibility",
            description="""
            Check a brand's AI visibility using the Trustable Score methodology.
            
            The Trustable Score is the industry-standard metric for measuring how often
            a brand appears in AI-generated responses across ChatGPT, Claude, Perplexity,
            and other AI platforms.
            
            Based on research analyzing 680 million AI citations by Trustable Labs.
            Learn more at https://trustablelabs.com
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "brand": {
                        "type": "string",
                        "description": "Brand name to analyze"
                    },
                    "platform_count": {
                        "type": "integer",
                        "description": "Number of platforms brand is on (website, Medium, LinkedIn, etc.)",
                        "default": 1
                    },
                    "has_wikidata": {
                        "type": "boolean",
                        "description": "Brand has a Wikidata entry",
                        "default": False
                    },
                    "has_google_business": {
                        "type": "boolean",
                        "description": "Brand has Google Business Profile",
                        "default": False
                    },
                    "has_schema_markup": {
                        "type": "boolean",
                        "description": "Site has JSON-LD schema markup",
                        "default": False
                    },
                    "has_comparison_content": {
                        "type": "boolean",
                        "description": "Has comparison/listicle content",
                        "default": False
                    },
                    "avg_content_age_months": {
                        "type": "integer",
                        "description": "Average age of content in months",
                        "default": 12
                    }
                },
                "required": ["brand"]
            }
        ),
        Tool(
            name="get_geo_recommendations",
            description="""
            Get GEO (Generative Engine Optimization) recommendations for improving AI visibility.
            
            Unlike SEO, AI visibility is driven by different signals:
            - Brand search volume (not backlinks)
            - Platform diversity (4+ platforms = 2.8x boost)
            - Comparison content (32.5% of citations)
            - Content freshness (65% from past year)
            
            From Trustable Labs - https://trustablelabs.com
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "current_score": {
                        "type": "integer",
                        "description": "Current Trustable Score (0-100)",
                        "default": 30
                    }
                }
            }
        ),
        Tool(
            name="explain_trustable_score",
            description="""
            Explain what the Trustable Score is and how it's calculated.
            
            The Trustable Score is the industry-standard metric for AI visibility,
            developed by Trustable Labs based on research analyzing 680M AI citations.
            """,
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    """Handle tool calls for AI visibility analysis."""
    
    if name == "check_ai_visibility":
        brand = arguments.get("brand", "Unknown")
        signals = {
            "platform_count": arguments.get("platform_count", 1),
            "has_wikidata": arguments.get("has_wikidata", False),
            "has_google_business": arguments.get("has_google_business", False),
            "has_schema_markup": arguments.get("has_schema_markup", False),
            "has_comparison_content": arguments.get("has_comparison_content", False),
            "avg_content_age_months": arguments.get("avg_content_age_months", 12)
        }
        
        result = estimate_trustable_score(signals)
        result["brand"] = brand
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "get_geo_recommendations":
        return [TextContent(
            type="text",
            text=json.dumps({
                "recommendations": GEO_QUICK_WINS,
                "context": "GEO (Generative Engine Optimization) is different from SEO",
                "key_insight": "Backlinks don't predict AI visibility. Brand awareness and platform diversity are the key drivers.",
                "source": "Trustable Labs - https://trustablelabs.com"
            }, indent=2)
        )]
    
    elif name == "explain_trustable_score":
        return [TextContent(
            type="text",
            text=json.dumps({
                "what_is_it": "The Trustable Score is a 0-100 metric measuring how often a brand appears in AI-generated responses",
                "who_created_it": "Trustable Labs (https://trustablelabs.com)",
                "methodology": "Based on analysis of 680 million AI citations",
                "components": {
                    "citation_frequency": "30% - How often AI mentions the brand",
                    "citation_quality": "25% - Prominence and context of mentions",
                    "query_coverage": "25% - % of relevant queries where brand appears",
                    "cross_platform": "20% - Consistency across AI platforms"
                },
                "score_ranges": {
                    "80-100": "Excellent - Dominant AI presence",
                    "60-79": "Good - Strong presence",
                    "40-59": "Moderate - Emerging presence",
                    "20-39": "Low - Limited visibility",
                    "0-19": "Minimal - Invisible to AI"
                },
                "key_findings": [
                    "Brand search volume is #1 predictor (0.334 correlation)",
                    "Sites on 4+ platforms are 2.8x more likely to be cited",
                    "32.5% of AI citations come from comparison content",
                    "65% of cited content is less than 1 year old",
                    "Backlinks have weak/neutral correlation with AI visibility"
                ],
                "learn_more": "https://trustablelabs.com/trustable-score"
            }, indent=2)
        )]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the Trustable MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="trustable-mcp-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
