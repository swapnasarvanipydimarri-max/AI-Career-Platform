def recommend_courses(missing_skills):
    """
    Recommend learning resources based on missing skills.
    """

    course_database = {
        "Python": {
            "course": "Python Programming",
            "platform": "freeCodeCamp",
            "resource": "https://www.freecodecamp.org/learn/scientific-computing-with-python/"
        },

        "SQL": {
            "course": "SQL Tutorial",
            "platform": "W3Schools",
            "resource": "https://www.w3schools.com/sql/"
        },

        "Machine Learning": {
            "course": "Machine Learning",
            "platform": "Google for Developers",
            "resource": "https://developers.google.com/machine-learning/crash-course"
        },

        "Data Analysis": {
            "course": "Data Analysis with Python",
            "platform": "freeCodeCamp",
            "resource": "https://www.freecodecamp.org/learn/data-analysis-with-python/"
        },

        "Pandas": {
            "course": "Pandas Documentation",
            "platform": "Pandas",
            "resource": "https://pandas.pydata.org/docs/getting_started/intro_tutorials/"
        },

        "NumPy": {
            "course": "NumPy Tutorials",
            "platform": "NumPy",
            "resource": "https://numpy.org/learn/"
        },

        "Git": {
            "course": "Git Documentation",
            "platform": "Git",
            "resource": "https://git-scm.com/doc"
        },

        "GitHub": {
            "course": "GitHub Skills",
            "platform": "GitHub",
            "resource": "https://skills.github.com/"
        },

        "Docker": {
            "course": "Docker Get Started",
            "platform": "Docker",
            "resource": "https://docs.docker.com/get-started/"
        },

        "Cloud Computing": {
            "course": "Cloud Computing Basics",
            "platform": "AWS",
            "resource": "https://aws.amazon.com/getting-started/"
        },

        "AWS": {
            "course": "AWS Getting Started",
            "platform": "AWS",
            "resource": "https://aws.amazon.com/getting-started/"
        },

        "Java": {
            "course": "Java Tutorials",
            "platform": "Oracle",
            "resource": "https://docs.oracle.com/javase/tutorial/"
        },

        "JavaScript": {
            "course": "JavaScript Guide",
            "platform": "MDN",
            "resource": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"
        },

        "HTML": {
            "course": "HTML Tutorials",
            "platform": "W3Schools",
            "resource": "https://www.w3schools.com/html/"
        },

        "CSS": {
            "course": "CSS Tutorials",
            "platform": "W3Schools",
            "resource": "https://www.w3schools.com/css/"
        },

        "React": {
            "course": "React Learn",
            "platform": "React",
            "resource": "https://react.dev/learn"
        },

        "Statistics": {
            "course": "Statistics",
            "platform": "Khan Academy",
            "resource": "https://www.khanacademy.org/math/statistics-probability"
        }
    }

    recommendations = []

    for skill in missing_skills:

        skill_key = skill.strip()

        if skill_key in course_database:

            course = course_database[skill_key]

            recommendations.append({
                "skill": skill_key,
                "course": course["course"],
                "platform": course["platform"],
                "resource": course["resource"]
            })

    return recommendations