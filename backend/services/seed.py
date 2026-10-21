from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from backend.database import SessionLocal, Base, engine
from backend.models.user import User
from backend.models.profile import StudentProfile
from backend.models.skill import Skill
from backend.models.assessment import Assessment, AssessmentQuestion, AssessmentSubmission, AssessmentAnswer
from backend.models.pathway import LearningPathway, PathwayStep
from backend.models.resource import LearningResource
from backend.models.mission import DailyMission
from backend.models.progress import StudentProgress
from backend.models.bookmark import Bookmark
from backend.services.auth import get_password_hash
from backend.services.recommender import recommender_engine

def seed_database(db: Session):
    print("[INFO] Checking and seeding SkillVerse database...")

    # 1. Seed Skills if empty
    if db.query(Skill).count() == 0:
        print("[INFO] Seeding Canonical Skills...")
        skills = [
            Skill(
                code="python",
                name="Python Programming",
                category="Programming Languages",
                description="Modern Python fundamentals, data structures, OOP, async programming, and backend systems.",
                icon_name="Terminal",
                difficulty="Beginner to Advanced",
                prerequisites=[],
                color_hex="#3b82f6",
                galaxy_orbit_radius=110
            ),
            Skill(
                code="sql",
                name="SQL & Relational Databases",
                category="Data Management",
                description="Relational database modeling, complex JOINs, indexing, aggregation, and query optimization.",
                icon_name="Database",
                difficulty="Beginner to Intermediate",
                prerequisites=[],
                color_hex="#06b6d4",
                galaxy_orbit_radius=160
            ),
            Skill(
                code="java",
                name="Java Enterprise",
                category="Programming Languages",
                description="Object-oriented architecture, collections framework, multi-threading, JVM internals, and microservices.",
                icon_name="Cpu",
                difficulty="Intermediate",
                prerequisites=[],
                color_hex="#f97316",
                galaxy_orbit_radius=210
            ),
            Skill(
                code="web_dev",
                name="Web Development",
                category="Frontend & Full-Stack",
                description="HTML5, CSS3, modern JavaScript (ES6+), React components, state management, and REST APIs.",
                icon_name="Globe",
                difficulty="Intermediate",
                prerequisites=["python", "sql"],
                color_hex="#8b5cf6",
                galaxy_orbit_radius=260
            ),
            Skill(
                code="data_analytics",
                name="Data Analytics",
                category="Data Science",
                description="Exploratory data analysis, Pandas, NumPy, data cleaning, statistical inference, and visual dashboards.",
                icon_name="BarChart3",
                difficulty="Intermediate",
                prerequisites=["python", "sql"],
                color_hex="#10b981",
                galaxy_orbit_radius=310
            ),
            Skill(
                code="ml",
                name="Machine Learning",
                category="Artificial Intelligence",
                description="Supervised & unsupervised learning, scikit-learn pipelines, model evaluation metrics, and feature engineering.",
                icon_name="Sparkles",
                difficulty="Advanced",
                prerequisites=["python", "data_analytics", "sql"],
                color_hex="#ec4899",
                galaxy_orbit_radius=360
            )
        ]
        db.add_all(skills)
        db.commit()

    # 2. Seed Diagnostic Assessment & Questions
    if db.query(Assessment).count() == 0:
        print("-> Seeding Comprehensive Assessment Questions...")
        assessment = Assessment(
            title="SkillVerse Global Technical Diagnostic",
            description="Comprehensive benchmark covering Python, Java, SQL, Data Analytics, Web Development, and Machine Learning.",
            category="Diagnostic"
        )
        db.add(assessment)
        db.commit()
        db.refresh(assessment)

        questions = [
            # Python Questions
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="python",
                topic="List Comprehensions & Immutability",
                difficulty="Beginner",
                question_text="What is the output of `[x * 2 for x in range(3)]` in Python?",
                options=["[0, 2, 4]", "[2, 4, 6]", "[0, 1, 2]", "[1, 2, 3]"],
                correct_option_index=0,
                explanation="range(3) produces 0, 1, 2. Multiplying each by 2 yields [0, 2, 4]."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="python",
                topic="Data Structures & Dictionary Lookup",
                difficulty="Intermediate",
                question_text="What is the average time complexity of key lookup in a Python dictionary?",
                options=["O(1)", "O(n)", "O(log n)", "O(n^2)"],
                correct_option_index=0,
                explanation="Python dictionaries are implemented with hash tables, providing average O(1) constant time lookup."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="python",
                topic="Generators & Memory Efficiency",
                difficulty="Intermediate",
                question_text="Which keyword converts a standard Python function into a generator iterator?",
                options=["yield", "return", "generate", "async"],
                correct_option_index=0,
                explanation="The 'yield' statement suspends function execution and yields a value back to the caller while maintaining state."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="python",
                topic="Variable Scope & Closures",
                difficulty="Advanced",
                question_text="Which keyword allows modifying a variable defined in an outer, non-global enclosing function scope?",
                options=["nonlocal", "global", "outer", "super"],
                correct_option_index=0,
                explanation="'nonlocal' binds a variable to an outer enclosing function scope instead of the global scope."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="python",
                topic="Exception Handling Mechanics",
                difficulty="Intermediate",
                question_text="In Python's try-except-else-finally construct, when does the 'else' block execute?",
                options=["Only if no exceptions were raised in the try block", "Always after the finally block", "Only when an exception is caught", "Never in production"],
                correct_option_index=0,
                explanation="The 'else' block executes only if the 'try' block completes without raising any exceptions."
            ),

            # Java Questions
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="java",
                topic="Object References & Memory",
                difficulty="Beginner",
                question_text="What is the default value of an uninitialized object reference instance variable in Java?",
                options=["null", "0", "false", "undefined"],
                correct_option_index=0,
                explanation="Reference types default to null when declared as fields in a class."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="java",
                topic="Collections & Maps",
                difficulty="Intermediate",
                question_text="Which Java collection class guarantees natural or comparator-based sorted order of keys?",
                options=["TreeMap", "HashMap", "LinkedHashMap", "HashSet"],
                correct_option_index=0,
                explanation="TreeMap is backed by a Red-Black tree and guarantees that keys are ordered according to natural ordering or a Comparator."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="java",
                topic="OOP Polymorphism & Method Overriding",
                difficulty="Intermediate",
                question_text="Can a private or static method be overridden in a Java subclass?",
                options=["No, neither can be overridden polymorphically", "Yes, both can be overridden", "Only static methods can be overridden", "Only private methods can be overridden"],
                correct_option_index=0,
                explanation="Static methods are hidden (method hiding, resolved at compile-time) and private methods are not inherited, so neither is polymorphically overridden."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="java",
                topic="JVM Memory Management",
                difficulty="Advanced",
                question_text="Where are Java local primitive variables and method frames allocated during execution?",
                options=["On the Thread Call Stack", "In the PermGen / Metaspace", "On the Garbage-Collected Heap", "In Native Memory"],
                correct_option_index=0,
                explanation="Local primitive variables and method call frames reside on the thread-specific stack, while objects reside on the heap."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="java",
                topic="Functional Interfaces & Streams",
                difficulty="Intermediate",
                question_text="Which functional interface in `java.util.function` takes one argument and returns a boolean?",
                options=["Predicate<T>", "Consumer<T>", "Function<T, R>", "Supplier<T>"],
                correct_option_index=0,
                explanation="Predicate<T> defines `boolean test(T t)` used extensively for filtering in Java Streams."
            ),

            # SQL Questions
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="sql",
                topic="JOIN Operations",
                difficulty="Beginner",
                question_text="Which SQL JOIN returns all rows from the left table and matched rows from the right table?",
                options=["LEFT JOIN", "INNER JOIN", "FULL OUTER JOIN", "CROSS JOIN"],
                correct_option_index=0,
                explanation="LEFT JOIN (or LEFT OUTER JOIN) preserves all records from the left table regardless of whether matches exist on the right."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="sql",
                topic="Aggregation & Filtering Conditions",
                difficulty="Intermediate",
                question_text="What is the critical distinction between WHERE and HAVING in SQL?",
                options=["WHERE filters individual rows before grouping; HAVING filters aggregated groups", "WHERE operates on groups; HAVING operates on columns", "They are 100% interchangeable aliases", "HAVING cannot be used with GROUP BY"],
                correct_option_index=0,
                explanation="WHERE applies filters before GROUP BY aggregation; HAVING filters the aggregated groups created by GROUP BY."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="sql",
                topic="Indexes & Query Optimization",
                difficulty="Intermediate",
                question_text="What data structure is standard for B-tree indexes in relational database engines like PostgreSQL?",
                options=["Balanced Search Tree (B-Tree)", "Linked List", "Adjacency Matrix", "Binary Min-Heap"],
                correct_option_index=0,
                explanation="B-Tree indexes maintain sorted keys and logarithmic search efficiency for equality and range queries."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="sql",
                topic="ACID Properties & Transactions",
                difficulty="Advanced",
                question_text="Which ACID property ensures that intermediate transaction states are invisible to other concurrent transactions?",
                options=["Isolation", "Atomicity", "Consistency", "Durability"],
                correct_option_index=0,
                explanation="Isolation defines transaction concurrency boundaries, preventing dirty reads or phantom reads based on isolation levels."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="sql",
                topic="Window Functions",
                difficulty="Advanced",
                question_text="Which clause is mandatory when using a SQL Window function like `ROW_NUMBER()` or `RANK()`?",
                options=["OVER ()", "GROUP BY", "CASCADE", "PARTITION ONLY"],
                correct_option_index=0,
                explanation="The OVER () clause designates a window over which the analytical calculation applies."
            ),

            # Web Development Questions
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="web_dev",
                topic="React Component State & Hooks",
                difficulty="Beginner",
                question_text="Why must React state never be mutated directly (e.g. `state.count = 5`)?",
                options=["Direct mutation bypasses React's virtual DOM reconciliation and does not trigger re-renders", "It triggers a JavaScript runtime syntax error", "It forces an immediate page reload", "State cannot hold numerical values"],
                correct_option_index=0,
                explanation="React relies on immutable state updates to detect changes through shallow comparison and trigger reconciliation."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="web_dev",
                topic="HTTP & REST Status Codes",
                difficulty="Intermediate",
                question_text="Which HTTP status code signifies that a new resource was successfully created on the server?",
                options=["201 Created", "200 OK", "204 No Content", "304 Not Modified"],
                correct_option_index=0,
                explanation="201 Created specifically denotes successful resource creation, commonly returned from POST endpoints."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="web_dev",
                topic="Asynchronous JavaScript & Event Loop",
                difficulty="Intermediate",
                question_text="In JavaScript's event loop, where do resolved Promise callbacks (`.then()`, `await`) execute?",
                options=["In the Microtask Queue", "In the Macrotask / Task Queue", "In the Call Stack directly without queuing", "Inside Web Worker threads"],
                correct_option_index=0,
                explanation="Promises resolve into the Microtask Queue, which executes with higher priority immediately following current script execution."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="web_dev",
                topic="CSS Layout & Flexbox",
                difficulty="Beginner",
                question_text="In CSS Flexbox, which property aligns items along the cross axis?",
                options=["align-items", "justify-content", "flex-direction", "flex-wrap"],
                correct_option_index=0,
                explanation="justify-content distributes along the main axis; align-items aligns items along the perpendicular cross axis."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="web_dev",
                topic="Web Security & CORS",
                difficulty="Advanced",
                question_text="What is the purpose of Cross-Origin Resource Sharing (CORS) in web browsers?",
                options=["Allow servers to declare which external origins are permitted to access their resources", "Encrypt all network payloads using TLS", "Prevent SQL injection attacks", "Speed up DNS resolution"],
                correct_option_index=0,
                explanation="CORS is a browser security mechanism that uses HTTP headers to tell browsers whether a web application running at one origin has permission to access resources from a different origin."
            ),

            # Data Analytics Questions
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="data_analytics",
                topic="Pandas DataFrame Operations",
                difficulty="Beginner",
                question_text="In Pandas, which method returns summary statistics (count, mean, std, min, quartiles, max) for numeric columns?",
                options=["df.describe()", "df.info()", "df.summary()", "df.aggregate()"],
                correct_option_index=0,
                explanation="df.describe() generates comprehensive descriptive statistics of numeric DataFrame columns."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="data_analytics",
                topic="Missing Value Imputation",
                difficulty="Intermediate",
                question_text="Why might median imputation be preferred over mean imputation for skewed numerical features?",
                options=["The median is robust against extreme outliers", "The median is always a whole integer", "The mean requires 10x more computation", "Median works on text strings"],
                correct_option_index=0,
                explanation="Outliers pull the mean away from the central tendency; the median is resistant to extreme values."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="data_analytics",
                topic="Data Visualization Charts",
                difficulty="Beginner",
                question_text="Which visualization chart is ideal for observing the frequency distribution of a continuous numeric variable?",
                options=["Histogram", "Pie Chart", "Spider Radar Chart", "Gantt Chart"],
                correct_option_index=0,
                explanation="Histograms bin continuous values into discrete intervals and display frequency counts across ranges."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="data_analytics",
                topic="Correlation vs Causation",
                difficulty="Intermediate",
                question_text="What does a Pearson correlation coefficient of -0.85 between variables X and Y indicate?",
                options=["A strong negative linear relationship", "Zero correlation", "X directly causes Y to decrease", "A calculation error (must be positive)"],
                correct_option_index=0,
                explanation="Pearson's r ranges from -1 to +1; -0.85 signifies a strong inverse linear relationship."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="data_analytics",
                topic="Grouping & Aggregation",
                difficulty="Intermediate",
                question_text="In Pandas, which method performs the 'split-apply-combine' workflow across categories?",
                options=["df.groupby()", "df.pivot()", "df.merge()", "df.melt()"],
                correct_option_index=0,
                explanation="groupby() splits the data into groups based on some criteria, applies a function, and combines the results."
            ),

            # Machine Learning Questions
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="ml",
                topic="Model Evaluation & Metrics",
                difficulty="Beginner",
                question_text="Why is raw Accuracy often misleading for evaluating models on highly imbalanced datasets (e.g. 99% negative, 1% positive)?",
                options=["A naive model predicting only the majority class achieves 99% accuracy while failing to detect the minority class", "Accuracy can only be computed for regression tasks", "Accuracy values cannot exceed 50%", "Scikit-learn disallows accuracy on imbalanced data"],
                correct_option_index=0,
                explanation="On imbalanced datasets, majority-class bias leads to high accuracy despite zero true positive detections. Precision, Recall, and F1-score are needed."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="ml",
                topic="Overfitting & Bias-Variance Tradeoff",
                difficulty="Intermediate",
                question_text="What symptom characterizes high variance in a machine learning model?",
                options=["High training accuracy but poor generalization / low test performance (overfitting)", "High error on both training and test data (underfitting)", "Zero gradient during backpropagation", "Model requires zero training data"],
                correct_option_index=0,
                explanation="High variance models overfit the noise in the training set and fail to generalize to unseen test data."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="ml",
                topic="Feature Preprocessing & Scaling",
                difficulty="Intermediate",
                question_text="Why must feature scaling (e.g. StandardScaler) be fit strictly on training data and not on the whole dataset before splitting?",
                options=["To prevent data leakage from the test set into the model training pipeline", "StandardScaler fails if run on more than 100 rows", "It saves memory in Python", "Test datasets cannot contain numeric values"],
                correct_option_index=0,
                explanation="Fitting scalers or encoders on the combined dataset leaks distribution parameters (mean/variance) from test data into training."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="ml",
                topic="Regularization Techniques",
                difficulty="Advanced",
                question_text="Which form of linear model regularization encourages sparse feature weights by driving irrelevant coefficients strictly to zero?",
                options=["L1 Regularization (Lasso)", "L2 Regularization (Ridge)", "Early Stopping", "Batch Normalization"],
                correct_option_index=0,
                explanation="L1 penalty (absolute values) produces diamond-shaped constraint boundaries that zero out coefficients, performing automatic feature selection."
            ),
            AssessmentQuestion(
                assessment_id=assessment.id,
                skill_code="ml",
                topic="Cross-Validation Strategies",
                difficulty="Intermediate",
                question_text="What is the primary advantage of k-fold cross-validation over a single train-test split?",
                options=["Provides a more reliable, lower-variance estimate of model generalization performance across data partitions", "Reduces computational training time by k times", "Guarantees 100% test accuracy", "Eliminates the need for hyperparameters"],
                correct_option_index=0,
                explanation="k-fold cross-validation rotates training and validation folds across all data points, minimizing sample bias."
            )
        ]
        db.add_all(questions)
        db.commit()

    # 3. Seed Learning Resources Catalog
    if db.query(LearningResource).count() == 0:
        print("-> Seeding Verified Learning Resources...")
        resources = [
            # Python
            LearningResource(
                title="Python Official Documentation & Tutorial",
                skill_code="python",
                category="Documentation",
                resource_type="documentation",
                url="https://docs.python.org/3/tutorial/",
                is_free=True,
                difficulty="Beginner",
                rating=4.9,
                estimated_time="4 hours",
                provider="Python Software Foundation",
                description="Comprehensive official guide covering fundamental data types, control flow, functions, modules, and error handling."
            ),
            LearningResource(
                title="Real Python: Idiomatic Python & OOP Guide",
                skill_code="python",
                category="Tutorial",
                resource_type="tutorial",
                url="https://realpython.com/python3-object-oriented-programming/",
                is_free=True,
                difficulty="Intermediate",
                rating=4.8,
                estimated_time="3 hours",
                provider="Real Python",
                description="In-depth dive into object-oriented architecture, classes, dunder methods, inheritance, and clean code principles."
            ),
            LearningResource(
                title="FastAPI Official Interactive Tutorial",
                skill_code="python",
                category="Web & API",
                resource_type="documentation",
                url="https://fastapi.tiangolo.com/tutorial/",
                is_free=True,
                difficulty="Intermediate",
                rating=4.9,
                estimated_time="5 hours",
                provider="FastAPI Docs",
                description="Modern Python web development with automatic OpenAPI documentation, Pydantic type validation, and asynchronous routes."
            ),

            # SQL
            LearningResource(
                title="PostgreSQL Official Documentation: SQL Tutorial",
                skill_code="sql",
                category="Database",
                resource_type="documentation",
                url="https://www.postgresql.org/docs/current/tutorial.html",
                is_free=True,
                difficulty="Beginner",
                rating=4.9,
                estimated_time="3 hours",
                provider="PostgreSQL Global Development Group",
                description="Authoritative guide to relational queries, table creation, foreign keys, transaction blocks, and indexing."
            ),
            LearningResource(
                title="SQLBolt: Interactive Interactive SQL Lessons",
                skill_code="sql",
                category="Practice",
                resource_type="practice",
                url="https://sqlbolt.com/",
                is_free=True,
                difficulty="Beginner",
                rating=4.8,
                estimated_time="2.5 hours",
                provider="SQLBolt",
                description="Hands-on browser-based exercises for SELECT queries, multi-table JOINs, aggregations, and subqueries."
            ),
            LearningResource(
                title="Use The Index, Luke: SQL Indexing Guide",
                skill_code="sql",
                category="Optimization",
                resource_type="tutorial",
                url="https://use-the-index-luke.com/",
                is_free=True,
                difficulty="Advanced",
                rating=4.9,
                estimated_time="4 hours",
                provider="Markus Winand",
                description="A definitive guide to database performance, B-tree indexes, execution plans, and query tuning for developers."
            ),

            # Java
            LearningResource(
                title="Oracle Java Tutorials: Learning the Java Language",
                skill_code="java",
                category="Documentation",
                resource_type="documentation",
                url="https://docs.oracle.com/javase/tutorial/java/index.html",
                is_free=True,
                difficulty="Beginner",
                rating=4.7,
                estimated_time="6 hours",
                provider="Oracle",
                description="Authoritative reference covering Java syntax, OOP, interfaces, inheritance, generics, and packages."
            ),
            LearningResource(
                title="Baeldung: Spring Boot Core Guides",
                skill_code="java",
                category="Frameworks",
                resource_type="tutorial",
                url="https://www.baeldung.com/spring-boot",
                is_free=True,
                difficulty="Intermediate",
                rating=4.8,
                estimated_time="5 hours",
                provider="Baeldung",
                description="Practical tutorials covering Spring Boot configuration, dependency injection, JPA persistence, and REST controllers."
            ),

            # Web Dev
            LearningResource(
                title="MDN Web Docs: Modern JavaScript (ES6+)",
                skill_code="web_dev",
                category="Frontend",
                resource_type="documentation",
                url="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
                is_free=True,
                difficulty="Beginner to Intermediate",
                rating=4.9,
                estimated_time="5 hours",
                provider="Mozilla Developer Network",
                description="Comprehensive documentation on JavaScript syntax, async/await, closures, prototypes, and the DOM."
            ),
            LearningResource(
                title="React Official Documentation: Quick Start & Hooks",
                skill_code="web_dev",
                category="Frontend",
                resource_type="documentation",
                url="https://react.dev/learn",
                is_free=True,
                difficulty="Intermediate",
                rating=4.9,
                estimated_time="4 hours",
                provider="React Core Team",
                description="Official interactive React documentation featuring component lifecycle, state management, and custom hooks."
            ),
            LearningResource(
                title="freeCodeCamp: Responsive Web Design",
                skill_code="web_dev",
                category="Practice",
                resource_type="course",
                url="https://www.freecodecamp.org/learn/2022/responsive-web-design/",
                is_free=True,
                difficulty="Beginner",
                rating=4.8,
                estimated_time="10 hours",
                provider="freeCodeCamp",
                description="Interactive HTML5, CSS Flexbox, Grid, and accessible responsive web development curriculum."
            ),

            # Data Analytics
            LearningResource(
                title="Pandas Official Getting Started Tutorials",
                skill_code="data_analytics",
                category="Data Science",
                resource_type="documentation",
                url="https://pandas.pydata.org/docs/getting_started/intro_tutorials/",
                is_free=True,
                difficulty="Beginner",
                rating=4.9,
                estimated_time="3.5 hours",
                provider="Pandas Development Team",
                description="Step-by-step guides for DataFrame filtering, aggregation, reshaping, missing data handling, and time series."
            ),
            LearningResource(
                title="Kaggle: Data Visualization Micro-Course",
                skill_code="data_analytics",
                category="Practice",
                resource_type="practice",
                url="https://www.kaggle.com/learn/data-visualization",
                is_free=True,
                difficulty="Intermediate",
                rating=4.8,
                estimated_time="4 hours",
                provider="Kaggle",
                description="Hands-on interactive notebooks covering Seaborn, Matplotlib, scatter plots, distributions, and heatmaps."
            ),

            # Machine Learning
            LearningResource(
                title="Scikit-Learn Official User Guide & Pipelines",
                skill_code="ml",
                category="Machine Learning",
                resource_type="documentation",
                url="https://scikit-learn.org/stable/user_guide.html",
                is_free=True,
                difficulty="Intermediate",
                rating=4.9,
                estimated_time="6 hours",
                provider="Scikit-Learn Developers",
                description="Complete guide to classification, regression, clustering, preprocessing pipelines, and model evaluation."
            ),
            LearningResource(
                title="Google Machine Learning Crash Course",
                skill_code="ml",
                category="Course",
                resource_type="course",
                url="https://developers.google.com/machine-learning/crash-course",
                is_free=True,
                difficulty="Beginner to Intermediate",
                rating=4.8,
                estimated_time="12 hours",
                provider="Google Developers",
                description="Fast-paced, practical introduction to machine learning concepts, loss functions, gradient descent, and neural networks."
            )
        ]
        db.add_all(resources)
        db.commit()

    # 4. Seed Demo Student User for Hackathon / Instant Testing
    demo_email = "demo@skillverse.ai"
    demo_user = db.query(User).filter(User.email == demo_email).first()
    if not demo_user:
        print("-> Seeding Hackathon Demo Student (demo@skillverse.ai)...")
        demo_user = User(
            email=demo_email,
            hashed_password=get_password_hash("Password123!"),
            full_name="Alex Mercer (Demo Student)",
            role="student"
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

        # Profile
        demo_profile = StudentProfile(
            user_id=demo_user.id,
            education_level="Bachelor of Engineering (4th Year)",
            branch="Computer Science & Engineering",
            career_goal="Full-Stack Web Developer",
            preferred_learning_style="Hands-on Project",
            daily_study_hours=2.5,
            target_date="2026-12-31",
            current_skills=["python", "sql", "web_dev"],
            bio="Aspiring full-stack software engineer passionate about cosmic web interfaces, clean scalable backend systems, and modern AI integration.",
            avatar_config={
                "theme": "ai_engineer",
                "outfit": "cyber_scout",
                "color": "#06b6d4",
                "accessory": "quantum_visor",
                "reduced_motion": False
            }
        )
        db.add(demo_profile)
        db.commit()

        # Demo Assessment Submission
        skill_scores = {
            "python": 80.0,
            "sql": 40.0,
            "java": 20.0,
            "web_dev": 70.0,
            "data_analytics": 50.0,
            "ml": 30.0
        }
        gaps = [
            {
                "skill_code": "sql",
                "topic": "JOIN Operations & Window Functions",
                "severity": "High",
                "recommendation": "Score is 40%. Master multi-table JOINs, subqueries, and execution plans."
            },
            {
                "skill_code": "ml",
                "topic": "Model Evaluation on Imbalanced Data",
                "severity": "High",
                "recommendation": "Score is 30%. Understand precision, recall, and cross-validation beyond accuracy."
            },
            {
                "skill_code": "data_analytics",
                "topic": "Missing Value Imputation & Outliers",
                "severity": "Medium",
                "recommendation": "Score is 50%. Practice robust statistical handling of missing values."
            }
        ]
        submission = AssessmentSubmission(
            user_id=demo_user.id,
            total_score=48.3,
            skill_scores=skill_scores,
            knowledge_gaps=gaps
        )
        db.add(submission)
        db.commit()

        # Student Progress
        for code, sc in skill_scores.items():
            level = "Master" if sc >= 85 else ("Advanced" if sc >= 70 else ("Intermediate" if sc >= 40 else "Novice"))
            prog = StudentProgress(
                user_id=demo_user.id,
                skill_code=code,
                proficiency_score=sc,
                proficiency_level=level,
                completed_steps=3 if sc >= 70 else (1 if sc >= 40 else 0),
                total_time_spent_mins=int(sc * 12)
            )
            db.add(prog)
        db.commit()

        # Pathway Generation for Demo User
        all_res = db.query(LearningResource).all()
        res_dicts = [{"id": r.id, "title": r.title, "skill_code": r.skill_code, "category": r.category, "url": r.url, "is_free": r.is_free, "difficulty": r.difficulty, "provider": r.provider, "description": r.description} for r in all_res]
        
        pathway_data = recommender_engine.generate_pathway(
            career_goal=demo_profile.career_goal,
            skill_scores=skill_scores,
            gaps=gaps,
            daily_study_hours=demo_profile.daily_study_hours,
            resources_catalog=res_dicts
        )

        pathway = LearningPathway(
            user_id=demo_user.id,
            career_goal=demo_profile.career_goal,
            title=pathway_data["title"],
            description=pathway_data["description"],
            target_date=demo_profile.target_date,
            total_duration_weeks=pathway_data["total_duration_weeks"],
            progress_percentage=25.0,
            status="active"
        )
        db.add(pathway)
        db.commit()
        db.refresh(pathway)

        for s_idx, st in enumerate(pathway_data["steps"]):
            is_comp = (s_idx == 0) # mark first step completed
            step = PathwayStep(
                pathway_id=pathway.id,
                order_index=st["order_index"],
                skill_code=st["skill_code"],
                stage_name=st["stage_name"],
                title=st["title"],
                description=st["description"],
                duration_hours=st["duration_hours"],
                learning_objectives=st["learning_objectives"],
                resources=st["resources"],
                quiz_data=st["quiz_data"],
                practical_tasks=st["practical_tasks"],
                is_completed=is_comp,
                completed_at=datetime.utcnow() if is_comp else None
            )
            db.add(step)
        db.commit()

        # Daily Missions
        today = date.today()
        missions = [
            DailyMission(
                user_id=demo_user.id,
                title="Close SQL JOIN Knowledge Gap",
                description="Complete the interactive SQLBolt lessons on multi-table queries.",
                mission_type="practice",
                skill_code="sql",
                xp_reward=60,
                target_url="https://sqlbolt.com/",
                is_completed=True,
                streak_count=4,
                assigned_date=today,
                completed_at=datetime.utcnow() - timedelta(hours=2)
            ),
            DailyMission(
                user_id=demo_user.id,
                title="React Hooks Mastery Challenge",
                description="Review custom hook patterns and pass the stage checkpoint quiz.",
                mission_type="quiz",
                skill_code="web_dev",
                xp_reward=80,
                target_url=None,
                is_completed=False,
                streak_count=4,
                assigned_date=today
            ),
            DailyMission(
                user_id=demo_user.id,
                title="Python Asynchronous Task Script",
                description="Write a sample script using asyncio to simulate concurrent requests.",
                mission_type="challenge",
                skill_code="python",
                xp_reward=100,
                target_url="https://docs.python.org/3/tutorial/",
                is_completed=False,
                streak_count=4,
                assigned_date=today
            )
        ]
        db.add_all(missions)
        db.commit()

        # Sample Bookmarks
        sql_res = db.query(LearningResource).filter(LearningResource.skill_code == "sql").first()
        fastapi_res = db.query(LearningResource).filter(LearningResource.title.like("%FastAPI%")).first()
        if sql_res:
            db.add(Bookmark(user_id=demo_user.id, resource_id=sql_res.id, notes="Essential reference for query optimization"))
        if fastapi_res:
            db.add(Bookmark(user_id=demo_user.id, resource_id=fastapi_res.id, notes="Recommended framework for project backend"))
        db.commit()

        print("[SUCCESS] Database successfully seeded with demo student!")
    else:
        print("[SUCCESS] Database already populated with seed data.")

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    db.close()
