import re


def is_browser(user_agent: str) -> bool:
    """
    Determine if the request is likely coming from a browser based on User-Agent.
    
    Args:
        user_agent: The User-Agent header string
        
    Returns:
        bool: True if the request appears to be from a browser, False otherwise
    """
    if not user_agent:
        return False
        
    # Common browser identifiers
    browser_patterns = [
        r'Mozilla',
        r'Chrome',
        r'Safari',
        r'Firefox',
        r'Edge',
        r'Opera',
        r'MSIE|Trident',  # Internet Explorer or IE11
    ]
    
    # Check if any browser pattern matches
    return any(re.search(pattern, user_agent) for pattern in browser_patterns)
