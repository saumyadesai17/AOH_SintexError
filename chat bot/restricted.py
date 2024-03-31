import google.generativeai as palm
from dotenv import load_dotenv
import os

load_dotenv()

palm_api_key = os.getenv('PALM_API_KEY')

palm.configure(api_key=palm_api_key)

print("Welcome to Education Placement Assistant!")
print("Ask me anything related to education placements, interview help, or technical skills. Type 'exit' to end the chat.")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Thank you for using Education Placement Assistant. Visit again!")
        break

    # Check if user input is relevant
    is_relevant = any(term in user_input.lower() for term in [
        # Education
        "education", "school", "university", "college", "degree", "major", 
        "minor", "course", "program", "curriculum", "transcript", "GPA", 
        "scholarship", "fellowship", "financial aid", "grant", "application", 
        "admission", "career guidance", "career counseling", "career path", 
        "career goals", "skill development", "training", "certification", 

        # Placement
        "placement", "job", "internship", "co-op", "career fair", 
        "resume", "CV", "cover letter", "application form", "portfolio", 
        "job search", "networking", "interview", "selection process", 
        "offer letter", "salary negotiation", "work culture", "company research",

        # Interview Help
        "interview", "soft skills", "technical skills", "communication", 
        "presentation", "teamwork", "leadership", "problem-solving", 
        "creativity", "critical thinking", "time management", "stress management", 
        "aptitude test", "aptitude questions", "logical reasoning", "verbal reasoning", 
        "quantitative reasoning", "analytical reasoning", "group discussion", 
        "DSA", "data structures", "algorithms", "coding test", "technical interview",

        # DSA Specific Keywords
        "array", "linked list", "stack", "queue", "hash table", "tree", "graph", 
        "binary search tree", "AVL tree", "red-black tree", "heap", "trie", 
        "sorting", "searching", "time complexity", "space complexity", 
        "big O notation", "dynamic programming", "recursion", "backtracking", 
        "greedy algorithms", "divide and conquer", "brute force", 
        "depth-first search", "breadth-first search", "topological sort", 
        "minimum spanning tree", "shortest path algorithms", 
        "dijkstra's algorithm", "bellman-ford algorithm", "floyd-warshall algorithm", 
        "gcd",

         # Data Science
        "data science", "data scientist", "statistics", "probability",
        "hypothesis testing", "data analysis", "data visualization",
        "machine learning", "deep learning", "natural language processing",
        "computer vision", "time series analysis", "big data", "Apache Spark",
        "Hadoop", "scikit-learn", "TensorFlow", "PyTorch", "R", "pandas",
        "NumPy", "exploratory data analysis", "data modeling", "data cleaning",
        "feature engineering", "model selection", "model evaluation",
        "A/B testing", "data storytelling", "business intelligence",

         # Software Developer
        "software development", "software engineer", "programmer",
        "coding", "programming language", "web development", "mobile development",
        "front-end", "back-end", "full-stack", "API", "database",
        "software design", "software architecture", "testing", "debugging",
        "version control", "agile methodology", "waterfall methodology",
        "DevOps", "cloud computing", "UX/UI design", "clean code",
        "OOP", "functional programming", "design patterns", "unit testing",
        "integration testing", "automation", "CI/CD","software Developer"

        # Data Analyst
        "data analyst", "data analysis", "business intelligence", "data visualization",
        "SQL", "NoSQL", "data mining", "data warehousing", "data storytelling",
        "reporting", "dashboards", "ETL", "data wrangling", "data cleaning",
        "descriptive statistics", "inferential statistics", "data interpretation",
        "data communication", "data exploration", "A/B testing",

        # Cybersecurity
        "cybersecurity", "cybersecurity analyst", "information security",
        "vulnerability assessment", "penetration testing", "ethical hacking",
        "network security", "cloud security", "application security",
        "incident response", "threat intelligence", "cryptography",
        "firewalls", "intrusion detection systems", "data security",
        "privacy", "compliance", "risk management", "social engineering",

        # Blockchain
        "blockchain", "distributed ledger technology", "cryptocurrency",
        "bitcoin", "ethereum", "smart contracts", "dapps", "consensus mechanisms",
        "mining", "hashing", "cryptography", "security", "scalability",
        "decentralization", "tokenization", "blockchain applications",

        # Additional Terms
        "skill", "experience", "qualification", "reference", "motivation", 
        "ethics", "professionalism", "work-life balance", "growth opportunities", 
        "benefits", "remote work", "compensation", "resignation", "layoff","dsa","professions"
    ])

    if is_relevant:
        response = palm.chat(messages=user_input)
        print(f"Assistant: {response.last}")
    else:
        print(f"Assistant: While my focus is on education placements, interview help, and technical skills, I'm still learning. How can I assist you today in these areas?")

