import json
from typing import List, Dict, Any

RAW_QUESTIONS: List[Dict[str, Any]] = [
    # ==========================================
    # 1. SQL -> JOINs
    # ==========================================
    {
        "id": "sql_join_001",
        "skill": "SQL",
        "topic": "Relational Queries",
        "subtopic": "SQL JOINs",
        "difficulty": 2,
        "question_text": "Given Table A with 5 rows and Table B with 4 rows. If Table A contains 2 NULL values in the join column and Table B contains 1 NULL value, how many rows will an INNER JOIN on that column produce if all non-null keys match uniquely?",
        "options": [
            "3 rows",
            "4 rows",
            "5 rows",
            "6 rows"
        ],
        "correct_index": 0,
        "explanation": "In SQL standard relational logic, NULL != NULL. Thus NULL values in the join predicate never match each other in an INNER JOIN. The 3 matching non-null rows will match 1-to-1, yielding 3 rows.",
        "expected_time_sec": 40,
        "code_snippet": "SELECT * FROM TableA A INNER JOIN TableB B ON A.id = B.id;",
        "tags": ["sql", "joins", "null-handling", "relational"]
    },
    {
        "id": "sql_join_002",
        "skill": "SQL",
        "topic": "Relational Queries",
        "subtopic": "SQL JOINs",
        "difficulty": 3,
        "question_text": "What is the primary operational difference between placing a filter condition in the ON clause vs the WHERE clause of a LEFT JOIN?",
        "options": [
            "The ON clause filter executes after the join is built, while WHERE executes before.",
            "The ON clause filter restricts which right-table rows join to the left table (preserving all left rows), whereas the WHERE clause filters out entire rows after the join.",
            "There is no difference in modern query planners like PostgreSQL or Oracle.",
            "The WHERE clause allows index scans whereas the ON clause forces a full table scan."
        ],
        "correct_index": 1,
        "explanation": "In a LEFT JOIN, predicates in the ON clause determine which right-table rows attach; unmatched left rows are still retained with NULLs. A predicate in the WHERE clause on the right table will filter out rows where right table attributes are NULL, effectively turning the LEFT JOIN into an INNER JOIN.",
        "expected_time_sec": 50,
        "code_snippet": "-- Case A: ON clause\nSELECT * FROM Users u LEFT JOIN Orders o ON u.id = o.user_id AND o.status = 'ACTIVE';\n\n-- Case B: WHERE clause\nSELECT * FROM Users u LEFT JOIN Orders o ON u.id = o.user_id WHERE o.status = 'ACTIVE';",
        "tags": ["sql", "joins", "left-join", "optimization"]
    },
    {
        "id": "sql_join_003",
        "skill": "SQL",
        "topic": "Relational Queries",
        "subtopic": "SQL JOINs",
        "difficulty": 4,
        "question_text": "Consider Table A with rows [1, 1, 2] and Table B with rows [1, 1, 1, 3]. What is the total row count resulting from a FULL OUTER JOIN on the ID column?",
        "options": [
            "6 rows",
            "7 rows",
            "8 rows",
            "9 rows"
        ],
        "correct_index": 2,
        "explanation": "Matching key '1': 2 rows in A * 3 rows in B = 6 rows. Unmatched key '2' from A = 1 row with NULLs for B. Unmatched key '3' from B = 1 row with NULLs for A. Total = 6 + 1 + 1 = 8 rows.",
        "expected_time_sec": 60,
        "code_snippet": "SELECT * FROM TableA FULL OUTER JOIN TableB ON TableA.id = TableB.id;",
        "tags": ["sql", "joins", "full-outer-join", "cardinality"]
    },

    # ==========================================
    # 2. SQL -> Subqueries
    # ==========================================
    {
        "id": "sql_sub_001",
        "skill": "SQL",
        "topic": "Advanced Queries",
        "subtopic": "SQL Subqueries",
        "difficulty": 3,
        "question_text": "Why does the query `SELECT * FROM Employees WHERE dept_id NOT IN (SELECT dept_id FROM Departments WHERE is_active = 0)` return 0 rows if even a single returned dept_id is NULL?",
        "options": [
            "SQL parser treats NOT IN as a syntax error when encountering NULL.",
            "Evaluating `x NOT IN (val1, NULL)` evaluates to UNKNOWN (neither TRUE nor FALSE), causing the WHERE clause filter to fail for all rows.",
            "The subquery automatically aborts with a runtime exception.",
            "NULL is converted to 0, which matches all active departments."
        ],
        "correct_index": 1,
        "explanation": "`x NOT IN (1, NULL)` is logically equivalent to `NOT (x = 1 OR x = NULL)`. Since `x = NULL` is UNKNOWN, `NOT (UNKNOWN)` is UNKNOWN. Under three-valued logic, WHERE UNKNOWN discards every row. Best practice is to use `NOT EXISTS` or filter `IS NOT NULL`.",
        "expected_time_sec": 45,
        "code_snippet": "SELECT emp_name FROM Employees \nWHERE dept_id NOT IN (SELECT dept_id FROM Departments);",
        "tags": ["sql", "subqueries", "not-in", "three-valued-logic"]
    },
    {
        "id": "sql_sub_002",
        "skill": "SQL",
        "topic": "Advanced Queries",
        "subtopic": "SQL Subqueries",
        "difficulty": 4,
        "question_text": "What distinguishes a correlated subquery from a standard non-correlated subquery in terms of execution mechanics?",
        "options": [
            "Correlated subqueries can only return scalar numbers, whereas non-correlated can return tables.",
            "A correlated subquery references values from the outer query and conceptually evaluates repeatedly for every row processed by the outer query.",
            "Correlated subqueries are always materialized into a temporary table prior to outer query execution.",
            "Correlated subqueries can only be used in the HAVING clause."
        ],
        "correct_index": 1,
        "explanation": "A correlated subquery contains one or more dependencies on columns from the enclosing (outer) query statement, requiring per-row evaluation (or optimization via decorrelation/semi-join by the optimizer).",
        "expected_time_sec": 45,
        "code_snippet": "SELECT e.name, e.salary \nFROM Employees e \nWHERE e.salary > (SELECT AVG(salary) FROM Employees sub WHERE sub.dept_id = e.dept_id);",
        "tags": ["sql", "subqueries", "correlated", "query-engine"]
    },

    # ==========================================
    # 3. Coding -> Arrays & Sliding Window
    # ==========================================
    {
        "id": "code_arr_001",
        "skill": "Coding",
        "topic": "Data Structures",
        "subtopic": "Arrays & Sliding Window",
        "difficulty": 2,
        "question_text": "What is the optimal time complexity to find the maximum sum of any contiguous subarray of size K in an array of size N?",
        "options": [
            "O(N * K)",
            "O(N log K)",
            "O(N)",
            "O(K^2)"
        ],
        "correct_index": 2,
        "explanation": "Using a sliding window of fixed size K, we compute the sum of the first K elements, then iterate from K to N-1, adding the incoming element and subtracting the outgoing element in O(1) per step, achieving overall O(N) linear time.",
        "expected_time_sec": 30,
        "code_snippet": "int maxSum = 0, windowSum = 0;\nfor (int i = 0; i < k; i++) windowSum += nums[i];\nmaxSum = windowSum;\nfor (int i = k; i < n; i++) {\n    windowSum += nums[i] - nums[i - k];\n    maxSum = Math.max(maxSum, windowSum);\n}",
        "tags": ["dsa", "arrays", "sliding-window", "time-complexity"]
    },
    {
        "id": "code_arr_002",
        "skill": "Coding",
        "topic": "Data Structures",
        "subtopic": "Arrays & Sliding Window",
        "difficulty": 3,
        "question_text": "Given an array containing positive integers, what technique allows finding the minimum length contiguous subarray whose sum is greater than or equal to target S in O(N) time and O(1) space?",
        "options": [
            "Dynamic Programming 2D Table",
            "Variable-size Dynamic Sliding Window (Two Pointers)",
            "Prefix sum with Binary Tree insertion",
            "Merge Sort partition"
        ],
        "correct_index": 1,
        "explanation": "Since all integers are positive, the prefix sum is monotonically increasing. We expand the right pointer to increase sum and shrink the left pointer as long as currentSum >= S, tracking min length. Both pointers traverse at most N steps -> O(N).",
        "expected_time_sec": 45,
        "code_snippet": "int left = 0, sum = 0, minLen = Integer.MAX_VALUE;\nfor (int right = 0; right < nums.length; right++) {\n    sum += nums[right];\n    while (sum >= target) {\n        minLen = Math.min(minLen, right - left + 1);\n        sum -= nums[left++];\n    }\n}",
        "tags": ["dsa", "arrays", "two-pointers", "sliding-window"]
    },

    # ==========================================
    # 4. Coding -> Recursion
    # ==========================================
    {
        "id": "code_rec_001",
        "skill": "Coding",
        "topic": "Algorithms",
        "subtopic": "Recursion",
        "difficulty": 2,
        "question_text": "What will happen if a recursive function is invoked without a proper base case or with a base case condition that is never reached?",
        "options": [
            "The compiler will throw a compilation error during build time.",
            "The program will encounter a StackOverflowError / segmentation fault due to exhausting call stack frames.",
            "The heap memory will instantly fragment into garbage collection pauses.",
            "The CPU will throttle to single-core frequency."
        ],
        "correct_index": 1,
        "explanation": "Each recursive invocation allocates a new stack frame on the thread call stack (local variables, return address). Without terminating at a base case, stack memory is exhausted, throwing java.lang.StackOverflowError in Java or segmentation fault in C/C++.",
        "expected_time_sec": 30,
        "code_snippet": "int infiniteRecursion(int n) {\n    return infiniteRecursion(n + 1); // No base case!\n}",
        "tags": ["dsa", "recursion", "call-stack", "memory"]
    },
    {
        "id": "code_rec_002",
        "skill": "Coding",
        "topic": "Algorithms",
        "subtopic": "Recursion",
        "difficulty": 4,
        "question_text": "What is the time complexity of the naive unmemoized recursive Fibonacci function `int fib(int n) { if(n <= 1) return n; return fib(n-1) + fib(n-2); }` and why?",
        "options": [
            "O(N) because it visits each integer from 1 to N.",
            "O(N^2) because each number is calculated twice.",
            "O(2^N) because each call spawns two subsequent recursive calls forming an exponential binary recursion tree.",
            "O(N log N) by the Master Theorem."
        ],
        "correct_index": 2,
        "explanation": "The recurrence relation T(n) = T(n-1) + T(n-2) + O(1) generates a recursion tree of height N with approximately 2^N leaf calls, resulting in O(2^N) exponential time complexity (precisely O(1.618^N)).",
        "expected_time_sec": 45,
        "code_snippet": "int fib(int n) {\n    if (n <= 1) return n;\n    return fib(n - 1) + fib(n - 2);\n}",
        "tags": ["dsa", "recursion", "time-complexity", "fibonacci"]
    },

    # ==========================================
    # 5. Java -> Core & Collections
    # ==========================================
    {
        "id": "java_col_001",
        "skill": "Java",
        "topic": "Collections & Core",
        "subtopic": "Collections Framework",
        "difficulty": 3,
        "question_text": "In Java 8+, what data structure does a `HashMap` bucket transform into when the number of colliding entries in that specific bucket exceeds the TREEIFY_THRESHOLD (8)?",
        "options": [
            "Doubly Linked List",
            "Red-Black Balanced Binary Search Tree (TreeNode)",
            "Circular Array Queue",
            "SkipList Map"
        ],
        "correct_index": 1,
        "explanation": "In Java 8+, to mitigate hash collision Denial of Service (DoS) attacks and preserve search performance, when a bucket contains more than 8 elements (and total table capacity >= 64), the linked list converts to a Red-Black Tree, improving worst-case search from O(N) to O(log N).",
        "expected_time_sec": 35,
        "code_snippet": "static final int TREEIFY_THRESHOLD = 8;\n// Node<K,V> becomes TreeNode<K,V>",
        "tags": ["java", "hashmap", "collections", "data-structures"]
    },
    {
        "id": "java_con_001",
        "skill": "Java",
        "topic": "Concurrency",
        "subtopic": "Multithreading & Concurrency",
        "difficulty": 4,
        "question_text": "What does the `volatile` keyword guarantee in Java multi-threaded memory architecture?",
        "options": [
            "Atomicity of compound operations such as i++.",
            "Happens-Before relationship and direct memory visibility across CPU thread caches without mutual exclusion locking.",
            "Guaranteed deadlock prevention by sorting lock acquisitions.",
            "Automatic thread pool serialization."
        ],
        "correct_index": 1,
        "explanation": "`volatile` establishes a happens-before order: writes to a volatile variable are immediately flushed to main memory and subsequent reads load from main memory, preventing thread CPU cache stale reads. However, it does NOT guarantee atomicity for compound operations (e.g. `count++`).",
        "expected_time_sec": 45,
        "code_snippet": "private volatile boolean isRunning = true;\n\npublic void stop() { isRunning = false; }",
        "tags": ["java", "multithreading", "volatile", "concurrency"]
    },

    # ==========================================
    # 6. OOP -> Principles
    # ==========================================
    {
        "id": "oop_poly_001",
        "skill": "OOP",
        "topic": "Object Oriented Principles",
        "subtopic": "OOP Polymorphism",
        "difficulty": 2,
        "question_text": "Consider the code below. What will be printed when `Parent p = new Child(); p.display();` is executed in Java?",
        "options": [
            "Parent Display",
            "Child Display",
            "Compilation Error",
            "Runtime ClassCastException"
        ],
        "correct_index": 1,
        "explanation": "Java implements runtime dynamic method dispatch (virtual methods by default). The runtime type of the instance is `Child`, so the overridden method in `Child` is invoked.",
        "expected_time_sec": 30,
        "code_snippet": "class Parent {\n    void display() { System.out.println(\"Parent Display\"); }\n}\nclass Child extends Parent {\n    void display() { System.out.println(\"Child Display\"); }\n}",
        "tags": ["oop", "polymorphism", "overriding", "dynamic-dispatch"]
    },
    {
        "id": "oop_poly_002",
        "skill": "OOP",
        "topic": "Object Oriented Principles",
        "subtopic": "OOP Polymorphism",
        "difficulty": 3,
        "question_text": "If a static method `public static void print()` exists in both Parent and Child classes with identical signatures, what happens when calling `Parent p = new Child(); p.print();`?",
        "options": [
            "It prints Child's output due to dynamic method overriding.",
            "It prints Parent's output because static methods are hidden (method hiding) and bound at compile time based on reference type.",
            "Compilation error: static methods cannot share names in inheritance hierarchy.",
            "AmbiguousMethodInvocationException at runtime."
        ],
        "correct_index": 1,
        "explanation": "Static methods belong to the class, not an instance. They cannot be overridden, only hidden. Static method resolution occurs at compile-time based on the reference type (`Parent`), printing Parent's output.",
        "expected_time_sec": 40,
        "code_snippet": "class Parent { static void print() { System.out.print(\"Parent\"); } }\nclass Child extends Parent { static void print() { System.out.print(\"Child\"); } }\nParent p = new Child();\np.print();",
        "tags": ["oop", "method-hiding", "static", "polymorphism"]
    },

    # ==========================================
    # 7. DBMS -> Normalization & ACID
    # ==========================================
    {
        "id": "dbms_norm_001",
        "skill": "DBMS",
        "topic": "Schema Design",
        "subtopic": "Normalization",
        "difficulty": 3,
        "question_text": "A relational table is in 2NF. What additional condition must be fulfilled for it to be in 3NF (Third Normal Form)?",
        "options": [
            "It must not contain any composite primary keys.",
            "Every non-prime attribute must be non-transitively dependent on every candidate key (no non-key determines another non-key).",
            "Every determinant must be a candidate key.",
            "All multivalued attributes must be converted to JSON fields."
        ],
        "correct_index": 1,
        "explanation": "3NF requires that the relation is in 2NF and contains no transitive dependencies for non-prime attributes (i.e. if X -> Y and Y -> Z where Z is non-prime, X must be a superkey).",
        "expected_time_sec": 40,
        "code_snippet": "-- 2NF: No partial dependencies on composite keys\n-- 3NF: No transitive dependencies (e.g. DeptID -> DeptName where DeptID is not candidate key)",
        "tags": ["dbms", "normalization", "3nf", "functional-dependency"]
    },
    {
        "id": "dbms_acid_001",
        "skill": "DBMS",
        "topic": "Transactions",
        "subtopic": "ACID Transactions",
        "difficulty": 3,
        "question_text": "In relational database transaction isolation levels, what concurrency phenomenon does the REPEATABLE READ level prevent that READ COMMITTED does not?",
        "options": [
            "Dirty Reads",
            "Non-Repeatable (Fuzzy) Reads",
            "Phantom Reads (in standard ANSI SQL definition)",
            "Lost Updates exclusively"
        ],
        "correct_index": 1,
        "explanation": "READ COMMITTED prevents Dirty Reads but allows Non-Repeatable Reads (where re-reading a row within the same transaction sees changes committed by another transaction). REPEATABLE READ prevents Non-Repeatable Reads using snapshot MVCC or shared read locks.",
        "expected_time_sec": 45,
        "code_snippet": "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;\nBEGIN TRANSACTION;\nSELECT balance FROM Account WHERE id = 101;\n-- Another committed update will not alter the balance seen here.\nSELECT balance FROM Account WHERE id = 101;\nCOMMIT;",
        "tags": ["dbms", "acid", "isolation-levels", "transactions"]
    },

    # ==========================================
    # 8. Aptitude -> Quantitative Reasoning
    # ==========================================
    {
        "id": "apt_prob_001",
        "skill": "Aptitude",
        "topic": "Quantitative Reasoning",
        "subtopic": "Aptitude & Probability",
        "difficulty": 2,
        "question_text": "Two fair 6-sided dice are rolled simultaneously. What is the probability that the sum of the numbers appearing on top is greater than 9?",
        "options": [
            "1/6",
            "1/9",
            "5/36",
            "1/4"
        ],
        "correct_index": 0,
        "explanation": "Total outcomes = 6 * 6 = 36. Favorable outcomes for sum > 9: Sum=10 -> (4,6), (5,5), (6,4) [3 pairs]; Sum=11 -> (5,6), (6,5) [2 pairs]; Sum=12 -> (6,6) [1 pair]. Total favorable = 3 + 2 + 1 = 6. Probability = 6/36 = 1/6.",
        "expected_time_sec": 45,
        "code_snippet": "P(Sum > 9) = Count({ (4,6),(5,5),(6,4),(5,6),(6,5),(6,6) }) / 36 = 6/36 = 1/6",
        "tags": ["aptitude", "probability", "combinatorics", "math"]
    },
    {
        "id": "apt_work_001",
        "skill": "Aptitude",
        "topic": "Quantitative Reasoning",
        "subtopic": "Aptitude & Probability",
        "difficulty": 3,
        "question_text": "Pipe A can fill a tank in 12 hours and Pipe B can fill it in 18 hours. If both pipes are opened simultaneously, but Pipe A is closed after 4 hours, how many total hours will it take to fill the entire tank?",
        "options": [
            "10 hours",
            "12 hours",
            "14 hours",
            "8 hours"
        ],
        "correct_index": 1,
        "explanation": "Let total tank capacity = LCM(12, 18) = 36 units. Rate A = 36/12 = 3 units/hr; Rate B = 36/18 = 2 units/hr. Combined rate (first 4 hrs) = (3+2)*4 = 20 units. Remaining = 36 - 20 = 16 units. Pipe B completes 16 units at 2 units/hr in 16/2 = 8 hours. Total time = 4 + 8 = 12 hours.",
        "expected_time_sec": 60,
        "code_snippet": "Capacity = 36\n(3+2)*4 + 2*T_remain = 36 => 20 + 2*T = 36 => T = 8\nTotal = 4 + 8 = 12 hours",
        "tags": ["aptitude", "time-and-work", "speed", "arithmetic"]
    },

    # ==========================================
    # 9. Communication -> Technical & Verbal
    # ==========================================
    {
        "id": "comm_001",
        "skill": "Communication",
        "topic": "Professional Verbal",
        "subtopic": "Technical Communication",
        "difficulty": 2,
        "question_text": "During a technical interview, when asked to explain a complex distributed deadlock bug you resolved, what is the most structured and impactful communication strategy?",
        "options": [
            "Immediately jump into writing 50 lines of thread lock code without explaining context.",
            "Use the STAR method (Situation, Task, Action, Result), highlighting root cause analysis and metric impact.",
            "State that your team senior fixed it while you reviewed the logs.",
            "Discuss the generic definition of deadlocks from an operating systems textbook."
        ],
        "correct_index": 1,
        "explanation": "The STAR (Situation, Task, Action, Result) method provides a structured framework for behavioral and technical post-mortem discussions, ensuring clarity, technical precision, and measurable outcome presentation.",
        "expected_time_sec": 30,
        "code_snippet": None,
        "tags": ["communication", "star-method", "interview-skills"]
    }
]

def get_all_questions() -> List[Dict[str, Any]]:
    return RAW_QUESTIONS

def get_questions_by_subtopic(subtopic: str) -> List[Dict[str, Any]]:
    return [q for q in RAW_QUESTIONS if q["subtopic"].lower() == subtopic.lower()]

def get_questions_by_skill(skill: str) -> List[Dict[str, Any]]:
    return [q for q in RAW_QUESTIONS if q["skill"].lower() == skill.lower()]

def get_question_by_id(question_id: str) -> Dict[str, Any]:
    for q in RAW_QUESTIONS:
        if q["id"] == question_id:
            return q
    return RAW_QUESTIONS[0]
