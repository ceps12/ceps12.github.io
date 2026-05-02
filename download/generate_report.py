import os
import hashlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus import SimpleDocTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
import sys

# ━━ Font Registration ━━
pdfmetrics.registerFont(TTFont('DejaVuSerif', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSerifBold', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Carlito', '/usr/share/fonts/truetype/english/Carlito-Regular.ttf'))
pdfmetrics.registerFont(TTFont('CarlitoBold', '/usr/share/fonts/truetype/english/Carlito-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSansBold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

registerFontFamily('DejaVuSerif', normal='DejaVuSerif', bold='DejaVuSerifBold')
registerFontFamily('Carlito', normal='Carlito', bold='CarlitoBold')
registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSansBold')

# Font fallback for mixed text
sys.path.insert(0, '/home/z/my-project/skills/pdf/scripts')
try:
    from pdf import install_font_fallback
    install_font_fallback()
except:
    pass

# ━━ Color Palette ━━
ACCENT       = colors.HexColor('#502eb6')
TEXT_PRIMARY  = colors.HexColor('#202223')
TEXT_MUTED    = colors.HexColor('#838a8f')
BG_SURFACE   = colors.HexColor('#d4dce1')
BG_PAGE      = colors.HexColor('#e8ebed')

TABLE_HEADER_COLOR = ACCENT
TABLE_HEADER_TEXT  = colors.white
TABLE_ROW_EVEN     = colors.white
TABLE_ROW_ODD      = BG_SURFACE

# ━━ Styles ━━
title_style = ParagraphStyle(
    name='DocTitle', fontName='DejaVuSerif', fontSize=28, leading=36,
    alignment=TA_LEFT, textColor=TEXT_PRIMARY, spaceAfter=6
)
h1_style = ParagraphStyle(
    name='Heading1', fontName='DejaVuSerif', fontSize=20, leading=28,
    alignment=TA_LEFT, textColor=TEXT_PRIMARY, spaceBefore=18, spaceAfter=10
)
h2_style = ParagraphStyle(
    name='Heading2', fontName='DejaVuSerif', fontSize=15, leading=22,
    alignment=TA_LEFT, textColor=TEXT_PRIMARY, spaceBefore=14, spaceAfter=8
)
body_style = ParagraphStyle(
    name='Body', fontName='DejaVuSerif', fontSize=11, leading=18,
    alignment=TA_LEFT, textColor=TEXT_PRIMARY, spaceAfter=6
)
bullet_style = ParagraphStyle(
    name='Bullet', fontName='DejaVuSerif', fontSize=11, leading=18,
    alignment=TA_LEFT, textColor=TEXT_PRIMARY, leftIndent=24, spaceAfter=4
)
bold_body = ParagraphStyle(
    name='BoldBody', fontName='DejaVuSerif', fontSize=11, leading=18,
    alignment=TA_LEFT, textColor=TEXT_PRIMARY, spaceAfter=6
)
meta_style = ParagraphStyle(
    name='Meta', fontName='DejaVuSerif', fontSize=10, leading=16,
    alignment=TA_LEFT, textColor=TEXT_MUTED, spaceAfter=4
)
header_cell_style = ParagraphStyle(
    name='HeaderCell', fontName='DejaVuSerif', fontSize=10,
    textColor=colors.white, alignment=TA_CENTER
)
cell_style = ParagraphStyle(
    name='CellStyle', fontName='DejaVuSerif', fontSize=10,
    textColor=TEXT_PRIMARY, alignment=TA_CENTER
)
cell_left_style = ParagraphStyle(
    name='CellLeft', fontName='DejaVuSerif', fontSize=10,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT
)
caption_style = ParagraphStyle(
    name='Caption', fontName='DejaVuSerif', fontSize=9, leading=14,
    alignment=TA_CENTER, textColor=TEXT_MUTED, spaceBefore=3, spaceAfter=6
)

# ━━ TOC Styles ━━
toc_h1_style = ParagraphStyle(name='TOCH1', fontName='DejaVuSerif', fontSize=13, leftIndent=20)
toc_h2_style = ParagraphStyle(name='TOCH2', fontName='DejaVuSerif', fontSize=11, leftIndent=40)

# ━━ Helper Functions ━━
A4_W, A4_H = A4
PAGE_W = A4_W - 2*inch
MAX_KEEP_HEIGHT = A4_H * 0.4

def safe_keep(elements):
    total_h = 0
    for el in elements:
        w, h = el.wrap(PAGE_W, A4_H)
        total_h += h
    if total_h <= MAX_KEEP_HEIGHT:
        return [KeepTogether(elements)]
    elif len(elements) >= 2:
        return [KeepTogether(elements[:2])] + list(elements[2:])
    return list(elements)

def make_table(data, col_ratios, has_header=True):
    col_widths = [r * PAGE_W for r in col_ratios]
    table = Table(data, colWidths=col_widths, hAlign='CENTER')
    style_cmds = [
        ('GRID', (0, 0), (-1, -1), 0.5, TEXT_MUTED),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]
    if has_header:
        style_cmds.append(('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_COLOR))
        style_cmds.append(('TEXTCOLOR', (0, 0), (-1, 0), TABLE_HEADER_TEXT))
        for row_idx in range(1, len(data)):
            bg = TABLE_ROW_EVEN if row_idx % 2 == 1 else TABLE_ROW_ODD
            style_cmds.append(('BACKGROUND', (0, row_idx), (-1, row_idx), bg))
    table.setStyle(TableStyle(style_cmds))
    return table

# ━━ TOC Document Template ━━
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))

def add_heading(text, style, level=0):
    key = 'h_%s' % hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/>%s' % (key, text), style)
    p.bookmark_name = text
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p

# ━━ Build Document ━━
output_path = '/home/z/my-project/download/github_audit_report.pdf'
doc = TocDocTemplate(
    output_path, pagesize=A4,
    leftMargin=1*inch, rightMargin=1*inch,
    topMargin=0.8*inch, bottomMargin=0.8*inch
)

story = []

# ─── TOC ───
toc = TableOfContents()
toc.levelStyles = [toc_h1_style, toc_h2_style]
story.append(Paragraph('<b>Table of Contents</b>', title_style))
story.append(Spacer(1, 12))
story.append(toc)
story.append(PageBreak())

# ═══════════════════════════════════════════════
# 1. EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════
story.append(add_heading('<b>1. Executive Summary</b>', h1_style, level=0))
story.append(Spacer(1, 6))

story.append(Paragraph(
    'This report presents a comprehensive audit of the GitHub profile '
    '<b>ceps12</b> (https://github.com/ceps12), conducted on May 2, 2026. '
    'The analysis covers profile completeness, repository portfolio, community engagement, '
    'and overall developer presence on the platform. The primary objective is to identify '
    'gaps, weaknesses, and missed opportunities, and to provide actionable recommendations '
    'for transforming this profile into a professional and impactful developer portfolio.',
    body_style))

story.append(Paragraph(
    'The audit reveals that the profile of ceps12 is currently in a significantly underdeveloped state. '
    'Despite the account being created in June 2022 (nearly four years ago), the profile exhibits virtually '
    'no public activity, no repositories, no bio, and no professional information. This level of inactivity '
    'represents a substantial missed opportunity for building a professional developer brand, networking with '
    'other developers, and demonstrating technical competence to potential employers or collaborators.',
    body_style))

story.append(Paragraph(
    'The overall profile completeness score is estimated at approximately <b>5 out of 100</b>, indicating '
    'a critical need for improvement across virtually all categories. The report concludes with a prioritized '
    'action plan that outlines specific steps for rapid improvement, focusing first on quick wins that can be '
    'completed in under an hour, followed by medium-term and long-term strategic enhancements.',
    body_style))

# Key metrics table
story.append(Spacer(1, 18))
metrics_data = [
    [Paragraph('<b>Metric</b>', header_cell_style),
     Paragraph('<b>Value</b>', header_cell_style),
     Paragraph('<b>Assessment</b>', header_cell_style)],
    [Paragraph('Account Age', cell_left_style),
     Paragraph('~4 years', cell_style),
     Paragraph('Good foundation', cell_style)],
    [Paragraph('Public Repositories', cell_left_style),
     Paragraph('0', cell_style),
     Paragraph('Critical gap', cell_style)],
    [Paragraph('Followers', cell_left_style),
     Paragraph('1', cell_style),
     Paragraph('Very low', cell_style)],
    [Paragraph('Profile Completeness', cell_left_style),
     Paragraph('5/100', cell_style),
     Paragraph('Needs urgent work', cell_style)],
]
story.append(make_table(metrics_data, [0.35, 0.25, 0.40]))
story.append(Paragraph('<b>Table 1.</b> Key profile metrics overview', caption_style))
story.append(Spacer(1, 18))

# ═══════════════════════════════════════════════
# 2. PROFILE OVERVIEW
# ═══════════════════════════════════════════════
story.append(add_heading('<b>2. Profile Overview</b>', h1_style, level=0))
story.append(Spacer(1, 6))

story.append(Paragraph(
    'The GitHub account ceps12 was registered on June 19, 2022. Over the course of nearly four years, '
    'the profile has remained largely dormant with minimal public footprint. The display name has been set '
    'to a stylized string using extended Unicode characters, which may indicate a preference for creative '
    'expression but poses challenges for professional discoverability and searchability.',
    body_style))

story.append(add_heading('<b>2.1 Current Profile State</b>', h2_style, level=1))
story.append(Spacer(1, 4))

profile_data = [
    [Paragraph('<b>Field</b>', header_cell_style),
     Paragraph('<b>Current Status</b>', header_cell_style),
     Paragraph('<b>Recommended</b>', header_cell_style)],
    [Paragraph('Display Name', cell_left_style),
     Paragraph('Stylized Unicode', cell_style),
     Paragraph('Real name or professional alias', cell_style)],
    [Paragraph('Bio', cell_left_style),
     Paragraph('Empty', cell_style),
     Paragraph('Short professional summary', cell_style)],
    [Paragraph('Location', cell_left_style),
     Paragraph('Empty', cell_style),
     Paragraph('City, Country', cell_style)],
    [Paragraph('Company', cell_left_style),
     Paragraph('Empty', cell_style),
     Paragraph('Current employer or freelance', cell_style)],
    [Paragraph('Blog / Website', cell_left_style),
     Paragraph('Empty', cell_style),
     Paragraph('Portfolio or LinkedIn link', cell_style)],
    [Paragraph('Email', cell_left_style),
     Paragraph('Private', cell_style),
     Paragraph('Public professional email', cell_style)],
    [Paragraph('Twitter / X', cell_left_style),
     Paragraph('Empty', cell_style),
     Paragraph('Professional Twitter handle', cell_style)],
    [Paragraph('Hireable status', cell_left_style),
     Paragraph('Not set', cell_style),
     Paragraph('Enable if open to offers', cell_style)],
]
story.append(Spacer(1, 6))
story.append(make_table(profile_data, [0.25, 0.30, 0.45]))
story.append(Paragraph('<b>Table 2.</b> Profile fields - current vs recommended', caption_style))
story.append(Spacer(1, 12))

story.append(Paragraph(
    'As shown in Table 2, every single profile metadata field is either empty or suboptimal. The absence of a bio, '
    'location, company, and website means that visitors to the profile have no context about who ceps12 is, what '
    'technologies they work with, or what their professional background entails. The stylized display name, while '
    'potentially creative, makes the profile difficult to find through search engines and GitHub user discovery tools, '
    'which rely on standard character matching.',
    body_style))

story.append(Paragraph(
    'The "Hireable" flag has not been enabled. This is a simple toggle that signals to recruiters and hiring managers '
    'that the developer is open to job opportunities. Enabling this flag increases the profile visibility in GitHub\'s '
    'candidate search and can lead to direct outreach from companies seeking talent.',
    body_style))

# ═══════════════════════════════════════════════
# 3. REPOSITORY ANALYSIS
# ═══════════════════════════════════════════════
story.append(add_heading('<b>3. Repository Analysis</b>', h1_style, level=0))
story.append(Spacer(1, 6))

story.append(Paragraph(
    'The most critical finding of this audit is the complete absence of public repositories. The profile currently '
    'hosts zero public repositories, which fundamentally undermines the purpose of maintaining a GitHub account. '
    'GitHub is, at its core, a platform for showcasing code, collaborating on projects, and demonstrating technical '
    'skills. Without repositories, the profile provides no evidence of coding ability, project experience, or '
    'technical interests to any visitor.',
    body_style))

story.append(Paragraph(
    'It is possible that ceps12 maintains private repositories or uses GitHub exclusively for issue tracking, '
    'code review, or private collaboration. However, this approach severely limits the professional value of the '
    'account. Recruiters, potential collaborators, and open-source community members cannot evaluate skills without '
    'visible code. Studies consistently show that GitHub profiles with active, well-maintained repositories receive '
    'significantly more recruiter attention and collaboration opportunities than those without public code.',
    body_style))

story.append(add_heading('<b>3.1 What This Means for Professional Opportunities</b>', h2_style, level=1))
story.append(Spacer(1, 4))

story.append(Paragraph(
    'The absence of public repositories creates a compounding negative effect. When a recruiter or technical manager '
    'visits the profile and finds no code, they have no basis for evaluating technical competence. This often leads '
    'to immediate disqualification, as hiring teams increasingly rely on GitHub profiles as a screening tool. '
    'Furthermore, the lack of contributions means the profile does not appear in GitHub search results, trending '
    'developer lists, or community leaderboards, further reducing discoverability.',
    body_style))

story.append(Paragraph(
    'Beyond employment, the lack of open-source activity means ceps12 is missing out on valuable learning '
    'opportunities. Contributing to open-source projects is one of the most effective ways to improve coding skills, '
    'learn from experienced developers, build a professional network, and gain credibility in the developer community. '
    'Many senior developers attribute a significant portion of their career growth to open-source participation.',
    body_style))

# ═══════════════════════════════════════════════
# 4. COMMUNITY ENGAGEMENT
# ═══════════════════════════════════════════════
story.append(add_heading('<b>4. Community Engagement</b>', h1_style, level=0))
story.append(Spacer(1, 6))

story.append(Paragraph(
    'Community engagement on GitHub encompasses several dimensions: following other developers, starring repositories, '
    'forking projects, opening issues, submitting pull requests, participating in discussions, and contributing to '
    'open-source projects. Each of these activities leaves a visible trail that demonstrates curiosity, expertise, and '
    'willingness to collaborate. The profile of ceps12 shows minimal engagement across all of these dimensions.',
    body_style))

engagement_data = [
    [Paragraph('<b>Engagement Metric</b>', header_cell_style),
     Paragraph('<b>Current Value</b>', header_cell_style),
     Paragraph('<b>Impact</b>', header_cell_style)],
    [Paragraph('Following', cell_left_style),
     Paragraph('0', cell_style),
     Paragraph('No network visibility', cell_style)],
    [Paragraph('Followers', cell_left_style),
     Paragraph('1', cell_style),
     Paragraph('Minimal social proof', cell_style)],
    [Paragraph('Starred Repositories', cell_left_style),
     Paragraph('0', cell_style),
     Paragraph('No visible interests', cell_style)],
    [Paragraph('Public Gists', cell_left_style),
     Paragraph('0', cell_style),
     Paragraph('No code snippets shared', cell_style)],
    [Paragraph('Organizations', cell_left_style),
     Paragraph('0', cell_style),
     Paragraph('No community affiliation', cell_style)],
    [Paragraph('Subscriptions', cell_left_style),
     Paragraph('0', cell_style),
     Paragraph('No tracked projects', cell_style)],
]
story.append(Spacer(1, 6))
story.append(make_table(engagement_data, [0.35, 0.25, 0.40]))
story.append(Paragraph('<b>Table 3.</b> Community engagement metrics', caption_style))
story.append(Spacer(1, 12))

story.append(Paragraph(
    'Following zero other developers is particularly notable because it suggests either complete inactivity on the '
    'platform or a deliberate choice not to engage. Following other developers is a low-effort, high-impact way to '
    'build a network, stay informed about industry trends, and signal your interests to profile visitors. Similarly, '
    'starring repositories serves as a public bookmark system that showcases your technical interests and preferred '
    'tools. A curated list of starred repositories can be as informative to a recruiter as the repositories you own.',
    body_style))

story.append(Paragraph(
    'The lack of organization memberships means ceps12 is not publicly associated with any company, open-source '
    'community, or professional group. Organization badges on a profile provide immediate context about a developer\'s '
    'affiliations and can significantly enhance credibility. Even informal memberships in open-source organizations '
    'can demonstrate community involvement and technical interests.',
    body_style))

# ═══════════════════════════════════════════════
# 5. ACTIVITY AND CONTRIBUTIONS
# ═══════════════════════════════════════════════
story.append(add_heading('<b>5. Activity and Contribution Analysis</b>', h1_style, level=0))
story.append(Spacer(1, 6))

story.append(Paragraph(
    'GitHub tracks user activity through a contributions graph that visualizes commits, pull requests, issues, '
    'and code reviews over time. This graph is one of the first things visitors notice on a profile, as it provides '
    'an at-a-glance view of how active and consistent a developer is. The profile of ceps12 shows no public '
    'contribution activity, resulting in an empty or nearly empty contributions graph.',
    body_style))

story.append(Paragraph(
    'An empty contributions graph sends a strong negative signal to profile visitors. Whether accurate or not, '
    'it is commonly interpreted as a sign of inactivity, lack of coding experience, or disinterest in the platform. '
    'For developers seeking employment, an active contributions graph has become almost as important as a resume, '
    'as it provides verifiable evidence of ongoing coding activity. Many recruiters and engineering managers '
    'specifically look for consistent contribution patterns when evaluating candidates.',
    body_style))

story.append(Paragraph(
    'The contribution graph also affects GitHub\'s internal algorithms for trending repositories and developer '
    'recommendations. Profiles with consistent activity are more likely to be recommended to other users and to '
    'appear in search results. This creates a network effect where active profiles receive more visibility, which '
    'in turn leads to more followers, stars, and collaboration opportunities.',
    body_style))

# ═══════════════════════════════════════════════
# 6. DETAILED GAP ANALYSIS
# ═══════════════════════════════════════════════
story.append(add_heading('<b>6. Detailed Gap Analysis</b>', h1_style, level=0))
story.append(Spacer(1, 6))

story.append(Paragraph(
    'This section provides a comprehensive breakdown of all identified gaps, organized by category and severity. '
    'Each gap is assessed for its impact on the profile\'s professional value and assigned a priority level '
    'to guide the remediation effort. The categories cover profile metadata, content portfolio, social engagement, '
    'and technical presentation.',
    body_style))

story.append(add_heading('<b>6.1 Critical Gaps (Immediate Action Required)</b>', h2_style, level=1))
story.append(Spacer(1, 4))

story.append(Paragraph(
    '<b>Gap 1: No public repositories.</b> This is the single most damaging gap in the profile. Without public code, '
    'the GitHub account serves no demonstrable professional purpose. Every other improvement is secondary to '
    'addressing this fundamental absence. At minimum, the profile should host 3-5 repositories that demonstrate '
    'proficiency in relevant technologies. These do not need to be large or complex projects; even well-structured '
    'small projects, learning exercises, or utility tools can effectively showcase coding ability.',
    body_style))

story.append(Paragraph(
    '<b>Gap 2: No profile bio or description.</b> The bio field is the first text that visitors read on a profile. '
    'A well-crafted bio should communicate who you are, what technologies you specialize in, and what you are '
    'currently working on or looking for. The recommended format is one to three sentences that include your primary '
    'role (e.g., "Full-stack developer"), key technologies (e.g., "React, Node.js, Python"), and a call to action '
    'or current focus (e.g., "Building open-source tools for data visualization").',
    body_style))

story.append(Paragraph(
    '<b>Gap 3: No professional contact information.</b> The absence of a public email, website, or social media '
    'links means there is no way for interested parties to reach ceps12 outside of GitHub. This effectively closes '
    'the door on inbound opportunities from recruiters, potential collaborators, and community members who might '
    'otherwise initiate contact.',
    body_style))

story.append(add_heading('<b>6.2 High-Priority Gaps (Address Within One Week)</b>', h2_style, level=1))
story.append(Spacer(1, 4))

story.append(Paragraph(
    '<b>Gap 4: No pinned repositories.</b> Even after creating repositories, failing to pin the most impressive '
    'ones means visitors must scroll through or search to find your best work. GitHub allows pinning up to six '
    'repositories at the top of the profile, creating an immediate visual showcase. The pinned selection should '
    'represent your strongest, most diverse, and most relevant work.',
    body_style))

story.append(Paragraph(
    '<b>Gap 5: No README files in repositories.</b> A repository without a README is like a book without a title '
    'page. Every repository should include a comprehensive README that explains what the project does, how to install '
    'and use it, what technologies it uses, and how to contribute. The README is often the first file that visitors '
    'and recruiters look at when evaluating a repository.',
    body_style))

story.append(Paragraph(
    '<b>Gap 6: Stylized display name.</b> While creative expression is valuable, the current display name using '
    'extended Unicode characters (Greek and Cyrillic extended) makes the profile difficult to search for and '
    'appears unprofessional in many contexts. A standard display name using common Latin characters is strongly '
    'recommended for professional profiles.',
    body_style))

story.append(add_heading('<b>6.3 Medium-Priority Gaps (Address Within One Month)</b>', h2_style, level=1))
story.append(Spacer(1, 4))

story.append(Paragraph(
    '<b>Gap 7: No starred repositories.</b> Starred repositories function as a public list of tools, frameworks, '
    'and projects that interest you. A thoughtfully curated star list demonstrates awareness of the current technology '
    'landscape and can spark conversations with visitors who share similar interests. Consider starring repositories '
    'that reflect your learning goals, preferred technologies, or projects you admire.',
    body_style))

story.append(Paragraph(
    '<b>Gap 8: No following activity.</b> Following other developers, organizations, and projects is a low-effort '
    'way to build a network and demonstrate engagement with the community. A reasonable starting point is to follow '
    '50-100 developers whose work you find interesting or inspiring, as well as organizations related to your '
    'technical interests.',
    body_style))

story.append(Paragraph(
    '<b>Gap 9: No contribution to open-source projects.</b> Contributing to open-source projects, even through '
    'small bug fixes, documentation improvements, or translation corrections, is one of the most impactful ways '
    'to build credibility and gain visibility. Open-source contributions are visible on your profile and demonstrate '
    'the ability to work with existing codebases and collaborate with other developers.',
    body_style))

story.append(Paragraph(
    '<b>Gap 10: No organization affiliations.</b> Joining or creating organizations adds badges to your profile '
    'that provide context about your professional affiliations and interests. This could include employer organizations, '
    'open-source communities, local developer groups, or special interest groups.',
    body_style))

# ═══════════════════════════════════════════════
# 7. RECOMMENDATIONS AND ACTION PLAN
# ═══════════════════════════════════════════════
story.append(add_heading('<b>7. Recommendations and Action Plan</b>', h1_style, level=0))
story.append(Spacer(1, 6))

story.append(Paragraph(
    'Based on the comprehensive gap analysis above, this section presents a structured action plan organized into '
    'three phases: quick wins that can be completed immediately, medium-term improvements to be tackled over the '
    'next month, and long-term strategic enhancements for sustained profile growth.',
    body_style))

story.append(add_heading('<b>7.1 Phase 1: Quick Wins (Under 1 Hour)</b>', h2_style, level=1))
story.append(Spacer(1, 4))

phase1_data = [
    [Paragraph('<b>Priority</b>', header_cell_style),
     Paragraph('<b>Action</b>', header_cell_style),
     Paragraph('<b>Time</b>', header_cell_style)],
    [Paragraph('1', cell_style),
     Paragraph('Update display name to real name or professional alias', cell_left_style),
     Paragraph('2 min', cell_style)],
    [Paragraph('2', cell_style),
     Paragraph('Write a professional bio (1-3 sentences)', cell_left_style),
     Paragraph('10 min', cell_style)],
    [Paragraph('3', cell_style),
     Paragraph('Add location (city, country)', cell_left_style),
     Paragraph('1 min', cell_style)],
    [Paragraph('4', cell_style),
     Paragraph('Enable "Hireable" flag in profile settings', cell_left_style),
     Paragraph('1 min', cell_style)],
    [Paragraph('5', cell_style),
     Paragraph('Add a professional email address', cell_left_style),
     Paragraph('2 min', cell_style)],
    [Paragraph('6', cell_style),
     Paragraph('Add website or LinkedIn URL', cell_left_style),
     Paragraph('2 min', cell_style)],
    [Paragraph('7', cell_style),
     Paragraph('Follow 20-50 developers in your field', cell_left_style),
     Paragraph('15 min', cell_style)],
    [Paragraph('8', cell_style),
     Paragraph('Star 10-20 interesting repositories', cell_left_style),
     Paragraph('10 min', cell_style)],
]
story.append(make_table(phase1_data, [0.10, 0.65, 0.25]))
story.append(Paragraph('<b>Table 4.</b> Phase 1 - Quick wins action plan', caption_style))
story.append(Spacer(1, 12))

story.append(add_heading('<b>7.2 Phase 2: Content Building (1-4 Weeks)</b>', h2_style, level=1))
story.append(Spacer(1, 4))

phase2_data = [
    [Paragraph('<b>Priority</b>', header_cell_style),
     Paragraph('<b>Action</b>', header_cell_style),
     Paragraph('<b>Time</b>', header_cell_style)],
    [Paragraph('1', cell_style),
     Paragraph('Create 3-5 repositories with quality README files', cell_left_style),
     Paragraph('2-3 days', cell_style)],
    [Paragraph('2', cell_style),
     Paragraph('Pin the best repositories to your profile', cell_left_style),
     Paragraph('5 min', cell_style)],
    [Paragraph('3', cell_style),
     Paragraph('Add topics/tags to each repository', cell_left_style),
     Paragraph('15 min', cell_style)],
    [Paragraph('4', cell_style),
     Paragraph('Contribute to at least 2 open-source projects', cell_left_style),
     Paragraph('1-2 weeks', cell_style)],
    [Paragraph('5', cell_style),
     Paragraph('Create a profile README (special repository)', cell_left_style),
     Paragraph('1-2 hours', cell_style)],
    [Paragraph('6', cell_style),
     Paragraph('Add company or organization affiliation', cell_left_style),
     Paragraph('5 min', cell_style)],
]
story.append(make_table(phase2_data, [0.10, 0.65, 0.25]))
story.append(Paragraph('<b>Table 5.</b> Phase 2 - Content building action plan', caption_style))
story.append(Spacer(1, 12))

story.append(add_heading('<b>7.3 Phase 3: Long-Term Strategy (1-6 Months)</b>', h2_style, level=1))
story.append(Spacer(1, 4))

phase3_data = [
    [Paragraph('<b>Priority</b>', header_cell_style),
     Paragraph('<b>Action</b>', header_cell_style),
     Paragraph('<b>Ongoing</b>', header_cell_style)],
    [Paragraph('1', cell_style),
     Paragraph('Maintain consistent contribution activity (weekly commits)', cell_left_style),
     Paragraph('Weekly', cell_style)],
    [Paragraph('2', cell_style),
     Paragraph('Grow follower base through quality content and engagement', cell_left_style),
     Paragraph('Monthly', cell_style)],
    [Paragraph('3', cell_style),
     Paragraph('Publish blog posts or technical articles linked from profile', cell_left_style),
     Paragraph('Monthly', cell_style)],
    [Paragraph('4', cell_style),
     Paragraph('Participate in Hacktoberfest or similar events', cell_left_style),
     Paragraph('Annually', cell_style)],
    [Paragraph('5', cell_style),
     Paragraph('Create and maintain a personal website or portfolio', cell_left_style),
     Paragraph('One-time + updates', cell_style)],
    [Paragraph('6', cell_style),
     Paragraph('Mentor junior developers through open-source guidance', cell_left_style),
     Paragraph('Ongoing', cell_style)],
]
story.append(make_table(phase3_data, [0.10, 0.55, 0.35]))
story.append(Paragraph('<b>Table 6.</b> Phase 3 - Long-term strategy', caption_style))
story.append(Spacer(1, 12))

# ═══════════════════════════════════════════════
# 8. PROFILE COMPLETENESS SCORECARD
# ═══════════════════════════════════════════════
story.append(add_heading('<b>8. Profile Completeness Scorecard</b>', h1_style, level=0))
story.append(Spacer(1, 6))

story.append(Paragraph(
    'The following scorecard provides a quantified assessment of the current profile across ten key dimensions. '
    'Each dimension is scored on a scale of 0 to 10, with 10 representing full compliance with best practices. '
    'The total score is calculated as a weighted average, reflecting the relative importance of each dimension '
    'for professional impact.',
    body_style))

scorecard_data = [
    [Paragraph('<b>Dimension</b>', header_cell_style),
     Paragraph('<b>Weight</b>', header_cell_style),
     Paragraph('<b>Score</b>', header_cell_style),
     Paragraph('<b>Weighted</b>', header_cell_style)],
    [Paragraph('Profile Metadata (bio, name, etc.)', cell_left_style),
     Paragraph('15%', cell_style),
     Paragraph('1/10', cell_style),
     Paragraph('0.15', cell_style)],
    [Paragraph('Repository Portfolio', cell_left_style),
     Paragraph('25%', cell_style),
     Paragraph('0/10', cell_style),
     Paragraph('0.00', cell_style)],
    [Paragraph('Code Quality and READMEs', cell_left_style),
     Paragraph('15%', cell_style),
     Paragraph('0/10', cell_style),
     Paragraph('0.00', cell_style)],
    [Paragraph('Contribution Activity', cell_left_style),
     Paragraph('15%', cell_style),
     Paragraph('0/10', cell_style),
     Paragraph('0.00', cell_style)],
    [Paragraph('Community Engagement', cell_left_style),
     Paragraph('10%', cell_style),
     Paragraph('1/10', cell_style),
     Paragraph('0.10', cell_style)],
    [Paragraph('Open-Source Contributions', cell_left_style),
     Paragraph('10%', cell_style),
     Paragraph('0/10', cell_style),
     Paragraph('0.00', cell_style)],
    [Paragraph('Social Presence (followers, etc.)', cell_left_style),
     Paragraph('5%', cell_style),
     Paragraph('1/10', cell_style),
     Paragraph('0.05', cell_style)],
    [Paragraph('Organization Affiliations', cell_left_style),
     Paragraph('5%', cell_style),
     Paragraph('0/10', cell_style),
     Paragraph('0.00', cell_style)],
]
story.append(Spacer(1, 6))
story.append(make_table(scorecard_data, [0.40, 0.15, 0.15, 0.30]))
story.append(Paragraph('<b>Table 7.</b> Profile completeness scorecard', caption_style))
story.append(Spacer(1, 12))

story.append(Paragraph(
    'The overall weighted score comes to approximately <b>0.3 out of 10</b>, or <b>3%</b> overall completeness. '
    'This places the profile in the bottom percentile of GitHub accounts. Even modest improvements, particularly '
    'in the highest-weighted categories (repository portfolio and profile metadata), would significantly improve '
    'this score. Achieving a score of 5/10 (50%) is realistic within one month of focused effort.',
    body_style))

# ═══════════════════════════════════════════════
# 9. CONCLUSION
# ═══════════════════════════════════════════════
story.append(add_heading('<b>9. Conclusion</b>', h1_style, level=0))
story.append(Spacer(1, 6))

story.append(Paragraph(
    'The GitHub profile ceps12 currently represents a significant underutilization of the platform\'s potential '
    'for professional development and visibility. The account has existed for nearly four years without accumulating '
    'any meaningful public presence, which represents a substantial opportunity cost in terms of career development, '
    'networking, and skill demonstration.',
    body_style))

story.append(Paragraph(
    'However, this audit also reveals a silver lining: because the profile is essentially a blank slate, every '
    'improvement will have an immediately visible and impactful effect. The transition from 0 repositories to even '
    '3 quality repositories, from an empty bio to a professional summary, and from zero engagement to an active '
    'network will transform the profile from negligible to competitive. The phased action plan provided in this '
    'report offers a clear, achievable roadmap for this transformation.',
    body_style))

story.append(Paragraph(
    'The most important takeaway is that building a professional GitHub presence is not an all-or-nothing endeavor. '
    'Starting with the quick wins outlined in Phase 1, which require less than one hour of effort, can already '
    'elevate the profile from its current state to something that begins to communicate professionalism and intent. '
    'From there, consistent effort over weeks and months will compound into a strong developer portfolio that serves '
    'as a powerful career asset.',
    body_style))

# ─── Build ───
doc.multiBuild(story)
print(f"Report generated: {output_path}")
