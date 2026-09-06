def generate_roadmap(missing_skills):
    roadmap = []

    resources = {
        "Python": "https://www.python.org/about/gettingstarted/",
        "SQL": "https://www.w3schools.com/sql/",
        "Excel": "https://support.microsoft.com/excel",
        "Pandas": "https://pandas.pydata.org/docs/getting_started/",
        "NumPy": "https://numpy.org/learn/",
        "Statistics": "https://www.khanacademy.org/math/statistics-probability",
        "Power BI": "https://learn.microsoft.com/power-bi/",
        "Tableau": "https://www.tableau.com/learn/training",
        "Machine Learning": "https://scikit-learn.org/stable/getting_started.html",
        "Deep Learning": "https://www.tensorflow.org/learn",
        "TensorFlow": "https://www.tensorflow.org/learn",
        "PyTorch": "https://pytorch.org/tutorials/",
        "HTML": "https://developer.mozilla.org/docs/Web/HTML",
        "CSS": "https://developer.mozilla.org/docs/Web/CSS",
        "JavaScript": "https://developer.mozilla.org/docs/Web/JavaScript",
        "React": "https://react.dev/learn",
        "Node.js": "https://nodejs.org/en/learn",
        "Git": "https://git-scm.com/doc",
        "REST API": "https://developer.mozilla.org/docs/Glossary/REST",
        "Java": "https://dev.java/learn/",
        "C++": "https://www.learncpp.com/",
        "Data Structures": "https://www.geeksforgeeks.org/data-structures/",
        "Algorithms": "https://www.geeksforgeeks.org/fundamentals-of-algorithms/",
        "AWS": "https://aws.amazon.com/training/",
        "Azure": "https://learn.microsoft.com/training/azure/",
        "Linux": "https://ubuntu.com/tutorials/command-line-for-beginners",
        "Docker": "https://docs.docker.com/get-started/",
        "Kubernetes": "https://kubernetes.io/docs/tutorials/",
        "Networking": "https://www.cisco.com/site/us/en/learn/training-certifications/training/index.html"
    }

    for index, skill in enumerate(missing_skills, start=1):

        resource = resources.get(
            skill,
            "https://www.google.com/search?q="
            + skill.replace(" ", "+")
            + "+tutorial"
        )

        roadmap.append({
            "step": index,
            "skill": skill,
            "recommendation": (
                f"Learn {skill} through tutorials, "
                "practice exercises, and a small project."
            ),
            "resource": resource
        })

    return roadmap