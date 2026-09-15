from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

def create_resume_pdf(filename, title, contact, summary, experience, skills):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette & Styles
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=12
    )
    
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=4,
        textTransform='uppercase'
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )
    
    role_title_style = ParagraphStyle(
        'RoleTitleStyle',
        parent=styles['Normal'],
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#0284C7'),
        fontName='Helvetica-Bold'
    )

    story = []

    # Header
    story.append(Paragraph(title, name_style))
    story.append(Paragraph(contact, contact_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=10))

    # Summary Section
    story.append(Paragraph("Professional Summary", section_style))
    story.append(Paragraph(summary, body_style))
    story.append(Spacer(1, 6))

    # Experience Section
    story.append(Paragraph("Professional Experience", section_style))
    for item in experience:
        story.append(Paragraph(f"<b>{item['role']}</b> — {item['company']} <i>({item['dates']})</i>", role_title_style))
        for bullet in item['bullets']:
            story.append(Paragraph(f"• {bullet}", body_style))
        story.append(Spacer(1, 4))

    # Skills Section
    story.append(Spacer(1, 4))
    story.append(Paragraph("Technical Skills & Core Competencies", section_style))
    story.append(Paragraph(skills, body_style))

    doc.build(story)

# -------------------------------------------------------------------
# 1. Senior Fullstack Engineer Resume
# -------------------------------------------------------------------
create_resume_pdf(
    "senior_fullstack_engineer_resume.pdf",
    "Alex Mercer",
    "San Francisco, CA | alex.mercer@email.com | github.com/alexmercer-dev",
    "Senior Fullstack Engineer with 7+ years of experience designing scalable web applications. Expert in React, Node.js, Python, AWS, and PostgreSQL. Proven track record of optimizing backend performance and delivering intuitive UI designs.",
    [
        {
            "role": "Senior Fullstack Engineer",
            "company": "TechScale Solutions",
            "dates": "2021 – Present",
            "bullets": [
                "Architected and deployed microservices using Node.js and Python on AWS ECS, servicing 2M+ active monthly users.",
                "Built responsive web applications with React, Redux, and TypeScript, improving page load speeds by 40%.",
                "Designed and optimized PostgreSQL database schemas, reducing query latency by 35% across high-traffic endpoints."
            ]
        },
        {
            "role": "Fullstack Developer",
            "company": "CloudPulse Systems",
            "dates": "2018 – 2021",
            "bullets": [
                "Developed RESTful and GraphQL APIs using Node.js and Express to support web and mobile frontends.",
                "Engineered CI/CD pipelines utilizing AWS CodePipeline and Docker, cutting deployment cycle times in half."
            ]
        }
    ],
    "<b>Languages:</b> Python, JavaScript, TypeScript, SQL<br/>"
    "<b>Frontend:</b> React, Redux, HTML5, CSS3, Tailwind CSS<br/>"
    "<b>Backend & Databases:</b> Node.js, Express, PostgreSQL, Redis, GraphQL<br/>"
    "<b>Cloud & DevOps:</b> AWS (EC2, S3, ECS, Lambda), Docker, CI/CD"
)

# -------------------------------------------------------------------
# 2. Lead Architect Executive Resume
# -------------------------------------------------------------------
create_resume_pdf(
    "lead_architect_executive_resume.pdf",
    "Eleanor Vance",
    "New York, NY | e.vance@enterprise-corp.com | linkedin.com/in/eleanor-vance-exec",
    "Executive-level Software Architect and Engineering Director with over 15 years of leadership driving cloud transformation, enterprise software governance, and multi-team engineering strategies. Successfully managed $20M+ technology budgets and scaled global engineering divisions.",
    [
        {
            "role": "VP of Enterprise Architecture",
            "company": "Global Enterprise Systems",
            "dates": "2019 – Present",
            "bullets": [
                "Spearheaded enterprise-wide cloud migration strategy across 4 business units, transitioning legacy monoliths to AWS cloud-native architecture.",
                "Directed 8 engineering managers and 60+ engineers across global teams, improving software delivery metrics by 300%.",
                "Established software architecture governance, security standards, and compliance protocols across enterprise data pipelines."
            ]
        },
        {
            "role": "Lead Systems Architect",
            "company": "FinTech Capital Technologies",
            "dates": "2013 – 2019",
            "bullets": [
                "Designed event-driven distributed architecture handling $5B+ in daily financial transactions using Kafka and Kubernetes.",
                "Mentored senior engineers, reduced architectural tech debt, and aligned technology roadmap with executive business goals."
            ]
        }
    ],
    "<b>Leadership:</b> Strategic Planning, Budgeting, Global Team Management, Vendor Relations<br/>"
    "<b>Architecture:</b> Cloud Transformation, Event-Driven Systems, Distributed Infrastructure, Security Governance<br/>"
    "<b>Technologies:</b> AWS, Kubernetes, Apache Kafka, Microservices, Enterprise Integration"
)

# -------------------------------------------------------------------
# 3. Frontend Specialist Resume
# -------------------------------------------------------------------
create_resume_pdf(
    "frontend_specialist_resume.pdf",
    "Jordan Lee",
    "Austin, TX | jordan.lee@ui-designs.io | portfolio.jordanlee.dev",
    "Frontend Specialist and Design Systems Engineer with 5+ years specializing in UI performance, component-driven design systems, and frontend architectural consistency across enterprise web apps.",
    [
        {
            "role": "Lead Frontend Specialist",
            "company": "CreativeUX Labs",
            "dates": "2022 – Present",
            "bullets": [
                "Authored and maintained enterprise-wide React component library used by 12 cross-functional product teams.",
                "Engineered accessible, WCAG 2.1 AA compliant design systems using React, Storybook, and Tailwind CSS.",
                "Implemented micro-frontend architecture using Webpack Module Federation to decouple legacy monolith frontend."
            ]
        },
        {
            "role": "UI Engineer",
            "company": "PixelCraft Studios",
            "dates": "2019 – 2022",
            "bullets": [
                "Developed interactive web dashboards using Vue.js, React, and D3.js for complex data visualization.",
                "Optimized Web Vitals score across web properties, achieving a 98+ Lighthouse performance score."
            ]
        }
    ],
    "<b>UI & Design Systems:</b> Component Architecture, Design Tokens, Storybook, Figma-to-Code<br/>"
    "<b>Core Frontend:</b> JavaScript (ES6+), TypeScript, React, Next.js, Vue.js, HTML5/CSS3<br/>"
    "<b>Styling & Tooling:</b> Tailwind CSS, Styled-Components, Sass, Webpack, Vite, Jest, Cypress"
)

print("PDF files generated successfully!")