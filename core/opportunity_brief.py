"""Generates executive-ready Opportunity Briefs for top-ranked business findings."""

from typing import List
from models.opportunity import Opportunity, OpportunityBrief, EvidenceReference
from utils.logger import logger


class OpportunityBriefGenerator:
    """Creates structured, evidence-grounded briefs for top opportunities."""

    def generate_briefs(self, opportunities: List[Opportunity], top_n: int = 5) -> List[Opportunity]:
        """
        Attaches detailed OpportunityBrief objects to the top N opportunities.
        """
        top_opportunities = opportunities[:top_n]

        for opp in top_opportunities:
            evidence_samples: List[EvidenceReference] = []
            source_links: List[str] = []

            # Gather real supporting evidence and URLs from signals
            for sig in opp.signals:
                if sig.source_url not in source_links:
                    source_links.append(sig.source_url)

                if sig.evidence and len(evidence_samples) < 5:
                    evidence_samples.append(
                        EvidenceReference(
                            excerpt=sig.evidence,
                            url=sig.source_url,
                            domain=sig.source_domain,
                            page_title=sig.page_title
                        )
                    )

            # Assign Solution Type classification
            sol_lower = opp.possible_solution.lower()
            if "saas" in sol_lower or "platform" in sol_lower:
                sol_type = "SaaS Platform"
            elif "extension" in sol_lower or "feature" in sol_lower:
                sol_type = "Software Feature / Add-on"
            elif "tool" in sol_lower or "linter" in sol_lower or "canvas" in sol_lower:
                sol_type = "Developer / Automation Tool"
            else:
                sol_type = "Managed Business Service"

            brief = OpportunityBrief(
                title=opp.title,
                problem_description=opp.problem_description,
                target_audience=opp.target_audience,
                why_it_matters=opp.why_it_matters,
                possible_solution=opp.possible_solution,
                validation_strategy=opp.validation_strategy,
                evidence_samples=evidence_samples,
                source_links=source_links,
                solution_type=sol_type
            )

            opp.brief = brief

        logger.info(f"Generated {len(top_opportunities)} opportunity briefs.")
        return opportunities

