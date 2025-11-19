import logging

logger = logging.getLogger(__name__)

class SEOAnalyzer:
    @staticmethod
    def analyze(page_data):
        """
        Analyze page data for SEO issues.
        
        Args:
            page_data (dict): Dictionary containing page metadata (title, meta_description, h1, load_time_ms, etc.)
            
        Returns:
            list: A list of dictionaries representing detected issues.
        """
        issues = []
        
        # 1. Title Checks
        title = page_data.get("title")
        if not title:
            issues.append({
                "issue_type": "missing_title",
                "severity": "critical",
                "description": "Page is missing a title tag."
            })
        elif len(title) < 10:
            issues.append({
                "issue_type": "short_title",
                "severity": "warning",
                "description": f"Title is too short ({len(title)} chars). Recommended: 10-60 chars."
            })
        elif len(title) > 60:
            issues.append({
                "issue_type": "long_title",
                "severity": "warning",
                "description": f"Title is too long ({len(title)} chars). Recommended: 10-60 chars."
            })
            
        # 2. Meta Description Checks
        meta_desc = page_data.get("meta_description")
        if not meta_desc:
            issues.append({
                "issue_type": "missing_meta_desc",
                "severity": "high",
                "description": "Page is missing a meta description."
            })
        elif len(meta_desc) < 50:
            issues.append({
                "issue_type": "short_meta_desc",
                "severity": "warning",
                "description": f"Meta description is too short ({len(meta_desc)} chars). Recommended: 50-160 chars."
            })
        elif len(meta_desc) > 160:
            issues.append({
                "issue_type": "long_meta_desc",
                "severity": "warning",
                "description": f"Meta description is too long ({len(meta_desc)} chars). Recommended: 50-160 chars."
            })
            
        # 3. H1 Checks
        h1 = page_data.get("h1")
        if not h1:
            issues.append({
                "issue_type": "missing_h1",
                "severity": "high",
                "description": "Page is missing an H1 heading."
            })
            
        # 4. Load Time Checks
        load_time = page_data.get("load_time_ms", 0)
        if load_time > 6000:
            issues.append({
                "issue_type": "slow_load_time",
                "severity": "critical",
                "description": f"Page load time is very slow ({load_time}ms). Recommended: < 3000ms."
            })
        elif load_time > 3000:
            issues.append({
                "issue_type": "slow_load_time",
                "severity": "warning",
                "description": f"Page load time is slow ({load_time}ms). Recommended: < 3000ms."
            })
            
        return issues
