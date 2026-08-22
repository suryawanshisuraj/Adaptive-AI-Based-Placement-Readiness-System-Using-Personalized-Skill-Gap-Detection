from typing import Dict, Any

LEARNING_RESOURCES: Dict[str, Dict[str, Any]] = {
    "SQL JOINs": {
        "title": "Mastering SQL Relational JOINs",
        "skill": "SQL",
        "topic": "Relational Queries",
        "key_concepts": [
            "INNER JOIN returns only rows with matches in both tables.",
            "LEFT (OUTER) JOIN returns all rows from the left table and NULLs for non-matching right table rows.",
            "FULL OUTER JOIN combines both LEFT and RIGHT outer join behaviors.",
            "CROSS JOIN produces a Cartesian product (M * N rows)."
        ],
        "common_pitfalls": [
            "Using WHERE condition instead of ON clause filters out rows prematurely in LEFT JOINs.",
            "Duplicating rows when joining against non-unique foreign keys without aggregation."
        ],
        "code_example": "SELECT u.name, o.order_date \nFROM users u \nLEFT JOIN orders o ON u.id = o.user_id \nWHERE o.total_amount > 100;",
        "curated_links": [
            {"title": "Visual SQL Joins Guide", "url": "https://mode.com/sql-tutorial/sql-joins/"},
            {"title": "JOIN Performance & Query Optimization", "url": "https://use-the-index-luke.com/sql/joins"}
        ]
    },
    "SQL Subqueries": {
        "title": "Correlated & Nested Subqueries",
        "skill": "SQL",
        "topic": "Advanced Queries",
        "key_concepts": [
            "Scalar subqueries return a single value and can be placed in SELECT or WHERE clauses.",
            "Correlated subqueries reference columns from the outer query and execute once per candidate outer row.",
            "EXISTS is generally faster than IN when the subquery table is large and indexed."
        ],
        "common_pitfalls": [
            "Using IN with NULL values in subqueries causing unexpected empty result sets.",
            "Overusing correlated subqueries when a JOIN with GROUP BY is significantly more performant."
        ],
        "code_example": "SELECT emp_name, salary \nFROM employees e1 \nWHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.department_id = e1.department_id);",
        "curated_links": [
            {"title": "SQL Subqueries Deep Dive", "url": "https://www.w3schools.com/sql/sql_subqueries.asp"}
        ]
    },
    "Recursion": {
        "title": "Recursion Foundations & Call Stack Dynamics",
        "skill": "Coding",
        "topic": "Algorithms",
        "key_concepts": [
            "Every recursive function requires a solid Base Case to prevent StackOverflowError.",
            "Recursive step moves the problem closer to the base case state.",
            "Call stack memory complexity is O(depth of recursion tree)."
        ],
        "common_pitfalls": [
            "Missing base case or incorrect termination condition leading to infinite loops.",
            "Recomputing overlapping subproblems without memoization (exponential O(2^N) explosion)."
        ],
        "code_example": "public int fib(int n, int[] memo) {\n    if (n <= 1) return n;\n    if (memo[n] != 0) return memo[n];\n    return memo[n] = fib(n - 1, memo) + fib(n - 2, memo);\n}",
        "curated_links": [
            {"title": "Recursion to Dynamic Programming", "url": "https://leetcode.com/explore/learn/card/recursion-i/"}
        ]
    },
    "Arrays & Sliding Window": {
        "title": "Array Manipulations & Sliding Window Optimization",
        "skill": "Coding",
        "topic": "Data Structures",
        "key_concepts": [
            "Sliding window converts brute force O(N^2) subarray problems to linear O(N) time.",
            "Prefix sums allow O(1) range sum queries after O(N) preprocessing.",
            "Two pointers technique (opposite ends or fast/slow pointers) optimizes sorted array scans."
        ],
        "common_pitfalls": [
            "Off-by-one errors when adjusting window boundaries (left/right pointers).",
            "Failing to shrink the window when invariant conditions are violated."
        ],
        "code_example": "int left = 0, currentSum = 0, minLen = Integer.MAX_VALUE;\nfor (int right = 0; right < nums.length; right++) {\n    currentSum += nums[right];\n    while (currentSum >= target) {\n        minLen = Math.min(minLen, right - left + 1);\n        currentSum -= nums[left++];\n    }\n}",
        "curated_links": [
            {"title": "Two Pointers & Sliding Window Patterns", "url": "https://github.com/ashishps1/awesome-leetcode-resources"}
        ]
    },
    "Normalization": {
        "title": "Database Normalization (1NF, 2NF, 3NF, BCNF)",
        "skill": "DBMS",
        "topic": "Schema Design",
        "key_concepts": [
            "1NF: Atomic values only, no repeating groups.",
            "2NF: In 1NF and no partial dependencies (every non-key attribute is fully functionally dependent on primary key).",
            "3NF: In 2NF and no transitive dependencies (X -> Y and Y -> Z where Z is non-prime).",
            "BCNF: For every functional dependency X -> Y, X must be a super key."
        ],
        "common_pitfalls": [
            "Confusing partial dependency (part of composite key) with transitive dependency (non-key to non-key).",
            "Over-normalizing in OLAP/Reporting systems where denormalization improves read throughput."
        ],
        "code_example": "-- 3NF Decomposition\n-- Instead of (StudentID, CourseID, Professor, ProfOffice)\n-- Decompose to (StudentID, CourseID), (CourseID, Professor), (Professor, ProfOffice)",
        "curated_links": [
            {"title": "DBMS Normalization Guide", "url": "https://www.geeksforgeeks.org/introduction-of-database-normalization/"}
        ]
    },
    "OOP Polymorphism": {
        "title": "Object-Oriented Polymorphism & Dynamic Dispatch",
        "skill": "OOP",
        "topic": "Object Oriented Principles",
        "key_concepts": [
            "Compile-time (Static) Polymorphism: Method Overloading (same name, different parameter signature).",
            "Runtime (Dynamic) Polymorphism: Method Overriding (subclass overrides superclass method).",
            "Virtual Method Table (vtable) handles dynamic binding at runtime in Java/C++."
        ],
        "common_pitfalls": [
            "Assuming private or static methods can be overridden (they are hidden, not overridden).",
            "Violating Liskov Substitution Principle (LSP) by changing expected behavior in derived class."
        ],
        "code_example": "class Animal { void sound() { System.out.println(\"Animal sound\"); } }\nclass Dog extends Animal { @Override void sound() { System.out.println(\"Bark\"); } }\nAnimal a = new Dog(); // Dynamic Dispatch\na.sound(); // prints 'Bark'",
        "curated_links": [
            {"title": "SOLID Principles & Polymorphism", "url": "https://refactoring.guru/design-patterns"}
        ]
    },
    "Multithreading & Concurrency": {
        "title": "Java Concurrency & Thread Synchronization",
        "skill": "Java",
        "topic": "Advanced Core Java",
        "key_concepts": [
            "Thread lifecycle: NEW -> RUNNABLE -> BLOCKED/WAITING -> TERMINATED.",
            "`volatile` ensures visibility of changes across threads by reading/writing directly to main memory.",
            "`synchronized` guarantees mutual exclusion and atomicity.",
            "`ReentrantLock` provides flexible locking, fairness policies, and tryLock."
        ],
        "common_pitfalls": [
            "Deadlocks caused by acquiring multiple locks in inconsistent order.",
            "Race conditions due to non-atomic compound operations (like `count++`)."
        ],
        "code_example": "private final AtomicInteger counter = new AtomicInteger(0);\npublic void increment() {\n    counter.incrementAndGet(); // Thread-safe atomic operation\n}",
        "curated_links": [
            {"title": "Java Concurrency in Practice", "url": "https://docs.oracle.com/javase/tutorial/essential/concurrency/"}
        ]
    },
    "Aptitude & Probability": {
        "title": "Quantitative Aptitude: Combinatorics & Probability",
        "skill": "Aptitude",
        "topic": "Quantitative Reasoning",
        "key_concepts": [
            "Permutations P(n, r) = n! / (n-r)! (Order matters).",
            "Combinations C(n, r) = n! / [r! * (n-r)!] (Order does not matter).",
            "Independent events: P(A ∩ B) = P(A) * P(B).",
            "Bayes Theorem: P(A|B) = [P(B|A) * P(A)] / P(B)."
        ],
        "common_pitfalls": [
            "Confusing with-replacement vs without-replacement sampling.",
            "Adding probabilities of non-mutually exclusive events without subtracting intersection."
        ],
        "code_example": "Formula: P(At least 1 success) = 1 - P(Zero successes)",
        "curated_links": [
            {"title": "Placement Aptitude Shortcuts", "url": "https://www.indiabix.com/aptitude/questions-and-answers/"}
        ]
    }
}

def get_resource_for_subtopic(subtopic: str) -> Dict[str, Any]:
    # Match exact or partial
    for key, val in LEARNING_RESOURCES.items():
        if key.lower() in subtopic.lower() or subtopic.lower() in key.lower():
            return val
    # Fallback
    return {
        "title": f"Study Guide for {subtopic}",
        "skill": "Technical",
        "topic": subtopic,
        "key_concepts": [
            f"Understand core principles and theoretical boundaries of {subtopic}.",
            "Review typical interview problem patterns and edge cases.",
            "Practice targeted implementation drills under timed conditions."
        ],
        "common_pitfalls": [
            "Rushing through implementation without validating edge cases and constraints."
        ],
        "code_example": "// Review fundamental implementation patterns\n// and analyze time/space complexity.",
        "curated_links": [
            {"title": "GeeksforGeeks Tutorial", "url": "https://www.geeksforgeeks.org/"},
            {"title": "LeetCode Practice Problems", "url": "https://leetcode.com/problemset/all/"}
        ]
    }
